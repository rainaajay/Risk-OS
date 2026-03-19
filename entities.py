"""
entities.py — Self-contained data layer for Credit Monitor

10 focus counterparties, their full corporate networks,
signals (direct + related entities), and computed scores.
"""

from __future__ import annotations
from typing import Dict, List, Any

# ─────────────────────────────────────────────────────────────
# 10 FOCUS COUNTERPARTIES
# ─────────────────────────────────────────────────────────────

ENTITIES: Dict[str, Dict] = {

    "CP001": {
        "id": "CP001", "name": "Volkswagen AG", "short": "VW",
        "sector": "Auto OEM", "country": "DE", "flag": "🇩🇪",
        "rating": "BBB", "ead_m": 245.0, "lgd": 0.45,
        "description": (
            "Europe's largest automaker. 35,000 job cuts and 3 plant closures "
            "announced 2024. EV transition burning €15bn+/yr capex. Net debt €20bn+. "
            "Rating at IG/HY boundary. ZF and Continental receiving volume downgrades."
        ),
    },
    "CP003": {
        "id": "CP003", "name": "Mercedes-Benz Group", "short": "Mercedes",
        "sector": "Auto OEM", "country": "DE", "flag": "🇩🇪",
        "rating": "A-", "ead_m": 180.0, "lgd": 0.40,
        "description": (
            "Ultra-luxury OEM. Supplies AMG powertrains to Aston Martin. China volume "
            "decline and EV price pressure are primary concerns. Strong FCF; net cash. "
            "A- floor supported by luxury pricing power."
        ),
    },
    "CP005": {
        "id": "CP005", "name": "Aston Martin Lagonda", "short": "Aston Martin",
        "sector": "Auto OEM", "country": "UK", "flag": "🇬🇧",
        "rating": "CCC", "ead_m": 52.0, "lgd": 0.55,
        "description": (
            "Serial capital raises since 2018 IPO. Going concern clause 2024. "
            "Cash runway under 6 months without fresh equity. Engine entirely sourced "
            "from Mercedes-Benz AMG. Ultra-luxury (7,000 units/yr); recovery ~55p/£."
        ),
    },
    "CP006": {
        "id": "CP006", "name": "ZF Friedrichshafen", "short": "ZF",
        "sector": "Auto Supply", "country": "DE", "flag": "🇩🇪",
        "rating": "BB", "ead_m": 195.0, "lgd": 0.50,
        "description": (
            "World's second-largest auto supplier. Post-Wabco net debt ~€12bn. "
            "OEM volume downgrades from VW and Stellantis hitting transmission revenues. "
            "Covenant waiver discussions active. EV transition shrinking addressable market."
        ),
    },
    "CP007": {
        "id": "CP007", "name": "Continental AG", "short": "Continental",
        "sector": "Auto Supply", "country": "DE", "flag": "🇩🇪",
        "rating": "BBB-", "ead_m": 160.0, "lgd": 0.45,
        "description": (
            "Diversified supplier: tyres, automotive tech, industrial. BBB- is the key "
            "floor — breach triggers refinancing costs. Tyres division (50% EBITDA) "
            "provides ballast against auto sector headwinds."
        ),
    },
    "CP009": {
        "id": "CP009", "name": "Northvolt AB", "short": "Northvolt",
        "sector": "Auto Supply", "country": "SE", "flag": "🇸🇪",
        "rating": "D", "ead_m": 38.0, "lgd": 0.70,
        "description": (
            "Swedish battery manufacturer in crisis. Chapter 11 filed after burning $15bn. "
            "BMW and VW cancelled multi-billion contracts. Skellefteå factory yield rates "
            "failed. Going concern; recovery dependent on Swedish state or trade sale."
        ),
    },
    "CP013": {
        "id": "CP013", "name": "Wizz Air Holdings", "short": "Wizz Air",
        "sector": "Airline", "country": "HU", "flag": "🇭🇺",
        "rating": "B", "ead_m": 88.0, "lgd": 0.55,
        "description": (
            "Highest Pratt & Whitney GTF engine exposure in Europe — up to 50 aircraft "
            "grounded. Wet-lease replacement costs ~$1.8M/month/aircraft. FY2025 EBITDA "
            "impact €280–350M. Bond maturity Nov 2026. Covenant pressure building."
        ),
    },
    "CP023": {
        "id": "CP023", "name": "Thames Water Utilities", "short": "Thames Water",
        "sector": "Utilities", "country": "UK", "flag": "🇬🇧",
        "rating": "BB-", "ead_m": 310.0, "lgd": 0.35,
        "description": (
            "UK's largest water utility: critical infrastructure, 16M customers. "
            "£18.3bn regulated debt; equity written to zero. Ofwat enforcement; potential "
            "special administration. CEO/CFO resigned. Urgent equity injection needed."
        ),
    },
    "CP028": {
        "id": "CP028", "name": "Signa Holding GmbH", "short": "Signa",
        "sector": "Real Estate", "country": "AT", "flag": "🇦🇹",
        "rating": "D", "ead_m": 140.0, "lgd": 0.65,
        "description": (
            "Largest corporate insolvency in German-speaking Europe (Nov 2023). €23bn "
            "liabilities. Julius Bär wrote off CHF 606M. Deutsche Bank, Credit Suisse "
            "impacted. KaDeWe, Selfridges in asset recovery. Haircuts estimated 40–70p/£."
        ),
    },
    "CP033": {
        "id": "CP033", "name": "Atos SE", "short": "Atos",
        "sector": "Technology", "country": "FR", "flag": "🇫🇷",
        "rating": "CCC", "ead_m": 72.0, "lgd": 0.55,
        "description": (
            "French IT services group in deep restructuring. €5bn debt restructuring "
            "completed mid-2024. Government contracts (defense, nuclear) ring-fenced in "
            "Eviden spin-out. Tech foundations business sold. Rating at distressed levels."
        ),
    },
}


# ─────────────────────────────────────────────────────────────
# CORPORATE NETWORKS  (loaded from split files due to size)
# ─────────────────────────────────────────────────────────────

from networks_a import NETWORKS_A  # CP001, CP003, CP005, CP006, CP007
from networks_b import NETWORKS_B  # CP009, CP013, CP023, CP028, CP033
NETWORKS: Dict[str, Dict] = {**NETWORKS_A, **NETWORKS_B}

_NETWORKS_PLACEHOLDER = {  # kept for reference only — not used

    "CP001": {  # Volkswagen
        "nodes": [
            # Subsidiaries
            {"id": "EXT_AUDI",      "name": "Audi AG",           "type": "SUBSIDIARY",  "country": "DE", "note": "Premium division; 900K units/yr"},
            {"id": "EXT_PORSCHE",   "name": "Porsche AG",        "type": "SUBSIDIARY",  "country": "DE", "note": "Listed 12.5% stake retained; €36bn market cap"},
            {"id": "EXT_SKODA",     "name": "Škoda Auto",        "type": "SUBSIDIARY",  "country": "CZ", "note": "Volume brand; €3bn+ EBIT; Czech state relations"},
            {"id": "EXT_SEAT",      "name": "SEAT/Cupra",        "type": "SUBSIDIARY",  "country": "ES", "note": "Cupra brand growing; SEAT loss-making"},
            {"id": "EXT_MAN",       "name": "MAN Truck & Bus",   "type": "SUBSIDIARY",  "country": "DE", "note": "Restructuring ongoing; 9,500 job cuts"},
            {"id": "EXT_BENTLEY",   "name": "Bentley Motors",    "type": "SUBSIDIARY",  "country": "UK", "note": "Ultra-luxury; strong FCF contributor"},
            # Suppliers (portfolio entities)
            {"id": "CP006",         "name": "ZF Friedrichshafen","type": "SUPPLIER",    "country": "DE", "note": "Tier-1: transmissions, chassis — €4bn+ annual spend"},
            {"id": "CP007",         "name": "Continental AG",    "type": "SUPPLIER",    "country": "DE", "note": "Tier-1: tyres, electronics — €3.2bn annual spend"},
            {"id": "CP009",         "name": "Northvolt AB",      "type": "SUPPLIER",    "country": "SE", "note": "Battery JV cancelled Nov 2024; €2bn contract terminated"},
            # External suppliers
            {"id": "EXT_BOSCH",     "name": "Robert Bosch GmbH", "type": "SUPPLIER",    "country": "DE", "note": "Tier-1: powertrain, ADAS — €5.1bn annual spend"},
            {"id": "EXT_BASF",      "name": "BASF SE",           "type": "SUPPLIER",    "country": "DE", "note": "Battery materials, coatings, plastics"},
            {"id": "EXT_CATL",      "name": "CATL",              "type": "SUPPLIER",    "country": "CN", "note": "EV battery cells (replacing Northvolt volumes)"},
            # Key markets
            {"id": "CTY_CN",        "name": "China",             "type": "COUNTRY",     "country": "CN", "flag": "🇨🇳", "note": "31% of global sales; JV with SAIC/FAW; BEV competition intensifying"},
            {"id": "CTY_DE",        "name": "Germany",           "type": "COUNTRY",     "country": "DE", "flag": "🇩🇪", "note": "15% of sales; home market; plant closure controversy"},
            {"id": "CTY_US",        "name": "United States",     "type": "COUNTRY",     "country": "US", "flag": "🇺🇸", "note": "12% of sales; Chattanooga plant; tariff risk under Trump 2.0"},
            # Shareholders
            {"id": "EXT_PORSCHE_SE","name": "Porsche SE (holding)","type": "SHAREHOLDER","country": "DE", "note": "31.9% voting rights; Piëch/Porsche family vehicle"},
            {"id": "EXT_LOWER_SAX", "name": "State of Lower Saxony","type": "SHAREHOLDER","country": "DE","note": "11.8% stake; veto rights on major decisions"},
            # Competitors
            {"id": "CP003",         "name": "Mercedes-Benz",     "type": "COMPETITOR",  "country": "DE", "note": "Premium segment overlap; shared German labour market"},
            {"id": "EXT_STELLANTIS","name": "Stellantis NV",     "type": "COMPETITOR",  "country": "FR", "note": "Volume segment; shared Tier-1 supplier base with VW"},
        ],
        "edges": [
            ("CP001", "EXT_AUDI",       "OWNS",      1.0),
            ("CP001", "EXT_PORSCHE",    "OWNS",      1.0),
            ("CP001", "EXT_SKODA",      "OWNS",      1.0),
            ("CP001", "EXT_SEAT",       "OWNS",      1.0),
            ("CP001", "EXT_MAN",        "OWNS",      1.0),
            ("CP001", "EXT_BENTLEY",    "OWNS",      1.0),
            ("CP006", "CP001",          "SUPPLIES",  0.9),
            ("CP007", "CP001",          "SUPPLIES",  0.85),
            ("CP009", "CP001",          "SUPPLIES",  0.6),
            ("EXT_BOSCH",  "CP001",     "SUPPLIES",  0.9),
            ("EXT_BASF",   "CP001",     "SUPPLIES",  0.5),
            ("EXT_CATL",   "CP001",     "SUPPLIES",  0.7),
            ("CP001", "CTY_CN",         "OPERATES",  0.9),
            ("CP001", "CTY_DE",         "OPERATES",  0.8),
            ("CP001", "CTY_US",         "OPERATES",  0.6),
            ("EXT_PORSCHE_SE", "CP001", "OWNS",      0.8),
            ("EXT_LOWER_SAX",  "CP001", "OWNS",      0.6),
            ("CP001", "CP003",          "COMPETES",  0.5),
            ("CP001", "EXT_STELLANTIS", "COMPETES",  0.5),
        ],
    },

    "CP003": {  # Mercedes-Benz
        "nodes": [
            {"id": "EXT_AMG",       "name": "Mercedes-AMG GmbH", "type": "SUBSIDIARY",  "country": "DE", "note": "Performance division; sole engine supplier to Aston Martin"},
            {"id": "EXT_MBFS",      "name": "MB Financial Svcs", "type": "SUBSIDIARY",  "country": "DE", "note": "Auto finance; €140bn+ assets; credit portfolio risk"},
            {"id": "EXT_DAIMLER_TR","name": "Daimler Truck (19%)","type": "SUBSIDIARY", "country": "DE", "note": "Residual 19% stake post demerger 2021"},
            {"id": "CP005",         "name": "Aston Martin",      "type": "CUSTOMER",    "country": "UK", "note": "Buys 100% of engines from AMG; critical customer dependency"},
            {"id": "CP006",         "name": "ZF Friedrichshafen","type": "SUPPLIER",    "country": "DE", "note": "Tier-1: transmissions, steering — €2.8bn annual spend"},
            {"id": "CP007",         "name": "Continental AG",    "type": "SUPPLIER",    "country": "DE", "note": "Tier-1: tyres, electronics — €2.5bn annual spend"},
            {"id": "EXT_BOSCH",     "name": "Robert Bosch GmbH", "type": "SUPPLIER",    "country": "DE", "note": "Tier-1: powertrain, sensors — €3.9bn annual spend"},
            {"id": "CTY_CN",        "name": "China",             "type": "COUNTRY",     "country": "CN", "flag": "🇨🇳", "note": "24% of global sales via BBAC JV; BYD competitive pressure"},
            {"id": "CTY_DE",        "name": "Germany",           "type": "COUNTRY",     "country": "DE", "flag": "🇩🇪", "note": "14% of sales; Stuttgart HQ; Sindelfingen flagship plant"},
            {"id": "CTY_US",        "name": "United States",     "type": "COUNTRY",     "country": "US", "flag": "🇺🇸", "note": "16% of sales; Tuscaloosa plant; S/GLE Class demand solid"},
            {"id": "EXT_KUWAIT_IA", "name": "Kuwait Inv. Auth.", "type": "SHAREHOLDER", "country": "KW", "note": "6.1% stake; sovereign wealth fund"},
            {"id": "EXT_LI_SHUFU",  "name": "Geely (Li Shufu)",  "type": "SHAREHOLDER", "country": "CN", "note": "9.7% economic stake via equity swaps"},
            {"id": "CP001",         "name": "Volkswagen AG",     "type": "COMPETITOR",  "country": "DE", "note": "Premium/luxury overlap; shared DE supplier base"},
        ],
        "edges": [
            ("CP003", "EXT_AMG",       "OWNS",     1.0),
            ("CP003", "EXT_MBFS",      "OWNS",     1.0),
            ("CP003", "EXT_DAIMLER_TR","OWNS",     0.5),
            ("EXT_AMG",  "CP005",      "SUPPLIES", 1.0),
            ("CP006",    "CP003",      "SUPPLIES", 0.85),
            ("CP007",    "CP003",      "SUPPLIES", 0.8),
            ("EXT_BOSCH","CP003",      "SUPPLIES", 0.9),
            ("CP003", "CTY_CN",        "OPERATES", 0.85),
            ("CP003", "CTY_DE",        "OPERATES", 0.75),
            ("CP003", "CTY_US",        "OPERATES", 0.65),
            ("EXT_KUWAIT_IA","CP003",  "OWNS",     0.5),
            ("EXT_LI_SHUFU", "CP003",  "OWNS",     0.6),
            ("CP003", "CP001",         "COMPETES", 0.5),
        ],
    },

    "CP005": {  # Aston Martin
        "nodes": [
            {"id": "CP003",         "name": "Mercedes-Benz AMG", "type": "SUPPLIER",    "country": "DE", "note": "Sole AMG V8/V12 engine supplier — 100% dependency, no alternative"},
            {"id": "EXT_GEELY",     "name": "Geely Automobile",  "type": "SHAREHOLDER", "country": "CN", "note": "Backstop rights issue; strategic Chinese industrial partner"},
            {"id": "EXT_PIF",       "name": "Saudi PIF",         "type": "SHAREHOLDER", "country": "SA", "note": "36% stake; sovereign wealth fund; key liquidity provider"},
            {"id": "EXT_STROLL",    "name": "Yew Tree (L. Stroll)","type": "SHAREHOLDER","country": "CA","note": "25%+ controlling shareholder; F1 connection drives brand"},
            {"id": "EXT_ASTON_F1",  "name": "Aston Martin F1",   "type": "SUBSIDIARY",  "country": "UK", "note": "F1 branding vehicle; costs ~£90M/yr; halo brand effect"},
            {"id": "CTY_US",        "name": "United States",     "type": "COUNTRY",     "country": "US", "flag": "🇺🇸", "note": "35% of sales; primary profit market; dealer network 150+"},
            {"id": "CTY_UK",        "name": "United Kingdom",    "type": "COUNTRY",     "country": "UK", "flag": "🇬🇧", "note": "30% of sales; Gaydon factory; heritage market"},
            {"id": "CTY_ME",        "name": "Middle East",       "type": "COUNTRY",     "country": "AE", "flag": "🇦🇪", "note": "20% of sales; ultra-high-net-worth customer base; PIF alignment"},
            {"id": "EXT_HY_BONDS",  "name": "HY Bond Market",    "type": "LENDER",      "country": "UK", "note": "~£1.3bn 10% senior secured notes; 2029 maturity; distressed trading levels"},
            {"id": "EXT_FERRARI",   "name": "Ferrari NV",        "type": "COMPETITOR",  "country": "IT", "note": "Primary luxury competitor; far stronger FCF and brand premium"},
        ],
        "edges": [
            ("CP003",        "CP005", "SUPPLIES",  1.0),
            ("EXT_GEELY",    "CP005", "OWNS",      0.4),
            ("EXT_PIF",      "CP005", "OWNS",      0.8),
            ("EXT_STROLL",   "CP005", "OWNS",      0.7),
            ("CP005", "EXT_ASTON_F1","OWNS",       0.6),
            ("CP005", "CTY_US",      "OPERATES",   0.9),
            ("CP005", "CTY_UK",      "OPERATES",   0.8),
            ("CP005", "CTY_ME",      "OPERATES",   0.7),
            ("EXT_HY_BONDS", "CP005","LENDS",      0.9),
            ("CP005", "EXT_FERRARI", "COMPETES",   0.5),
        ],
    },

    "CP006": {  # ZF Friedrichshafen
        "nodes": [
            {"id": "CP001",         "name": "Volkswagen AG",     "type": "CUSTOMER",    "country": "DE", "note": "~18% of ZF revenue; volume downgrades ongoing; covenant trigger"},
            {"id": "CP003",         "name": "Mercedes-Benz",     "type": "CUSTOMER",    "country": "DE", "note": "~12% of ZF revenue; premium segment more resilient"},
            {"id": "EXT_FORD",      "name": "Ford Motor Company","type": "CUSTOMER",    "country": "US", "note": "~10% of ZF revenue; F-150 and commercial vehicle transmissions"},
            {"id": "EXT_STELLANTIS","name": "Stellantis NV",     "type": "CUSTOMER",    "country": "FR", "note": "~8% of ZF revenue; Dodge/Jeep/Ram drivetrain packages"},
            {"id": "EXT_WABCO",     "name": "WABCO (acquired)",  "type": "SUBSIDIARY",  "country": "US", "note": "2020 acquisition; $7bn; added €5.5bn net debt — primary leverage driver"},
            {"id": "EXT_SCHAEFFLER","name": "Schaeffler AG",     "type": "SUPPLIER",    "country": "DE", "note": "Bearings and transmission components; Tier-2 to ZF"},
            {"id": "EXT_BOSCH",     "name": "Robert Bosch GmbH", "type": "COMPETITOR",  "country": "DE", "note": "Direct competitor in ADAS, steering, braking systems"},
            {"id": "CP007",         "name": "Continental AG",    "type": "COMPETITOR",  "country": "DE", "note": "Direct competitor in powertrain and chassis electronics"},
            {"id": "CTY_DE",        "name": "Germany",           "type": "COUNTRY",     "country": "DE", "flag": "🇩🇪", "note": "35% of revenue; Friedrichshafen HQ; 40,000 German employees"},
            {"id": "CTY_US",        "name": "United States",     "type": "COUNTRY",     "country": "US", "flag": "🇺🇸", "note": "20% of revenue; WABCO operations; Detroit presence"},
            {"id": "CTY_CN",        "name": "China",             "type": "COUNTRY",     "country": "CN", "flag": "🇨🇳", "note": "15% of revenue; JV structures; EV transition impacting ICE revenues"},
            {"id": "EXT_ZF_BANKS",  "name": "Syndicate Lenders", "type": "LENDER",      "country": "DE", "note": "€8bn RCF/term loan; covenant waiver discussions Q1 2025"},
        ],
        "edges": [
            ("CP006", "CP001",        "SUPPLIES",  0.9),
            ("CP006", "CP003",        "SUPPLIES",  0.8),
            ("CP006", "EXT_FORD",     "SUPPLIES",  0.7),
            ("CP006", "EXT_STELLANTIS","SUPPLIES", 0.6),
            ("CP006", "EXT_WABCO",    "OWNS",      1.0),
            ("EXT_SCHAEFFLER","CP006","SUPPLIES",  0.6),
            ("CP006", "EXT_BOSCH",    "COMPETES",  0.5),
            ("CP006", "CP007",        "COMPETES",  0.5),
            ("CP006", "CTY_DE",       "OPERATES",  0.9),
            ("CP006", "CTY_US",       "OPERATES",  0.7),
            ("CP006", "CTY_CN",       "OPERATES",  0.6),
            ("EXT_ZF_BANKS","CP006",  "LENDS",     0.9),
        ],
    },

    "CP007": {  # Continental AG
        "nodes": [
            {"id": "CP001",         "name": "Volkswagen AG",     "type": "CUSTOMER",    "country": "DE", "note": "~14% of auto revenue; volume pressure flowing through"},
            {"id": "CP003",         "name": "Mercedes-Benz",     "type": "CUSTOMER",    "country": "DE", "note": "~11% of auto revenue; premium segment resilience"},
            {"id": "EXT_VITESCO",   "name": "Vitesco Technologies","type": "SUBSIDIARY","country": "DE", "note": "Demerged 2021; electrification powertrain — Schaeffler takeover 2024"},
            {"id": "EXT_MICHELIN",  "name": "Michelin",          "type": "COMPETITOR",  "country": "FR", "note": "Primary tyre competitor; tyres are 50% of Continental EBITDA"},
            {"id": "CP006",         "name": "ZF Friedrichshafen","type": "COMPETITOR",  "country": "DE", "note": "Direct competitor in braking, chassis, ADAS systems"},
            {"id": "EXT_SCHAEFFLER","name": "Schaeffler AG",     "type": "SHAREHOLDER", "country": "DE", "note": "46% voting control via preferred shares; governance risk"},
            {"id": "CTY_DE",        "name": "Germany",           "type": "COUNTRY",     "country": "DE", "flag": "🇩🇪", "note": "30% revenue; Hanover HQ; Automotive HQ in Frankfurt"},
            {"id": "CTY_US",        "name": "United States",     "type": "COUNTRY",     "country": "US", "flag": "🇺🇸", "note": "20% revenue; US tyre market; automotive tech customers"},
            {"id": "CTY_CN",        "name": "China",             "type": "COUNTRY",     "country": "CN", "flag": "🇨🇳", "note": "15% revenue; local competition from Chinese tyre makers"},
            {"id": "EXT_CONT_BANKS","name": "EUR Bond Markets",  "type": "LENDER",      "country": "EU", "note": "€6bn+ EUR bond outstanding; BBB- is key rating floor for inclusion"},
        ],
        "edges": [
            ("CP007", "CP001",         "SUPPLIES",  0.85),
            ("CP007", "CP003",         "SUPPLIES",  0.8),
            ("CP007", "EXT_VITESCO",   "OWNS",      0.6),
            ("CP007", "EXT_MICHELIN",  "COMPETES",  0.5),
            ("CP007", "CP006",         "COMPETES",  0.5),
            ("EXT_SCHAEFFLER","CP007", "OWNS",      0.8),
            ("CP007", "CTY_DE",        "OPERATES",  0.9),
            ("CP007", "CTY_US",        "OPERATES",  0.7),
            ("CP007", "CTY_CN",        "OPERATES",  0.6),
            ("EXT_CONT_BANKS","CP007", "LENDS",     0.7),
        ],
    },

    "CP009": {  # Northvolt
        "nodes": [
            {"id": "EXT_BMW",       "name": "BMW Group",         "type": "CUSTOMER",    "country": "DE", "note": "Cancelled €2bn battery contract Nov 2024; key trigger for Chapter 11"},
            {"id": "CP001",         "name": "Volkswagen AG",     "type": "CUSTOMER",    "country": "DE", "note": "VW was founding investor; contracts terminated; €800M write-down"},
            {"id": "EXT_SCANIA",    "name": "Scania (VW Group)", "type": "CUSTOMER",    "country": "SE", "note": "Commercial vehicle batteries; smaller volume; still pending"},
            {"id": "EXT_GOLDMAN",   "name": "Goldman Sachs",     "type": "SHAREHOLDER", "country": "US", "note": "Early investor; ~8% stake; substantial write-down"},
            {"id": "EXT_EIB",       "name": "European Inv. Bank","type": "LENDER",      "country": "EU", "note": "€350M green loan; EIB political exposure to strategic EU battery goal"},
            {"id": "EXT_SWEDISH_ST","name": "Swedish State",     "type": "LENDER",      "country": "SE", "note": "SEK 9.5bn support discussions; political pressure for industrial rescue"},
            {"id": "CTY_SE",        "name": "Sweden",            "type": "COUNTRY",     "country": "SE", "flag": "🇸🇪", "note": "Skellefteå gigafactory; 5,000+ employees; local political significance"},
            {"id": "CTY_DE",        "name": "Germany",           "type": "COUNTRY",     "country": "DE", "flag": "🇩🇪", "note": "Stockholm+Hamburg offices; primary customer market"},
            {"id": "EXT_CATL",      "name": "CATL",              "type": "COMPETITOR",  "country": "CN", "note": "Chinese battery giant taking share vacated by Northvolt collapse"},
        ],
        "edges": [
            ("CP009", "EXT_BMW",       "SUPPLIES",  0.9),
            ("CP009", "CP001",         "SUPPLIES",  0.8),
            ("CP009", "EXT_SCANIA",    "SUPPLIES",  0.5),
            ("EXT_GOLDMAN",  "CP009",  "OWNS",      0.5),
            ("EXT_EIB",      "CP009",  "LENDS",     0.7),
            ("EXT_SWEDISH_ST","CP009", "LENDS",     0.8),
            ("CP009", "CTY_SE",        "OPERATES",  1.0),
            ("CP009", "CTY_DE",        "OPERATES",  0.5),
            ("CP009", "EXT_CATL",      "COMPETES",  0.4),
        ],
    },

    "CP013": {  # Wizz Air
        "nodes": [
            {"id": "EXT_PW",        "name": "Pratt & Whitney",   "type": "SUPPLIER",    "country": "US", "note": "GTF engine sole supplier; AOG crisis — 50 aircraft grounded; $1.8M/mth replacement cost"},
            {"id": "EXT_AIRBUS",    "name": "Airbus SE",         "type": "SUPPLIER",    "country": "FR", "note": "A320neo/A321 fleet supplier; 328 aircraft order book; delivery delays compound crisis"},
            {"id": "EXT_AERCAP",    "name": "AerCap Holdings",   "type": "LENDER",      "country": "IE", "note": "Largest aircraft lessor; wet lease wet-lease agreements for grounded fleet"},
            {"id": "EXT_AIR_LEASE", "name": "Air Lease Corp",    "type": "LENDER",      "country": "US", "note": "Secondary lessor; operating lease terms under stress renegotiation"},
            {"id": "EXT_BP_FUEL",   "name": "BP / Shell",        "type": "SUPPLIER",    "country": "UK", "note": "Jet fuel supply; unhedged exposure to Brent crude price swings"},
            {"id": "CTY_HU",        "name": "Hungary",           "type": "COUNTRY",     "country": "HU", "flag": "🇭🇺", "note": "Incorporated in Hungary; Orban government relations; HUF risk"},
            {"id": "CTY_UK",        "name": "United Kingdom",    "type": "COUNTRY",     "country": "UK", "flag": "🇬🇧", "note": "Luton/Gatwick bases; 20%+ of capacity; UK CAA oversight"},
            {"id": "CTY_UA",        "name": "Ukraine",           "type": "COUNTRY",     "country": "UA", "flag": "🇺🇦", "note": "Kiev hub suspended since Feb 2022; 7% of pre-war capacity lost"},
            {"id": "EXT_RYANAIR",   "name": "Ryanair Holdings",  "type": "COMPETITOR",  "country": "IE", "note": "Primary LCC competitor; stronger balance sheet; no GTF exposure"},
            {"id": "EXT_EASYJET",   "name": "easyJet plc",       "type": "COMPETITOR",  "country": "UK", "note": "UK LCC competitor; CFM engines — no GTF issue"},
            {"id": "EXT_WIZZ_BONDS","name": "Eurobond Holders",  "type": "LENDER",      "country": "EU", "note": "€500M 2026 maturity bond; trading at distressed levels; refi risk"},
        ],
        "edges": [
            ("EXT_PW",      "CP013", "SUPPLIES",  1.0),
            ("EXT_AIRBUS",  "CP013", "SUPPLIES",  0.8),
            ("EXT_AERCAP",  "CP013", "LENDS",     0.8),
            ("EXT_AIR_LEASE","CP013","LENDS",     0.6),
            ("EXT_BP_FUEL", "CP013", "SUPPLIES",  0.6),
            ("CP013", "CTY_HU",      "OPERATES",  0.9),
            ("CP013", "CTY_UK",      "OPERATES",  0.8),
            ("CP013", "CTY_UA",      "OPERATES",  0.3),
            ("CP013", "EXT_RYANAIR", "COMPETES",  0.5),
            ("CP013", "EXT_EASYJET", "COMPETES",  0.5),
            ("EXT_WIZZ_BONDS","CP013","LENDS",    0.9),
        ],
    },

    "CP023": {  # Thames Water
        "nodes": [
            {"id": "EXT_OFWAT",     "name": "Ofwat",             "type": "REGULATOR",   "country": "UK", "note": "PR24 final determination: £3.25bn allowance vs £7.2bn requested — primary trigger"},
            {"id": "EXT_ENV_AGENCY","name": "Environment Agency","type": "REGULATOR",   "country": "UK", "note": "278 sewage spill investigations; enforcement notices; potential criminal referrals"},
            {"id": "EXT_OMERS",     "name": "OMERS (Ontario)",   "type": "SHAREHOLDER", "country": "CA", "note": "31.8% economic stake; written to zero; resisting further equity injection"},
            {"id": "EXT_USS",       "name": "Universities SS",   "type": "SHAREHOLDER", "country": "UK", "note": "20% stake; UK pension fund; political sensitivity high"},
            {"id": "EXT_CPPIB",     "name": "CPP Investments",   "type": "SHAREHOLDER", "country": "CA", "note": "10% stake; Canadian pension; also equity written down"},
            {"id": "EXT_TW_BONDS",  "name": "Class A Bondholders","type":"LENDER",      "country": "UK", "note": "£10.2bn Class A; investment-grade covenant; creditor committee formed"},
            {"id": "EXT_TW_B_BONDS","name": "Class B Bondholders","type":"LENDER",      "country": "UK", "note": "£5.1bn Class B; below investment grade; 40-60p recovery scenarios"},
            {"id": "EXT_UK_GOV",    "name": "UK Government",     "type": "REGULATOR",   "country": "UK", "note": "Special administration fallback; political cost of nationalisation £15bn+"},
            {"id": "CTY_UK",        "name": "United Kingdom",    "type": "COUNTRY",     "country": "UK", "flag": "🇬🇧", "note": "100% UK operations; London and Thames Valley; 16M customers"},
            {"id": "EXT_SEVERN",    "name": "Severn Trent",      "type": "COMPETITOR",  "country": "UK", "note": "Peer water company; better regulatory record; used as pricing benchmark"},
        ],
        "edges": [
            ("EXT_OFWAT",      "CP023", "REGULATES", 1.0),
            ("EXT_ENV_AGENCY", "CP023", "REGULATES", 0.9),
            ("EXT_OMERS",      "CP023", "OWNS",      0.7),
            ("EXT_USS",        "CP023", "OWNS",      0.6),
            ("EXT_CPPIB",      "CP023", "OWNS",      0.5),
            ("EXT_TW_BONDS",   "CP023", "LENDS",     1.0),
            ("EXT_TW_B_BONDS", "CP023", "LENDS",     0.8),
            ("EXT_UK_GOV",     "CP023", "REGULATES", 0.7),
            ("CP023", "CTY_UK",          "OPERATES",  1.0),
            ("CP023", "EXT_SEVERN",      "COMPETES",  0.4),
        ],
    },

    "CP028": {  # Signa
        "nodes": [
            {"id": "EXT_SELFRIDGES","name": "Selfridges Group",  "type": "SUBSIDIARY",  "country": "UK", "note": "50% stake; in administration; sale process ongoing; £4bn+ asset value"},
            {"id": "EXT_KADEWE",    "name": "KaDeWe",            "type": "SUBSIDIARY",  "country": "DE", "note": "Berlin luxury dept store; receiver appointed; Thai Central Group bidding"},
            {"id": "EXT_GALERIA",   "name": "Galeria Karstadt",  "type": "SUBSIDIARY",  "country": "DE", "note": "Insolvency #3 (2024); 92 stores; 17,000 jobs at risk; state aid refused"},
            {"id": "EXT_JULIUS_BAR","name": "Julius Bär",        "type": "LENDER",      "country": "CH", "note": "CHF 606M written off Jan 2024; triggered CEO resignation; reputational damage"},
            {"id": "EXT_DEUBA",     "name": "Deutsche Bank",     "type": "LENDER",      "country": "DE", "note": "~€600M exposure; provisioned; part of creditor committee"},
            {"id": "EXT_COMMERZB",  "name": "Commerzbank",       "type": "LENDER",      "country": "DE", "note": "~€200M exposure; restructuring provision taken"},
            {"id": "EXT_BAYERNLB",  "name": "BayernLB",          "type": "LENDER",      "country": "DE", "note": "~€300M exposure; Bavarian state-owned bank"},
            {"id": "EXT_BENKO",     "name": "René Benko (founder)","type":"SHAREHOLDER","country": "AT", "note": "Arrested Dec 2024; fraud/insolvency investigations; personal bankruptcy filed"},
            {"id": "CTY_AT",        "name": "Austria",           "type": "COUNTRY",     "country": "AT", "flag": "🇦🇹", "note": "Vienna HQ; FMA investigation; insolvency proceedings active"},
            {"id": "CTY_DE",        "name": "Germany",           "type": "COUNTRY",     "country": "DE", "flag": "🇩🇪", "note": "Largest asset base; Galeria + commercial RE portfolio"},
            {"id": "CTY_UK",        "name": "United Kingdom",    "type": "COUNTRY",     "country": "UK", "flag": "🇬🇧", "note": "Selfridges; Oxford Street anchor; UK administration proceedings"},
        ],
        "edges": [
            ("CP028", "EXT_SELFRIDGES","OWNS",     0.8),
            ("CP028", "EXT_KADEWE",    "OWNS",     1.0),
            ("CP028", "EXT_GALERIA",   "OWNS",     1.0),
            ("EXT_JULIUS_BAR","CP028", "LENDS",    0.9),
            ("EXT_DEUBA",     "CP028", "LENDS",    0.9),
            ("EXT_COMMERZB",  "CP028", "LENDS",    0.7),
            ("EXT_BAYERNLB",  "CP028", "LENDS",    0.8),
            ("EXT_BENKO",     "CP028", "OWNS",     0.9),
            ("CP028", "CTY_AT",        "OPERATES", 0.9),
            ("CP028", "CTY_DE",        "OPERATES", 0.9),
            ("CP028", "CTY_UK",        "OPERATES", 0.7),
        ],
    },

    "CP033": {  # Atos SE
        "nodes": [
            {"id": "EXT_EVIDEN",    "name": "Eviden (spun out)", "type": "SUBSIDIARY",  "country": "FR", "note": "Cybersecurity/HPC/digital gov; sold to Onepoint consortium; ring-fenced"},
            {"id": "EXT_TECH_FOUND","name": "Tech Foundations",  "type": "SUBSIDIARY",  "country": "FR", "note": "Legacy IT outsourcing; sold to EP Equity Investment; highly leveraged"},
            {"id": "EXT_FR_GOVT",   "name": "French Government", "type": "CUSTOMER",    "country": "FR", "note": "25%+ of revenue from public sector contracts; nuclear/defense critical"},
            {"id": "EXT_ONEPOINT",  "name": "Onepoint (David Layani)","type":"SHAREHOLDER","country":"FR","note": "Largest single shareholder; creditor + shareholder; complex conflict of interest"},
            {"id": "EXT_ATOS_BONDS","name": "Atos Bondholders",  "type": "LENDER",      "country": "EU", "note": "€2.4bn restructured; 75% equity conversion; residual 25% in new bonds"},
            {"id": "EXT_SOPRA",     "name": "Sopra Steria",      "type": "COMPETITOR",  "country": "FR", "note": "French IT peer; stronger balance sheet; taking Atos contracts"},
            {"id": "EXT_CAPGEMINI", "name": "Capgemini SE",      "type": "COMPETITOR",  "country": "FR", "note": "Larger French IT peer; A-rated; winning displaced Atos government clients"},
            {"id": "CTY_FR",        "name": "France",            "type": "COUNTRY",     "country": "FR", "flag": "🇫🇷", "note": "50%+ of revenue; Bezons HQ; French state strategic asset designation"},
            {"id": "CTY_DE",        "name": "Germany",           "type": "COUNTRY",     "country": "DE", "flag": "🇩🇪", "note": "20% of revenue; major German public sector contracts; Bull brand"},
            {"id": "CTY_UK",        "name": "United Kingdom",    "type": "COUNTRY",     "country": "UK", "flag": "🇬🇧", "note": "10% of revenue; NHS, MoD contracts under review post-restructuring"},
        ],
        "edges": [
            ("CP033", "EXT_EVIDEN",    "OWNS",     0.8),
            ("CP033", "EXT_TECH_FOUND","OWNS",     0.7),
            ("EXT_FR_GOVT",  "CP033",  "CUSTOMER", 0.9),
            ("EXT_ONEPOINT", "CP033",  "OWNS",     0.7),
            ("EXT_ATOS_BONDS","CP033", "LENDS",    0.9),
            ("CP033", "EXT_SOPRA",     "COMPETES", 0.5),
            ("CP033", "EXT_CAPGEMINI", "COMPETES", 0.5),
            ("CP033", "CTY_FR",        "OPERATES", 0.95),
            ("CP033", "CTY_DE",        "OPERATES", 0.7),
            ("CP033", "CTY_UK",        "OPERATES", 0.5),
        ],
    },
}


# ─────────────────────────────────────────────────────────────
# SIGNALS
# Direct signals on each entity + signals on related entities
# sentiment: -1.0 (very negative) → +1.0 (very positive)
# ─────────────────────────────────────────────────────────────

SIGNALS: List[Dict] = [

    # ── VW (CP001) ────────────────────────────────────────
    {
        "id": "S001", "entity_id": "CP001", "direct": True,
        "category": "FINANCIAL_STRESS", "severity": "HIGH", "score": 72,
        "sentiment": -0.72, "source": "Company filing / Moody's",
        "headline": "VW announces 35,000 job cuts and 3 German plant closures",
        "detail": "Unprecedented restructuring: first plant closures in VW's 87-year history. "
                  "€4bn+ annual cost savings targeted. IG3 Works Council opposition likely to delay. "
                  "EV transition burning €15bn/yr capex vs €8bn depreciation — structural cash burn.",
        "observed_at": "2025-01-15",
    },
    {
        "id": "S002", "entity_id": "CP001", "direct": True,
        "category": "RATING_ACTION", "severity": "MEDIUM", "score": 55,
        "sentiment": -0.55, "source": "S&P Rating Action",
        "headline": "S&P places VW on CreditWatch Negative — BBB at risk",
        "detail": "CreditWatch Negative reflects €20bn+ net debt, declining China volumes (-15% YoY), "
                  "and EV transition uncertainty. Downgrade to BBB- would not trigger fallen angel concerns "
                  "as VW retains IG status. Key metric: FCF/debt ratio must stay above 8%.",
        "observed_at": "2025-02-08",
    },
    {
        "id": "S003", "entity_id": "CP001", "direct": True,
        "category": "MARKET_POSITION", "severity": "MEDIUM", "score": 58,
        "sentiment": -0.58, "source": "CAAM / Bloomberg",
        "headline": "China sales -15% YoY; BYD surpasses VW in local market share for first time",
        "detail": "BYD now holds 14.2% China market share vs VW's 13.8%. JV profits declining. "
                  "SAIC-VW and FAW-VW both reducing production. Local EV pricing pressure compressing "
                  "margins on imported ICE models. VW EV ID series priced uncompetitively vs domestic players.",
        "observed_at": "2025-02-20",
    },

    # ── Mercedes (CP003) ─────────────────────────────────
    {
        "id": "S004", "entity_id": "CP003", "direct": True,
        "category": "MARKET_POSITION", "severity": "MEDIUM", "score": 42,
        "sentiment": -0.42, "source": "Company results / analyst",
        "headline": "Mercedes Q3 profit warning: China volume -13%, EV margin pressure",
        "detail": "EBIT margin guidance cut from 12-14% to 10-11% for FY2024. "
                  "China luxury slowdown (24% of global sales) and aggressive local EV pricing "
                  "forcing margin concessions. Premium segment more resilient than volume — A- maintained.",
        "observed_at": "2025-01-22",
    },
    {
        "id": "S005", "entity_id": "CP003", "direct": True,
        "category": "SUPPLIER_RISK", "severity": "LOW", "score": 25,
        "sentiment": -0.25, "source": "Reuters",
        "headline": "Mercedes confirms Aston Martin engine supply dependency; no replacement if AML defaults",
        "detail": "AMG V8/V12 supply contract runs to 2030. If Aston Martin enters administration, "
                  "Mercedes faces reputational damage and potential supply overhang on specialist engines. "
                  "Mitigant: AML volume is <0.5% of AMG production capacity.",
        "observed_at": "2025-02-14",
    },

    # ── Aston Martin (CP005) ──────────────────────────────
    {
        "id": "S006", "entity_id": "CP005", "direct": True,
        "category": "GOING_CONCERN", "severity": "CRITICAL", "score": 92,
        "sentiment": -0.92, "source": "Company annual report",
        "headline": "Aston Martin: going concern material uncertainty clause in FY2024 accounts",
        "detail": "Auditors (KPMG) flagged going concern uncertainty for second consecutive year. "
                  "Cash runway <6 months at current burn rate without rights issue. "
                  "£1.3bn HY bonds trading at 72p/£ (implied yield 15%). Geely backstop rights "
                  "issue at 50% discount to market — highly dilutive.",
        "observed_at": "2025-03-01",
    },
    {
        "id": "S007", "entity_id": "CP005", "direct": True,
        "category": "PRODUCTION", "severity": "HIGH", "score": 78,
        "sentiment": -0.78, "source": "Company trading update",
        "headline": "AML volume guidance cut: 5,800 units FY2025 (vs 7,200 target)",
        "detail": "Production constraints at Gaydon limited by supply chain disruption and "
                  "weak demand in key US market (-22% YoY). DBX707 launch delays. "
                  "Revenue guided £1.35–1.45bn vs £1.7bn target. Management credibility issues.",
        "observed_at": "2025-02-25",
    },

    # ── ZF (CP006) ────────────────────────────────────────
    {
        "id": "S008", "entity_id": "CP006", "direct": True,
        "category": "FINANCIAL_STRESS", "severity": "CRITICAL", "score": 95,
        "sentiment": -0.95, "source": "Reuters / Moody's",
        "headline": "ZF enters covenant waiver discussions with €8bn lending syndicate",
        "detail": "Net debt/EBITDA approaching 5.5x vs 4.5x covenant. WABCO acquisition leverage "
                  "compounded by VW volume cuts (-20% transmission volumes). Moody's on review "
                  "for downgrade from Ba1. Liquidity: €2.4bn RCF drawn 60%. "
                  "10,000 job cut programme announced to reduce cost base by €800M.",
        "observed_at": "2025-01-10",
    },
    {
        "id": "S009", "entity_id": "CP006", "direct": True,
        "category": "CUSTOMER_CONCENTRATION", "severity": "HIGH", "score": 80,
        "sentiment": -0.80, "source": "Company filing",
        "headline": "VW volume cuts removing €900M annual ZF revenue — covenant impact",
        "detail": "VW's production cuts at German plants directly reduce ZF transmission and "
                  "chassis orders. With VW representing ~18% of ZF revenue, the demand shock "
                  "is structural not cyclical. ICE transmission market declining 8% pa as EV "
                  "adoption accelerates — ZF's core product becoming obsolete.",
        "observed_at": "2025-01-18",
    },

    # ── Continental (CP007) ───────────────────────────────
    {
        "id": "S010", "entity_id": "CP007", "direct": True,
        "category": "RATING_RISK", "severity": "MEDIUM", "score": 52,
        "sentiment": -0.52, "source": "Fitch",
        "headline": "Continental BBB- on negative outlook — IG boundary risk",
        "detail": "Fitch revised outlook to Negative reflecting OEM volume pressure and "
                  "automotive segment margin compression. BBB- breach would trigger "
                  "IG index exclusion affecting €6bn+ bond spread. Tyre division FCF "
                  "provides buffer but automotive decline accelerating.",
        "observed_at": "2025-02-01",
    },
    {
        "id": "S011", "entity_id": "CP007", "direct": True,
        "category": "SHAREHOLDER_RISK", "severity": "MEDIUM", "score": 48,
        "sentiment": -0.48, "source": "Bloomberg",
        "headline": "Schaeffler 46% voting stake creates governance risk for Continental",
        "detail": "Schaeffler family controls 46% voting rights. Activist investor pressure "
                  "building for Continental to separate tyres from automotive. Governance discount "
                  "applied by bond markets. Any Schaeffler forced disposal of stake would be "
                  "overhang on Continental equity and signal distress in wider auto supply chain.",
        "observed_at": "2025-02-18",
    },

    # ── Northvolt (CP009) ─────────────────────────────────
    {
        "id": "S012", "entity_id": "CP009", "direct": True,
        "category": "DEFAULT", "severity": "CRITICAL", "score": 98,
        "sentiment": -0.98, "source": "US Bankruptcy Court / FT",
        "headline": "Northvolt files Chapter 11 — BMW and VW contracts terminated",
        "detail": "Chapter 11 filed in Delaware Nov 2024 after burning $15bn. BMW cancelled "
                  "€2bn battery contract; VW wrote down €800M investment. Skellefteå factory "
                  "yield rates reached only 35% of target. Swedish government emergency "
                  "support SEK 9.5bn — political liability. 5,000 employees affected.",
        "observed_at": "2024-11-22",
    },
    {
        "id": "S013", "entity_id": "CP009", "direct": True,
        "category": "RECOVERY", "severity": "HIGH", "score": 85,
        "sentiment": -0.85, "source": "Reuters",
        "headline": "Northvolt asset sale: Skellefteå factory valued at 15–25p/£ — recovery bleak",
        "detail": "Skellefteå gigafactory estimated €500–800M recovery value vs €4bn book. "
                  "CATL and Samsung SDI cited as potential buyers at distressed valuation. "
                  "IP value limited by failed manufacturing process. "
                  "EIB €350M green loan: EU political embarrassment.",
        "observed_at": "2025-01-08",
    },

    # ── Wizz Air (CP013) ──────────────────────────────────
    {
        "id": "S014", "entity_id": "CP013", "direct": True,
        "category": "OPERATIONAL_STRESS", "severity": "HIGH", "score": 78,
        "sentiment": -0.78, "source": "Company trading statement",
        "headline": "Wizz Air: 50 aircraft grounded by P&W GTF inspections — €350M EBITDA impact",
        "detail": "Pratt & Whitney GTF powder metal contamination: up to 50 Wizz aircraft "
                  "requiring engine inspections. Wet lease replacement: $1.8M/aircraft/month. "
                  "FY2025 EBITDA guidance cut from €600M to €250–300M. "
                  "November 2026 bond €500M maturity — refinancing risk high if EBITDA doesn't recover.",
        "observed_at": "2025-01-12",
    },
    {
        "id": "S015", "entity_id": "CP013", "direct": True,
        "category": "COUNTRY_RISK", "severity": "MEDIUM", "score": 55,
        "sentiment": -0.55, "source": "FT / Bloomberg",
        "headline": "Wizz Air Hungary operations: HUF -22% YTD; Orban policy risk increasing",
        "detail": "Hungarian forint weakness adds €40M FX cost on EUR-denominated fleet leases. "
                  "Orban government's alignment with Russia creates secondary sanctions risk "
                  "for cross-border operations. Hungary blocking Ukraine aid: "
                  "further EU tension could impact operating permits.",
        "observed_at": "2025-02-05",
    },

    # ── Thames Water (CP023) ──────────────────────────────
    {
        "id": "S016", "entity_id": "CP023", "direct": True,
        "category": "REGULATORY_ACTION", "severity": "CRITICAL", "score": 90,
        "sentiment": -0.90, "source": "Ofwat Final Determination",
        "headline": "Ofwat PR24 determination: £3.25bn allowed vs £7.2bn requested — equity crisis",
        "detail": "Ofwat's final determination for 2025-2030 period grants only 45% of capital "
                  "investment requested by Thames Water. Equity holders concluded injecting "
                  "new capital is not viable at this determination. "
                  "Government special administration now probability >40%. "
                  "Class A bonds trading 85p/£; Class B at 45p/£.",
        "observed_at": "2024-12-19",
    },
    {
        "id": "S017", "entity_id": "CP023", "direct": True,
        "category": "GOING_CONCERN", "severity": "CRITICAL", "score": 88,
        "sentiment": -0.88, "source": "Company / Parliament",
        "headline": "Thames Water: equity written to zero; £18.3bn debt unsustainable",
        "detail": "All shareholders have written equity to zero. New equity injection "
                  "requires Ofwat regulatory reset — circular dependency. "
                  "Parliamentary hearing: CEO/CFO resigned; interim management. "
                  "£5bn bridging loan being negotiated with Class A bondholders. "
                  "Timeline to resolution: 12-18 months before cash exhaustion.",
        "observed_at": "2025-01-25",
    },
    {
        "id": "S018", "entity_id": "CP023", "direct": True,
        "category": "LEGAL_REGULATORY", "severity": "HIGH", "score": 75,
        "sentiment": -0.75, "source": "Environment Agency",
        "headline": "278 sewage spill investigations; criminal referral risk; EA enforcement action",
        "detail": "Environment Agency escalated 278 investigations into illegal sewage spills. "
                  "Material risk of criminal prosecution of directors. Fines could reach £500M+. "
                  "Parliamentary committee: 'worst regulated company in the UK'. "
                  "Operational licence at risk in extreme scenario.",
        "observed_at": "2025-02-12",
    },

    # ── Signa (CP028) ─────────────────────────────────────
    {
        "id": "S019", "entity_id": "CP028", "direct": True,
        "category": "DEFAULT", "severity": "CRITICAL", "score": 100,
        "sentiment": -1.00, "source": "Insolvency administrator",
        "headline": "Signa insolvency: €23bn liabilities; Julius Bär CHF 606M loss",
        "detail": "Largest corporate insolvency in German-speaking Europe confirmed Nov 2023. "
                  "René Benko arrested Dec 2024 on fraud charges. "
                  "Julius Bär CEO resignation; stock down 22% on announcement. "
                  "Deutsche Bank: ~€600M exposure provisioned. "
                  "KaDeWe: Thai Central Group winning bidder at €700M vs €1.5bn book.",
        "observed_at": "2023-11-29",
    },
    {
        "id": "S020", "entity_id": "CP028", "direct": True,
        "category": "RECOVERY_RISK", "severity": "CRITICAL", "score": 95,
        "sentiment": -0.95, "source": "Insolvency administrator",
        "headline": "Signa recovery: 30–60p/£ on secured; unsecured near-zero",
        "detail": "Insolvency administrator confirms secured creditor recovery 30-60p/£. "
                  "Selfridges sale: Thai Central Group / Qatar Investment Authority at £3.2bn "
                  "vs £4bn book. Galeria Karstadt: state rejected rescue; 92 stores closing. "
                  "Unsecured creditors (€5bn+) expected 5-15p/£ recovery.",
        "observed_at": "2024-06-15",
    },

    # ── Atos (CP033) ──────────────────────────────────────
    {
        "id": "S021", "entity_id": "CP033", "direct": True,
        "category": "RESTRUCTURING", "severity": "HIGH", "score": 82,
        "sentiment": -0.82, "source": "Atos / French courts",
        "headline": "Atos €5bn debt restructuring: 75% equity conversion; new bonds distressed",
        "detail": "Safeguard procedure (French equivalent of Ch.11) completed mid-2024. "
                  "€2.4bn debt converted to 75% equity for bondholders; 25% in new 8% PIK bonds. "
                  "Onepoint (founder's vehicle) becomes largest shareholder with conflicted interests. "
                  "Tech Foundations sold to EP Equity; Eviden ring-fenced. "
                  "Ongoing contract cancellation risk from government clients.",
        "observed_at": "2024-08-10",
    },
    {
        "id": "S022", "entity_id": "CP033", "direct": True,
        "category": "REVENUE_RISK", "severity": "HIGH", "score": 74,
        "sentiment": -0.74, "source": "French Ministry of Defence",
        "headline": "French government reviewing Atos defense/nuclear contracts post-restructuring",
        "detail": "Atos holds critical contracts: French nuclear deterrent IT, French MoD, OTAN. "
                  "Post-restructuring ownership uncertainty triggering government review. "
                  "Capgemini and Sopra Steria positioned to take displaced contracts. "
                  "Revenue from French public sector: 25%+ of total — loss would be existential.",
        "observed_at": "2025-01-30",
    },

    # ── RELATED ENTITY SIGNALS (affect portfolio CPs via network) ──

    # Pratt & Whitney GTF — affects Wizz Air
    {
        "id": "S023", "entity_id": None, "related_entity": "EXT_PW",
        "affects": ["CP013"], "relationship": "SUPPLIER", "direct": False,
        "category": "PRODUCT_DEFECT", "severity": "CRITICAL", "score": 88,
        "sentiment": -0.88, "source": "FAA / Pratt & Whitney",
        "headline": "P&W GTF powder metal contamination: 600+ aircraft affected globally",
        "detail": "FAA Airworthiness Directive: all GTF engines require accelerated inspection. "
                  "600+ aircraft grounded globally across IndiGo, Wizz, Spirit. "
                  "P&W/RTX reserving $3bn+ for compensatory payments to airlines. "
                  "Wizz Air highest proportional exposure in Europe.",
        "observed_at": "2024-10-05",
    },

    # Ofwat final determination — affects Thames Water
    {
        "id": "S024", "entity_id": None, "related_entity": "EXT_OFWAT",
        "affects": ["CP023"], "relationship": "REGULATOR", "direct": False,
        "category": "REGULATORY_CHANGE", "severity": "CRITICAL", "score": 85,
        "sentiment": -0.85, "source": "Ofwat",
        "headline": "Ofwat final determination: sector-wide capex cut; Thames worst affected",
        "detail": "Ofwat PR24 final determination grants 55% of industry capex requests. "
                  "Thames Water receives lowest allowance relative to need. "
                  "Severn Trent and United Utilities better positioned. "
                  "Signals systemic underfunding of UK water infrastructure.",
        "observed_at": "2024-12-19",
    },

    # VW plant closures — affect ZF, Continental (OEM customers)
    {
        "id": "S025", "entity_id": None, "related_entity": "CP001",
        "affects": ["CP006", "CP007"], "relationship": "CUSTOMER", "direct": False,
        "category": "VOLUME_SHOCK", "severity": "HIGH", "score": 72,
        "sentiment": -0.72, "source": "Reuters",
        "headline": "VW plant closures cut Tier-1 supplier orders by €2bn+",
        "detail": "Three German plant closures eliminate 300,000 annual production units. "
                  "ZF and Continental are primary Tier-1 impact: combined order loss estimated "
                  "€2.1bn/yr. Accelerates covenant pressure at ZF. Continental automotive "
                  "margin compression worsens. Tyre division less affected.",
        "observed_at": "2025-01-16",
    },

    # BMW Northvolt contract cancellation — confirm Northvolt distress
    {
        "id": "S026", "entity_id": None, "related_entity": "EXT_BMW",
        "affects": ["CP009"], "relationship": "CUSTOMER", "direct": False,
        "category": "CONTRACT_TERMINATION", "severity": "CRITICAL", "score": 92,
        "sentiment": -0.92, "source": "BMW Group",
        "headline": "BMW cancels €2bn Northvolt battery contract — Chapter 11 trigger",
        "detail": "BMW's cancellation following repeated quality failures was the proximate "
                  "trigger for Northvolt's Chapter 11 filing. Yield rates at Skellefteå "
                  "remained at 35% of contractual specification after 18 months of ramp. "
                  "BMW now sourcing exclusively from CATL and Samsung SDI.",
        "observed_at": "2024-11-15",
    },

    # Julius Bär Signa loss — context on Signa recovery
    {
        "id": "S027", "entity_id": None, "related_entity": "EXT_JULIUS_BAR",
        "affects": ["CP028"], "relationship": "LENDER", "direct": False,
        "category": "LENDER_DISTRESS", "severity": "HIGH", "score": 80,
        "sentiment": -0.80, "source": "Julius Bär",
        "headline": "Julius Bär CHF 606M Signa write-off triggers CEO resignation",
        "detail": "Julius Bär's largest ever single credit loss. Provision of CHF 606M "
                  "against €600M+ Signa exposure. CEO Philipp Rickenbacher resigned Jan 2024. "
                  "Stock down 22% on day of announcement. FINMA investigation into governance "
                  "of lending process. Signals poor institutional credit oversight.",
        "observed_at": "2024-01-22",
    },

    # Aston Martin engine dependency on Mercedes — amplifier
    {
        "id": "S028", "entity_id": None, "related_entity": "EXT_AMG",
        "affects": ["CP005"], "relationship": "SUPPLIER", "direct": False,
        "category": "SUPPLY_DEPENDENCY", "severity": "HIGH", "score": 70,
        "sentiment": -0.70, "source": "Analyst / AML filings",
        "headline": "Aston Martin 100% dependent on Mercedes-AMG engines — no alternative",
        "detail": "All current AML models (DB12, Vantage, DBX707) use AMG V8/V12 powertrains. "
                  "No in-house engine capability. Contract runs to 2030 with renewal clauses. "
                  "If AML enters administration, engine supply would continue only under "
                  "special arrangement — suppliers uncertain.",
        "observed_at": "2025-02-10",
    },

    # ──────────────────────────────────────────────────────────────────────────
    # MARKET-PRICE SIGNALS  (Yahoo Finance / Markit / Bloomberg)
    # ──────────────────────────────────────────────────────────────────────────

    # VW — CDS spread widening
    {
        "id": "S029", "entity_id": "CP001", "direct": True,
        "signal_type": "CDS",
        "category": "MARKET_PRICE", "severity": "HIGH", "score": 68,
        "sentiment": -0.68, "source": "Markit CDS / Bloomberg",
        "headline": "VW 5yr CDS widens 45bps to 185bps — highest since 2020",
        "detail": "VW AG 5-year CDS spread: 185bps vs 140bps 30 days prior (+45bps). "
                  "Spread widening driven by restructuring announcement and CreditWatch Negative. "
                  "Market implied probability of default over 5yr ≈ 8.5%. "
                  "Basis vs iTraxx Europe Main: +110bps (sector premium elevated).",
        "observed_at": "2025-02-10",
    },
    # VW — equity price
    {
        "id": "S030", "entity_id": "CP001", "direct": True,
        "signal_type": "EQUITY",
        "category": "MARKET_PRICE", "severity": "MEDIUM", "score": 55,
        "sentiment": -0.55, "source": "Yahoo Finance (VOW3.DE)",
        "headline": "VW ordinary shares −28% YTD; market cap below €40bn for first time since 2012",
        "detail": "VOW3.DE: €89.20 vs €123.50 at Jan 1 (−28% YTD). "
                  "Volume surge on plant closure announcement: 3× ADV. "
                  "P/E compressed to 3.2×  — market pricing restructuring failure. "
                  "Porsche SE (31.9% shareholder) NAV discount widening to 40%.",
        "observed_at": "2025-02-28",
    },

    # Continental — CDS
    {
        "id": "S031", "entity_id": "CP007", "direct": True,
        "signal_type": "CDS",
        "category": "MARKET_PRICE", "severity": "MEDIUM", "score": 50,
        "sentiment": -0.50, "source": "Markit CDS / Bloomberg",
        "headline": "Continental 5yr CDS at 165bps — tracking VW auto sector contagion",
        "detail": "CON.DE CDS: 165bps (+30bps in 30 days). Tighter than ZF (private, no CDS) "
                  "but widening faster than peers. IG/HY differential: if downgraded to BB+, "
                  "forced sellers across €6bn+ IG bond ETFs. Bond spread: +220bps vs Bund.",
        "observed_at": "2025-02-12",
    },
    # Continental — equity
    {
        "id": "S032", "entity_id": "CP007", "direct": True,
        "signal_type": "EQUITY",
        "category": "MARKET_PRICE", "severity": "MEDIUM", "score": 46,
        "sentiment": -0.46, "source": "Yahoo Finance (CON.DE)",
        "headline": "Continental equity −22% YTD; Schaeffler stake worth €3.8bn vs €5bn peak",
        "detail": "CON.DE: €52.10 vs €66.80 on Jan 1. Options market: elevated put-call ratio 1.8× "
                  "(bearish positioning). Short interest: 4.2% of float (rising). "
                  "Schaeffler's 46% stake paper loss: €1.3bn YTD — increasing forced-sale risk.",
        "observed_at": "2025-02-28",
    },

    # Thames Water — bond price signal
    {
        "id": "S033", "entity_id": "CP023", "direct": True,
        "signal_type": "BOND",
        "category": "MARKET_PRICE", "severity": "CRITICAL", "score": 88,
        "sentiment": -0.88, "source": "Bloomberg Bond Monitor",
        "headline": "Thames Water Class B bonds at 43p/£ — implied loss >55%; Class A at 82p",
        "detail": "TW Class B sub bonds: 43p/£ (yield 22.4%) — market pricing near-total loss. "
                  "TW Class A: 82p/£ (yield 9.1%) — distressed but ring-fenced OpCo structure. "
                  "CDS equivalent (synthetic): 1,850bps — deep distress zone. "
                  "Compared to peers: Severn Trent bonds at 98p/£ (A- rated, normal).",
        "observed_at": "2025-03-01",
    },

    # Aston Martin — bond price / HY signal
    {
        "id": "S034", "entity_id": "CP005", "direct": True,
        "signal_type": "BOND",
        "category": "MARKET_PRICE", "severity": "HIGH", "score": 80,
        "sentiment": -0.80, "source": "Bloomberg / ICE BofA HY Index",
        "headline": "AML 10.5% 2029 bonds at 71p/£ — yield 18.9%; distress territory",
        "detail": "Aston Martin Lagonda 10.5% Senior Secured 2029: 71p/£ (yield 18.9%). "
                  "ICE BofA distressed threshold: >1000bps over UST. AML spread: 1,410bps. "
                  "Rights issue dilution premium: equity at 50p vs 180p 12 months prior. "
                  "Geely backstop letter filed but terms not binding — bond market pricing failure.",
        "observed_at": "2025-02-28",
    },

    # Mercedes — equity (relative outperformer signal — positive)
    {
        "id": "S035", "entity_id": "CP003", "direct": True,
        "signal_type": "EQUITY",
        "category": "MARKET_PRICE", "severity": "LOW", "score": 22,
        "sentiment": +0.22, "source": "Yahoo Finance (MBG.DE)",
        "headline": "Mercedes outperforms auto sector by 14% YTD; dividend yield 8.5% supports floor",
        "detail": "MBG.DE −8% YTD vs auto sector −22%. Dividend yield 8.5% attracting value buyers. "
                  "FCF yield 12% — strong cash generation vs peers. Options: put-call ratio 0.7× "
                  "(relatively balanced). Short interest: 1.8% of float (low vs sector average 3.5%).",
        "observed_at": "2025-03-01",
    },

    # ──────────────────────────────────────────────────────────────────────────
    # NEWS NLP & SENTIMENT SIGNALS  (RavenPack / Reuters / FT NLP)
    # ──────────────────────────────────────────────────────────────────────────

    {
        "id": "S036", "entity_id": "CP001", "direct": True,
        "signal_type": "NEWS_NLP",
        "category": "MEDIA_SENTIMENT", "severity": "HIGH", "score": 65,
        "sentiment": -0.65, "source": "RavenPack News Analytics",
        "headline": "VW news sentiment score: −0.62 (30-day avg) — most negative in European auto sector",
        "detail": "RavenPack Entity Sentiment Score (ESS): −0.62 vs sector avg −0.18. "
                  "Article volume +340% vs 90-day avg — driven by plant closure, job cut, and "
                  "IG3 union stories. Negative tone: 78% of articles. Key themes: "
                  "'restructuring' (34%), 'job cuts' (28%), 'China' (22%), 'EV transition' (16%).",
        "observed_at": "2025-02-28",
    },
    {
        "id": "S037", "entity_id": "CP023", "direct": True,
        "signal_type": "NEWS_NLP",
        "category": "MEDIA_SENTIMENT", "severity": "CRITICAL", "score": 86,
        "sentiment": -0.86, "source": "RavenPack / Refinitiv News Sentiment",
        "headline": "Thames Water media sentiment: worst in FTSE 350 for 3rd consecutive month",
        "detail": "Refinitiv News Sentiment Index (NSI): −0.84 (range −1 to +1). "
                  "Article volume: 2,400 articles/month vs 180 baseline. "
                  "Parliamentary committee coverage: 100% negative tone. "
                  "Consumer complaint articles: +520% YoY. ESG/environmental breach coverage "
                  "generating governance discount in bond pricing.",
        "observed_at": "2025-03-01",
    },
    {
        "id": "S038", "entity_id": "CP013", "direct": True,
        "signal_type": "NEWS_NLP",
        "category": "MEDIA_SENTIMENT", "severity": "MEDIUM", "score": 54,
        "sentiment": -0.54, "source": "Reuters NLP / RavenPack",
        "headline": "Wizz Air passenger complaint volume +180% YoY — reputational signal",
        "detail": "Wizz Air mentions in consumer complaint outlets (TrustPilot, CAA reports): "
                  "+180% YoY. Driven by GTF groundings causing flight cancellations. "
                  "CAA enforcement action threatened. ESS from Reuters: −0.51 vs −0.12 easyJet. "
                  "Net Promoter Score (NPS) -42 — worst among European LCCs.",
        "observed_at": "2025-02-20",
    },

    # ──────────────────────────────────────────────────────────────────────────
    # SOCIAL MEDIA & ALTERNATIVE SIGNALS  (Twitter/X, LinkedIn, Glassdoor)
    # ──────────────────────────────────────────────────────────────────────────

    {
        "id": "S039", "entity_id": "CP001", "direct": True,
        "signal_type": "SOCIAL_MEDIA",
        "category": "EMPLOYEE_SENTIMENT", "severity": "MEDIUM", "score": 48,
        "sentiment": -0.48, "source": "LinkedIn / Glassdoor",
        "headline": "VW Glassdoor rating drops to 3.1/5 — employee sentiment at decade low",
        "detail": "VW Glassdoor: 3.1/5 (was 3.8/5 12M ago). CEO approval: 34% (was 61%). "
                  "LinkedIn: Job postings −55% YoY (leading indicator of hiring freeze). "
                  "Key themes in reviews: 'uncertainty', 'job cuts', 'lack of direction'. "
                  "German works council (IG Metall) social activity: 3× volume — organised opposition.",
        "observed_at": "2025-02-25",
    },
    {
        "id": "S040", "entity_id": "CP023", "direct": True,
        "signal_type": "SOCIAL_MEDIA",
        "category": "CONSUMER_SENTIMENT", "severity": "HIGH", "score": 72,
        "sentiment": -0.72, "source": "Twitter/X API / Consumer sentiment",
        "headline": "Thames Water #thameswater trending: 850K mentions in 30 days; 91% negative",
        "detail": "Twitter/X: 850K mentions in March 2025 (vs 25K baseline). "
                  "Viral sewage spill videos: 40M+ combined views. "
                  "Government petition for nationalisation: 2.1M signatures. "
                  "Negative mention ratio: 91%. Key hashtags: #sewagescandal #thameswater. "
                  "Ofwat formal inquiry directly referenced in social campaign.",
        "observed_at": "2025-03-01",
    },
    {
        "id": "S041", "entity_id": "CP033", "direct": True,
        "signal_type": "SOCIAL_MEDIA",
        "category": "EMPLOYEE_SENTIMENT", "severity": "HIGH", "score": 70,
        "sentiment": -0.70, "source": "LinkedIn / Glassdoor",
        "headline": "Atos LinkedIn departures: 800+ senior staff left in 90 days post-restructuring",
        "detail": "LinkedIn job change announcements: 800+ Atos employees departing in 90 days. "
                  "Majority: senior engineers and technical architects. "
                  "Government contract risk elevated — deep institutional knowledge leaving. "
                  "Glassdoor: 2.7/5 (was 3.4/5). Recruitment: offers declined rate +40% — "
                  "talent retention crisis compounding contract delivery risk.",
        "observed_at": "2025-02-28",
    },

    # ──────────────────────────────────────────────────────────────────────────
    # MACRO & SECTOR SIGNALS  (ECB / ONS / Eurostat / Bloomberg Economics)
    # ──────────────────────────────────────────────────────────────────────────

    {
        "id": "S042", "entity_id": None, "related_entity": "CTY_DE",
        "affects": ["CP001", "CP003", "CP006", "CP007"], "relationship": "OPERATES",
        "direct": False, "signal_type": "MACRO",
        "category": "MACRO_DATA", "severity": "MEDIUM", "score": 55,
        "sentiment": -0.55, "source": "Eurostat / Destatis",
        "headline": "Germany PMI Manufacturing: 42.5 (11th consecutive sub-50 month) — recession confirmed",
        "detail": "German Manufacturing PMI February 2025: 42.5 (consensus 43.2). "
                  "11 consecutive months below 50 — longest streak since 2002. "
                  "Industrial production −4.2% YoY. Auto sector component: 38.1 — deep contraction. "
                  "GDP Q4 2024: −0.3% (second consecutive negative quarter). "
                  "Direct exposure for VW/ZF/Continental: domestic market demand deterioration.",
        "observed_at": "2025-03-03",
    },
    {
        "id": "S043", "entity_id": None, "related_entity": "CTY_CN",
        "affects": ["CP001", "CP003"], "relationship": "OPERATES",
        "direct": False, "signal_type": "MACRO",
        "category": "MACRO_DATA", "severity": "HIGH", "score": 70,
        "sentiment": -0.70, "source": "CAAM / Bloomberg Economics",
        "headline": "China auto market: BEV penetration 42%; foreign OEM share collapses to 38%",
        "detail": "CAAM Feb 2025 data: BEV market share 42% of new car sales. "
                  "Foreign OEM collective market share: 38% (was 58% in 2021). "
                  "VW China market share: 13.8% (was 19.3% in 2020). "
                  "Mercedes China revenue −13% YoY despite luxury premium. "
                  "BYD, SAIC-GM-Wuling, Li Auto taking structural market share — not cyclical.",
        "observed_at": "2025-03-02",
    },
    {
        "id": "S044", "entity_id": None, "related_entity": "CTY_UK",
        "affects": ["CP023", "CP005"], "relationship": "OPERATES",
        "direct": False, "signal_type": "MACRO",
        "category": "MACRO_DATA", "severity": "MEDIUM", "score": 42,
        "sentiment": -0.42, "source": "ONS / Bank of England",
        "headline": "UK water sector: Ofwat estimates £96bn infrastructure gap over 25 years",
        "detail": "Ofwat State of the Sector report: £96bn investment gap in UK water infrastructure. "
                  "All 10 regulated water companies rated 'requires improvement' or below. "
                  "BoE systemic risk assessment: water sector flagged as potential financial stability concern. "
                  "ONS: UK consumer water bill set to rise 26% in 2025 — political pressure increasing.",
        "observed_at": "2025-02-15",
    },

    # ──────────────────────────────────────────────────────────────────────────
    # ALTERNATIVE DATA — Satellite / Shipping / Web Traffic
    # ──────────────────────────────────────────────────────────────────────────

    {
        "id": "S045", "entity_id": "CP001", "direct": True,
        "signal_type": "ALT_DATA",
        "category": "OPERATIONAL", "severity": "MEDIUM", "score": 52,
        "sentiment": -0.52, "source": "Orbital Insight (satellite imagery)",
        "headline": "VW Wolfsburg factory parking: occupancy −35% vs prior year — production below plan",
        "detail": "Orbital Insight satellite analysis of VW Wolfsburg factory complex: "
                  "car park occupancy 65% of normal (daily avg). Consistent with 30-35% production cut. "
                  "Finished vehicle storage lots: +18% vs seasonal norm — inventory build. "
                  "Emden export port: VW car loading vessels down 2 per week vs baseline.",
        "observed_at": "2025-02-22",
    },
    {
        "id": "S046", "entity_id": "CP013", "direct": True,
        "signal_type": "ALT_DATA",
        "category": "OPERATIONAL", "severity": "MEDIUM", "score": 50,
        "sentiment": -0.50, "source": "FlightAware / ADS-B data",
        "headline": "Wizz Air utilisation: 71% (vs 89% LY) — 52 aircraft confirmed grounded",
        "detail": "ADS-B/FlightAware fleet tracking: 52 Wizz aircraft showing no movement >30 days. "
                  "Fleet utilisation: 71% of scheduled rotations operated (vs 89% prior year). "
                  "Budapest base worst affected: 12 aircraft grounded (30% of hub fleet). "
                  "Revenue impact: ~€350M annualised at €18K/day/aircraft wet lease cost.",
        "observed_at": "2025-03-01",
    },
    {
        "id": "S047", "entity_id": "CP023", "direct": True,
        "signal_type": "ALT_DATA",
        "category": "ESG_ENVIRONMENTAL", "severity": "HIGH", "score": 76,
        "sentiment": -0.76, "source": "Environment Agency / Surfers Against Sewage",
        "headline": "Thames Water sewage sensor data: 2,847 spill-hours in Q1 2025 — EA referral imminent",
        "detail": "EA real-time overflow sensor network: Thames Water 2,847 hours of combined "
                  "sewer overflow (CSO) events in Q1 2025. Regulatory threshold: 600 hours/quarter. "
                  "4.75× breach of operating licence limits. Surfers Against Sewage Sewage Map "
                  "confirms 147 river/coastal locations affected. Criminal referral threshold met.",
        "observed_at": "2025-03-10",
    },
]


# ─────────────────────────────────────────────────────────────
# COMPUTED SCORES
# ─────────────────────────────────────────────────────────────

# ── Category-level financial impact weights ───────────────────────────────────
# Tuple: (score_multiplier, revenue_frac, cost_frac, growth_frac)
# revenue_frac = proportion of signal impact hitting P&L / earnings
# cost_frac    = proportion hitting provisions / credit losses / OpEx
# growth_frac  = proportion hitting forward growth / market position
_CAT_W: Dict[str, tuple] = {
    # Existential events — highest multiplier, all dimensions affected
    "DEFAULT":               (2.0, 0.25, 0.55, 0.20),
    "GOING_CONCERN":         (1.9, 0.20, 0.50, 0.30),
    "RECOVERY_RISK":         (1.8, 0.30, 0.50, 0.20),
    # Balance sheet / restructuring
    "FINANCIAL_STRESS":      (1.6, 0.50, 0.40, 0.10),
    "RESTRUCTURING":         (1.5, 0.40, 0.40, 0.20),
    "LENDER_DISTRESS":       (1.4, 0.10, 0.70, 0.20),
    # Rating / capital cost
    "RATING_ACTION":         (1.3, 0.20, 0.60, 0.20),
    "RATING_RISK":           (1.2, 0.20, 0.60, 0.20),
    # Regulatory / legal
    "REGULATORY_ACTION":     (1.3, 0.10, 0.60, 0.30),
    "REGULATORY_CHANGE":     (1.2, 0.10, 0.50, 0.40),
    "LEGAL_REGULATORY":      (1.3, 0.10, 0.60, 0.30),
    "PRODUCT_DEFECT":        (1.2, 0.30, 0.50, 0.20),
    # Revenue / customer loss
    "CONTRACT_TERMINATION":  (1.5, 0.70, 0.20, 0.10),
    "REVENUE_RISK":          (1.3, 0.70, 0.20, 0.10),
    "CUSTOMER_CONCENTRATION":(1.2, 0.60, 0.10, 0.30),
    "VOLUME_SHOCK":          (1.3, 0.60, 0.30, 0.10),
    # Cost / supply chain
    "SUPPLIER_RISK":         (1.1, 0.10, 0.70, 0.20),
    "SUPPLY_DEPENDENCY":     (1.2, 0.10, 0.70, 0.20),
    "OPERATIONAL_STRESS":    (1.2, 0.20, 0.60, 0.20),
    "PRODUCTION":            (1.1, 0.20, 0.70, 0.10),
    # Market / macro
    "MARKET_POSITION":       (1.0, 0.20, 0.10, 0.70),
    "MARKET_PRICE":          (1.1, 0.40, 0.20, 0.40),
    "COUNTRY_RISK":          (1.1, 0.20, 0.20, 0.60),
    "SHAREHOLDER_RISK":      (0.9, 0.10, 0.10, 0.80),
    "RECOVERY":              (1.0, 0.50, 0.30, 0.20),
}
_CAT_W_DEFAULT = (1.0, 0.33, 0.34, 0.33)


def _weighted_signal_score(items: List[tuple]) -> tuple:
    """
    items: list of (raw_score, category)
    Returns (agg_score, rev_impact, cost_impact, growth_impact)

    Method:
    1. Multiply each signal score by its category multiplier
    2. Rank descending; apply exponential decay (0.80^rank) so top signal
       dominates but subsequent signals still contribute
    3. Weighted-average the adjusted scores and impact fractions
    4. Apply mild logistic sharpening around 50 to create an S-curve
    """
    if not items:
        return 0.0, 0.0, 0.0, 0.0

    DECAY = 0.80
    adjusted = []
    for raw, cat in items:
        mult, rev_f, cost_f, grow_f = _CAT_W.get(cat, _CAT_W_DEFAULT)
        adjusted.append((raw * mult, rev_f, cost_f, grow_f))
    adjusted.sort(key=lambda x: -x[0])

    total_w = total_s = rev_t = cost_t = grow_t = 0.0
    for i, (adj, rev_f, cost_f, grow_f) in enumerate(adjusted):
        w = DECAY ** i
        total_w  += w
        total_s  += w * adj
        rev_t    += w * adj * rev_f
        cost_t   += w * adj * cost_f
        grow_t   += w * adj * grow_f

    raw_avg = total_s / total_w if total_w else 0.0
    # Logistic sharpening: mild S-curve, leaves 0 and 100 unchanged
    sharpened = raw_avg * (1 + 0.004 * (raw_avg - 50))
    agg   = min(100.0, max(0.0, sharpened))
    rev   = min(100.0, rev_t  / total_w) if total_w else 0.0
    cost  = min(100.0, cost_t / total_w) if total_w else 0.0
    grow  = min(100.0, grow_t / total_w) if total_w else 0.0
    return agg, rev, cost, grow


def compute_scores() -> Dict[str, Dict]:
    """
    ML-inspired risk scoring with financial impact decomposition.

    Improvements over simple mean:
    - Category multipliers weight signals by financial materiality
    - Exponential decay across ranked signals (top signal dominates)
    - Logistic S-curve on final composite for more decisive RAG assignment
    - Decomposed into Revenue / Cost / Growth impact channels
    - Confidence score based on signal coverage
    """
    scores = {}

    direct:  Dict[str, List[tuple]] = {eid: [] for eid in ENTITIES}
    related: Dict[str, List[tuple]] = {eid: [] for eid in ENTITIES}

    for sig in SIGNALS:
        cat = sig.get("category", "")
        if sig["direct"] and sig["entity_id"] in direct:
            direct[sig["entity_id"]].append((sig["score"], cat))
        elif not sig["direct"] and sig.get("affects"):
            for eid in sig["affects"]:
                if eid in related:
                    # Network hop: discount score by 50 %
                    related[eid].append((sig["score"] * 0.50, cat))

    for eid, entity in ENTITIES.items():
        own,  own_rev,  own_cost,  own_grow  = _weighted_signal_score(direct.get(eid, []))
        prop, prop_rev, prop_cost, prop_grow = _weighted_signal_score(related.get(eid, []))

        # Composite: own-score dominant (65 %), network propagation (35 %)
        linear    = own * 0.65 + prop * 0.35
        composite = min(100.0, max(0.0, linear * (1 + 0.004 * (linear - 50))))

        # Impact decomposition
        rev_impact  = round(own_rev  * 0.70 + prop_rev  * 0.30, 1)
        cost_impact = round(own_cost * 0.70 + prop_cost * 0.30, 1)
        grow_impact = round(own_grow * 0.60 + prop_grow * 0.40, 1)

        # Confidence: rises with signal count, capped at 95 %
        n_sigs     = len(direct.get(eid, [])) + len(related.get(eid, []))
        confidence = round(min(0.95, 0.35 + n_sigs * 0.07), 2)

        sents = [s["sentiment"] for s in SIGNALS if s["direct"] and s["entity_id"] == eid]
        sentiment = sum(sents) / len(sents) if sents else 0.0

        rating = entity["rating"]
        rag    = "RED" if composite >= 70 else "AMBER" if composite >= 30 else "GREEN"

        scores[eid] = {
            "entity_id":   eid,
            "name":        entity["name"],
            "own_score":   round(own, 1),
            "prop_score":  round(prop, 1),
            "composite":   round(composite, 1),
            "sentiment":   round(sentiment, 3),
            "rag":         rag,
            "rating":      rating,
            "ead_m":       entity["ead_m"],
            "ecl_m":       round(entity["ead_m"] * entity.get("lgd", 0.45) * _pd(rating), 2),
            "rev_impact":  rev_impact,
            "cost_impact": cost_impact,
            "grow_impact": grow_impact,
            "confidence":  confidence,
        }

    return scores


def _pd(rating: str) -> float:
    """Approximate 1yr PD from credit rating."""
    return {
        "AAA": 0.0001, "AA+": 0.0002, "AA": 0.0003, "AA-": 0.0004,
        "A+":  0.0005, "A":  0.0008, "A-": 0.0012,
        "BBB+":0.0020, "BBB":0.0035, "BBB-":0.0060,
        "BB+": 0.0100, "BB": 0.0160, "BB-": 0.0250,
        "B+":  0.0400, "B":  0.0650, "B-": 0.1000,
        "CCC": 0.2000, "CC": 0.3500, "C":  0.5000, "D": 1.0000,
    }.get(rating, 0.0500)


def signals_for_entity(entity_id: str) -> List[Dict]:
    """Return all signals relevant to an entity (direct + related)."""
    out = []
    for sig in SIGNALS:
        if sig["direct"] and sig["entity_id"] == entity_id:
            out.append({**sig, "relevance": "DIRECT"})
        elif not sig["direct"] and entity_id in (sig.get("affects") or []):
            out.append({**sig, "relevance": "RELATED",
                        "via": sig.get("related_entity", "")})
    return sorted(out, key=lambda x: x["score"], reverse=True)
