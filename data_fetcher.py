"""
data_fetcher.py
===============
Fetches real financial data from yfinance for every ticker in the training
universe.  Results are cached to data_cache.json (TTL = 24 h).  On cache
hit the heavy network loop is skipped entirely.

Main entry point:  get_data(tickers) → pd.DataFrame
Enrichment:        enrich_with_ecosystem(df)  → df with derived features
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import pandas as pd
import yfinance as yf

from ecosystems import TICKER_COUNTRY, TICKER_ECOSYSTEM

# --------------------------------------------------------------------------- #
# Configuration                                                                #
# --------------------------------------------------------------------------- #
CACHE_FILE = os.path.join(os.path.dirname(__file__), "data_cache.json")
CACHE_TTL_HOURS = 24

YFINANCE_FIELDS = [
    "trailingPE",
    "forwardPE",
    "priceToBook",
    "beta",
    "enterpriseToEbitda",
    "enterpriseValue",
    "marketCap",
    "totalRevenue",
    "ebitda",
    "freeCashflow",
    "totalDebt",
    "totalCash",
    "returnOnEquity",
    "returnOnAssets",
    "operatingMargins",
    "grossMargins",
    "profitMargins",
    "revenueGrowth",
    "earningsGrowth",
    "debtToEquity",
    "currentRatio",
    "trailingEps",
    "forwardEps",
    "sector",
    "industry",
    "country",
    "fullTimeEmployees",
    "dividendYield",
    "payoutRatio",
    "shortRatio",
    "heldPercentInstitutions",
]

# Numeric fields (everything except string meta-data)
_NUMERIC_FIELDS = [
    f for f in YFINANCE_FIELDS
    if f not in {"sector", "industry", "country"}
]

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(name)s  %(message)s",
)


# --------------------------------------------------------------------------- #
# Per-ticker fetch                                                              #
# --------------------------------------------------------------------------- #
def fetch_ticker(ticker: str) -> dict:
    """
    Fetch yfinance .info dict for a single ticker.
    Returns a dict with only the YFINANCE_FIELDS keys (or {} on failure).
    """
    try:
        info = yf.Ticker(ticker).info
        if not info or len(info) <= 1:
            logger.warning("yfinance returned empty info for %s", ticker)
            return {}
        result = {"ticker": ticker}
        for field in YFINANCE_FIELDS:
            result[field] = info.get(field, None)
        return result
    except Exception as exc:
        logger.warning("fetch_ticker(%s) failed: %s", ticker, exc)
        return {}


# --------------------------------------------------------------------------- #
# Batch fetch                                                                   #
# --------------------------------------------------------------------------- #
def fetch_all(tickers: list[str], delay: float = 0.3) -> dict[str, dict]:
    """
    Fetch all tickers sequentially with `delay` seconds between calls.
    Returns  {ticker: {field: value, ...}, ...}.
    Tickers that fail are stored as empty dicts.
    """
    results: dict[str, dict] = {}
    total = len(tickers)
    for i, ticker in enumerate(tickers, 1):
        logger.info("Fetching %s  (%d/%d)", ticker, i, total)
        data = fetch_ticker(ticker)
        results[ticker] = data
        if i < total:
            time.sleep(delay)
    return results


# --------------------------------------------------------------------------- #
# Cache helpers                                                                 #
# --------------------------------------------------------------------------- #
def load_cache() -> Optional[dict]:
    """
    Load the on-disk JSON cache.
    Returns the full cache dict if it exists and is younger than CACHE_TTL_HOURS,
    otherwise returns None.
    """
    if not os.path.isfile(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as fh:
            cache = json.load(fh)
        ts_str = cache.get("_timestamp")
        if ts_str is None:
            return None
        ts = datetime.fromisoformat(ts_str)
        age = datetime.utcnow() - ts
        if age < timedelta(hours=CACHE_TTL_HOURS):
            logger.info(
                "Cache hit — age %.1f h (TTL %d h)", age.total_seconds() / 3600, CACHE_TTL_HOURS
            )
            return cache
        logger.info(
            "Cache stale — age %.1f h, will re-fetch", age.total_seconds() / 3600
        )
        return None
    except Exception as exc:
        logger.warning("load_cache() error: %s — ignoring cache", exc)
        return None


def save_cache(data: dict) -> None:
    """
    Persist `data` to CACHE_FILE, stamping a UTC ISO timestamp.
    `data` is the raw {ticker: {field: value}} dict returned by fetch_all().
    """
    try:
        payload = dict(data)
        payload["_timestamp"] = datetime.utcnow().isoformat()
        with open(CACHE_FILE, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, default=_json_default, indent=2)
        logger.info("Cache saved → %s", CACHE_FILE)
    except Exception as exc:
        logger.warning("save_cache() failed: %s", exc)


def _json_default(obj):
    """JSON serialiser that converts numpy / pandas scalars to Python natives."""
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
        return None
    return str(obj)


# --------------------------------------------------------------------------- #
# Main entry point                                                              #
# --------------------------------------------------------------------------- #
def get_data(tickers: list[str], force_refresh: bool = False) -> pd.DataFrame:
    """
    Return a DataFrame with one row per ticker and columns = YFINANCE_FIELDS + ['ticker'].

    Logic:
    1. If force_refresh=False and cache is fresh  → use cache.
    2. Otherwise fetch live data and refresh cache.

    Numeric fields are coerced to float; non-numeric values and failures → NaN.
    String fields (sector, industry, country) are kept as-is (or empty string).
    """
    raw: dict[str, dict] = {}

    if not force_refresh:
        cache = load_cache()
        if cache is not None:
            # Extract only the tickers we need from the cache
            for t in tickers:
                if t in cache:
                    raw[t] = cache[t]
            # If all tickers are in cache, we're done
            missing = [t for t in tickers if t not in raw]
            if not missing:
                logger.info("All %d tickers served from cache", len(tickers))
            else:
                logger.info(
                    "%d tickers missing from cache — fetching live", len(missing)
                )
                fresh = fetch_all(missing)
                raw.update(fresh)
                # Merge with existing cache and re-save
                full_cache = {**{k: v for k, v in cache.items() if not k.startswith("_")}, **fresh}
                save_cache(full_cache)
        else:
            raw = fetch_all(tickers)
            save_cache(raw)
    else:
        logger.info("Force refresh — fetching all %d tickers live", len(tickers))
        raw = fetch_all(tickers)
        save_cache(raw)

    # Build DataFrame
    rows = []
    for ticker in tickers:
        entry = raw.get(ticker, {})
        row = {"ticker": ticker}
        for field in YFINANCE_FIELDS:
            row[field] = entry.get(field, None)
        rows.append(row)

    df = pd.DataFrame(rows)

    # Coerce numeric fields to float
    for col in _NUMERIC_FIELDS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Ensure string fields are strings (not None)
    for col in ["sector", "industry", "country"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)

    df = df.reset_index(drop=True)
    logger.info("get_data() complete — shape %s", df.shape)
    return df


# --------------------------------------------------------------------------- #
# Ecosystem enrichment + derived features                                       #
# --------------------------------------------------------------------------- #
def enrich_with_ecosystem(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add ecosystem and country from TICKER_ECOSYSTEM / TICKER_COUNTRY maps,
    then compute the following derived features:

    leverage_ratio       = totalDebt / (ebitda + 1)
        Proxy for financial leverage; higher = more indebted relative to earnings.

    fcf_margin           = freeCashflow / (totalRevenue + 1)
        Free cash flow as a fraction of revenue; key quality metric.

    interest_cover_proxy = ebitda / max(totalDebt * 0.05, 1)
        Approximates interest coverage assuming ~5 % average cost of debt.

    log_market_cap       = log(marketCap + 1)
        Log-transforms the highly skewed market-cap distribution.

    ev_revenue           = enterpriseValue / (totalRevenue + 1)
        Enterprise-value to revenue; widely used for high-growth or low-margin firms.
    """
    df = df.copy()

    # --- Ecosystem and country from our own maps (override yfinance 'country') --- #
    df["ecosystem"] = df["ticker"].map(TICKER_ECOSYSTEM).fillna("Unknown")
    df["domicile"] = df["ticker"].map(TICKER_COUNTRY).fillna("Unknown")

    # --- Guard: ensure required numeric columns exist and are float -------------- #
    for col in ["totalDebt", "ebitda", "freeCashflow", "totalRevenue", "marketCap", "enterpriseValue"]:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Derived features -------------------------------------------------------- #
    # leverage_ratio
    df["leverage_ratio"] = df["totalDebt"] / (df["ebitda"].abs() + 1.0)
    # Clip extreme values (e.g. negative EBITDA producing nonsense ratios)
    df["leverage_ratio"] = df["leverage_ratio"].clip(-50, 50)

    # fcf_margin
    df["fcf_margin"] = df["freeCashflow"] / (df["totalRevenue"].abs() + 1.0)
    df["fcf_margin"] = df["fcf_margin"].clip(-5, 5)

    # interest_cover_proxy: ebitda / max(totalDebt * 0.05, 1)
    assumed_interest = (df["totalDebt"].fillna(0) * 0.05).clip(lower=1.0)
    df["interest_cover_proxy"] = df["ebitda"] / assumed_interest
    df["interest_cover_proxy"] = df["interest_cover_proxy"].clip(-200, 200)

    # log_market_cap
    df["log_market_cap"] = np.log1p(df["marketCap"].clip(lower=0))

    # ev_revenue
    df["ev_revenue"] = df["enterpriseValue"] / (df["totalRevenue"].abs() + 1.0)
    df["ev_revenue"] = df["ev_revenue"].clip(-100, 500)

    logger.info("enrich_with_ecosystem() — derived features added, shape %s", df.shape)
    return df
