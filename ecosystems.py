"""
ecosystems.py
=============
Defines the 8 credit ecosystems, their 5 archetype firms each,
and a broader ~120-firm training universe for the ML relative-value model.
All tickers are verified against yfinance coverage.
ADR tickers are used for European firms where available.
"""

from __future__ import annotations

ECOSYSTEMS: dict[str, dict] = {

    # ------------------------------------------------------------------ #
    # 1. GLOBAL BANKS                                                      #
    # ------------------------------------------------------------------ #
    "Global Banks": {
        "description": (
            "Systemically important financial institutions spanning commercial banking, "
            "investment banking, and wealth management. Revenue mix diversified across "
            "net-interest income, fees, and trading. Capital ratios and credit quality "
            "drive relative value."
        ),
        "color": "#3b82f6",
        "archetypes": [
            {"ticker": "JPM",  "name": "JPMorgan Chase",   "archetype": "Quality Compounder",  "country": "US"},
            {"ticker": "BAC",  "name": "Bank of America",  "archetype": "Rate-Sensitive Beta", "country": "US"},
            {"ticker": "GS",   "name": "Goldman Sachs",    "archetype": "Capital-Markets Pure", "country": "US"},
            {"ticker": "UBS",  "name": "UBS Group",        "archetype": "Wealth-Management Franchise", "country": "CH"},
            {"ticker": "DB",   "name": "Deutsche Bank",    "archetype": "Restructuring Recovery", "country": "DE"},
        ],
    },

    # ------------------------------------------------------------------ #
    # 2. PHARMA / MEDTECH                                                  #
    # ------------------------------------------------------------------ #
    "Pharma / MedTech": {
        "description": (
            "Global pharmaceutical manufacturers and medical-technology companies "
            "with durable IP moats, patent cliffs, and pipeline optionality. "
            "Valuation anchored on EV/Sales and pipeline-adjusted DCF."
        ),
        "color": "#10b981",
        "archetypes": [
            {"ticker": "LLY",   "name": "Eli Lilly",        "archetype": "GLP-1 Hypergrowth",      "country": "US"},
            {"ticker": "PFE",   "name": "Pfizer",           "archetype": "Patent-Cliff Turnaround", "country": "US"},
            {"ticker": "NVO",   "name": "Novo Nordisk",     "archetype": "Quality Compounder",      "country": "DK"},
            {"ticker": "RHHBY", "name": "Roche",            "archetype": "Diagnostics Integrated",  "country": "CH"},
            {"ticker": "AZN",   "name": "AstraZeneca",      "archetype": "Oncology Grower",         "country": "GB"},
        ],
    },

    # ------------------------------------------------------------------ #
    # 3. ENTERPRISE SOFTWARE / AI                                          #
    # ------------------------------------------------------------------ #
    "Enterprise Software / AI": {
        "description": (
            "Mission-critical enterprise software vendors with high recurring revenue, "
            "strong free-cash-flow margins, and AI-embedded roadmaps. "
            "Priced on forward EV/FCF and Rule-of-40 metrics."
        ),
        "color": "#8b5cf6",
        "archetypes": [
            {"ticker": "MSFT", "name": "Microsoft",       "archetype": "Platform Compounder",   "country": "US"},
            {"ticker": "SAP",  "name": "SAP SE",          "archetype": "ERP Cloud Migrator",    "country": "DE"},
            {"ticker": "NOW",  "name": "ServiceNow",      "archetype": "Workflow AI Pure-Play", "country": "US"},
            {"ticker": "CRM",  "name": "Salesforce",      "archetype": "AI CRM Transition",     "country": "US"},
            {"ticker": "ADBE", "name": "Adobe",           "archetype": "Creative AI Incumbent", "country": "US"},
        ],
    },

    # ------------------------------------------------------------------ #
    # 4. SEMICONDUCTORS                                                    #
    # ------------------------------------------------------------------ #
    "Semiconductors": {
        "description": (
            "Chipmakers and semiconductor-equipment firms at the heart of AI infrastructure "
            "and consumer electronics. Highly cyclical with long capex cycles; "
            "valued on EV/EBITDA through-cycle and price-to-book on fab assets."
        ),
        "color": "#f59e0b",
        "archetypes": [
            {"ticker": "NVDA", "name": "NVIDIA",           "archetype": "AI Accelerator Leader",  "country": "US"},
            {"ticker": "AMD",  "name": "Advanced Micro Devices", "archetype": "Challenger Platform", "country": "US"},
            {"ticker": "ASML", "name": "ASML Holding",    "archetype": "EUV Monopoly",            "country": "NL"},
            {"ticker": "TSM",  "name": "TSMC",            "archetype": "Foundry Champion",        "country": "TW"},
            {"ticker": "INTC", "name": "Intel",           "archetype": "Turnaround Foundry",      "country": "US"},
        ],
    },

    # ------------------------------------------------------------------ #
    # 5. INDUSTRIAL AUTOMATION                                             #
    # ------------------------------------------------------------------ #
    "Industrial Automation": {
        "description": (
            "Industrial conglomerates and specialist automation vendors supplying "
            "process control, robotics, and electrification solutions to manufacturers. "
            "Valued on EV/EBIT and order-book growth as digitisation accelerates."
        ),
        "color": "#ef4444",
        "archetypes": [
            {"ticker": "HON",   "name": "Honeywell",        "archetype": "Diversified Compounder", "country": "US"},
            {"ticker": "EMR",   "name": "Emerson Electric",  "archetype": "Process Automation Pure","country": "US"},
            {"ticker": "ABB",   "name": "ABB Ltd",           "archetype": "Robotics & Grid Leader", "country": "CH"},
            {"ticker": "ETN",   "name": "Eaton",             "archetype": "Electrification Proxy",  "country": "IE"},
            {"ticker": "ROK",   "name": "Rockwell Automation","archetype": "Discrete Automation Pure","country": "US"},
        ],
    },

    # ------------------------------------------------------------------ #
    # 6. ENERGY MAJORS                                                     #
    # ------------------------------------------------------------------ #
    "Energy Majors": {
        "description": (
            "Integrated oil & gas majors navigating the energy transition while "
            "generating substantial free cash flow. Valued on EV/DACF and "
            "dividend sustainability; exposed to commodity price and policy risk."
        ),
        "color": "#f97316",
        "archetypes": [
            {"ticker": "XOM",  "name": "ExxonMobil",      "archetype": "Scale Integrator",        "country": "US"},
            {"ticker": "CVX",  "name": "Chevron",         "archetype": "Disciplined Capital Return","country": "US"},
            {"ticker": "SHEL", "name": "Shell",           "archetype": "Transition Hedger",        "country": "GB"},
            {"ticker": "TTE",  "name": "TotalEnergies",   "archetype": "Renewables Integrator",    "country": "FR"},
            {"ticker": "BP",   "name": "BP",              "archetype": "Restructuring Energy Play", "country": "GB"},
        ],
    },

    # ------------------------------------------------------------------ #
    # 7. AEROSPACE & DEFENCE                                               #
    # ------------------------------------------------------------------ #
    "Aerospace & Defence": {
        "description": (
            "Prime defence contractors and commercial aerospace OEMs benefiting from "
            "elevated government budgets and civil aviation recovery. Long-cycle "
            "backlog provides revenue visibility; valued on EV/EBIT and backlog-to-sales."
        ),
        "color": "#6366f1",
        "archetypes": [
            {"ticker": "LMT",   "name": "Lockheed Martin",  "archetype": "Defence Prime",           "country": "US"},
            {"ticker": "RTX",   "name": "RTX Corporation",  "archetype": "Engines & Missiles Dual",  "country": "US"},
            {"ticker": "BA",    "name": "Boeing",           "archetype": "Commercial Turnaround",    "country": "US"},
            {"ticker": "EADSY", "name": "Airbus",           "archetype": "Duopoly Compounder",       "country": "FR"},
            {"ticker": "RYCEY", "name": "Rolls-Royce",      "archetype": "Engine Aftermarket Play",  "country": "GB"},
        ],
    },

    # ------------------------------------------------------------------ #
    # 8. INFRASTRUCTURE & LOGISTICS                                        #
    # ------------------------------------------------------------------ #
    "Infrastructure & Logistics": {
        "description": (
            "Rail networks, parcel couriers, and waste-management firms operating "
            "essential physical infrastructure with pricing power and high barriers. "
            "Valued on EV/EBITDA and free-cash-flow yield; defensive through cycles."
        ),
        "color": "#14b8a6",
        "archetypes": [
            {"ticker": "UNP",  "name": "Union Pacific",    "archetype": "Rail Pricing Power",      "country": "US"},
            {"ticker": "CSX",  "name": "CSX Corporation",  "archetype": "Eastern Rail Compounder", "country": "US"},
            {"ticker": "FDX",  "name": "FedEx",            "archetype": "Express Network Leader",  "country": "US"},
            {"ticker": "UPS",  "name": "UPS",              "archetype": "Parcel Yield Optimizer",  "country": "US"},
            {"ticker": "WM",   "name": "Waste Management", "archetype": "Waste Infrastructure Moat","country": "US"},
        ],
    },
}


# --------------------------------------------------------------------------- #
# FLAT ARCHETYPE TICKER LIST (40 total, 5 per ecosystem)                       #
# --------------------------------------------------------------------------- #
ARCHETYPE_TICKERS: list[str] = [
    firm["ticker"]
    for eco in ECOSYSTEMS.values()
    for firm in eco["archetypes"]
]


# --------------------------------------------------------------------------- #
# TRAINING UNIVERSE  (~120 firms)                                              #
# All archetype tickers + extra peers per ecosystem                            #
# --------------------------------------------------------------------------- #
TRAINING_UNIVERSE: list[dict] = [

    # ---- Global Banks (archetype 5 + 10 peers = 15) ---------------------- #
    {"ticker": "JPM",  "ecosystem": "Global Banks", "country": "US"},
    {"ticker": "BAC",  "ecosystem": "Global Banks", "country": "US"},
    {"ticker": "GS",   "ecosystem": "Global Banks", "country": "US"},
    {"ticker": "UBS",  "ecosystem": "Global Banks", "country": "CH"},
    {"ticker": "DB",   "ecosystem": "Global Banks", "country": "DE"},
    # peers
    {"ticker": "MS",   "ecosystem": "Global Banks", "country": "US"},
    {"ticker": "C",    "ecosystem": "Global Banks", "country": "US"},
    {"ticker": "WFC",  "ecosystem": "Global Banks", "country": "US"},
    {"ticker": "BCS",  "ecosystem": "Global Banks", "country": "GB"},   # Barclays ADR
    {"ticker": "HSBC", "ecosystem": "Global Banks", "country": "GB"},   # HSBC ADR
    {"ticker": "ING",  "ecosystem": "Global Banks", "country": "NL"},   # ING ADR
    {"ticker": "BNP",  "ecosystem": "Global Banks", "country": "FR"},   # BNP Paribas OTC
    {"ticker": "SAN",  "ecosystem": "Global Banks", "country": "ES"},   # Santander ADR
    {"ticker": "USB",  "ecosystem": "Global Banks", "country": "US"},
    {"ticker": "TFC",  "ecosystem": "Global Banks", "country": "US"},

    # ---- Pharma / MedTech (archetype 5 + 10 peers = 15) ------------------ #
    {"ticker": "LLY",   "ecosystem": "Pharma / MedTech", "country": "US"},
    {"ticker": "PFE",   "ecosystem": "Pharma / MedTech", "country": "US"},
    {"ticker": "NVO",   "ecosystem": "Pharma / MedTech", "country": "DK"},
    {"ticker": "RHHBY", "ecosystem": "Pharma / MedTech", "country": "CH"},
    {"ticker": "AZN",   "ecosystem": "Pharma / MedTech", "country": "GB"},
    # peers
    {"ticker": "SNY",   "ecosystem": "Pharma / MedTech", "country": "FR"},   # Sanofi ADR
    {"ticker": "BAYRY", "ecosystem": "Pharma / MedTech", "country": "DE"},   # Bayer ADR
    {"ticker": "NVS",   "ecosystem": "Pharma / MedTech", "country": "CH"},   # Novartis ADR
    {"ticker": "ABBV",  "ecosystem": "Pharma / MedTech", "country": "US"},
    {"ticker": "MRK",   "ecosystem": "Pharma / MedTech", "country": "US"},
    {"ticker": "BMY",   "ecosystem": "Pharma / MedTech", "country": "US"},
    {"ticker": "AMGN",  "ecosystem": "Pharma / MedTech", "country": "US"},
    {"ticker": "GILD",  "ecosystem": "Pharma / MedTech", "country": "US"},
    {"ticker": "MDT",   "ecosystem": "Pharma / MedTech", "country": "IE"},
    {"ticker": "SYK",   "ecosystem": "Pharma / MedTech", "country": "US"},

    # ---- Enterprise Software / AI (archetype 5 + 10 peers = 15) ---------- #
    {"ticker": "MSFT",  "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "SAP",   "ecosystem": "Enterprise Software / AI", "country": "DE"},
    {"ticker": "NOW",   "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "CRM",   "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "ADBE",  "ecosystem": "Enterprise Software / AI", "country": "US"},
    # peers
    {"ticker": "ORCL",  "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "ACN",   "ecosystem": "Enterprise Software / AI", "country": "IE"},
    {"ticker": "INTU",  "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "GOOGL", "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "META",  "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "SNOW",  "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "WDAY",  "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "TEAM",  "ecosystem": "Enterprise Software / AI", "country": "AU"},
    {"ticker": "DDOG",  "ecosystem": "Enterprise Software / AI", "country": "US"},
    {"ticker": "MDB",   "ecosystem": "Enterprise Software / AI", "country": "US"},

    # ---- Semiconductors (archetype 5 + 10 peers = 15) -------------------- #
    {"ticker": "NVDA",  "ecosystem": "Semiconductors", "country": "US"},
    {"ticker": "AMD",   "ecosystem": "Semiconductors", "country": "US"},
    {"ticker": "ASML",  "ecosystem": "Semiconductors", "country": "NL"},
    {"ticker": "TSM",   "ecosystem": "Semiconductors", "country": "TW"},
    {"ticker": "INTC",  "ecosystem": "Semiconductors", "country": "US"},
    # peers
    {"ticker": "QCOM",  "ecosystem": "Semiconductors", "country": "US"},
    {"ticker": "STM",   "ecosystem": "Semiconductors", "country": "CH"},   # STMicroelectronics ADR
    {"ticker": "NXPI",  "ecosystem": "Semiconductors", "country": "NL"},
    {"ticker": "AVGO",  "ecosystem": "Semiconductors", "country": "US"},
    {"ticker": "TXN",   "ecosystem": "Semiconductors", "country": "US"},
    {"ticker": "MRVL",  "ecosystem": "Semiconductors", "country": "US"},
    {"ticker": "MPWR",  "ecosystem": "Semiconductors", "country": "US"},
    {"ticker": "ON",    "ecosystem": "Semiconductors", "country": "US"},
    {"ticker": "WOLF",  "ecosystem": "Semiconductors", "country": "US"},
    {"ticker": "AMAT",  "ecosystem": "Semiconductors", "country": "US"},

    # ---- Industrial Automation (archetype 5 + 10 peers = 15) ------------- #
    {"ticker": "HON",   "ecosystem": "Industrial Automation", "country": "US"},
    {"ticker": "EMR",   "ecosystem": "Industrial Automation", "country": "US"},
    {"ticker": "ABB",   "ecosystem": "Industrial Automation", "country": "CH"},
    {"ticker": "ETN",   "ecosystem": "Industrial Automation", "country": "IE"},
    {"ticker": "ROK",   "ecosystem": "Industrial Automation", "country": "US"},
    # peers
    {"ticker": "SIEGY", "ecosystem": "Industrial Automation", "country": "DE"},  # Siemens ADR
    {"ticker": "SGSOY", "ecosystem": "Industrial Automation", "country": "FR"},  # Schneider ADR
    {"ticker": "PH",    "ecosystem": "Industrial Automation", "country": "US"},
    {"ticker": "AME",   "ecosystem": "Industrial Automation", "country": "US"},
    {"ticker": "DHR",   "ecosystem": "Industrial Automation", "country": "US"},
    {"ticker": "ITW",   "ecosystem": "Industrial Automation", "country": "US"},
    {"ticker": "GE",    "ecosystem": "Industrial Automation", "country": "US"},
    {"ticker": "MMM",   "ecosystem": "Industrial Automation", "country": "US"},
    {"ticker": "IR",    "ecosystem": "Industrial Automation", "country": "IE"},
    {"ticker": "FANUY", "ecosystem": "Industrial Automation", "country": "JP"},  # Fanuc ADR

    # ---- Energy Majors (archetype 5 + 10 peers = 15) --------------------- #
    {"ticker": "XOM",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "CVX",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "SHEL",  "ecosystem": "Energy Majors", "country": "GB"},
    {"ticker": "TTE",   "ecosystem": "Energy Majors", "country": "FR"},
    {"ticker": "BP",    "ecosystem": "Energy Majors", "country": "GB"},
    # peers
    {"ticker": "EQNR",  "ecosystem": "Energy Majors", "country": "NO"},
    {"ticker": "COP",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "EOG",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "SLB",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "HAL",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "PSX",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "VLO",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "MPC",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "PXD",   "ecosystem": "Energy Majors", "country": "US"},
    {"ticker": "OXY",   "ecosystem": "Energy Majors", "country": "US"},

    # ---- Aerospace & Defence (archetype 5 + 10 peers = 15) --------------- #
    {"ticker": "LMT",   "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "RTX",   "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "BA",    "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "EADSY", "ecosystem": "Aerospace & Defence", "country": "FR"},
    {"ticker": "RYCEY", "ecosystem": "Aerospace & Defence", "country": "GB"},
    # peers
    {"ticker": "NOC",   "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "GD",    "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "SAFRY", "ecosystem": "Aerospace & Defence", "country": "FR"},  # Safran ADR
    {"ticker": "HII",   "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "LHX",   "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "TDG",   "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "HEI",   "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "SPR",   "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "AXON",  "ecosystem": "Aerospace & Defence", "country": "US"},
    {"ticker": "LDOS",  "ecosystem": "Aerospace & Defence", "country": "US"},

    # ---- Infrastructure & Logistics (archetype 5 + 10 peers = 15) -------- #
    {"ticker": "UNP",   "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "CSX",   "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "FDX",   "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "UPS",   "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "WM",    "ecosystem": "Infrastructure & Logistics", "country": "US"},
    # peers
    {"ticker": "NSC",   "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "CP",    "ecosystem": "Infrastructure & Logistics", "country": "CA"},
    {"ticker": "CNI",   "ecosystem": "Infrastructure & Logistics", "country": "CA"},
    {"ticker": "EXPD",  "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "CHRW",  "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "JBHT",  "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "XPO",   "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "ODFL",  "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "SAIA",  "ecosystem": "Infrastructure & Logistics", "country": "US"},
    {"ticker": "RSG",   "ecosystem": "Infrastructure & Logistics", "country": "US"},
]


# --------------------------------------------------------------------------- #
# DERIVED LOOKUP STRUCTURES                                                    #
# --------------------------------------------------------------------------- #

# Flat list of all training tickers
TRAINING_TICKERS: list[str] = [t["ticker"] for t in TRAINING_UNIVERSE]

# Ecosystem colour map
ECOSYSTEM_COLORS: dict[str, str] = {
    ecosystem: data["color"] for ecosystem, data in ECOSYSTEMS.items()
}

# Ticker → ecosystem
TICKER_ECOSYSTEM: dict[str, str] = {
    t["ticker"]: t["ecosystem"] for t in TRAINING_UNIVERSE
}

# Ticker → country
TICKER_COUNTRY: dict[str, str] = {
    t["ticker"]: t["country"] for t in TRAINING_UNIVERSE
}
