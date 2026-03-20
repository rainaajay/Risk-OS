"""
app.py — Risk OS
Streamlit: portfolio · full network · entity deep-dive
Features: signal ticker, exposure breakdown, score drilldown, scenarios, nav history, node inspector
"""
from __future__ import annotations
import math
import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from entities import ENTITIES, NETWORKS, SIGNALS, compute_scores, signals_for_entity

# ─── THEME ────────────────────────────────────────────────────────────────────
BG      = "#0f172a"
CARD_BG = "#1e293b"
BORDER  = "#334155"
TEXT    = "#e2e8f0"
MUTED   = "#94a3b8"
RAG_COL = {"RED": "#ef4444", "AMBER": "#f59e0b", "GREEN": "#22c55e"}
NODE_COL = {
    "CP": "#3b82f6", "SUBSIDIARY": "#8b5cf6", "SUPPLIER": "#f97316",
    "CUSTOMER": "#14b8a6", "COUNTRY": "#22c55e", "SHAREHOLDER": "#eab308",
    "LENDER": "#ef4444", "COMPETITOR": "#ec4899", "REGULATOR": "#94a3b8",
}
EDGE_COL = {
    "OWNS": "#8b5cf6", "SUPPLIES": "#f97316", "CUSTOMER": "#14b8a6",
    "OPERATES": "#22c55e", "LENDS": "#ef4444", "COMPETES": "#ec4899",
    "REGULATES": "#94a3b8",
}

# ─── EXPOSURE DATA (instrument breakdown per CP) ──────────────────────────────
EXPOSURES: dict = {
    "CP001": [
        {"type": "Syndicated Loan", "notional_m": 95.0,  "detail": "RCF €12bn syndicate; BBB- rating trigger; 2027 maturity"},
        {"type": "Bond Holding",    "notional_m": 85.0,  "detail": "VW Finance 0.875% EUR senior unsecured 2026; fair value ~£82M"},
        {"type": "Trade Finance",   "notional_m": 45.0,  "detail": "LC/guarantee supply chain; co-fronted DZ Bank; revolving"},
        {"type": "FX Derivative",   "notional_m": 20.0,  "detail": "EUR/GBP forward 2025-12; MTM loss -£2.1M; collateral posted"},
    ],
    "CP003": [
        {"type": "Bond Holding",    "notional_m": 110.0, "detail": "Mercedes-Benz 1.5% EUR senior 2027; A- rated; fair value ~£108M"},
        {"type": "Syndicated Loan", "notional_m": 50.0,  "detail": "Revolving credit facility; MB FS captive; 2026 maturity"},
        {"type": "Interest Rate Swap","notional_m": 20.0,"detail": "EUR fixed-to-float IRS; positive MTM +£1.3M; hedging bond"},
    ],
    "CP005": [
        {"type": "HY Bond Holding", "notional_m": 30.0,  "detail": "AML 10.5% senior secured 2029; trading 88p/£; fair value ~£26M"},
        {"type": "Syndicated Loan", "notional_m": 15.0,  "detail": "Term loan B; super-senior secured; Gaydon plant collateral"},
        {"type": "2nd Lien Note",   "notional_m": 7.0,   "detail": "Second lien notes 2030; trading 72p/£; fair value ~£5M"},
    ],
    "CP006": [
        {"type": "Syndicated Loan", "notional_m": 120.0, "detail": "RCF €12bn syndicate; BB rated; covenant waiver active; 2026"},
        {"type": "Term Loan",       "notional_m": 50.0,  "detail": "TLB WABCO acquisition legacy; BB-; amortising; 2027 maturity"},
        {"type": "Trade Finance",   "notional_m": 25.0,  "detail": "Performance bonds; supply chain guarantees; revolving"},
    ],
    "CP007": [
        {"type": "Bond Holding",    "notional_m": 95.0,  "detail": "Continental 0.0% EUR 2025 (IG); BBB- watch; fair value ~£94M"},
        {"type": "Syndicated Loan", "notional_m": 50.0,  "detail": "RCF €5bn syndicate; BBB- trigger; 2026 maturity; margin step-up"},
        {"type": "FX Derivative",   "notional_m": 15.0,  "detail": "USD/EUR cross-currency swap; MTM neutral; hedging USD revenues"},
    ],
    "CP009": [
        {"type": "Term Loan",       "notional_m": 25.0,  "detail": "Green term loan; D-rated; Ch.11 DIP financing claim; senior secured"},
        {"type": "Green Bond",      "notional_m": 13.0,  "detail": "EIB co-guaranteed green notes; battery gigafactory; impaired"},
    ],
    "CP013": [
        {"type": "Bond Holding",    "notional_m": 55.0,  "detail": "Wizz Air 1.35% EUR 500M Nov 2026; B rated; trading 91p/£"},
        {"type": "Revolving Credit","notional_m": 20.0,  "detail": "RCF £300M facility; drawn £20M; GTF crisis drawing risk"},
        {"type": "Aircraft Finance","notional_m": 13.0,  "detail": "JOLCO aircraft lease receivable; A320neo collateral"},
    ],
    "CP023": [
        {"type": "Class A Bond",    "notional_m": 180.0, "detail": "Thames Water Class A index-linked bonds; ring-fenced OpCo; 85p/£"},
        {"type": "Class B Bond",    "notional_m": 60.0,  "detail": "Thames Water Class B subordinated; 45p/£; near-zero expected recovery"},
        {"type": "RCF",             "notional_m": 70.0,  "detail": "Revolving credit facility; undrawn £180M; committed to 2026"},
    ],
    "CP028": [
        {"type": "Secured RE Loan", "notional_m": 90.0,  "detail": "First-charge RE loan; prime Vienna/Berlin collateral; 30-60p/£ recovery"},
        {"type": "Unsecured Bond",  "notional_m": 50.0,  "detail": "Signa unsecured notes; insolvency proceedings; 5-15p/£ recovery"},
    ],
    "CP033": [
        {"type": "Bond Holding",    "notional_m": 45.0,  "detail": "Atos 8% PIK new bonds post-restructuring; CCC rated; distressed"},
        {"type": "RCF",             "notional_m": 20.0,  "detail": "Restructured revolving facility; CCC; French safeguard terms"},
        {"type": "Trade Finance",   "notional_m": 7.0,   "detail": "IT equipment/licence bonds; small; cross-default risk"},
    ],
}

# ─── SCENARIO DATA per CP ─────────────────────────────────────────────────────
SCENARIOS: dict = {
    "CP001": [
        {"name": "Fallen Angel",        "dir": "worse", "prob": "25%", "impact": "+£35M ECL",
         "trigger": "S&P downgrades to BB+; IG index exclusion",
         "detail": "Bond forced-selling (~€6bn); loan covenant triggered; ZF/Continental cascade. Full portfolio impact likely."},
        {"name": "China Stabilisation", "dir": "better","prob": "30%", "impact": "-£12M ECL",
         "trigger": "VW China volume +10% YoY; BYD share plateaus",
         "detail": "JV profits recover; FCF >8% of debt; CreditWatch Negative lifted; BBB stable restored."},
        {"name": "IG Metall Deal",      "dir": "better","prob": "40%", "impact": "-£8M ECL",
         "trigger": "Works council agrees plant closure plan",
         "detail": "€4bn annual savings crystallise; management credibility restored; market relief rally."},
        {"name": "Supply Chain Seizure","dir": "worse", "prob": "5%",  "impact": "+£65M ECL",
         "trigger": "ZF + Continental both miss covenant — simultaneous stress",
         "detail": "Production halted; revenue -€8bn; immediate CCC downgrade; accelerated loan maturity."},
    ],
    "CP003": [
        {"name": "China Luxury Collapse","dir":"worse","prob":"20%","impact":"+£18M ECL",
         "trigger":"China luxury revenue -30%; ASP compression on EQ range",
         "detail":"A- breached; BBB+ downgrade; dividend suspended; FCF negative; MB FS RCF drawn."},
        {"name": "EV Resurgence",       "dir":"better","prob":"35%","impact":"-£6M ECL",
         "trigger":"EQS/EQE demand inflects +20%; Taycan competition eases",
         "detail":"EV margin improves to 8%; net cash position grows; A- reaffirmed with stable outlook."},
        {"name": "AML Engine Contract Ends","dir":"neutral","prob":"15%","impact":"Neutral",
         "trigger":"Aston Martin enters administration; AMG supply terminated",
         "detail":"<0.5% AMG revenue impact; reputational headline risk; AMG unit resold to new manufacturer."},
    ],
    "CP005": [
        {"name": "Going Concern Resolved","dir":"better","prob":"30%","impact":"-£8M ECL",
         "trigger":"Saudi PIF / Geely inject fresh equity at market; going concern clause removed",
         "detail":"Cash runway extends to 18M+; bonds rally to par; going concern clause removed; CCC→CC lifted."},
        {"name": "Administration",       "dir":"worse", "prob":"30%","impact":"+£18M ECL",
         "trigger":"Rights issue fails; cash exhausted within 6 months",
         "detail":"UK administration; receivers appointed; Mercedes engine supply ceases; Gaydon sold; ~30p/£ recovery."},
        {"name": "Geely Full Acquisition","dir":"better","prob":"20%","impact":"-£15M ECL",
         "trigger":"Geely increases to 51%; provides balance sheet backing",
         "detail":"Debt refinanced at investment grade rates; EV powertrain access secured; CCC→B+ upgrade path."},
    ],
    "CP006": [
        {"name": "Covenant Breach",      "dir":"worse","prob":"35%","impact":"+£40M ECL",
         "trigger":"Net debt/EBITDA exceeds 5.5x; waiver not obtained",
         "detail":"Acceleration of €12bn RCF; forced asset sales; ZF's private structure means no market signal before breach."},
        {"name": "EV Pivot Success",     "dir":"better","prob":"25%","impact":"-£20M ECL",
         "trigger":"ZF e-axle volumes replace 50% of ICE transmission revenue",
         "detail":"2026-28 EV products ramp; BMW 8HP successor wins; debt/EBITDA falls below 4x; Ba1 upgrade path."},
        {"name": "OEM Consolidation",    "dir":"better","prob":"20%","impact":"-£10M ECL",
         "trigger":"VW stabilises production; Stellantis renews 8HP contract",
         "detail":"Revenue -volume shock reverses; €800M cost savings delivered; liquidity improves."},
    ],
    "CP007": [
        {"name": "IG Breach",            "dir":"worse","prob":"30%","impact":"+£22M ECL",
         "trigger":"Fitch downgrades to BB+; IG index removal",
         "detail":"Bond spread +200bps; RCF step-up triggered; tyre division margin under pressure; Schaeffler forced sell-down."},
        {"name": "Tyre / Auto Split",    "dir":"better","prob":"25%","impact":"-£12M ECL",
         "trigger":"Conglomerate separation; pure-play tyre company",
         "detail":"Tyre multiple 12-14x vs automotive 6-8x; €4bn+ value unlocked; remaining auto stub refinanced."},
        {"name": "Schaeffler Distress",  "dir":"worse","prob":"15%","impact":"+£30M ECL",
         "trigger":"Schaeffler forced to sell 46% Continental stake at distressed price",
         "detail":"Massive selling overhang; Continental share -30%; refinancing risk elevated; governance vacuum."},
    ],
    "CP009": [
        {"name": "CATL Asset Sale",      "dir":"better","prob":"40%","impact":"-£8M ECL",
         "trigger":"CATL acquires Skellefteå factory at €600M+",
         "detail":"D-rated; recovery improves to 40p/£; our £38M EAD recovers ~£15M; above base case."},
        {"name": "Liquidation",          "dir":"worse","prob":"35%","impact":"+£8M ECL",
         "trigger":"No buyer; factory scrapped; IP worthless",
         "detail":"Recovery <15p/£; our £38M EAD losses ~£33M; EIB political fallout; Swedish state losses."},
        {"name": "Swedish State Rescue",  "dir":"better","prob":"15%","impact":"-£12M ECL",
         "trigger":"Swedish government provides DIP-to-exit; restructured as national champion",
         "detail":"Political decision; recovery path to 60p/£; restructured bonds trading up; 24M process."},
    ],
    "CP013": [
        {"name": "Nov 2026 Bond Default","dir":"worse","prob":"20%","impact":"+£28M ECL",
         "trigger": "EBITDA <€200M; Nov 2026 €500M bond cannot be refinanced",
         "detail": "B-rated; cross-default on RCF; aircraft lessors repossess; administration; 40p/£ recovery."},
        {"name": "GTF Resolution",       "dir":"better","prob":"45%","impact":"-£15M ECL",
         "trigger":"All P&W-affected aircraft return to service by Q3 2025",
         "detail":"EBITDA guidance restored to €550M+; bond refinanced successfully; B→B+ upgrade path."},
        {"name": "Hungary Crisis",       "dir":"worse","prob":"15%","impact":"+£10M ECL",
         "trigger":"Hungary EU sanctions; Wizz Hungary AOC suspended",
         "detail":"EU regulatory action on Hungary; Wizz restructures to Malta/UK OpCos; 6-month ops disruption."},
    ],
    "CP023": [
        {"name": "Special Administration","dir":"worse","prob":"40%","impact":"+£35M ECL",
         "trigger":"Equity injection fails; HMG appoints SAR administrator",
         "detail":"Class B bonds near-zero; Class A 60-75p/£; restructuring 18-24M; operational continuity maintained."},
        {"name": "Equity Injection",     "dir":"better","prob":"25%","impact":"-£25M ECL",
         "trigger":"New investors inject £4-5bn; Ofwat resets PR24 determination",
         "detail":"Bonds trade to par; RCF undrawn; going concern lifted; ratings recover to BBB over 3 years."},
        {"name": "Ofwat Reset",          "dir":"better","prob":"20%","impact":"-£10M ECL",
         "trigger":"Courts overturn PR24; Ofwat grants £5.5bn capex",
         "detail":"Regulatory certainty returns; Class A bonds recover to 95p; equity slim value restored."},
    ],
    "CP028": [
        {"name": "Selfridges Sale Closes","dir":"better","prob":"60%","impact":"-£15M ECL",
         "trigger":"Thai Central/QIA acquire Selfridges at £3.2bn+",
         "detail":"Secured RE lenders recover 40-60p/£; our secured loan recovers ~£54M of £90M."},
        {"name": "Elbtower Fire-sale",    "dir":"worse","prob":"30%","impact":"+£10M ECL",
         "trigger":"Hamburg Elbtower sold at €200M vs €800M book",
         "detail":"Unsecured creditor recovery falls to 5p/£; further Helaba/BayernLB provisions."},
        {"name": "Benko Fraud Conviction","dir":"neutral","prob":"70%","impact":"Neutral",
         "trigger":"René Benko convicted; personal assets confiscated",
         "detail":"No incremental impact on our position; Laret Foundation assets already frozen in proceedings."},
    ],
    "CP033": [
        {"name": "French Gov Contract Loss","dir":"worse","prob":"30%","impact":"+£20M ECL",
         "trigger":"French MoD/nuclear contracts lost to Capgemini post-restructuring review",
         "detail":"25% revenue loss; Tech Foundations EP Equity covenant breach; CCC bonds trade to 50p."},
        {"name": "Onepoint Conflict Resolved","dir":"better","prob":"20%","impact":"-£8M ECL",
         "trigger":"Onepoint divests or governance restructured; clean board established",
         "detail":"Corporate governance discount removed; bonds trade up; new management credibility restored."},
        {"name": "Eviden Sold at Premium","dir":"better","prob":"25%","impact":"-£12M ECL",
         "trigger":"Strategic buyer acquires Eviden for €2bn+; proceeds distributed",
         "detail":"PIK bonds redeemed at par; RCF fully repaid; residual Tech Foundations de-risks further."},
    ],
}

# ─── COUNTRY RISK SCORES (for network diagram RAG colouring) ──────────────────
COUNTRY_SCORES: dict = {
    "CTY_DE": {"rag":"AMBER","score":52,"flag":"🇩🇪","note":"Recession 2024; industrial contraction; fiscal stalemate"},
    "CTY_CN": {"rag":"RED",  "score":74,"flag":"🇨🇳","note":"Property crisis; BYD disruption; US tariff war escalating"},
    "CTY_US": {"rag":"AMBER","score":46,"flag":"🇺🇸","note":"Strong growth; tariff uncertainty under Trump 2.0"},
    "CTY_UK": {"rag":"AMBER","score":44,"flag":"🇬🇧","note":"Fiscal consolidation; regulatory risk; Thames/water crisis"},
    "CTY_SE": {"rag":"GREEN","score":27,"flag":"🇸🇪","note":"Stable AAA; Northvolt political exposure limited"},
    "CTY_FR": {"rag":"AMBER","score":45,"flag":"🇫🇷","note":"Political uncertainty; Atos/defense sector review"},
    "CTY_AT": {"rag":"GREEN","score":21,"flag":"🇦🇹","note":"Stable AA; Signa contagion contained"},
    "CTY_PL": {"rag":"GREEN","score":24,"flag":"🇵🇱","note":"Strong growth; EU funds; A- rated"},
    "CTY_HU": {"rag":"RED",  "score":76,"flag":"🇭🇺","note":"EU sanctions risk; Orban/Russia alignment; Wizz Air AOC risk"},
    "CTY_JP": {"rag":"GREEN","score":30,"flag":"🇯🇵","note":"Stable A+; Toyota competition to EU autos"},
    "CTY_KR": {"rag":"GREEN","score":28,"flag":"🇰🇷","note":"AA-; Samsung SDI/POSCO key battery suppliers"},
    "CTY_NL": {"rag":"GREEN","score":19,"flag":"🇳🇱","note":"AAA; stable; major holding co domicile"},
    "CTY_ES": {"rag":"GREEN","score":33,"flag":"🇪🇸","note":"A; improving fiscal; SEAT/Cupra hub"},
    "CTY_CZ": {"rag":"GREEN","score":25,"flag":"🇨🇿","note":"A+; Škoda hub; stable EU member"},
    "CTY_RO": {"rag":"AMBER","score":43,"flag":"🇷🇴","note":"Fiscal deficit; Wizz hub; EU transfer risk"},
    "CTY_UA": {"rag":"RED",  "score":89,"flag":"🇺🇦","note":"Active war; supply disruption; wire harness risk"},
    "CTY_IN": {"rag":"GREEN","score":31,"flag":"🇮🇳","note":"BBB-; strong growth; Tata Motors / JLR exposure"},
    "CTY_CH": {"rag":"GREEN","score":17,"flag":"🇨🇭","note":"AAA; stable; Julius Bär / UBS headquartered"},
    "CTY_NO": {"rag":"GREEN","score":15,"flag":"🇳🇴","note":"AAA; Norges Bank sovereign wealth fund"},
    "CTY_AU": {"rag":"GREEN","score":22,"flag":"🇦🇺","note":"AAA; Macquarie infra ownership in networks"},
}

# ─── ENTITY RISK SCORES for key named network nodes ─────────────────────────
# Covers banks, investors, regulators, major suppliers that appear across networks.
# Same schema as COUNTRY_SCORES: rag, score (0-100), note
NODE_RISK_SCORES: dict = {
    # ── Banks / lenders ───────────────────────────────────────────────────────
    "BANK_DB":          {"rag":"AMBER","score":48,"note":"Deutsche Bank: CIB restructuring; €600M Signa provision; Russia exposure"},
    "BANK_BNP":         {"rag":"GREEN","score":29,"note":"BNP Paribas: A+; solid capital; diversified; minimal distressed exposure"},
    "BANK_HSBC":        {"rag":"AMBER","score":38,"note":"HSBC: A; Hong Kong/China concentration; strategic pivot ongoing"},
    "BANK_COMMERZ":     {"rag":"AMBER","score":42,"note":"Commerzbank: BBB+; UniCredit takeover bid; capital uncertainty"},
    "BANK_UNICREDIT":   {"rag":"GREEN","score":31,"note":"UniCredit: A-; strong Italy/CEE franchise; Commerzbank acquisition risk"},
    "BANK_LLOYDS":      {"rag":"GREEN","score":26,"note":"Lloyds: A; strong UK retail; motor finance PCP liability risk (£3.9bn)"},
    "BANK_BARCLAYS":    {"rag":"GREEN","score":28,"note":"Barclays: A; diversified; US card book; TNAV discount narrowing"},
    "BANK_GS":          {"rag":"GREEN","score":24,"note":"Goldman Sachs: A+; IB revenues recovering; consumer exit complete"},
    "BANK_JPM":         {"rag":"GREEN","score":18,"note":"JP Morgan: AA-; fortress balance sheet; best-in-class capital ratios"},
    "BANK_MS":          {"rag":"GREEN","score":22,"note":"Morgan Stanley: A+; WM majority earnings; stable revenue mix"},
    "BANK_CS":          {"rag":"RED",  "score":72,"note":"Credit Suisse: absorbed by UBS Mar 2023; legacy litigation risk remains"},
    "BANK_JULIUS_BAR":  {"rag":"AMBER","score":55,"note":"Julius Bär: CHF 606M Signa loss; CEO resigned Jan 2024; FINMA scrutiny"},
    "BANK_EIB":         {"rag":"GREEN","score":20,"note":"EIB: AAA; EU policy bank; Northvolt SEK 9.5bn political embarrassment"},
    "BANK_HELABA":      {"rag":"AMBER","score":44,"note":"Helaba: A; Signa Elbtower exposure; Frankfurt RE market stress"},
    "BANK_BAYERNLB":    {"rag":"AMBER","score":41,"note":"BayernLB: A; Signa exposure provisioned; CRE portfolio watch"},
    "BANK_NATWEST":     {"rag":"GREEN","score":27,"note":"NatWest: A; strong retail; government stake reducing; clean book"},
    "BANK_MEDIOB":      {"rag":"GREEN","score":33,"note":"Mediobanca: BBB+; Italy exposure; Monte Paschi stake risk"},
    # ── Investors / shareholders ───────────────────────────────────────────────
    "INV_BLACKROCK":    {"rag":"GREEN","score":14,"note":"BlackRock: AA-; $10tn AUM; systemic but stable; no credit concern"},
    "INV_NORGES":       {"rag":"GREEN","score":12,"note":"Norges Bank Investment Mgmt: AAA (sovereign); 1.5% of global equities"},
    "INV_VANGUARD":     {"rag":"GREEN","score":13,"note":"Vanguard: AA; passive giant; no credit risk; governance voting influence"},
    "INV_STATESTREET":  {"rag":"GREEN","score":15,"note":"State Street: A+; custodian bank; ESG proxy voting pressure"},
    "INV_APOLLO":       {"rag":"AMBER","score":40,"note":"Apollo: BBB+; distressed debt specialist; Signa / Thames exposure"},
    "INV_PIMCO":        {"rag":"GREEN","score":19,"note":"PIMCO: AA (Allianz backed); large IG/HY bond holder across CPs"},
    "INV_GEELY":        {"rag":"AMBER","score":45,"note":"Geely: BB+; Aston Martin 17% stake; over-extended acquisition strategy"},
    "INV_PIF":          {"rag":"GREEN","score":22,"note":"Saudi PIF: AA (sovereign); AML potential investor; deep pockets"},
    "INV_QIA":          {"rag":"GREEN","score":18,"note":"Qatar Investment Authority: AA (sovereign); Selfridges bidder"},
    "INV_THAI_CENTRAL": {"rag":"GREEN","score":25,"note":"Central Group (Thailand): Selfridges acquirer; family-owned retail giant"},
    "INV_SCHAEFFER":    {"rag":"AMBER","score":52,"note":"Schaeffler family: 46% Continental stake; €1.3bn paper loss; disposal risk"},
    "INV_PORSCHE_FAM":  {"rag":"AMBER","score":38,"note":"Porsche/Piëch family: controls VW via Porsche SE; 31.9% voting rights"},
    # ── Regulators ────────────────────────────────────────────────────────────
    "REG_EUCOMM":       {"rag":"AMBER","score":35,"note":"EU Commission: CBAM + EV mandate uncertainty; auto lobby pressure"},
    "REG_BAFIN":        {"rag":"GREEN","score":20,"note":"BaFin: stable; Signa oversight scrutinised; Wirecard legacy reforms done"},
    "REG_FCA":          {"rag":"GREEN","score":22,"note":"FCA: active enforcement; motor PCP investigation; Thames scrutiny"},
    "REG_ECB":          {"rag":"GREEN","score":18,"note":"ECB: rate plateau; bank supervision tightened post-SVB; stable"},
    "REG_OFWAT":        {"rag":"RED",  "score":65,"note":"Ofwat: PR24 determination triggering Thames administration risk; political pressure"},
    "REG_OFGEM":        {"rag":"AMBER","score":36,"note":"Ofgem: energy sector oversight; spillover scrutiny to water"},
    "REG_FAA":          {"rag":"AMBER","score":42,"note":"FAA: P&W GTF AD; global grounding orders; airline fleet risk"},
    "REG_EASA":         {"rag":"AMBER","score":38,"note":"EASA: mirrors FAA GTF directive; Wizz European fleet risk"},
    "REG_FRENCH_GOV":   {"rag":"AMBER","score":44,"note":"French government: Atos defense contract review; political uncertainty"},
    "REG_CMAUK":        {"rag":"GREEN","score":21,"note":"CMA: merger review; water sector; standard regulatory activity"},
    # ── Major suppliers / named companies ─────────────────────────────────────
    "EXT_BOSCH":        {"rag":"AMBER","score":40,"note":"Robert Bosch: private; AA equivalent; EV transition cost €1.5bn/yr"},
    "EXT_CATL":         {"rag":"GREEN","score":29,"note":"CATL: A-; dominant EV battery; Northvolt volume winner; China risk"},
    "EXT_SAMSUNG_SDI":  {"rag":"GREEN","score":24,"note":"Samsung SDI: A; diversified battery; European gigafactory on track"},
    "EXT_BMW":          {"rag":"GREEN","score":26,"note":"BMW: A; Northvolt €2bn loss absorbed; CATL pivot complete; strong FCF"},
    "EXT_AIRBUS":       {"rag":"GREEN","score":21,"note":"Airbus: A; record backlog 8,598 aircraft; P&W GTF compensated"},
    "EXT_PRATT_WHITNEY": {"rag":"RED", "score":68,"note":"Pratt & Whitney: $3bn GTF reserve; 600+ aircraft grounded globally"},
    "EXT_BASF":         {"rag":"AMBER","score":37,"note":"BASF: BBB+; energy cost shock; auto chemicals exposure; restructuring"},
    "EXT_PORSCHE":      {"rag":"GREEN","score":28,"note":"Porsche AG: A-; strong FCF; luxury demand resilient vs volume brands"},
    "EXT_LOWER_SAX":    {"rag":"GREEN","score":18,"note":"Lower Saxony: AA (German Länder); VW golden share; stable"},
    "EXT_OFWAT":        {"rag":"RED",  "score":65,"note":"Ofwat: PR24 triggering Thames crisis (same risk as REG_OFWAT)"},
    "EXT_JULIUS_BAR":   {"rag":"AMBER","score":55,"note":"Julius Bär: CHF 606M Signa loss; CEO resigned; see BANK_JULIUS_BAR"},
    "EXT_AMG":          {"rag":"GREEN","score":23,"note":"Mercedes-AMG: profitable AMG division; AML supply <0.5% capacity"},
    "EXT_RENAULT":      {"rag":"AMBER","score":41,"note":"Renault: BB+; Nissan alliance friction; EV transition costs"},
    "EXT_TOYOTA":       {"rag":"GREEN","score":17,"note":"Toyota: A+; strong hybrid strategy; record profits 2024"},
    "EXT_TATA":         {"rag":"AMBER","score":36,"note":"Tata Motors / JLR: BB; EV capex heavy; UK plant dependent on govt support"},
}

# ─── SCENARIO → LINKED SIGNALS (short tags) ────────────────────────────────
SCENARIO_LINKED_SIGNALS: dict = {
    "CP001": {
        "Fallen Angel":        ["S&P CreditWatch Negative", "VW 35K job cuts + plant closures", "China sales −15% YoY"],
        "China Stabilisation": ["China BYD market share signal", "VW China JV profits declining"],
        "IG Metall Deal":      ["VW job cuts + works council opposition"],
        "Supply Chain Seizure":["ZF covenant waiver discussions", "VW volume cuts → €900M ZF impact"],
    },
    "CP003": {
        "China Luxury Collapse":   ["Mercedes Q3 profit warning: China −13%"],
        "EV Resurgence":           ["Mercedes Q3 profit warning: EV margin pressure"],
        "AML Engine Contract Ends":["Mercedes AMG supply dependency confirmed"],
    },
    "CP005": {
        "Going Concern Resolved": ["Going concern clause FY2024 accounts", "AML volume guidance cut"],
        "Administration":         ["Going concern clause FY2024 accounts", "100% AMG engine dependency"],
        "Geely Full Acquisition": ["Going concern clause FY2024 accounts"],
    },
    "CP006": {
        "Covenant Breach":    ["ZF covenant waiver discussions", "VW volume cuts −€900M ZF revenue", "VW plant closures → Tier-1 orders −€2bn"],
        "EV Pivot Success":   ["ZF covenant waiver — EV e-axle context"],
        "OEM Consolidation":  ["VW plant closures cut Tier-1 orders", "VW volume cuts removing ZF revenue"],
    },
    "CP007": {
        "IG Breach":        ["Continental BBB− negative outlook", "VW plant closures cut Tier-1 orders"],
        "Tyre / Auto Split":["Schaeffler 46% voting stake — governance risk"],
        "Schaeffler Distress":["Schaeffler 46% voting stake — forced disposal risk"],
    },
    "CP009": {
        "CATL Asset Sale":     ["Northvolt Chapter 11 filed", "Skellefteå factory: 15–25p/£ recovery"],
        "Liquidation":         ["Northvolt Chapter 11 filed", "BMW €2bn contract cancellation trigger"],
        "Swedish State Rescue":["Northvolt Chapter 11 filed", "SEK 9.5bn emergency state support"],
    },
    "CP013": {
        "Nov 2026 Bond Default":["50 aircraft grounded by P&W GTF — €350M EBITDA", "P&W GTF 600+ aircraft affected globally"],
        "GTF Resolution":       ["50 aircraft grounded by P&W GTF inspections", "P&W GTF powder metal contamination"],
        "Hungary Crisis":       ["Wizz Hungary: HUF −22% YTD; Orban policy risk"],
    },
    "CP023": {
        "Special Administration":["Ofwat PR24: £3.25bn allowed vs £7.2bn asked", "Thames equity written to zero", "278 sewage spill investigations"],
        "Equity Injection":      ["Thames Water: equity written to zero; £18.3bn debt"],
        "Ofwat Reset":           ["Ofwat PR24 determination: sector-wide capex cut", "Ofwat final determination — Thames worst affected"],
    },
    "CP028": {
        "Selfridges Sale Closes": ["Signa insolvency: €23bn liabilities", "Signa recovery: 30–60p/£ secured"],
        "Elbtower Fire-sale":     ["Signa recovery: unsecured near-zero", "Julius Bär CHF 606M write-off"],
        "Benko Fraud Conviction": ["Signa insolvency: Benko arrested Dec 2024"],
    },
    "CP033": {
        "French Gov Contract Loss":   ["Atos €5bn restructuring: distressed PIK bonds", "French MoD reviewing Atos contracts"],
        "Onepoint Conflict Resolved": ["Atos €5bn restructuring: Onepoint conflict"],
        "Eviden Sold at Premium":     ["Atos €5bn restructuring: Eviden ring-fenced"],
    },
}

st.set_page_config(page_title="Risk OS", page_icon="🏦",
                   layout="wide", initial_sidebar_state="expanded")
st.markdown(f"""
<style>
  html,body,[data-testid="stAppViewContainer"]{{background:{BG};color:{TEXT};}}
  [data-testid="stSidebar"]{{background:#0a1628;}}
  div[data-testid="stMetricValue"]{{color:{TEXT};}}
  div[data-testid="stMetricLabel"]{{color:{MUTED};font-size:12px;}}
  h1,h2,h3{{color:{TEXT};}}
  .stTabs [data-baseweb="tab"]{{color:{MUTED};}}
  .stTabs [aria-selected="true"]{{color:{TEXT};}}
  div[data-testid="stButton"]>button{{background:transparent;border:1px solid {BORDER};color:{TEXT};text-align:left;}}
  div[data-testid="stButton"]>button:hover{{background:{CARD_BG};border-color:{MUTED};}}
</style>""", unsafe_allow_html=True)

@st.cache_data
def get_scores():
    return compute_scores()
SCORES = get_scores()

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def sentiment_icon(s: float) -> str:
    if s >= 0.3:  return "🟢"
    if s >= 0.0:  return "🟡"
    if s >= -0.3: return "🟠"
    return "🔴"

def rating_color(r: str) -> str:
    if r in ("AAA","AA+","AA","AA-","A+","A","A-"):  return "#22c55e"
    if r in ("BBB+","BBB","BBB-"):                   return "#3b82f6"
    if r in ("BB+","BB","BB-","B+","B","B-"):         return "#f59e0b"
    return "#ef4444"

def sent_color(s: float) -> str:
    if s < -0.4: return "#ef4444"
    if s < 0.0:  return "#f59e0b"
    if s > 0.3:  return "#22c55e"
    return "#64748b"

def _navigate_to(page: str, cp_id: str | None = None):
    hist = st.session_state.get("nav_history", [])
    hist.append((st.session_state.get("page","portfolio"), st.session_state.get("selected_cp")))
    st.session_state.nav_history = hist[-15:]
    st.session_state.page = page
    st.session_state.selected_cp = cp_id
    st.rerun()

def _navigate_back():
    hist = st.session_state.get("nav_history", [])
    if hist:
        prev_page, prev_cp = hist.pop()
        st.session_state.nav_history = hist
        st.session_state.page = prev_page
        st.session_state.selected_cp = prev_cp
        st.rerun()

# ─── NETWORK GRAPHS ───────────────────────────────────────────────────────────

def _build_full_graph() -> nx.DiGraph:
    G = nx.DiGraph()
    for cp_id, ent in ENTITIES.items():
        sc = SCORES[cp_id]
        G.add_node(cp_id, label=ent["short"], node_type="CP",
                   sector=ent["sector"], rating=ent["rating"],
                   ead=ent["ead_m"], rag=sc["rag"], score=sc["composite"],
                   country=ent["country"])
    for cp_id, net in NETWORKS.items():
        for n in net["nodes"]:
            if n["id"] not in G:
                G.add_node(n["id"], label=n["name"], node_type=n["type"],
                           country=n.get("country",""), note=n.get("note",""),
                           ead=0, rag="", score=0, rating="")
        for (src, tgt, rel, w) in net["edges"]:
            G.add_edge(src, tgt, rel=rel, weight=w)
    return G

def _build_ego_graph(cp_id: str) -> nx.DiGraph:
    G = nx.DiGraph()
    ent = ENTITIES[cp_id]
    sc  = SCORES[cp_id]
    G.add_node(cp_id, label=ent["short"], node_type="CP",
               sector=ent["sector"], rating=ent["rating"],
               ead=ent["ead_m"], rag=sc["rag"], score=sc["composite"])
    net = NETWORKS.get(cp_id, {})
    for n in net.get("nodes", []):
        G.add_node(n["id"], label=n["name"], node_type=n["type"],
                   country=n.get("country",""), note=n.get("note",""))
    # Resolve CP-to-CP edges
    for (src, tgt, rel, w) in net.get("edges", []):
        for nid in [src, tgt]:
            if nid not in G:
                if nid in ENTITIES:
                    e2 = ENTITIES[nid]; s2 = SCORES[nid]
                    G.add_node(nid, label=e2["short"], node_type="CP",
                               rating=e2["rating"], ead=e2["ead_m"],
                               rag=s2["rag"], score=s2["composite"])
                else:
                    G.add_node(nid, label=nid, node_type="UNKNOWN",
                               country="", note="")
        G.add_edge(src, tgt, rel=rel, weight=w)
    # Add lateral edges: each entity → its country node (makes network more ball-like)
    for nid, nd in list(G.nodes(data=True)):
        country = nd.get("country", "")
        if country:
            cty_node = f"CTY_{country}"
            if cty_node in G and cty_node != nid and not G.has_edge(nid, cty_node):
                G.add_edge(nid, cty_node, rel="OPERATES", weight=0.3)
    # Cross-edges: if two nodes in this graph also share an edge in any other network, add it
    for other_cp, other_net in NETWORKS.items():
        if other_cp == cp_id:
            continue
        for (src, tgt, rel, w) in other_net.get("edges", []):
            if src in G and tgt in G and not G.has_edge(src, tgt):
                G.add_edge(src, tgt, rel=rel, weight=w * 0.5)
    return G

def _graph_to_fig(G: nx.DiGraph, height: int = 680) -> go.Figure:
    pos = nx.spring_layout(G, k=2.2, iterations=80, seed=42)
    edge_traces, grouped = [], {}
    for u, v, d in G.edges(data=True):
        rel = d.get("rel","OTHER")
        grouped.setdefault(rel, {"x":[],"y":[]})
        x0,y0=pos[u]; x1,y1=pos[v]
        grouped[rel]["x"] += [x0,x1,None]
        grouped[rel]["y"] += [y0,y1,None]
    for rel, coords in grouped.items():
        edge_traces.append(go.Scatter(x=coords["x"],y=coords["y"],mode="lines",
            line=dict(width=0.9,color=EDGE_COL.get(rel,"#475569")),
            hoverinfo="none",name=rel,showlegend=False))

    # Group nodes per RAG bucket so legend is clean (RED / AMBER / GREEN / UNKNOWN)
    rag_data: dict = {}
    for node, d in G.nodes(data=True):
        t   = d.get("node_type","OTHER")
        lbl = d.get("label", node)
        x, y = pos[node]

        if t == "CP":
            size = max(18, min(46, math.sqrt(d.get("ead",0)+1)*2.1))
            rag  = d.get("rag",""); col = RAG_COL.get(rag,"#3b82f6")
            score_disp = f"{d.get('score',0):.0f}"
            hov  = (f"<b>{lbl}</b><br>Type: Portfolio CP<br>"
                    f"Rating: {d.get('rating','')}<br>"
                    f"Score: {d.get('score',0):.0f}  RAG: {rag}<br>"
                    f"EAD: £{d.get('ead',0):.0f}M")
        elif t == "COUNTRY":
            cty = COUNTRY_SCORES.get(node, {})
            if cty:
                rag  = cty["rag"]; score = cty["score"]; flag = cty.get("flag","")
                col  = RAG_COL.get(rag,"#22c55e"); size = 15
                score_disp = f"{flag}{score}"
                hov  = (f"<b>{flag} {lbl}</b><br>Type: Country<br>"
                        f"Country Risk: {rag}  Score: {score}<br>"
                        f"{cty.get('note','')[:85]}")
            else:
                rag = "UNKNOWN"; col = "#475569"; size = 10; score_disp = ""
                hov = f"<b>{lbl}</b><br>Type: Country"
        else:
            note = (d.get("note","") or "")[:85]
            nrs  = NODE_RISK_SCORES.get(node, {})
            if nrs:
                rag  = nrs["rag"]; col = RAG_COL.get(rag,"#64748b"); size = 13
                score_disp = str(nrs["score"])
                hov  = (f"<b>{lbl}</b><br>Type: {t}<br>"
                        f"Risk: {rag}  Score: {nrs['score']}<br>"
                        f"{nrs.get('note','')[:85]}")
            else:
                rag = "UNKNOWN"; col = "#475569"; size = 10; score_disp = ""
                hov = f"<b>{lbl}</b><br>Type: {t} · {d.get('country','')}<br>{note}"

        bucket = rag if rag in RAG_COL else "UNKNOWN"
        rag_data.setdefault(bucket, dict(x=[],y=[],text=[],hover=[],size=[],color=[],ids=[]))
        rag_data[bucket]["x"].append(x);       rag_data[bucket]["y"].append(y)
        rag_data[bucket]["text"].append(score_disp)
        rag_data[bucket]["hover"].append(hov)
        rag_data[bucket]["size"].append(size);  rag_data[bucket]["color"].append(col)
        rag_data[bucket]["ids"].append(node)

    BUCKET_NAME = {"RED":"🔴 RED","AMBER":"🟡 AMBER","GREEN":"🟢 GREEN","UNKNOWN":"⚪ Unscored"}
    node_traces = []
    for bucket, g in rag_data.items():
        node_traces.append(go.Scatter(
            x=g["x"], y=g["y"], mode="markers+text",
            marker=dict(size=g["size"], color=g["color"],
                        line=dict(width=1.5, color="#0f172a"), opacity=0.92),
            text=g["text"], textposition="top center",
            textfont=dict(size=9, color=TEXT),
            hovertext=g["hover"], hoverinfo="text",
            customdata=g["ids"],
            name=BUCKET_NAME.get(bucket, bucket), showlegend=True))

    fig = go.Figure(data=edge_traces + node_traces)
    fig.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, height=height,
        margin=dict(l=5,r=5,t=5,b=5),
        legend=dict(bgcolor=CARD_BG, font=dict(color=TEXT,size=11),
                    bordercolor=BORDER, borderwidth=1),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        hovermode="closest")
    return fig

# ─── SIGNAL CARD ──────────────────────────────────────────────────────────────

def _signal_card(sig: dict, propagated: bool = False):
    import html as _html
    sent  = sig["sentiment"]
    sc    = sent_color(sent)
    sev_c = "#ef4444" if sig["severity"]=="HIGH" else ("#f59e0b" if sig["severity"]=="MEDIUM" else "#64748b")

    # Build variable HTML parts separately to avoid nested f-string issues
    via_html = ""
    if propagated:
        re_name = _html.escape(str(sig.get("related_entity","?")))
        via_html = (f'<span style="background:#1e3a5f;color:#60a5fa;font-size:11px;'
                    f'padding:1px 6px;border-radius:4px;margin-left:6px">via {re_name}</span>')

    stype = sig.get("signal_type","")
    type_badge = ""
    if stype:
        type_badge = (f'<span style="background:#1e3a2f;color:#22c55e;font-size:10px;'
                      f'padding:2px 7px;border-radius:4px">{_html.escape(stype)}</span>')

    headline = _html.escape(sig.get("headline",""))
    detail   = _html.escape(sig.get("detail",""))
    source   = _html.escape(sig.get("source",""))
    category = _html.escape(sig.get("category",""))
    observed = _html.escape(sig.get("observed_at",""))
    icon     = sentiment_icon(sent)

    st.markdown(
        f'<div style="background:{CARD_BG};border:1px solid {BORDER};border-left:3px solid {sc};'
        f'border-radius:8px;padding:12px 16px;margin-bottom:8px">'
        f'<div style="display:flex;align-items:flex-start;justify-content:space-between">'
        f'<div style="flex:1">'
        f'<div style="font-weight:600;color:{TEXT};font-size:14px">{icon} {headline} {via_html}</div>'
        f'<div style="color:{MUTED};font-size:12px;margin-top:4px;line-height:1.5">{detail}</div>'
        f'</div>'
        f'<div style="text-align:right;margin-left:16px;flex-shrink:0">'
        f'<div style="font-size:20px;font-weight:700;color:{sc}">{sent:+.2f}</div>'
        f'<div style="font-size:11px;color:{sev_c}">{sig["severity"]}</div>'
        f'<div style="font-size:11px;color:{MUTED}">{observed}</div>'
        f'</div></div>'
        f'<div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:6px;align-items:center">'
        f'<span style="background:#0f172a;color:{MUTED};font-size:11px;padding:2px 8px;border-radius:4px">{category}</span>'
        f'{type_badge}'
        f'<span style="color:{MUTED};font-size:11px">{source}</span>'
        f'</div></div>',
        unsafe_allow_html=True
    )

# ─── SIGNAL TICKER ────────────────────────────────────────────────────────────

def _signal_ticker(cp_id: str):
    sigs = signals_for_entity(cp_id)
    if not sigs: return
    items = "  ·  ".join([
        f'{sentiment_icon(s["sentiment"])} {s["headline"][:60]}{"…" if len(s["headline"])>60 else ""}'
        for s in sigs[:6]
    ])
    st.markdown(f"""
    <div style="background:{CARD_BG};border:1px solid {BORDER};border-radius:6px;
                padding:7px 12px;margin-bottom:10px;overflow:hidden">
      <marquee behavior="scroll" direction="left" scrollamount="2"
               style="color:{MUTED};font-size:12px;white-space:nowrap">{items}</marquee>
    </div>""", unsafe_allow_html=True)

# ─── EXPOSURE BAR ─────────────────────────────────────────────────────────────

def _exposure_breakdown(cp_id: str):
    exps = EXPOSURES.get(cp_id, [])
    if not exps: return
    TYPE_COL = {
        "Syndicated Loan": "#3b82f6", "Bond Holding": "#8b5cf6",
        "HY Bond Holding": "#ef4444", "Class A Bond": "#3b82f6",
        "Class B Bond": "#ef4444",    "Term Loan": "#f97316",
        "Trade Finance": "#14b8a6",   "FX Derivative": "#eab308",
        "Interest Rate Swap": "#eab308", "Aircraft Finance": "#22c55e",
        "Revolving Credit": "#3b82f6", "RCF": "#3b82f6",
        "Green Bond": "#22c55e",       "2nd Lien Note": "#ef4444",
        "Secured RE Loan": "#f97316",  "Unsecured Bond": "#94a3b8",
    }
    total = sum(e["notional_m"] for e in exps)
    parts = []
    for e in exps:
        pct = e["notional_m"] / total * 100
        col = TYPE_COL.get(e["type"], "#64748b")
        parts.append(f'<div style="flex:{pct};background:{col};height:10px;'
                      f'border-radius:2px;margin-right:2px" title="{e["type"]}: £{e["notional_m"]:.0f}M"></div>')
    bars = "".join(parts)
    labels = "  ".join([
        f'<span style="color:{TYPE_COL.get(e["type"],"#64748b")};font-size:11px">■ {e["type"]} £{e["notional_m"]:.0f}M</span>'
        for e in exps
    ])
    st.markdown(f"""
    <div style="margin-bottom:12px">
      <div style="color:{MUTED};font-size:11px;font-weight:600;margin-bottom:4px">EXPOSURE BREAKDOWN  Total £{total:.0f}M</div>
      <div style="display:flex;gap:2px;margin-bottom:6px">{bars}</div>
      <div style="display:flex;flex-wrap:wrap;gap:8px">{labels}</div>
    </div>""", unsafe_allow_html=True)
    # Optional detail rows
    with st.expander("Instrument detail", expanded=False):
        for e in exps:
            col = TYPE_COL.get(e["type"], "#64748b")
            st.markdown(
                f'<div style="padding:5px 0;border-bottom:1px solid {BORDER}">'
                f'<span style="color:{col};font-weight:600">{e["type"]}</span>'
                f' <span style="color:{TEXT};font-weight:700">£{e["notional_m"]:.0f}M</span>'
                f' <span style="color:{MUTED};font-size:12px"> — {e["detail"]}</span></div>',
                unsafe_allow_html=True)

# ─── SCORE DRILLDOWN ─────────────────────────────────────────────────────────

def _score_drilldown(cp_id: str, sc: dict):
    rag_c = RAG_COL.get(sc["rag"], MUTED)
    with st.expander(f"📊  Score {sc['composite']:.0f} — click to drill down", expanded=False):
        st.markdown(f"""
        <div style="display:flex;gap:16px;margin-bottom:12px">
          <div style="flex:1;background:{BG};border:1px solid {BORDER};border-radius:8px;padding:12px;text-align:center">
            <div style="font-size:24px;font-weight:800;color:{rag_c}">{sc['own_score']:.0f}</div>
            <div style="color:{MUTED};font-size:12px">Own Score (70% weight)</div>
            <div style="color:{MUTED};font-size:11px">from direct signals on this entity</div>
          </div>
          <div style="flex:1;background:{BG};border:1px solid {BORDER};border-radius:8px;padding:12px;text-align:center">
            <div style="font-size:24px;font-weight:800;color:#60a5fa">{sc['prop_score']:.0f}</div>
            <div style="color:{MUTED};font-size:12px">Propagated Score (30% weight)</div>
            <div style="color:{MUTED};font-size:11px">from signals on network entities (0.6× weight)</div>
          </div>
          <div style="flex:1;background:{BG};border:1px solid {BORDER};border-radius:8px;padding:12px;text-align:center">
            <div style="font-size:24px;font-weight:800;color:{rag_c}">{sc['sentiment']:+.2f}</div>
            <div style="color:{MUTED};font-size:12px">Avg Sentiment</div>
            <div style="color:{MUTED};font-size:11px">-1.0 (very negative) → +1.0</div>
          </div>
        </div>""", unsafe_allow_html=True)
        direct_sigs  = [s for s in SIGNALS if s.get("direct") and s.get("entity_id") == cp_id]
        related_sigs = [s for s in SIGNALS if not s.get("direct") and cp_id in (s.get("affects") or [])]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Direct signal drivers** ({len(direct_sigs)} signals)")
            for sig in sorted(direct_sigs, key=lambda x: -x["score"]):
                sc2 = sent_color(sig["sentiment"])
                hl = sig["headline"][:55] + ("…" if len(sig["headline"])>55 else "")
                st.markdown(
                    f'<div style="padding:3px 0;border-bottom:1px solid {BORDER}">'
                    f'<span style="color:{sc2};font-size:13px">●</span> '
                    f'<span style="font-size:12px;color:{TEXT}">{hl}</span> '
                    f'<span style="color:{MUTED};font-size:11px;float:right">{sig["score"]}</span></div>',
                    unsafe_allow_html=True)
        with c2:
            st.markdown(f"**Propagated signal drivers** ({len(related_sigs)} signals)")
            for sig in sorted(related_sigs, key=lambda x: -x["score"]):
                sc2 = sent_color(sig["sentiment"])
                re  = sig.get("related_entity","?")
                hl  = sig["headline"][:45] + ("…" if len(sig["headline"])>45 else "")
                st.markdown(
                    f'<div style="padding:3px 0;border-bottom:1px solid {BORDER}">'
                    f'<span style="color:{sc2};font-size:13px">●</span> '
                    f'<span style="color:#60a5fa;font-size:11px">via {re}</span> '
                    f'<span style="font-size:12px;color:{TEXT}">{hl}</span> '
                    f'<span style="color:{MUTED};font-size:11px;float:right">{sig["score"]:.0f}×0.6</span></div>',
                    unsafe_allow_html=True)

# ─── PAGE: SIGNAL SOURCES ────────────────────────────────────────────────────

def page_sources():
    st.markdown("## 📡 Signal Sources")
    st.caption("Risk OS ingests signals across five cadence tiers and four data modalities. "
               "Live sources are active in this prototype; Planned sources will be integrated in production.")

    # ── Summary metrics ──────────────────────────────────────────────────────
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Total Sources",  "32")
    m2.metric("Live (demo)",    "8")
    m3.metric("Signal Types",   "7")
    m4.metric("Min Latency",    "<1 min")
    m5.metric("Signals / CP",   "4–9")
    st.divider()

    SOURCES = [
        # ── REAL-TIME / INTRADAY ───────────────────────────────────────────────
        {
            "tier": "⚡ Real-time  (<1 min)",
            "tier_col": "#ef4444",
            "items": [
                {
                    "name": "Yahoo Finance",
                    "icon": "📈",
                    "type": "Equity · Options · Volume",
                    "cadence": "Real-time",
                    "coverage": "All listed CPs + key network entities",
                    "metrics": "Price, % change, 52w high/low, volume vs ADV, short interest, put-call ratio",
                    "status": "PLANNED",
                    "note": "yfinance Python library; free tier; upgrade to Bloomberg API for production",
                },
                {
                    "name": "Markit / ICE CDS",
                    "icon": "📊",
                    "type": "Credit Default Swaps",
                    "cadence": "EOD + intraday",
                    "coverage": "All IG/HY rated CPs; sovereign CDS for countries",
                    "metrics": "5yr CDS spread (bps), 1yr CDS, CDS/Bond basis, implied default probability",
                    "status": "PLANNED",
                    "note": "Single-name CDS most liquid for IG entities; proxy spreads for private firms",
                },
                {
                    "name": "Bloomberg Bond Monitor",
                    "icon": "🔵",
                    "type": "Bond prices · Yield spreads",
                    "cadence": "Real-time",
                    "coverage": "All bond-holding CPs (CP001/003/005/007/009/013/023/028/033)",
                    "metrics": "Clean price (p/£), yield-to-maturity, OAS spread, Z-spread, distress flag",
                    "status": "PLANNED",
                    "note": "TRACE/Bloomberg composite pricing; alert on >5% single-day move",
                },
                {
                    "name": "Twitter / X API v2",
                    "icon": "🐦",
                    "type": "Social media sentiment",
                    "cadence": "Real-time streaming",
                    "coverage": "Entity mentions, hashtags, executive names",
                    "metrics": "Mention volume, positive/negative ratio, viral spike alert, influencer reach",
                    "status": "PLANNED",
                    "note": "Filtered search stream; NLP classification (FinBERT); volume z-score alerting",
                },
            ],
        },
        # ── DAILY ─────────────────────────────────────────────────────────────
        {
            "tier": "🔄 Daily",
            "tier_col": "#f59e0b",
            "items": [
                {
                    "name": "RavenPack News Analytics",
                    "icon": "📰",
                    "type": "News NLP · Entity Sentiment",
                    "cadence": "Daily (intraday available)",
                    "coverage": "Global news; 900K+ sources; all portfolio entities",
                    "metrics": "Entity Sentiment Score (ESS −1→+1), Event novelty score, Relevance score, Topic breakdown",
                    "status": "PLANNED",
                    "note": "Gold standard for quantitative news sentiment; used by 900+ hedge funds",
                },
                {
                    "name": "Refinitiv News Sentiment",
                    "icon": "📡",
                    "type": "News NLP · Volume",
                    "cadence": "Daily",
                    "coverage": "Reuters + 60K news sources; sector and entity level",
                    "metrics": "News Sentiment Index (NSI), article count vs baseline, topic clustering",
                    "status": "PLANNED",
                    "note": "Alternative to RavenPack; Thomson Reuters Eikon integration available",
                },
                {
                    "name": "Reuters / FT / WSJ Scraper",
                    "icon": "🗞️",
                    "type": "Qualitative news",
                    "cadence": "Hourly",
                    "coverage": "Curated financial press; all portfolio CPs",
                    "metrics": "Headline, article body, named entity extraction, manual severity tagging",
                    "status": "LIVE (demo)",
                    "note": "Current demo signals use structured versions of real Reuters/FT headlines",
                },
                {
                    "name": "FlightAware / ADS-B Exchange",
                    "icon": "✈️",
                    "type": "Alt data — fleet tracking",
                    "cadence": "Daily",
                    "coverage": "Wizz Air (CP013), airline network entities",
                    "metrics": "Active aircraft count, utilisation %, grounded fleet, hub-level breakdown",
                    "status": "PLANNED",
                    "note": "Free ADS-B feeds supplemented by FlightAware commercial API",
                },
                {
                    "name": "LinkedIn Talent Flow",
                    "icon": "💼",
                    "type": "Employee signals",
                    "cadence": "Weekly (daily lag)",
                    "coverage": "All CPs with >500 employees",
                    "metrics": "Job posting volume, senior departure rate, CEO approval (Glassdoor), hiring freeze signal",
                    "status": "PLANNED",
                    "note": "LinkedIn data partnership or scraping; Glassdoor API for rating time series",
                },
            ],
        },
        # ── WEEKLY ────────────────────────────────────────────────────────────
        {
            "tier": "📆 Weekly",
            "tier_col": "#3b82f6",
            "items": [
                {
                    "name": "Glassdoor / Indeed",
                    "icon": "⭐",
                    "type": "Employee review sentiment",
                    "cadence": "Weekly",
                    "coverage": "All portfolio CPs + key suppliers",
                    "metrics": "Overall rating, CEO approval %, culture score, layoff mentions, review volume",
                    "status": "PLANNED",
                    "note": "Leading indicator of operational stress; correlated with restructuring events",
                },
                {
                    "name": "Google Trends",
                    "icon": "🔍",
                    "type": "Search volume signals",
                    "cadence": "Daily (weekly aggregated)",
                    "coverage": "Entity names, product names, crisis keywords",
                    "metrics": "Search volume index (0–100), geographic breakdown, related query surge",
                    "status": "PLANNED",
                    "note": "Free pytrends API; useful for consumer-facing entities (Thames, Wizz, AML)",
                },
                {
                    "name": "S&P / Moody's / Fitch Alerts",
                    "icon": "🏷️",
                    "type": "Rating actions",
                    "cadence": "As published",
                    "coverage": "All rated CPs + country ratings",
                    "metrics": "Outlook change, watch placement, notch upgrade/downgrade, trigger covenants",
                    "status": "LIVE (demo)",
                    "note": "Demo uses actual rating actions from 2024-25; production via rating agency feeds",
                },
                {
                    "name": "Orbital Insight (Satellite)",
                    "icon": "🛰️",
                    "type": "Alt data — satellite imagery",
                    "cadence": "Weekly",
                    "coverage": "Manufacturing CPs: VW, ZF, Continental, Northvolt, Atos data centres",
                    "metrics": "Factory parking occupancy, vehicle inventory lots, logistics activity",
                    "status": "PLANNED",
                    "note": "15–50cm resolution; weekly revisit rate for most European industrial sites",
                },
            ],
        },
        # ── MONTHLY / QUARTERLY ───────────────────────────────────────────────
        {
            "tier": "📊 Monthly / Quarterly",
            "tier_col": "#22c55e",
            "items": [
                {
                    "name": "EDGAR / Companies House",
                    "icon": "📄",
                    "type": "Regulatory filings",
                    "cadence": "Quarterly",
                    "coverage": "All CPs with public filings; UK/US/EU entities",
                    "metrics": "Revenue, EBITDA, net debt, FCF, covenant headroom, going concern flag, auditor opinion",
                    "status": "LIVE (demo)",
                    "note": "Structured extraction via sec-edgar-downloader + NLP for UK filings",
                },
                {
                    "name": "Eurostat / ONS / Destatis",
                    "icon": "🏛️",
                    "type": "Macro — economic indicators",
                    "cadence": "Monthly",
                    "coverage": "DE, UK, FR, CN, US, HU — all country nodes in networks",
                    "metrics": "PMI (manufacturing + services), GDP growth, industrial production, unemployment",
                    "status": "PLANNED",
                    "note": "Eurostat API (free); used for country node risk scoring and macro propagation",
                },
                {
                    "name": "IMF / World Bank / OECD",
                    "icon": "🌐",
                    "type": "Sovereign risk",
                    "cadence": "Quarterly / Annual",
                    "coverage": "All country nodes in all 10 CP networks",
                    "metrics": "Debt/GDP, current account, FX reserves, political stability index, ease of doing business",
                    "status": "PLANNED",
                    "note": "Country risk scores on landing page sourced from this; updated quarterly",
                },
                {
                    "name": "Environment Agency / Ofwat",
                    "icon": "💧",
                    "type": "Regulatory compliance data",
                    "cadence": "Monthly",
                    "coverage": "Thames Water (CP023); UK water sector",
                    "metrics": "CSO spill hours, enforcement notices, fine amounts, licence condition breaches",
                    "status": "LIVE (demo)",
                    "note": "EA Open Data Portal; real spill sensor data used in demo signals",
                },
            ],
        },
        # ── INTERNAL BANK DATA ────────────────────────────────────────────────
        {
            "tier": "🏦 Internal Bank Data",
            "tier_col": "#8b5cf6",
            "items": [
                {
                    "name": "Loan Management System",
                    "icon": "📋",
                    "type": "Credit facility data",
                    "cadence": "Real-time / daily",
                    "coverage": "All portfolio CPs with loan exposure",
                    "metrics": "Utilisation %, covenant test results, margin step-up triggers, maturity alerts",
                    "status": "PLANNED",
                    "note": "Integration via API to core banking system (Temenos / FIS / Finastra)",
                },
                {
                    "name": "Trading / Derivatives MTM",
                    "icon": "⚖️",
                    "type": "Derivative exposure + collateral",
                    "cadence": "Daily EOD / intraday",
                    "coverage": "All CPs with FX, IRS, or other derivative exposure",
                    "metrics": "MTM value, net exposure, collateral held/posted, close-out amount",
                    "status": "PLANNED",
                    "note": "Front-office risk system (Murex / Calypso); netting set level aggregation",
                },
                {
                    "name": "Payment Behaviour",
                    "icon": "💳",
                    "type": "Transaction signals",
                    "cadence": "Daily",
                    "coverage": "CPs with current account / trade finance relationships",
                    "metrics": "Days payable trend, large payment anomalies, FX purchase patterns, sweep behaviour",
                    "status": "PLANNED",
                    "note": "Strong early warning signal; payment slowdown precedes public distress by 3–6M",
                },
                {
                    "name": "Relationship Manager Notes",
                    "icon": "🗣️",
                    "type": "Qualitative intelligence",
                    "cadence": "As filed",
                    "coverage": "All portfolio CPs",
                    "metrics": "Management tone, strategic updates, covenant waiver discussions, site visit notes",
                    "status": "PLANNED",
                    "note": "NLP extraction from CRM (Salesforce / Dealogic); sentiment trend over calls",
                },
            ],
        },
    ]

    for tier_data in SOURCES:
        tc = tier_data["tier_col"]
        st.markdown(f"""
        <div style="border-left:3px solid {tc};padding-left:12px;margin:20px 0 10px">
          <span style="font-size:15px;font-weight:800;color:{tc}">{tier_data['tier']}</span>
        </div>""", unsafe_allow_html=True)

        n = len(tier_data["items"])
        cols = st.columns(min(n, 4), gap="small")
        for col, src in zip(cols, tier_data["items"]):
            status_c = "#22c55e" if "LIVE" in src["status"] else "#64748b"
            status_bg= "#22c55e18" if "LIVE" in src["status"] else "#1e293b"
            col.markdown(f"""
            <div style="background:{CARD_BG};border:1px solid {BORDER};border-radius:10px;
                        padding:14px;height:100%">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
                <span style="font-size:22px">{src['icon']}</span>
                <div>
                  <div style="font-weight:700;color:{TEXT};font-size:13px">{src['name']}</div>
                  <div style="font-size:10px;font-weight:700;color:{status_c};
                              background:{status_bg};padding:1px 7px;border-radius:8px;
                              display:inline-block">{src['status']}</div>
                </div>
              </div>
              <div style="color:{tc};font-size:11px;font-weight:600;margin-bottom:4px">{src['type']}</div>
              <div style="color:{MUTED};font-size:11px;margin-bottom:2px">🕐 {src['cadence']}</div>
              <div style="color:{MUTED};font-size:11px;margin-bottom:6px">🌍 {src['coverage']}</div>
              <div style="color:{TEXT};font-size:11px;margin-bottom:6px;line-height:1.5">
                <span style="color:{MUTED}">Metrics: </span>{src['metrics']}
              </div>
              <div style="color:{MUTED};font-size:10px;font-style:italic;
                          border-top:1px solid {BORDER};padding-top:6px;margin-top:4px">
                {src['note']}
              </div>
            </div>""", unsafe_allow_html=True)

    st.divider()
    # Signal type breakdown
    st.markdown("#### Signal type mix in current demo")
    from collections import Counter
    from entities import SIGNALS
    type_counts = Counter(s.get("signal_type","NARRATIVE") for s in SIGNALS)
    type_labels = {
        "NARRATIVE":     ("📝 Narrative / Filing", "#64748b"),
        "CDS":           ("📊 CDS Spread",         "#ef4444"),
        "EQUITY":        ("📈 Equity Price",        "#3b82f6"),
        "BOND":          ("🔵 Bond Price",          "#8b5cf6"),
        "NEWS_NLP":      ("📰 News NLP",            "#f59e0b"),
        "SOCIAL_MEDIA":  ("🐦 Social Media",        "#ec4899"),
        "MACRO":         ("🏛️ Macro Data",          "#22c55e"),
        "ALT_DATA":      ("🛰️ Alt Data",            "#14b8a6"),
    }
    total_sigs = sum(type_counts.values())
    bar_parts = []
    legend_parts = []
    for stype, cnt in sorted(type_counts.items(), key=lambda x:-x[1]):
        label, color = type_labels.get(stype, (stype, MUTED))
        pct = cnt / total_sigs * 100
        bar_parts.append(f'<div style="flex:{pct};background:{color};height:12px;border-radius:3px;margin-right:2px" title="{label}: {cnt}"></div>')
        legend_parts.append(f'<span style="color:{color};font-size:11px">■ {label} {cnt}</span>')
    st.markdown(f"""
    <div style="margin-bottom:10px">
      <div style="display:flex;gap:2px;margin-bottom:8px">{"".join(bar_parts)}</div>
      <div style="display:flex;flex-wrap:wrap;gap:12px">{"".join(legend_parts)}</div>
    </div>""", unsafe_allow_html=True)


# ─── PAGE: HOME (landing) ─────────────────────────────────────────────────────

def page_home():
    total_ead = sum(e["ead_m"] for e in ENTITIES.values())
    total_ecl = sum(SCORES[cp]["ecl_m"] for cp in ENTITIES)
    n_red    = sum(1 for cp in ENTITIES if SCORES[cp]["rag"]=="RED")
    n_amber  = sum(1 for cp in ENTITIES if SCORES[cp]["rag"]=="AMBER")
    n_green  = sum(1 for cp in ENTITIES if SCORES[cp]["rag"]=="GREEN")
    all_sigs = len(SIGNALS)

    # ── Header ──────────────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="font-size:26px;font-weight:900;color:{TEXT};margin-bottom:4px">'
        f'📊 Executive Early Warning Dashboard</div>'
        f'<div style="color:{MUTED};font-size:12px;margin-bottom:20px">'
        f'Risk OS · {len(ENTITIES)} entities monitored · {all_sigs} live signals</div>',
        unsafe_allow_html=True)

    # ── Top stat boxes ───────────────────────────────────────────────────────────
    for col, val, label, col_c in zip(
        st.columns(5),
        [n_red, n_amber, n_green, f"£{total_ead/1000:.1f}bn", f"£{total_ecl:.0f}M"],
        ["CRITICAL", "HIGH", "NORMAL", "TOTAL EAD", "ECL UPLIFT"],
        ["#ef4444", "#f59e0b", "#22c55e", TEXT, "#f59e0b"],
    ):
        col.markdown(
            f'<div style="background:{CARD_BG};border:1px solid {BORDER};border-radius:10px;'
            f'padding:18px 12px;text-align:center;margin-bottom:16px">'
            f'<div style="font-size:34px;font-weight:900;color:{col_c};line-height:1">{val}</div>'
            f'<div style="font-size:10px;letter-spacing:2px;color:{MUTED};margin-top:6px">{label}</div>'
            f'</div>', unsafe_allow_html=True)

    # ── Main content: table left, charts right ────────────────────────────────
    tbl_col, chart_col = st.columns([3, 2], gap="large")

    with tbl_col:
        st.markdown(
            f'<div style="font-size:16px;font-weight:700;color:{TEXT};margin-bottom:10px">'
            f'🚨 Top Risk Entities</div>', unsafe_allow_html=True)
        top_ids = sorted(ENTITIES.keys(), key=lambda x: -SCORES[x]["composite"])[:18]
        rag_label = {"RED": "CRITICAL", "AMBER": "HIGH", "GREEN": "NORMAL"}
        rows_html = ""
        for eid in top_ids:
            ent = ENTITIES[eid]; sc = SCORES[eid]
            rc  = RAG_COL.get(sc["rag"], MUTED)
            rows_html += (
                f'<tr style="border-bottom:1px solid {BORDER}">'
                f'<td style="padding:7px 6px;color:{TEXT};font-weight:600;white-space:nowrap">'
                f'{ent["flag"]} {ent["short"]}</td>'
                f'<td style="padding:7px 6px;color:{MUTED};font-size:11px">{ent["sector"]}</td>'
                f'<td style="padding:7px 6px;text-align:right;color:{rc};font-weight:700">'
                f'{sc["composite"]:.0f}</td>'
                f'<td style="padding:7px 6px;text-align:center">'
                f'<span style="background:{rc}22;color:{rc};padding:2px 7px;border-radius:4px;'
                f'font-size:10px;font-weight:700">{rag_label.get(sc["rag"],"—")}</span></td>'
                f'<td style="padding:7px 6px;text-align:right;color:{TEXT}">{ent["ead_m"]:.0f}</td>'
                f'<td style="padding:7px 6px;text-align:right;color:{rc}">{sc["ecl_m"]:.1f}</td>'
                f'</tr>'
            )
        st.markdown(
            f'<table style="width:100%;border-collapse:collapse;font-size:12px">'
            f'<thead><tr style="border-bottom:2px solid {BORDER}">'
            f'<th style="text-align:left;padding:6px;color:{MUTED}">Entity</th>'
            f'<th style="text-align:left;padding:6px;color:{MUTED}">Sector</th>'
            f'<th style="text-align:right;padding:6px;color:{MUTED}">Score</th>'
            f'<th style="text-align:center;padding:6px;color:{MUTED}">RAG</th>'
            f'<th style="text-align:right;padding:6px;color:{MUTED}">EAD £M</th>'
            f'<th style="text-align:right;padding:6px;color:{MUTED}">ECL £M</th>'
            f'</tr></thead><tbody>{rows_html}</tbody></table>',
            unsafe_allow_html=True)

    with chart_col:
        # Score distribution histogram
        st.markdown(
            f'<div style="font-size:14px;font-weight:700;color:{TEXT};margin-bottom:6px">'
            f'Score Distribution</div>', unsafe_allow_html=True)
        scores_list = [SCORES[cp]["composite"] for cp in ENTITIES]
        fig_h = go.Figure(go.Histogram(
            x=scores_list, nbinsx=10,
            marker_color="#3b82f6", marker_line_color=BG, marker_line_width=1))
        fig_h.add_vline(x=70, line_color="#ef4444", line_dash="dash", line_width=1)
        fig_h.add_vline(x=30, line_color="#f59e0b", line_dash="dash", line_width=1)
        fig_h.update_layout(
            height=200, margin=dict(l=0, r=0, t=4, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Composite Risk Score", color=MUTED, gridcolor=BORDER, tickfont=dict(size=10)),
            yaxis=dict(title="# Entities", color=MUTED, gridcolor=BORDER, tickfont=dict(size=10)),
            font=dict(color=MUTED, size=10), showlegend=False)
        st.plotly_chart(fig_h, use_container_width=True)

        # Sector risk concentration
        st.markdown(
            f'<div style="font-size:14px;font-weight:700;color:{TEXT};margin-bottom:6px">'
            f'Sector Risk Concentration</div>', unsafe_allow_html=True)
        sec_data: dict = {}
        for cp in ENTITIES:
            s   = ENTITIES[cp]["sector"]
            rag = SCORES[cp]["rag"]
            sec_data.setdefault(s, {"RED": 0, "AMBER": 0, "GREEN": 0})
            sec_data[s][rag] += 1
        secs = sorted(sec_data)
        fig_s = go.Figure()
        for rag, rc in [("GREEN", "#22c55e"), ("AMBER", "#f59e0b"), ("RED", "#ef4444")]:
            fig_s.add_trace(go.Bar(
                name=rag, x=secs,
                y=[sec_data[s].get(rag, 0) for s in secs],
                marker_color=rc))
        fig_s.update_layout(
            barmode="stack", height=240, margin=dict(l=0, r=0, t=4, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color=MUTED, gridcolor=BORDER, tickangle=-35, tickfont=dict(size=9)),
            yaxis=dict(color=MUTED, gridcolor=BORDER, tickfont=dict(size=10)),
            font=dict(color=MUTED, size=10),
            legend=dict(orientation="h", y=1.1, font=dict(size=10)))
        st.plotly_chart(fig_s, use_container_width=True)

    st.divider()

    # ── Module tiles ─────────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="font-size:14px;font-weight:700;color:{TEXT};margin-bottom:12px">'
        f'Modules</div>', unsafe_allow_html=True)
    mc1, mc2, mc3, mc4 = st.columns(4, gap="small")
    for col, icon, title, desc, active in [
        (mc1, "🏦", "Counterparty", f"{len(ENTITIES)} entities · LIVE", True),
        (mc2, "🌍", "Country",      "Sovereign risk · Coming soon",      False),
        (mc3, "🏭", "Supplier",     "Supply chain · Coming soon",        False),
        (mc4, "👤", "Others",       "Key-person risk · Coming soon",     False),
    ]:
        border = "#3b82f6" if active else BORDER
        opacity = "1" if active else "0.45"
        col.markdown(
            f'<div style="background:{CARD_BG};border:1px solid {border};border-radius:10px;'
            f'padding:18px;text-align:center;opacity:{opacity};margin-bottom:8px">'
            f'<div style="font-size:28px">{icon}</div>'
            f'<div style="font-weight:700;color:{TEXT};margin-top:6px;font-size:14px">{title}</div>'
            f'<div style="color:{MUTED};font-size:11px;margin-top:4px">{desc}</div>'
            f'</div>', unsafe_allow_html=True)
        if active:
            if col.button("Open →", key=f"mod_{title}", use_container_width=True, type="primary"):
                _navigate_to("portfolio")

    # ── Signal sources strip ─────────────────────────────────────────────────────
    st.divider()
    hdr_c, hdr_b = st.columns([4, 1])
    hdr_c.markdown(
        f'<div style="color:{MUTED};font-size:11px;font-weight:700;letter-spacing:1px;padding-top:8px">'
        f'SIGNAL SOURCES  —  32 sources across 5 cadence tiers</div>', unsafe_allow_html=True)
    with hdr_b:
        if st.button("View all sources →", key="home_sources_btn", use_container_width=True):
            _navigate_to("sources")

    st.markdown(f"""
    <div style="text-align:center;padding:40px 0 28px">
      <div style="font-size:36px;font-weight:900;letter-spacing:-1px;color:{TEXT}">
        Risk <span style="color:#3b82f6">OS</span>
      </div>
      <div style="color:{MUTED};font-size:15px;margin-top:6px">
        AI-powered counterparty risk intelligence — monitor, score, and stress-test
        any entity and its full network in real time
      </div>
    </div>""", unsafe_allow_html=True)

    MODULES = [
        {
            "icon": "🏦", "title": "Counterparty",
            "desc": "Full network intelligence on borrowers and trading counterparties. "
                    "Signals 1–2 hops away, scored and stress-tested.",
            "status": "LIVE",
            "stats": [
                ("Counterparties", "10"),
                ("Total EAD", f"£{total_ead:.0f}M"),
                ("Total ECL", f"£{total_ecl:.1f}M"),
                ("🔴 RED", str(n_red)),
                ("🟡 AMBER", str(n_amber)),
            ],
            "action": "portfolio",
            "btn": "Open Portfolio →",
            "color": "#3b82f6",
        },
        {
            "icon": "🌍", "title": "Country",
            "desc": "Sovereign risk monitors: macro signals, political stability, "
                    "regulatory environment, and cross-border contagion paths.",
            "status": "COMING SOON",
            "stats": [],
            "action": None,
            "btn": "Coming Soon",
            "color": "#22c55e",
        },
        {
            "icon": "🏭", "title": "Supplier",
            "desc": "Supply chain risk: Tier-1 and Tier-2 supplier networks, "
                    "single-source dependencies, and operational disruption scoring.",
            "status": "COMING SOON",
            "stats": [],
            "action": None,
            "btn": "Coming Soon",
            "color": "#f97316",
        },
        {
            "icon": "👤", "title": "Others",
            "desc": "Key-person risk: politicians, central bankers, tech leaders, "
                    "and other individuals who can have a material impact on firm value.",
            "status": "COMING SOON",
            "stats": [],
            "action": None,
            "btn": "Coming Soon",
            "color": "#8b5cf6",
        },
    ]

    cols = st.columns(2, gap="large")
    for i, m in enumerate(MODULES):
        with cols[i % 2]:
            live = m["status"] == "LIVE"
            status_col = "#22c55e" if live else MUTED
            status_bg  = "#22c55e18" if live else "#1e293b"
            border_col = m["color"] if live else BORDER
            st.markdown(f"""
            <div style="background:{CARD_BG};border:1px solid {border_col};border-radius:12px;
                        padding:24px;margin-bottom:20px;min-height:220px">
              <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px">
                <div style="display:flex;align-items:center;gap:12px">
                  <span style="font-size:32px">{m['icon']}</span>
                  <div>
                    <div style="font-size:20px;font-weight:800;color:{TEXT}">{m['title']}</div>
                    <div style="font-size:11px;font-weight:700;color:{status_col};
                                background:{status_bg};padding:2px 8px;border-radius:10px;
                                display:inline-block;margin-top:4px">{m['status']}</div>
                  </div>
                </div>
              </div>
              <div style="color:{MUTED};font-size:13px;line-height:1.6;margin-bottom:16px">
                {m['desc']}
              </div>
              {"".join([
                f'<span style="background:{BG};border:1px solid {BORDER};border-radius:6px;'
                f'padding:4px 10px;margin-right:8px;font-size:12px">'
                f'<span style="color:{MUTED}">{s[0]}</span> '
                f'<span style="color:{TEXT};font-weight:700">{s[1]}</span></span>'
                for s in m["stats"]
              ])}
            </div>""", unsafe_allow_html=True)
            if live:
                if st.button(m["btn"], key=f"mod_{m['title']}", use_container_width=True,
                             type="primary"):
                    _navigate_to(m["action"])
            else:
                st.button(m["btn"], key=f"mod_{m['title']}", use_container_width=True,
                          disabled=True)

    # Data source overview
    st.divider()
    hdr_c, hdr_b = st.columns([3,1])
    hdr_c.markdown(f'<div style="color:{MUTED};font-size:11px;font-weight:700;letter-spacing:1px;padding-top:8px">SIGNAL SOURCES  —  32 sources across 5 cadence tiers</div>', unsafe_allow_html=True)
    with hdr_b:
        if st.button("View all sources →", key="home_sources_btn", use_container_width=True):
            _navigate_to("sources")
    SOURCE_ROWS = [
        ("⚡ Real-time",  "#ef4444",
         "Yahoo Finance equity · CDS spreads (Markit) · Bond MTM (Bloomberg) · Twitter/X sentiment stream"),
        ("🔄 Daily",           "#f59e0b",
         "RavenPack news NLP · FlightAware fleet data · LinkedIn talent flow · Rating agency alerts"),
        ("📊 Monthly / Quarterly","#3b82f6",
         "Financial statements (EDGAR) · Satellite imagery · Eurostat/ONS macro · Glassdoor sentiment"),
        ("🏦 Internal bank data",      "#8b5cf6",
         "Loan covenants · Derivative MTM · Payment behaviour · RM relationship notes"),
    ]
    cols2 = st.columns(4)
    for col, (label, color, items) in zip(cols2, SOURCE_ROWS):
        col.markdown(f"""
        <div style="background:{CARD_BG};border:1px solid {BORDER};border-radius:8px;padding:14px">
          <div style="font-size:12px;font-weight:700;color:{color};margin-bottom:8px">{label}</div>
          <div style="color:{MUTED};font-size:11px;line-height:1.7">{items.replace(" · ", "<br>· ")}</div>
        </div>""", unsafe_allow_html=True)


# ─── PAGE: PORTFOLIO ──────────────────────────────────────────────────────────

def page_portfolio():
    # ── Summary stats ──────────────────────────────────────────────────────────
    total_ead = sum(e["ead_m"] for e in ENTITIES.values())
    total_ecl = sum(SCORES[cp]["ecl_m"] for cp in ENTITIES)
    n_red     = sum(1 for cp in ENTITIES if SCORES[cp]["rag"] == "RED")
    n_amber   = sum(1 for cp in ENTITIES if SCORES[cp]["rag"] == "AMBER")
    n_green   = sum(1 for cp in ENTITIES if SCORES[cp]["rag"] == "GREEN")

    st.markdown("## 📊 Counterparty Portfolio")
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    m1.metric("Counterparties", len(ENTITIES))
    m2.metric("Total EAD",  f"£{total_ead:.0f}M")
    m3.metric("Total ECL",  f"£{total_ecl:.1f}M")
    m4.metric("🔴 RED",    n_red)
    m5.metric("🟡 AMBER",  n_amber)
    m6.metric("🟢 GREEN",  n_green)

    st.divider()

    # ── Filters ────────────────────────────────────────────────────────────────
    all_sectors  = sorted(set(e["sector"]  for e in ENTITIES.values()))
    # Build country options with flags, deduplicated
    seen_c: dict = {}
    for e in ENTITIES.values():
        seen_c[e["country"]] = e.get("flag", "")
    country_opts = [f'{seen_c[c]} {c}' for c in sorted(seen_c)]

    fc1, fc2, fc3, fc4 = st.columns([2, 2, 1.5, 1.5])
    with fc1:
        sel_sectors = st.multiselect("🏭 Sector", all_sectors,
                                     default=st.session_state.get("pf_sectors", []),
                                     key="pf_sectors", placeholder="All sectors")
    with fc2:
        sel_countries_disp = st.multiselect("🌍 HQ Country", country_opts,
                                             default=st.session_state.get("pf_countries", []),
                                             key="pf_countries", placeholder="All countries")
        sel_countries = [c.split()[-1] for c in sel_countries_disp]
    with fc3:
        sel_rag = st.selectbox("🚦 Risk", ["All","🔴 RED","🟡 AMBER","🟢 GREEN"],
                               key="pf_rag")
    with fc4:
        sort_by = st.selectbox("Sort", ["Risk Score ↓","EAD ↓","Rating","Name"],
                               key="pf_sort")

    # ── Apply filters ──────────────────────────────────────────────────────────
    def _passes(eid):
        e  = ENTITIES[eid]; s = SCORES[eid]
        if sel_sectors  and e["sector"]  not in sel_sectors:  return False
        if sel_countries and e["country"] not in sel_countries: return False
        if sel_rag != "All" and s["rag"] not in sel_rag:        return False
        return True

    RATING_ORDER = {"AAA":0,"AA+":1,"AA":2,"AA-":3,"A+":4,"A":5,"A-":6,
                    "BBB+":7,"BBB":8,"BBB-":9,"BB+":10,"BB":11,"BB-":12,
                    "B+":13,"B":14,"B-":15,"CCC":16,"CC":17,"C":18,"D":19}

    def _sort_key(eid):
        e = ENTITIES[eid]; s = SCORES[eid]
        if sort_by == "Risk Score ↓": return -s["composite"]
        if sort_by == "EAD ↓":        return -e["ead_m"]
        if sort_by == "Rating":        return RATING_ORDER.get(e["rating"], 20)
        return e["short"]

    filtered = sorted([eid for eid in ENTITIES if _passes(eid)], key=_sort_key)

    st.markdown(
        f'<div style="color:{MUTED};font-size:12px;margin-bottom:14px">'
        f'Showing <b style="color:{TEXT}">{len(filtered)}</b> of {len(ENTITIES)} counterparties</div>',
        unsafe_allow_html=True)

    if not filtered:
        st.info("No counterparties match the selected filters.")
        return

    # ── Card grid (3 per row) ──────────────────────────────────────────────────
    COLS = 3
    for row_start in range(0, len(filtered), COLS):
        row_ids = filtered[row_start : row_start + COLS]
        cols    = st.columns(COLS)
        for col, eid in zip(cols, row_ids):
            ent   = ENTITIES[eid]; sc = SCORES[eid]
            rag_c = RAG_COL.get(sc["rag"], MUTED)
            r_c   = rating_color(ent["rating"])
            sigs  = signals_for_entity(eid)
            top   = sigs[0] if sigs else None
            top_txt = ""
            if top:
                icon  = sentiment_icon(top["sentiment"])
                top_txt = (f'<div style="margin-top:8px;padding-top:8px;'
                           f'border-top:1px solid {BORDER};font-size:11px;'
                           f'color:{sent_color(top["sentiment"])};line-height:1.4">'
                           f'{icon} {top["headline"][:70]}{"…" if len(top["headline"])>70 else ""}'
                           f'</div>')
            with col:
                st.markdown(
                    f'<div style="background:{CARD_BG};border:1px solid {BORDER};'
                    f'border-left:4px solid {rag_c};border-radius:10px;'
                    f'padding:14px;margin-bottom:10px">'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
                    f'<div>'
                    f'<div style="font-size:22px;line-height:1">{ent["flag"]}</div>'
                    f'<div style="font-weight:700;color:{TEXT};font-size:14px;margin-top:6px">'
                    f'{ent["short"]}</div>'
                    f'<div style="color:{MUTED};font-size:11px;margin-top:2px">{ent["sector"]}</div>'
                    f'<div style="color:{MUTED};font-size:11px">{ent["country"]}</div>'
                    f'<div style="color:{r_c};font-size:12px;font-weight:700;margin-top:4px">'
                    f'{ent["rating"]}</div>'
                    f'</div>'
                    f'<div style="text-align:right">'
                    f'<div style="font-size:28px;font-weight:900;color:{rag_c};line-height:1">'
                    f'{sc["composite"]:.0f}</div>'
                    f'<div style="font-size:11px;color:{rag_c};font-weight:700">{sc["rag"]}</div>'
                    f'<div style="font-size:11px;color:{MUTED};margin-top:4px">'
                    f'£{ent["ead_m"]:.0f}M EAD</div>'
                    f'<div style="font-size:11px;color:{MUTED}">ECL £{sc["ecl_m"]:.1f}M</div>'
                    f'</div></div>'
                    f'{top_txt}</div>',
                    unsafe_allow_html=True)
                if st.button(f"View {ent['short']} →", key=f"pf_{eid}",
                             use_container_width=True):
                    _navigate_to("entity", eid)

# ─── PAGE: FULL NETWORK ───────────────────────────────────────────────────────

def page_full_network():
    st.markdown("## Full Portfolio Network")
    st.caption("All 10 counterparties + complete ecosystems. CP size = EAD. CP colour = RAG.")
    all_types = list(NODE_COL.keys())
    sel_types = st.multiselect("Node types",options=all_types,default=all_types,key="full_net_types")
    G = _build_full_graph()
    remove = [n for n,d in G.nodes(data=True) if d.get("node_type","") not in sel_types]
    Gf = G.copy(); Gf.remove_nodes_from(remove)
    st.plotly_chart(_graph_to_fig(Gf,height=700),use_container_width=True)
    cols = st.columns(len(NODE_COL))
    for i,(t,c) in enumerate(NODE_COL.items()):
        cols[i].markdown(f'<div style="text-align:center"><span style="color:{c};font-size:20px">●</span><br><span style="font-size:10px;color:{MUTED}">{t.title()}</span></div>',unsafe_allow_html=True)

# ─── PAGE: ENTITY DEEP DIVE ───────────────────────────────────────────────────

def _scen_card(cp_id: str, s: dict, border_c: str, impact_c: str):
    import html as _html
    linked = SCENARIO_LINKED_SIGNALS.get(cp_id, {}).get(s["name"], [])
    badges = "".join([
        f'<span style="background:#1e3a5f;color:#60a5fa;font-size:10px;'
        f'padding:2px 7px;border-radius:4px;margin-right:4px;white-space:nowrap">'
        f'📡 {_html.escape(tag)}</span>'
        for tag in linked
    ])
    linked_html = (
        f'<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px">'
        f'<span style="color:{MUTED};font-size:10px;margin-right:4px">Linked signals:</span>{badges}</div>'
        if linked else ""
    )
    st.markdown(
        f'<div style="background:{CARD_BG};border:1px solid {border_c}44;border-left:3px solid {border_c};'
        f'border-radius:8px;padding:12px 16px;margin-bottom:8px">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
        f'<div style="flex:1">'
        f'<div style="font-weight:700;color:{TEXT};font-size:14px">{_html.escape(s["name"])}</div>'
        f'<div style="color:{MUTED};font-size:12px;margin-top:2px">Trigger: {_html.escape(s["trigger"])}</div>'
        f'<div style="color:{MUTED};font-size:12px;margin-top:4px">{_html.escape(s["detail"])}</div>'
        f'{linked_html}'
        f'</div>'
        f'<div style="text-align:right;margin-left:16px;flex-shrink:0">'
        f'<div style="font-size:15px;font-weight:700;color:{impact_c}">{_html.escape(s["impact"])}</div>'
        f'<div style="font-size:12px;color:{MUTED}">Prob: {s["prob"]}</div>'
        f'</div></div></div>',
        unsafe_allow_html=True
    )


def page_entity(cp_id: str):
    ent  = ENTITIES[cp_id]; sc = SCORES[cp_id]
    sigs = signals_for_entity(cp_id)
    rag  = sc["rag"]; rag_c = RAG_COL.get(rag, MUTED); r_col = rating_color(ent["rating"])

    _signal_ticker(cp_id)

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:6px">'
        f'<span style="font-size:40px">{ent["flag"]}</span>'
        f'<div style="flex:1">'
        f'<h2 style="margin:0;color:{TEXT}">{ent["name"]}</h2>'
        f'<div style="color:{MUTED};font-size:13px">{ent["sector"]} · {ent["country"]} · '
        f'<span style="color:{r_col};font-weight:700">{ent["rating"]}</span></div>'
        f'</div>'
        f'<div style="background:{rag_c}22;border:1px solid {rag_c};border-radius:10px;'
        f'padding:10px 20px;text-align:center">'
        f'<div style="font-size:28px;font-weight:800;color:{rag_c}">{sc["composite"]:.0f}</div>'
        f'<div style="font-size:12px;color:{rag_c};font-weight:600">{rag}</div>'
        f'</div></div>'
        f'<p style="color:{MUTED};font-size:13px;line-height:1.6;margin-bottom:12px">{ent["description"]}</p>',
        unsafe_allow_html=True
    )
    _exposure_breakdown(cp_id)
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("EAD",   f"£{ent['ead_m']:.0f}M")
    m2.metric("LGD",   f"{ent['lgd']*100:.0f}%")
    m3.metric("Own Risk Score",    f"{sc['own_score']:.0f}")
    m4.metric("Propagated Score",  f"{sc['prop_score']:.0f}")
    m5.metric("ECL",   f"£{sc['ecl_m']:.1f}M")

    # Financial impact decomposition (from ML scoring)
    imp_cols = st.columns([1,1,1,1,2])
    imp_cols[0].metric("Revenue Impact",  f"{sc.get('rev_impact',0):.0f}",
                       help="Earnings / top-line impact score (0–100)")
    imp_cols[1].metric("Cost Impact",     f"{sc.get('cost_impact',0):.0f}",
                       help="Provisions, OpEx, credit-loss impact (0–100)")
    imp_cols[2].metric("Growth Impact",   f"{sc.get('grow_impact',0):.0f}",
                       help="Forward market position / growth impact (0–100)")
    imp_cols[3].metric("Confidence",      f"{sc.get('confidence',0)*100:.0f}%",
                       help="Model confidence based on signal coverage")
    _score_drilldown(cp_id, sc)

    st.divider()

    # ── Build node map before columns (shared by both columns) ─────────────────
    net   = NETWORKS.get(cp_id, {})
    nodes = net.get("nodes", [])
    node_map: dict = {n["id"]: n for n in nodes}
    for nid in ([e[0] for e in net.get("edges",[])] +
                [e[1] for e in net.get("edges",[])]):
        if nid in ENTITIES and nid not in node_map:
            e2 = ENTITIES[nid]
            node_map[nid] = {"id": nid, "name": e2["name"], "type": "CP",
                             "country": e2["country"], "note": e2["description"][:120]}

    # ── Two-column layout: Network left | Signals+Scenarios right ─────────────
    net_col, info_col = st.columns([3, 2], gap="large")

    # ── LEFT: Network ──────────────────────────────────────────────────────────
    with net_col:
        st.markdown("### 🕸️ Network")

        # Compact node-type stats
        type_counts: dict = {}
        for n in nodes:
            type_counts[n["type"]] = type_counts.get(n["type"], 0) + 1
        stat_cols = st.columns(min(len(type_counts) + 1, 8))
        stat_cols[0].metric("Nodes", len(nodes) + 1)
        for i, (t, cnt) in enumerate(list(type_counts.items())[:7]):
            stat_cols[i+1].markdown(
                f'<div style="text-align:center">'
                f'<div style="font-size:16px;font-weight:700;color:{MUTED}">{cnt}</div>'
                f'<div style="font-size:10px;color:{MUTED}">{t.title()}</div></div>',
                unsafe_allow_html=True)

        # Network graph
        G_ego = _build_ego_graph(cp_id)
        fig   = _graph_to_fig(G_ego, height=480)
        try:
            event = st.plotly_chart(fig, use_container_width=True,
                                    on_select="rerun", key=f"ego_{cp_id}",
                                    selection_mode=["points"])
            if event and hasattr(event, "selection") and event.selection:
                pts = event.selection.get("points", [])
                if pts:
                    clicked_id = pts[0].get("customdata")
                    if clicked_id and clicked_id in ENTITIES and clicked_id != cp_id:
                        _navigate_to("entity", clicked_id)
                    elif clicked_id:
                        st.session_state[f"node_sel_{cp_id}"] = clicked_id
        except Exception:
            st.plotly_chart(fig, use_container_width=True)

        # Node inspector dropdown
        sel_opts = ["— select node —"] + sorted(node_map.keys(),
                                                key=lambda x: node_map[x]["name"])
        pre = st.session_state.get(f"node_sel_{cp_id}", "— select node —")
        sel = st.selectbox(
            "Inspect network entity", options=sel_opts,
            format_func=lambda x: node_map[x]["name"] if x in node_map else x,
            index=sel_opts.index(pre) if pre in sel_opts else 0,
            key=f"node_sel_{cp_id}")

        # Node card
        if sel and sel != "— select node —" and sel in node_map:
            nd    = node_map[sel]
            nrs   = NODE_RISK_SCORES.get(sel, COUNTRY_SCORES.get(sel, {}))
            rag2  = nrs.get("rag", ""); rc2 = RAG_COL.get(rag2, MUTED)
            score2 = nrs.get("score", "—")
            flag2  = nd.get("flag", "")
            st.markdown(
                f'<div style="background:{CARD_BG};border:1px solid {BORDER};'
                f'border-left:4px solid {rc2};border-radius:8px;padding:12px 16px;'
                f'margin-top:6px;display:flex;justify-content:space-between">'
                f'<div style="flex:1">'
                f'<div style="font-weight:700;color:{TEXT};font-size:14px">{flag2} {nd["name"]}</div>'
                f'<div style="color:{MUTED};font-size:11px;margin-top:2px">'
                f'{nd["type"]} · {nd.get("country","")}</div>'
                f'<div style="color:{MUTED};font-size:11px;margin-top:6px;line-height:1.5">'
                f'{nd.get("note","")}</div></div>'
                f'<div style="text-align:right;flex-shrink:0;padding-left:12px">'
                f'<div style="font-size:20px;font-weight:800;color:{rc2}">{score2}</div>'
                f'<div style="font-size:11px;color:{rc2};font-weight:600">{rag2}</div>'
                f'</div></div>', unsafe_allow_html=True)
            if nd["type"] == "CP" and sel in ENTITIES:
                if st.button(f"Open {ENTITIES[sel]['short']} →",
                             key=f"goto_{sel}_{cp_id}"):
                    _navigate_to("entity", sel)

        with st.expander("All network entities", expanded=False):
            for t_type in ["SUBSIDIARY","SUPPLIER","CUSTOMER","SHAREHOLDER",
                           "LENDER","COMPETITOR","REGULATOR","COUNTRY"]:
                t_nodes = [n for n in nodes if n["type"] == t_type]
                if not t_nodes: continue
                st.markdown(
                    f'<div style="color:{MUTED};font-weight:700;margin-top:8px;'
                    f'margin-bottom:4px">{t_type.title()}s</div>',
                    unsafe_allow_html=True)
                for n in t_nodes:
                    flag3 = n.get("flag",""); note3 = n.get("note","") or ""
                    st.markdown(
                        f'<div style="padding:3px 0;border-bottom:1px solid {BORDER}">'
                        f'<span style="font-weight:600;color:{TEXT};font-size:12px">'
                        f'{flag3} {n["name"]}</span>'
                        f'<span style="color:{MUTED};font-size:11px"> · {n.get("country","")}</span><br>'
                        f'<span style="color:{MUTED};font-size:11px">{note3}</span></div>',
                        unsafe_allow_html=True)

    # ── RIGHT: Signals + Scenarios (node-aware) ────────────────────────────────
    with info_col:
        # Determine which entity's data to show
        sel_node = st.session_state.get(f"node_sel_{cp_id}", "— select node —")
        if sel_node and sel_node != "— select node —":
            # Show signals about the selected network entity
            node_sigs = ([s for s in SIGNALS if s.get("related_entity") == sel_node]
                         + (signals_for_entity(sel_node)
                            if sel_node in ENTITIES else []))
            node_sigs = sorted(node_sigs, key=lambda x: -x["score"])
            node_scens = SCENARIOS.get(sel_node, [])
            nd_name    = node_map.get(sel_node, {}).get("name", sel_node)
            show_label = nd_name
        else:
            node_sigs  = sigs
            node_scens = SCENARIOS.get(cp_id, [])
            show_label = ent["short"]

        # Signals header + CSV download
        direct_ct  = sum(1 for s in node_sigs if s.get("direct", True))
        network_ct = len(node_sigs) - direct_ct
        sig_hdr, sig_dl = st.columns([4, 1])
        sig_hdr.markdown(
            f"### 📡 Signals"
            f"<div style='font-size:11px;color:{MUTED};margin-top:2px'>"
            f"{show_label} · {direct_ct} direct · {network_ct} network</div>",
            unsafe_allow_html=True)

        if node_sigs:
            import csv, io as _io
            buf = _io.StringIO()
            flds = ["scope","entity_id","headline","category","sentiment",
                    "severity","score","source","observed_at","detail"]
            cw = csv.DictWriter(buf, fieldnames=flds, extrasaction="ignore")
            cw.writeheader()
            for s in node_sigs:
                cw.writerow({
                    "scope":       "DIRECT" if s.get("direct", True) else "NETWORK",
                    "entity_id":   s.get("entity_id",""),
                    "headline":    s.get("headline",""),
                    "category":    s.get("category",""),
                    "sentiment":   s.get("sentiment",""),
                    "severity":    s.get("severity",""),
                    "score":       s.get("score",""),
                    "source":      s.get("source",""),
                    "observed_at": s.get("observed_at",""),
                    "detail":      s.get("detail",""),
                })
            sig_dl.download_button(
                "⬇ CSV", data=buf.getvalue(),
                file_name=f"signals_{sel_node or cp_id}.csv",
                mime="text/csv", use_container_width=True)

        if not node_sigs:
            st.info(f"No signals for {show_label}.")
        else:
            for sig in node_sigs[:7]:
                _signal_card(sig, propagated=not sig.get("direct", True))
            if len(node_sigs) > 7:
                with st.expander(f"All {len(node_sigs)} signals"):
                    for sig in node_sigs[7:]:
                        _signal_card(sig, propagated=not sig.get("direct", True))

        st.markdown(f'<div style="border-bottom:1px solid {BORDER};margin:12px 0 10px"></div>',
                    unsafe_allow_html=True)

        # Scenarios
        st.markdown("### ⚡ Scenarios")
        if not node_scens:
            st.info(f"No scenarios for {show_label}.")
        else:
            worse   = [s for s in node_scens if s["dir"] == "worse"]
            better  = [s for s in node_scens if s["dir"] == "better"]
            neutral = [s for s in node_scens if s["dir"] == "neutral"]
            scen_eid = sel_node if sel_node and sel_node != "— select node —" else cp_id
            if worse:
                st.markdown(f'<div style="color:#ef4444;font-weight:700;font-size:12px;'
                            f'margin-bottom:4px">⬇ ADVERSE</div>', unsafe_allow_html=True)
                for s in worse:   _scen_card(scen_eid, s, "#ef4444", "#ef4444")
            if better:
                st.markdown(f'<div style="color:#22c55e;font-weight:700;font-size:12px;'
                            f'margin:8px 0 4px">⬆ UPSIDE</div>', unsafe_allow_html=True)
                for s in better:  _scen_card(scen_eid, s, "#22c55e", "#22c55e")
            if neutral:
                st.markdown(f'<div style="color:{MUTED};font-weight:700;font-size:12px;'
                            f'margin:8px 0 4px">↔ WATCH</div>', unsafe_allow_html=True)
                for s in neutral: _scen_card(scen_eid, s, MUTED, MUTED)

# ─── AGENTS PAGE ─────────────────────────────────────────────────────────────

def page_agents():
    import random, datetime

    st.markdown(
        f'<h2 style="color:{TEXT};margin:0 0 4px">🤖 AI Monitoring Agents</h2>'
        f'<div style="color:{MUTED};font-size:13px;margin-bottom:20px">'
        f'Autonomous agents scanning news, filings, CDS markets and alt-data sources 24/7. '
        f'Each agent monitors a specific sector or country and feeds signals into the risk engine.</div>',
        unsafe_allow_html=True)

    # ── derive sector/country counts from ENTITIES ─────────────────────────────
    from collections import defaultdict
    sector_cps: dict = defaultdict(list)
    country_cps: dict = defaultdict(list)
    for cp_id, e in ENTITIES.items():
        sector_cps[e["sector"]].append(cp_id)
        country_cps[e["country"]].append(cp_id)

    # signal counts per sector / country
    sig_by_sector: dict = defaultdict(int)
    sig_by_country: dict = defaultdict(int)
    for sig in SIGNALS:
        eid = sig.get("entity_id","")
        if eid in ENTITIES:
            sig_by_sector[ENTITIES[eid]["sector"]] += 1
            sig_by_country[ENTITIES[eid]["country"]] += 1

    # deterministic "last scan" offsets so they don't change on every rerun
    def _last_scan(seed: str, max_mins: int = 45) -> str:
        r = random.Random(seed)
        mins = r.randint(1, max_mins)
        t = datetime.datetime.utcnow() - datetime.timedelta(minutes=mins)
        return t.strftime("%H:%M UTC")

    def _next_scan(seed: str) -> str:
        r = random.Random(seed + "_next")
        mins = r.randint(5, 30)
        t = datetime.datetime.utcnow() + datetime.timedelta(minutes=mins)
        return t.strftime("%H:%M UTC")

    def _agent_card(icon: str, name: str, description: str,
                    n_entities: int, n_signals: int, seed: str,
                    status: str = "ACTIVE", alert: bool = False):
        border_col = "#ef4444" if alert else "#3b82f6"
        status_col = {"ACTIVE": "#22c55e", "SCANNING": "#f59e0b", "IDLE": "#94a3b8"}.get(status, "#22c55e")
        status_dot = {"ACTIVE": "🟢", "SCANNING": "🟡", "IDLE": "⚫"}.get(status, "🟢")
        last = _last_scan(seed)
        nxt  = _next_scan(seed)
        st.markdown(f"""
<div style="background:{CARD_BG};border:1px solid {border_col};border-radius:8px;
            padding:14px 16px;margin-bottom:10px">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
    <div>
      <div style="font-size:15px;font-weight:700;color:{TEXT}">{icon} {name}</div>
      <div style="font-size:11px;color:{MUTED};margin-top:2px">{description}</div>
    </div>
    <div style="text-align:right;flex-shrink:0;margin-left:12px">
      <div style="font-size:11px;font-weight:700;color:{status_col}">{status_dot} {status}</div>
      <div style="font-size:10px;color:{MUTED}">Last: {last}</div>
      <div style="font-size:10px;color:{MUTED}">Next: {nxt}</div>
    </div>
  </div>
  <div style="display:flex;gap:20px;margin-top:10px;border-top:1px solid {BORDER};padding-top:10px">
    <div><span style="font-size:18px;font-weight:800;color:{TEXT}">{n_entities}</span>
         <span style="font-size:10px;color:{MUTED};margin-left:4px">entities</span></div>
    <div><span style="font-size:18px;font-weight:800;color:#f59e0b">{n_signals}</span>
         <span style="font-size:10px;color:{MUTED};margin-left:4px">signals</span></div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Platform Agents ────────────────────────────────────────────────────────
    st.markdown(f'<div style="font-size:11px;letter-spacing:1px;color:{MUTED};'
                f'margin:0 0 10px">PLATFORM AGENTS</div>', unsafe_allow_html=True)

    platform_agents = [
        ("🌐", "News NLP Agent",      "Real-time news ingestion — Reuters, Bloomberg, FT, WSJ, Le Monde, Handelsblatt",  len(ENTITIES), len(SIGNALS), "news_nlp",    "ACTIVE", True),
        ("📈", "CDS Monitor",         "Sovereign and corporate CDS spread monitoring across 100+ reference entities",     len(ENTITIES), int(len(SIGNALS)*0.4), "cds_mon",  "ACTIVE", False),
        ("📄", "Filings Scraper",     "SEC/EDGAR, Bundesanzeiger, AMF, Companies House — earnings, 8-K, profit warnings",len(ENTITIES), int(len(SIGNALS)*0.25), "filings", "ACTIVE", False),
        ("🛰️", "Alt-Data Agent",     "Satellite imagery, shipping AIS, job postings, web traffic, app downloads",        len(ENTITIES), int(len(SIGNALS)*0.15), "altdata",  "SCANNING", False),
        ("⚖️", "Regulatory Watch",   "ECB, FCA, BaFin, AMF supervisory actions, enforcement, fines, capital requirements",len(ENTITIES), int(len(SIGNALS)*0.1), "reg_watch","ACTIVE", False),
        ("🔗", "Supply Chain Radar",  "Tier-1/2 supplier disruption, port congestion, logistics stress, factory shutdowns",len(ENTITIES), int(len(SIGNALS)*0.12), "sc_radar", "ACTIVE", False),
    ]
    pcols = st.columns(2)
    for i, (icon, name, desc, ne, ns, seed, status, alert) in enumerate(platform_agents):
        with pcols[i % 2]:
            _agent_card(icon, name, desc, ne, ns, seed, status, alert)

    # ── Sector Agents ──────────────────────────────────────────────────────────
    st.markdown(f'<div style="border-top:1px solid {BORDER};margin:16px 0 14px"></div>',
                unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:11px;letter-spacing:1px;color:{MUTED};'
                f'margin-bottom:10px">SECTOR AGENTS — {len(sector_cps)} sectors covered</div>',
                unsafe_allow_html=True)

    SECTOR_ICONS = {
        "Auto OEM": "🚗", "Auto Supply": "⚙️", "Airlines": "✈️",
        "Aerospace & Defense": "🛩️", "Energy": "⛽", "Renewables": "🌱",
        "Utilities": "💡", "Telecom": "📶", "Technology": "💻",
        "Pharma": "💊", "FMCG": "🛒", "Retail": "🏪",
        "Chemicals": "🧪", "Industrials": "🏭", "Mining": "⛏️",
        "Real Estate": "🏢", "Infrastructure": "🏗️", "Shipping": "🚢",
        "Media": "📺", "Construction Materials": "🧱", "Healthcare": "🏥",
    }

    sorted_sectors = sorted(sector_cps.keys(), key=lambda s: -sig_by_sector.get(s, 0))
    scols = st.columns(3)
    for i, sector in enumerate(sorted_sectors):
        cps_in_sector = sector_cps[sector]
        n_sigs = sig_by_sector.get(sector, 0)
        icon = SECTOR_ICONS.get(sector, "📊")
        alert = n_sigs >= 4
        with scols[i % 3]:
            _agent_card(icon, f"{sector} Agent",
                        f"Monitoring {', '.join(ENTITIES[c]['short'] for c in cps_in_sector[:3])}"
                        + (f" +{len(cps_in_sector)-3} more" if len(cps_in_sector) > 3 else ""),
                        len(cps_in_sector), n_sigs, f"sector_{sector}", "ACTIVE", alert)

    # ── Country Agents ─────────────────────────────────────────────────────────
    st.markdown(f'<div style="border-top:1px solid {BORDER};margin:16px 0 14px"></div>',
                unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:11px;letter-spacing:1px;color:{MUTED};'
                f'margin-bottom:10px">COUNTRY AGENTS — {len(country_cps)} countries covered</div>',
                unsafe_allow_html=True)

    # build flag map
    flag_map: dict = {}
    for e in ENTITIES.values():
        flag_map[e["country"]] = e.get("flag", "🌍")

    sorted_countries = sorted(country_cps.keys(), key=lambda c: -sig_by_country.get(c, 0))
    ccols = st.columns(3)
    for i, country in enumerate(sorted_countries):
        cps_in_country = country_cps[country]
        n_sigs = sig_by_country.get(country, 0)
        flag   = flag_map.get(country, "🌍")
        alert  = n_sigs >= 3
        with ccols[i % 3]:
            _agent_card(flag, f"{country} Agent",
                        f"{len(cps_in_country)} counterpart{'y' if len(cps_in_country)==1 else 'ies'} — "
                        + ", ".join(ENTITIES[c]["short"] for c in cps_in_country[:3])
                        + (f" +{len(cps_in_country)-3} more" if len(cps_in_country) > 3 else ""),
                        len(cps_in_country), n_sigs, f"country_{country}", "ACTIVE", alert)


# ─── SIDEBAR (hidden — nav is via top bar) ───────────────────────────────────

def sidebar():
    page   = st.session_state.get("page", "home")
    cp_id  = st.session_state.get("selected_cp")

    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────────
        st.markdown(
            f'<div style="padding:14px 0 12px;border-bottom:1px solid {BORDER};margin-bottom:14px">'
            f'<div style="font-size:18px;font-weight:900;color:{TEXT}">'
            f'🏦 Risk <span style="color:#3b82f6">OS</span></div>'
            f'<div style="font-size:10px;color:{MUTED}">AI Risk Intelligence Platform</div>'
            f'</div>', unsafe_allow_html=True)

        # ── Navigation ────────────────────────────────────────────────────────
        st.markdown(
            f'<div style="font-size:10px;letter-spacing:1px;color:{MUTED};margin-bottom:6px">'
            f'NAVIGATION</div>', unsafe_allow_html=True)

        NAV = [
            ("home",      "📊", "Executive Dashboard"),
            ("portfolio", "🕸️", "Network Explorer"),
            ("network",   "🔍", "Full Network View"),
            ("sources",   "📡", "Signal Feed"),
            ("agents",    "🤖", "AI Agents"),
        ]
        for target, icon, label in NAV:
            active = (page == target) or (page == "entity" and target == "portfolio")
            if active:
                st.markdown(
                    f'<div style="background:#1e3a5f;border:1px solid #3b82f6;border-radius:6px;'
                    f'padding:8px 10px;margin-bottom:4px">'
                    f'<span style="color:#60a5fa;font-size:13px;font-weight:600">{icon} {label}</span>'
                    f'</div>', unsafe_allow_html=True)
            else:
                if st.button(f"{icon} {label}", key=f"sb_{target}",
                             use_container_width=True):
                    _navigate_to(target)

        # ── Quick stats ───────────────────────────────────────────────────────
        st.markdown(
            f'<div style="border-top:1px solid {BORDER};margin:14px 0 10px"></div>',
            unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:10px;letter-spacing:1px;color:{MUTED};margin-bottom:8px">'
            f'QUICK STATS</div>', unsafe_allow_html=True)

        n_red   = sum(1 for cp in ENTITIES if SCORES[cp]["rag"] == "RED")
        n_amber = sum(1 for cp in ENTITIES if SCORES[cp]["rag"] == "AMBER")
        total_ead = sum(e["ead_m"] for e in ENTITIES.values())

        for dot, label, val in [
            ("🔴", "Critical",   str(n_red)),
            ("🟡", "High",       str(n_amber)),
            ("🏛️", "Total EAD", f"£{total_ead/1000:.1f}bn"),
            ("📡", "Signals",    str(len(SIGNALS))),
        ]:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;'
                f'padding:4px 0;border-bottom:1px solid {BORDER}">'
                f'<span style="color:{MUTED};font-size:12px">{dot} {label}</span>'
                f'<span style="color:{TEXT};font-weight:700;font-size:12px">{val}</span>'
                f'</div>', unsafe_allow_html=True)

        # ── CP selector (entity pages only) ───────────────────────────────────
        if page == "entity":
            st.markdown(
                f'<div style="border-top:1px solid {BORDER};margin:14px 0 8px"></div>',
                unsafe_allow_html=True)
            st.markdown(
                f'<div style="font-size:10px;letter-spacing:1px;color:{MUTED};margin-bottom:6px">'
                f'JUMP TO COUNTERPARTY</div>', unsafe_allow_html=True)
            sorted_cps = sorted(ENTITIES.keys(), key=lambda c: -SCORES[c]["composite"])
            opts = ["— select —"] + sorted_cps
            current = st.session_state.get("selected_cp")
            idx = opts.index(current) if current in opts else 0

            def _fmt(c):
                if c == "— select —": return c
                e = ENTITIES[c]; s = SCORES[c]
                dot = {"RED": "🔴", "AMBER": "🟡", "GREEN": "🟢"}.get(s["rag"], "⚪")
                return f"{dot} {e['flag']} {e['short']} ({s['composite']:.0f})"

            sel = st.selectbox("CP", opts, format_func=_fmt, index=idx,
                               key="sb_cp_sel", label_visibility="collapsed")
            if sel and sel != "— select —" and sel != current:
                _navigate_to("entity", sel)

        # ── Footer ────────────────────────────────────────────────────────────
        st.markdown(
            f'<div style="position:absolute;bottom:16px;left:0;right:0;text-align:center;'
            f'color:{MUTED};font-size:10px">Prototype v0.1 — Not for production use</div>',
            unsafe_allow_html=True)


# ─── TOP NAV BAR (shown on all non-home pages) ────────────────────────────────

def _top_nav():
    page    = st.session_state.get("page","home")
    cp_id   = st.session_state.get("selected_cp")
    cp_name = ENTITIES[cp_id]["short"] if cp_id and cp_id in ENTITIES else None

    # Breadcrumb
    crumb_parts = ["Home"]
    if page == "portfolio":            crumb_parts.append("Counterparty")
    elif page == "network":            crumb_parts.append("Full Network")
    elif page == "sources":            crumb_parts.append("Signal Sources")
    elif page == "agents":             crumb_parts.append("AI Agents")
    elif page == "entity" and cp_name: crumb_parts += ["Counterparty", cp_name]

    sep = " <span style='color:#475569'>›</span> "
    crumb_spans = []
    for i, p in enumerate(crumb_parts):
        col_c = TEXT if i == len(crumb_parts)-1 else MUTED
        fw    = "600" if i == len(crumb_parts)-1 else "400"
        crumb_spans.append(f'<span style="color:{col_c};font-weight:{fw}">{p}</span>')
    st.markdown(
        f'<div style="font-size:12px;margin-bottom:4px">{sep.join(crumb_spans)}</div>',
        unsafe_allow_html=True)

    # Nav buttons + CP dropdown in one row
    NAV = [
        ("🏠 Home",        "home",     "tnb_home"),
        ("📊 Portfolio",   "portfolio","tnb_port"),
        ("🕸️ Network",    "network",  "tnb_net"),
        ("📡 Sources",     "sources",  "tnb_src"),
        ("🤖 Agents",      "agents",   "tnb_agents"),
    ]
    btn_cols = st.columns([1, 1, 1, 1, 1, 2])
    for col, (label, target, key) in zip(btn_cols[:5], NAV):
        active = (page == target) or (page == "entity" and target == "portfolio")
        with col:
            if active:
                st.markdown(
                    f'<div style="background:{CARD_BG};border:1px solid #3b82f6;'
                    f'border-radius:6px;padding:5px 0;text-align:center;'
                    f'font-size:12px;font-weight:700;color:#3b82f6">{label}</div>',
                    unsafe_allow_html=True)
            else:
                if st.button(label, key=key, use_container_width=True):
                    _navigate_to(target)

    # Sector + Country quick-filters (right side of nav)
    with btn_cols[5]:
        qf1, qf2 = st.columns(2)
        all_sectors = ["All sectors"] + sorted(set(e["sector"] for e in ENTITIES.values()))
        seen_c2: dict = {}
        for _e in ENTITIES.values(): seen_c2[_e["country"]] = _e.get("flag","")
        all_countries = ["All countries"] + [f'{seen_c2[c]} {c}' for c in sorted(seen_c2)]

        prev_sec = st.session_state.get("topnav_sector", "All sectors")
        prev_cty = st.session_state.get("topnav_country", "All countries")

        with qf1:
            new_sec = st.selectbox("Sector", all_sectors,
                                   index=all_sectors.index(prev_sec) if prev_sec in all_sectors else 0,
                                   key="topnav_sector", label_visibility="collapsed")
        with qf2:
            new_cty = st.selectbox("Country", all_countries,
                                   index=all_countries.index(prev_cty) if prev_cty in all_countries else 0,
                                   key="topnav_country", label_visibility="collapsed")

        # Sync top-nav quick filter → portfolio page multiselects + navigate
        if new_sec != "All sectors" or new_cty != "All countries":
            if new_sec != "All sectors":
                st.session_state["pf_sectors"] = [new_sec]
            if new_cty != "All countries":
                cty_code = new_cty.split()[-1]
                # find matching display value in portfolio options
                st.session_state["pf_countries"] = [new_cty]
            if st.session_state.get("page") != "portfolio":
                _navigate_to("portfolio")

    st.markdown(
        f'<div style="border-bottom:1px solid {BORDER};margin:6px 0 14px"></div>',
        unsafe_allow_html=True)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    if "page" not in st.session_state:        st.session_state.page = "home"
    if "selected_cp" not in st.session_state: st.session_state.selected_cp = None
    if "nav_history" not in st.session_state: st.session_state.nav_history = []

    # Mobile-responsive CSS
    st.markdown("""<style>
    @media (max-width: 768px) {
        section.main > div { padding: 0.5rem !important; }
        div[data-testid="column"] { min-width: 100% !important; flex: 1 1 100% !important; }
        h2 { font-size: 1.1rem !important; }
        div[data-testid="stMetric"] label { font-size: 10px !important; }
    }
    </style>""", unsafe_allow_html=True)

    sidebar()
    page = st.session_state.page
    cp   = st.session_state.selected_cp

    if page != "home":
        _top_nav()

    if page == "home":               page_home()
    elif page == "portfolio":        page_portfolio()
    elif page == "network":          page_full_network()
    elif page == "sources":          page_sources()
    elif page == "agents":           page_agents()
    elif page == "entity" and cp and cp in ENTITIES: page_entity(cp)
    else:                            page_home()

if __name__ == "__main__":
    main()
