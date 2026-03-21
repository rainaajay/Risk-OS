"""
rv_model.py
===========
XGBoost multi-output relative-value model.

Pipeline
--------
1.  add_ecosystem_features(df)       — peer-group context columns
2.  prepare_features(df)             — select & validate X / y
3.  train(df)                        — fit XGBoost + return (model, imputer, scaler)
4.  predict(df, model, imputer, scaler) — fair-value multiples
5.  dislocation_score(df)            — % deviation + composite z-score
6.  load_or_train(df)                — cache-aware entry point
7.  get_dislocation_summary(df)      — ranked output table

Model is persisted to rv_model.pkl (joblib).  It is retrained automatically
when the file is missing or older than MODEL_TTL_HOURS.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(name)s  %(message)s",
)

# --------------------------------------------------------------------------- #
# Paths & constants                                                             #
# --------------------------------------------------------------------------- #
MODEL_FILE = os.path.join(os.path.dirname(__file__), "rv_model.pkl")
MODEL_TTL_HOURS = 24

# --------------------------------------------------------------------------- #
# Feature & target definitions                                                  #
# --------------------------------------------------------------------------- #
FEATURE_COLS: list[str] = [
    # Profitability
    "operatingMargins",
    "profitMargins",
    "returnOnEquity",
    "returnOnAssets",
    # Growth
    "revenueGrowth",
    "earningsGrowth",
    # Leverage / balance sheet
    "debtToEquity",
    "leverage_ratio",
    "fcf_margin",
    "interest_cover_proxy",
    # Size & valuation context
    "log_market_cap",
    "ev_revenue",
    "grossMargins",
    "currentRatio",
    # Peer-group context (added by add_ecosystem_features)
    "ecosystem_median_pe",
    "ecosystem_median_evebita",
    "ecosystem_median_margin",
    "ecosystem_size",
]

TARGET_COLS: list[str] = [
    "forwardPE",
    "priceToBook",
    "enterpriseToEbitda",
    "beta",
]

# Predicted column names
PRED_COLS: list[str] = [f"pred_{t}" for t in TARGET_COLS]

# Dislocation column names
DISLOC_COLS: list[str] = [f"disloc_{t}" for t in TARGET_COLS]


# --------------------------------------------------------------------------- #
# 1. Ecosystem-level aggregate features                                         #
# --------------------------------------------------------------------------- #
def add_ecosystem_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-ecosystem summary statistics from the supplied df and merge
    them back so that each firm sees its peer group context as model inputs.

    Added columns
    -------------
    ecosystem_median_pe      — median forwardPE across ecosystem peers
    ecosystem_median_evebita — median enterpriseToEbitda across peers
    ecosystem_median_margin  — median operatingMargins across peers
    ecosystem_size           — number of firms in the ecosystem present in df
    """
    df = df.copy()

    # Ensure ecosystem column exists
    if "ecosystem" not in df.columns:
        df["ecosystem"] = "Unknown"

    # Compute aggregates
    agg = (
        df.groupby("ecosystem", observed=True)
        .agg(
            ecosystem_median_pe=("forwardPE", "median"),
            ecosystem_median_evebita=("enterpriseToEbitda", "median"),
            ecosystem_median_margin=("operatingMargins", "median"),
            ecosystem_size=("ticker", "count"),
        )
        .reset_index()
    )

    # Merge back on ecosystem
    df = df.merge(agg, on="ecosystem", how="left")

    # Coerce to float (ecosystem_size is int but StandardScaler needs float)
    for col in ["ecosystem_median_pe", "ecosystem_median_evebita",
                "ecosystem_median_margin", "ecosystem_size"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    logger.info("add_ecosystem_features() — added 4 peer-group columns, shape %s", df.shape)
    return df


# --------------------------------------------------------------------------- #
# 2. Prepare features                                                           #
# --------------------------------------------------------------------------- #
def prepare_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extract (X, y) from df.

    - Ensures all FEATURE_COLS and TARGET_COLS exist (fills missing with NaN).
    - Drops rows where ALL target values are NaN (no signal for training).
    - Does NOT impute or scale here — that is done inside train().

    Returns
    -------
    X : pd.DataFrame   shape (n_valid, len(FEATURE_COLS))
    y : pd.DataFrame   shape (n_valid, len(TARGET_COLS))
    """
    df = df.copy()

    # Add any missing feature / target columns as NaN
    for col in FEATURE_COLS + TARGET_COLS:
        if col not in df.columns:
            logger.warning("Column '%s' missing from df — filling with NaN", col)
            df[col] = np.nan

    # Drop rows where every target is NaN (cannot train on them)
    all_nan_mask = df[TARGET_COLS].isna().all(axis=1)
    n_dropped = int(all_nan_mask.sum())
    if n_dropped > 0:
        logger.info("prepare_features() — dropping %d rows with all-NaN targets", n_dropped)
    df = df[~all_nan_mask].copy()

    X = df[FEATURE_COLS].copy()
    y = df[TARGET_COLS].copy()

    logger.info(
        "prepare_features() — X %s, y %s, rows with ≥1 valid target: %d",
        X.shape, y.shape, len(df),
    )
    return X, y


# --------------------------------------------------------------------------- #
# 3. Train                                                                      #
# --------------------------------------------------------------------------- #
def train(df: pd.DataFrame) -> Tuple[object, object, object]:
    """
    Train a MultiOutputRegressor(XGBRegressor) on the supplied df.

    Pipeline
    --------
    1. add_ecosystem_features
    2. prepare_features  → (X, y)
    3. SimpleImputer (median) on X
    4. StandardScaler on X
    5. MultiOutputRegressor(XGBRegressor) on (X_scaled, y_imputed)

    For y, we impute each target column independently with its median so that
    XGBoost can train even when some target values are missing for certain firms.

    Returns
    -------
    model   : MultiOutputRegressor
    imputer : SimpleImputer  (fitted on X)
    scaler  : StandardScaler (fitted on X_imputed)
    """
    logger.info("train() — starting model training on %d rows", len(df))

    df = add_ecosystem_features(df)
    X, y = prepare_features(df)

    # Impute features
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    # Impute targets column-by-column with median
    y_filled = y.copy()
    for col in TARGET_COLS:
        col_median = y_filled[col].median()
        y_filled[col] = y_filled[col].fillna(col_median if not np.isnan(col_median) else 0.0)

    # XGBoost base estimator
    xgb_base = XGBRegressor(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbosity=0,
        tree_method="hist",   # faster on CPU
    )

    model = MultiOutputRegressor(xgb_base, n_jobs=-1)
    model.fit(X_scaled, y_filled.values)

    logger.info("train() — model fitted successfully")
    return model, imputer, scaler


# --------------------------------------------------------------------------- #
# 4. Predict                                                                    #
# --------------------------------------------------------------------------- #
def predict(
    df: pd.DataFrame,
    model,
    imputer,
    scaler,
) -> pd.DataFrame:
    """
    Run inference on all rows in df.

    Steps
    -----
    1. add_ecosystem_features (needed so peer-group columns exist)
    2. Extract FEATURE_COLS, impute, scale
    3. model.predict → pred_forwardPE, pred_priceToBook,
                       pred_enterpriseToEbitda, pred_beta

    Returns the original df (copy) with the four pred_* columns appended.
    """
    df = df.copy()
    df = add_ecosystem_features(df)

    # Ensure all feature columns exist
    for col in FEATURE_COLS:
        if col not in df.columns:
            df[col] = np.nan

    X = df[FEATURE_COLS].values
    X_imputed = imputer.transform(X)
    X_scaled = scaler.transform(X_imputed)

    preds = model.predict(X_scaled)   # shape (n, 4)

    for i, pred_col in enumerate(PRED_COLS):
        df[pred_col] = preds[:, i]

    logger.info("predict() — predictions added for %d firms", len(df))
    return df


# --------------------------------------------------------------------------- #
# 5. Dislocation score                                                          #
# --------------------------------------------------------------------------- #
def dislocation_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-firm dislocation for each target:

        disloc_<target> = (actual - predicted) / |predicted| * 100   [%]

    Where predicted is ~0 or undefined the raw difference is used instead
    to avoid division explosions.

    composite_dislocation
    ---------------------
    Each individual dislocation is z-scored across the cross-section, then
    the composite is the simple mean of those z-scores.  This puts all four
    metrics on equal footing regardless of their natural scale.

    Interpretation
    --------------
     positive  →  firm trades RICHER than model expects (potentially overvalued)
     negative  →  firm trades CHEAPER than model expects (potentially undervalued)
    """
    df = df.copy()

    disloc_arrays: list[pd.Series] = []

    for target, pred_col, disloc_col in zip(TARGET_COLS, PRED_COLS, DISLOC_COLS):
        if target not in df.columns or pred_col not in df.columns:
            df[disloc_col] = np.nan
            disloc_arrays.append(df[disloc_col])
            continue

        actual = pd.to_numeric(df[target], errors="coerce")
        predicted = pd.to_numeric(df[pred_col], errors="coerce")

        # Percentage deviation where |predicted| > 0.5, else raw difference
        abs_pred = predicted.abs()
        pct_dev = np.where(
            abs_pred > 0.5,
            (actual - predicted) / abs_pred * 100.0,
            actual - predicted,       # raw difference for near-zero predictions
        )

        df[disloc_col] = pct_dev
        disloc_arrays.append(df[disloc_col])

    # Composite dislocation — mean of per-metric z-scores
    z_scores = pd.DataFrame(index=df.index)
    for disloc_col in DISLOC_COLS:
        col_data = df[disloc_col].copy()
        col_mean = col_data.mean(skipna=True)
        col_std = col_data.std(skipna=True)
        if col_std and col_std > 0:
            z_scores[disloc_col] = (col_data - col_mean) / col_std
        else:
            z_scores[disloc_col] = 0.0

    df["composite_dislocation"] = z_scores.mean(axis=1, skipna=True)

    logger.info("dislocation_score() — dislocation computed for %d firms", len(df))
    return df


# --------------------------------------------------------------------------- #
# 6. Load-or-train (cache-aware entry point)                                   #
# --------------------------------------------------------------------------- #
def _model_is_fresh() -> bool:
    """Return True if MODEL_FILE exists and is younger than MODEL_TTL_HOURS."""
    if not os.path.isfile(MODEL_FILE):
        return False
    mtime = datetime.utcfromtimestamp(os.path.getmtime(MODEL_FILE))
    age = datetime.utcnow() - mtime
    return age < timedelta(hours=MODEL_TTL_HOURS)


def load_or_train(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, object, object, object]:
    """
    High-level entry point:

    - If MODEL_FILE exists and is <MODEL_TTL_HOURS old  → load model artefacts.
    - Otherwise  → retrain, serialise to MODEL_FILE, return fresh artefacts.

    After loading/training, runs predict() and dislocation_score() on the
    full df and returns:

        (predictions_df, model, imputer, scaler)

    where predictions_df contains all original columns plus:
        pred_forwardPE, pred_priceToBook, pred_enterpriseToEbitda, pred_beta,
        disloc_forwardPE, disloc_priceToBook, disloc_enterpriseToEbitda, disloc_beta,
        composite_dislocation
    """
    if _model_is_fresh():
        logger.info("load_or_train() — loading cached model from %s", MODEL_FILE)
        try:
            artefacts = joblib.load(MODEL_FILE)
            model = artefacts["model"]
            imputer = artefacts["imputer"]
            scaler = artefacts["scaler"]
            logger.info("Model loaded successfully")
        except Exception as exc:
            logger.warning("Failed to load model (%s) — retraining", exc)
            model, imputer, scaler = _fit_and_save(df)
    else:
        logger.info("load_or_train() — model stale or missing — retraining")
        model, imputer, scaler = _fit_and_save(df)

    # Run full inference pipeline
    predictions_df = predict(df, model, imputer, scaler)
    predictions_df = dislocation_score(predictions_df)

    return predictions_df, model, imputer, scaler


def _fit_and_save(df: pd.DataFrame) -> Tuple[object, object, object]:
    """Train the model and persist artefacts to MODEL_FILE."""
    model, imputer, scaler = train(df)
    try:
        joblib.dump(
            {"model": model, "imputer": imputer, "scaler": scaler,
             "trained_at": datetime.utcnow().isoformat()},
            MODEL_FILE,
        )
        logger.info("Model artefacts saved → %s", MODEL_FILE)
    except Exception as exc:
        logger.warning("Could not save model: %s", exc)
    return model, imputer, scaler


# --------------------------------------------------------------------------- #
# 7. Dislocation summary                                                        #
# --------------------------------------------------------------------------- #
def get_dislocation_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a clean, ranked summary DataFrame.

    Columns
    -------
    ticker, ecosystem, composite_dislocation,
    disloc_forwardPE, disloc_priceToBook, disloc_enterpriseToEbitda, disloc_beta,
    forwardPE, pred_forwardPE, enterpriseToEbitda, pred_enterpriseToEbitda

    Sorted by composite_dislocation descending
    (most 'rich' firms at the top, most 'cheap' firms at the bottom).
    """
    desired_cols = [
        "ticker",
        "ecosystem",
        "composite_dislocation",
        "disloc_forwardPE",
        "disloc_priceToBook",
        "disloc_enterpriseToEbitda",
        "disloc_beta",
        "forwardPE",
        "pred_forwardPE",
        "enterpriseToEbitda",
        "pred_enterpriseToEbitda",
    ]

    # Only include columns that actually exist
    present_cols = [c for c in desired_cols if c in df.columns]
    summary = df[present_cols].copy()

    # Round numeric columns for readability
    numeric_cols = [c for c in present_cols if c not in {"ticker", "ecosystem"}]
    for col in numeric_cols:
        summary[col] = pd.to_numeric(summary[col], errors="coerce").round(4)

    summary = summary.sort_values("composite_dislocation", ascending=False, na_position="last")
    summary = summary.reset_index(drop=True)

    logger.info(
        "get_dislocation_summary() — returning %d rows, %d columns",
        len(summary), len(summary.columns),
    )
    return summary


# --------------------------------------------------------------------------- #
# 8. Feature attribution                                                        #
# --------------------------------------------------------------------------- #
FEATURE_DISPLAY_NAMES: dict[str, str] = {
    "operatingMargins":         "Operating Margin",
    "profitMargins":            "Net Profit Margin",
    "returnOnEquity":           "Return on Equity",
    "returnOnAssets":           "Return on Assets",
    "revenueGrowth":            "Revenue Growth",
    "earningsGrowth":           "Earnings Growth",
    "debtToEquity":             "Debt / Equity",
    "leverage_ratio":           "Leverage (Debt/EBITDA)",
    "fcf_margin":               "FCF Margin",
    "interest_cover_proxy":     "Interest Coverage",
    "log_market_cap":           "Market Cap (log)",
    "ev_revenue":               "EV / Revenue",
    "grossMargins":             "Gross Margin",
    "currentRatio":             "Current Ratio",
    "ecosystem_median_pe":      "Peer Median P/E",
    "ecosystem_median_evebita": "Peer Median EV/EBITDA",
    "ecosystem_median_margin":  "Peer Median Margin",
    "ecosystem_size":           "Ecosystem Size",
}


def feature_attribution(
    ticker: str,
    full_df: pd.DataFrame,
    model,
    top_n: int = 7,
) -> pd.DataFrame:
    """
    Explain *why* a firm is RICH or CHEAP.

    For each input feature the function computes:
      - firm_value   : the firm's actual feature value
      - peer_median  : median across ecosystem peers
      - z_deviation  : (firm_value − peer_median) / peer_std
      - importance   : XGBoost feature importance averaged across 4 sub-models
      - score        : abs(z_deviation) × importance  (ranking signal)

    Returns a DataFrame of the top_n rows sorted by score descending.
    Columns: feature, display_name, firm_value, peer_median,
             z_deviation, importance, score
    """
    df = add_ecosystem_features(full_df.copy())

    mask = df["ticker"].str.upper() == ticker.upper()
    if not mask.any():
        logger.warning("feature_attribution: ticker %s not found", ticker)
        return pd.DataFrame()

    firm      = df[mask].iloc[0]
    ecosystem = firm.get("ecosystem", "Unknown")
    peer_df   = df[df["ecosystem"] == ecosystem] if ecosystem != "Unknown" else df

    # Average feature importances across all sub-estimators
    importances = np.zeros(len(FEATURE_COLS))
    try:
        for est in model.estimators_:
            importances += est.feature_importances_
        importances /= max(len(model.estimators_), 1)
    except AttributeError:
        importances = np.ones(len(FEATURE_COLS)) / len(FEATURE_COLS)

    rows = []
    for i, feat in enumerate(FEATURE_COLS):
        if feat not in df.columns:
            continue
        firm_val = firm.get(feat, np.nan)
        if pd.isna(firm_val):
            continue

        peer_vals   = pd.to_numeric(peer_df[feat], errors="coerce").dropna()
        if len(peer_vals) < 2:
            continue

        peer_median = float(peer_vals.median())
        peer_std    = float(peer_vals.std())
        z_dev       = (float(firm_val) - peer_median) / peer_std if peer_std > 0 else 0.0
        importance  = float(importances[i])
        score       = abs(z_dev) * importance

        rows.append({
            "feature":      feat,
            "display_name": FEATURE_DISPLAY_NAMES.get(feat, feat),
            "firm_value":   float(firm_val),
            "peer_median":  peer_median,
            "z_deviation":  z_dev,
            "importance":   importance,
            "score":        score,
        })

    if not rows:
        return pd.DataFrame()

    result = (
        pd.DataFrame(rows)
        .sort_values("score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    logger.info("feature_attribution(%s) — top %d drivers computed", ticker, len(result))
    return result


# --------------------------------------------------------------------------- #
# CLI convenience                                                                #
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    """
    Quick smoke-test: fetch data, train model, print dislocation summary.
    Usage:  python rv_model.py
    """
    from data_fetcher import get_data, enrich_with_ecosystem
    from ecosystems import TRAINING_TICKERS

    logger.info("=== Credit OS RV Model — smoke test ===")

    df_raw = get_data(TRAINING_TICKERS)
    df_enriched = enrich_with_ecosystem(df_raw)

    predictions_df, model, imputer, scaler = load_or_train(df_enriched)
    summary = get_dislocation_summary(predictions_df)

    print("\n=== Relative-Value Dislocation Summary ===")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 160)
    print(summary.to_string(index=False))
    print(f"\nModel file: {MODEL_FILE}")
    print("Done.")
