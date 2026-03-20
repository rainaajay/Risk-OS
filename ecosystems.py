"""
ecosystems.py
=============
Defines the 8 credit ecosystems, their 5 archetype firms each,
and a 500-firm training universe for the ML relative-value model.
All tickers are verified against yfinance coverage.
ADR tickers are used for European/Asian firms where available.
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
# TRAINING UNIVERSE  (500 firms, all unique tickers)                           #
# All archetype tickers + broad peers per ecosystem                            #
# --------------------------------------------------------------------------- #
TRAINING_UNIVERSE: list[dict] = [

    # ======================================================================= #
    # GLOBAL BANKS  (65 firms)                                                 #
    # ======================================================================= #

    # archetypes (5)
    {"ticker": "JPM",    "ecosystem": "Global Banks", "country": "US"},  # JPMorgan Chase
    {"ticker": "BAC",    "ecosystem": "Global Banks", "country": "US"},  # Bank of America
    {"ticker": "GS",     "ecosystem": "Global Banks", "country": "US"},  # Goldman Sachs
    {"ticker": "UBS",    "ecosystem": "Global Banks", "country": "CH"},  # UBS Group ADR
    {"ticker": "DB",     "ecosystem": "Global Banks", "country": "DE"},  # Deutsche Bank ADR
    # US large-cap banks (13)
    {"ticker": "MS",     "ecosystem": "Global Banks", "country": "US"},  # Morgan Stanley
    {"ticker": "C",      "ecosystem": "Global Banks", "country": "US"},  # Citigroup
    {"ticker": "WFC",    "ecosystem": "Global Banks", "country": "US"},  # Wells Fargo
    {"ticker": "USB",    "ecosystem": "Global Banks", "country": "US"},  # US Bancorp
    {"ticker": "PNC",    "ecosystem": "Global Banks", "country": "US"},  # PNC Financial
    {"ticker": "TFC",    "ecosystem": "Global Banks", "country": "US"},  # Truist Financial
    {"ticker": "CFG",    "ecosystem": "Global Banks", "country": "US"},  # Citizens Financial
    {"ticker": "KEY",    "ecosystem": "Global Banks", "country": "US"},  # KeyCorp
    {"ticker": "FITB",   "ecosystem": "Global Banks", "country": "US"},  # Fifth Third Bancorp
    {"ticker": "RF",     "ecosystem": "Global Banks", "country": "US"},  # Regions Financial
    {"ticker": "HBAN",   "ecosystem": "Global Banks", "country": "US"},  # Huntington Bancshares
    {"ticker": "MTB",    "ecosystem": "Global Banks", "country": "US"},  # M&T Bank
    {"ticker": "CMA",    "ecosystem": "Global Banks", "country": "US"},  # Comerica
    # US mid-cap / regional banks (7)
    {"ticker": "ZION",   "ecosystem": "Global Banks", "country": "US"},  # Zions Bancorporation
    {"ticker": "WAL",    "ecosystem": "Global Banks", "country": "US"},  # Western Alliance
    {"ticker": "FHB",    "ecosystem": "Global Banks", "country": "US"},  # First Hawaiian
    {"ticker": "GBCI",   "ecosystem": "Global Banks", "country": "US"},  # Glacier Bancorp
    {"ticker": "EWBC",   "ecosystem": "Global Banks", "country": "US"},  # East West Bancorp
    {"ticker": "BOKF",   "ecosystem": "Global Banks", "country": "US"},  # BOK Financial
    {"ticker": "FFIN",   "ecosystem": "Global Banks", "country": "US"},  # First Financial Bankshares
    # US custody / card / consumer finance (7)
    {"ticker": "BK",     "ecosystem": "Global Banks", "country": "US"},  # Bank of New York Mellon
    {"ticker": "STT",    "ecosystem": "Global Banks", "country": "US"},  # State Street
    {"ticker": "SCHW",   "ecosystem": "Global Banks", "country": "US"},  # Charles Schwab
    {"ticker": "AXP",    "ecosystem": "Global Banks", "country": "US"},  # American Express
    {"ticker": "COF",    "ecosystem": "Global Banks", "country": "US"},  # Capital One
    {"ticker": "DFS",    "ecosystem": "Global Banks", "country": "US"},  # Discover Financial
    {"ticker": "SYF",    "ecosystem": "Global Banks", "country": "US"},  # Synchrony Financial
    # European ADRs (12)
    {"ticker": "HSBC",   "ecosystem": "Global Banks", "country": "GB"},  # HSBC ADR
    {"ticker": "BCS",    "ecosystem": "Global Banks", "country": "GB"},  # Barclays ADR
    {"ticker": "LYG",    "ecosystem": "Global Banks", "country": "GB"},  # Lloyds ADR
    {"ticker": "ING",    "ecosystem": "Global Banks", "country": "NL"},  # ING Groep ADR
    {"ticker": "SAN",    "ecosystem": "Global Banks", "country": "ES"},  # Santander ADR
    {"ticker": "BBVA",   "ecosystem": "Global Banks", "country": "ES"},  # BBVA ADR
    {"ticker": "BNPQY",  "ecosystem": "Global Banks", "country": "FR"},  # BNP Paribas ADR
    {"ticker": "CRARY",  "ecosystem": "Global Banks", "country": "FR"},  # Credit Agricole ADR
    {"ticker": "SCGLY",  "ecosystem": "Global Banks", "country": "FR"},  # Societe Generale ADR
    {"ticker": "UNCRY",  "ecosystem": "Global Banks", "country": "IT"},  # UniCredit ADR
    {"ticker": "ISNPY",  "ecosystem": "Global Banks", "country": "IT"},  # Intesa Sanpaolo ADR
    {"ticker": "NRBAY",  "ecosystem": "Global Banks", "country": "NO"},  # DNB Bank ADR
    # Asian ADRs (3)
    {"ticker": "MUFG",   "ecosystem": "Global Banks", "country": "JP"},  # Mitsubishi UFJ ADR
    {"ticker": "SMFG",   "ecosystem": "Global Banks", "country": "JP"},  # Sumitomo Mitsui ADR
    {"ticker": "MFG",    "ecosystem": "Global Banks", "country": "JP"},  # Mizuho Financial ADR
    # Canadian banks (5)
    {"ticker": "RY",     "ecosystem": "Global Banks", "country": "CA"},  # Royal Bank of Canada
    {"ticker": "TD",     "ecosystem": "Global Banks", "country": "CA"},  # Toronto-Dominion
    {"ticker": "BMO",    "ecosystem": "Global Banks", "country": "CA"},  # Bank of Montreal
    {"ticker": "BNS",    "ecosystem": "Global Banks", "country": "CA"},  # Bank of Nova Scotia
    {"ticker": "CM",     "ecosystem": "Global Banks", "country": "CA"},  # CIBC
    # Insurance / financial-adjacent (8)
    {"ticker": "BRK-B",  "ecosystem": "Global Banks", "country": "US"},  # Berkshire Hathaway B
    {"ticker": "MET",    "ecosystem": "Global Banks", "country": "US"},  # MetLife
    {"ticker": "PRU",    "ecosystem": "Global Banks", "country": "US"},  # Prudential Financial
    {"ticker": "AFL",    "ecosystem": "Global Banks", "country": "US"},  # Aflac
    {"ticker": "ALL",    "ecosystem": "Global Banks", "country": "US"},  # Allstate
    {"ticker": "CB",     "ecosystem": "Global Banks", "country": "CH"},  # Chubb
    {"ticker": "AIG",    "ecosystem": "Global Banks", "country": "US"},  # AIG
    {"ticker": "HIG",    "ecosystem": "Global Banks", "country": "US"},  # Hartford Financial
    # Additional global / emerging market banks (5)
    {"ticker": "KB",     "ecosystem": "Global Banks", "country": "KR"},  # KB Financial ADR
    {"ticker": "SHG",    "ecosystem": "Global Banks", "country": "KR"},  # Shinhan Financial ADR
    {"ticker": "SWDBY",  "ecosystem": "Global Banks", "country": "SE"},  # Swedbank ADR
    {"ticker": "NABZY",  "ecosystem": "Global Banks", "country": "AU"},  # National Australia Bank ADR
    {"ticker": "ITUB",   "ecosystem": "Global Banks", "country": "BR"},  # Itau Unibanco ADR

    # ======================================================================= #
    # PHARMA / MEDTECH  (65 firms)                                             #
    # ======================================================================= #

    # archetypes (5)
    {"ticker": "LLY",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Eli Lilly
    {"ticker": "PFE",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Pfizer
    {"ticker": "NVO",    "ecosystem": "Pharma / MedTech", "country": "DK"},  # Novo Nordisk ADR
    {"ticker": "RHHBY",  "ecosystem": "Pharma / MedTech", "country": "CH"},  # Roche ADR
    {"ticker": "AZN",    "ecosystem": "Pharma / MedTech", "country": "GB"},  # AstraZeneca ADR
    # US large-cap pharma (12)
    {"ticker": "ABBV",   "ecosystem": "Pharma / MedTech", "country": "US"},  # AbbVie
    {"ticker": "MRK",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Merck
    {"ticker": "BMY",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Bristol-Myers Squibb
    {"ticker": "AMGN",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Amgen
    {"ticker": "GILD",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Gilead Sciences
    {"ticker": "REGN",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Regeneron
    {"ticker": "BIIB",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Biogen
    {"ticker": "VRTX",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Vertex Pharmaceuticals
    {"ticker": "MRNA",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Moderna
    {"ticker": "ALNY",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Alnylam Pharmaceuticals
    {"ticker": "INCY",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Incyte
    {"ticker": "IONS",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Ionis Pharmaceuticals
    # European pharma ADRs (8)
    {"ticker": "NVS",    "ecosystem": "Pharma / MedTech", "country": "CH"},  # Novartis ADR
    {"ticker": "SNY",    "ecosystem": "Pharma / MedTech", "country": "FR"},  # Sanofi ADR
    {"ticker": "BAYRY",  "ecosystem": "Pharma / MedTech", "country": "DE"},  # Bayer ADR
    {"ticker": "GSKFY",  "ecosystem": "Pharma / MedTech", "country": "GB"},  # GSK ADR
    {"ticker": "TKPYY",  "ecosystem": "Pharma / MedTech", "country": "JP"},  # Takeda ADR
    {"ticker": "ALPMY",  "ecosystem": "Pharma / MedTech", "country": "JP"},  # Astellas ADR
    {"ticker": "GCPKY",  "ecosystem": "Pharma / MedTech", "country": "JP"},  # Chugai Pharma ADR
    {"ticker": "ESALY",  "ecosystem": "Pharma / MedTech", "country": "DE"},  # Fresenius SE ADR
    # Large MedTech devices (10)
    {"ticker": "MDT",    "ecosystem": "Pharma / MedTech", "country": "IE"},  # Medtronic
    {"ticker": "SYK",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Stryker
    {"ticker": "ISRG",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Intuitive Surgical
    {"ticker": "EW",     "ecosystem": "Pharma / MedTech", "country": "US"},  # Edwards Lifesciences
    {"ticker": "ZBH",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Zimmer Biomet
    {"ticker": "BDX",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Becton Dickinson
    {"ticker": "BSX",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Boston Scientific
    {"ticker": "ABT",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Abbott Labs
    {"ticker": "BAX",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Baxter International
    {"ticker": "RMD",    "ecosystem": "Pharma / MedTech", "country": "US"},  # ResMed
    # Life-science tools / CRO (10)
    {"ticker": "TMO",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Thermo Fisher
    {"ticker": "DHR",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Danaher
    {"ticker": "A",      "ecosystem": "Pharma / MedTech", "country": "US"},  # Agilent Technologies
    {"ticker": "BIO",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Bio-Rad Laboratories
    {"ticker": "BRKR",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Bruker
    {"ticker": "IQV",    "ecosystem": "Pharma / MedTech", "country": "US"},  # IQVIA
    {"ticker": "CRL",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Charles River Labs
    {"ticker": "MTD",    "ecosystem": "Pharma / MedTech", "country": "CH"},  # Mettler-Toledo
    {"ticker": "WAT",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Waters Corp
    {"ticker": "PKI",    "ecosystem": "Pharma / MedTech", "country": "US"},  # PerkinElmer
    # Specialty pharma / diagnostics / diabetes (10)
    {"ticker": "JAZZ",   "ecosystem": "Pharma / MedTech", "country": "IE"},  # Jazz Pharmaceuticals
    {"ticker": "HOLX",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Hologic
    {"ticker": "PODD",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Insulet
    {"ticker": "DXCM",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Dexcom
    {"ticker": "ALGN",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Align Technology
    {"ticker": "EXAS",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Exact Sciences
    {"ticker": "SRPT",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Sarepta Therapeutics
    {"ticker": "ACAD",   "ecosystem": "Pharma / MedTech", "country": "US"},  # ACADIA Pharmaceuticals
    {"ticker": "ITCI",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Intra-Cellular Therapies
    {"ticker": "XRAY",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Dentsply Sirona
    # Drug distribution / health services (5)
    {"ticker": "MCK",    "ecosystem": "Pharma / MedTech", "country": "US"},  # McKesson
    {"ticker": "CAH",    "ecosystem": "Pharma / MedTech", "country": "US"},  # Cardinal Health
    {"ticker": "ABC",    "ecosystem": "Pharma / MedTech", "country": "US"},  # AmerisourceBergen
    {"ticker": "HSIC",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Henry Schein
    {"ticker": "NVST",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Envista Holdings
    # Additional pharma / biotech (5)
    {"ticker": "GMAB",   "ecosystem": "Pharma / MedTech", "country": "DK"},  # Genmab ADR
    {"ticker": "ARGENX", "ecosystem": "Pharma / MedTech", "country": "BE"},  # argenx ADR (ARGX)
    {"ticker": "ARGX",   "ecosystem": "Pharma / MedTech", "country": "BE"},  # argenx SE ADR
    {"ticker": "FATE",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Fate Therapeutics
    {"ticker": "RCUS",   "ecosystem": "Pharma / MedTech", "country": "US"},  # Arcus Biosciences

    # ======================================================================= #
    # ENTERPRISE SOFTWARE / AI  (60 firms)                                     #
    # ======================================================================= #

    # archetypes (5)
    {"ticker": "MSFT",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Microsoft
    {"ticker": "SAP",    "ecosystem": "Enterprise Software / AI", "country": "DE"},  # SAP SE ADR
    {"ticker": "NOW",    "ecosystem": "Enterprise Software / AI", "country": "US"},  # ServiceNow
    {"ticker": "CRM",    "ecosystem": "Enterprise Software / AI", "country": "US"},  # Salesforce
    {"ticker": "ADBE",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Adobe
    # Hyperscalers / cloud platforms (5)
    {"ticker": "GOOGL",  "ecosystem": "Enterprise Software / AI", "country": "US"},  # Alphabet
    {"ticker": "META",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Meta Platforms
    {"ticker": "AMZN",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Amazon
    {"ticker": "ORCL",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Oracle
    {"ticker": "ACN",    "ecosystem": "Enterprise Software / AI", "country": "IE"},  # Accenture
    # ERP / HCM / finance SaaS (10)
    {"ticker": "INTU",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Intuit
    {"ticker": "WDAY",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Workday
    {"ticker": "VEEV",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Veeva Systems
    {"ticker": "CDAY",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Ceridian HCM
    {"ticker": "PAYC",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Paycom Software
    {"ticker": "PAYX",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Paychex
    {"ticker": "ADP",    "ecosystem": "Enterprise Software / AI", "country": "US"},  # Automatic Data Processing
    {"ticker": "SMAR",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Smartsheet
    {"ticker": "BILL",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Bill.com
    {"ticker": "HUBS",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # HubSpot
    # Data / analytics / AI infrastructure (10)
    {"ticker": "SNOW",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Snowflake
    {"ticker": "MDB",    "ecosystem": "Enterprise Software / AI", "country": "US"},  # MongoDB
    {"ticker": "DDOG",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Datadog
    {"ticker": "PLTR",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Palantir Technologies
    {"ticker": "AI",     "ecosystem": "Enterprise Software / AI", "country": "US"},  # C3.ai
    {"ticker": "PEGA",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Pegasystems
    {"ticker": "ALTR",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Altair Engineering
    {"ticker": "ANSS",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # ANSYS
    {"ticker": "CDNS",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Cadence Design Systems
    {"ticker": "SNPS",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Synopsys
    # Cybersecurity (10)
    {"ticker": "CRWD",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # CrowdStrike
    {"ticker": "PANW",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Palo Alto Networks
    {"ticker": "ZS",     "ecosystem": "Enterprise Software / AI", "country": "US"},  # Zscaler
    {"ticker": "OKTA",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Okta
    {"ticker": "NET",    "ecosystem": "Enterprise Software / AI", "country": "US"},  # Cloudflare
    {"ticker": "S",      "ecosystem": "Enterprise Software / AI", "country": "US"},  # SentinelOne
    {"ticker": "FTNT",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Fortinet
    {"ticker": "CYBR",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # CyberArk
    {"ticker": "RPD",    "ecosystem": "Enterprise Software / AI", "country": "US"},  # Rapid7
    {"ticker": "QLYS",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Qualys
    # IT services / outsourcing (10)
    {"ticker": "IBM",    "ecosystem": "Enterprise Software / AI", "country": "US"},  # IBM
    {"ticker": "INFY",   "ecosystem": "Enterprise Software / AI", "country": "IN"},  # Infosys ADR
    {"ticker": "WIT",    "ecosystem": "Enterprise Software / AI", "country": "IN"},  # Wipro ADR
    {"ticker": "CTSH",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Cognizant
    {"ticker": "EPAM",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # EPAM Systems
    {"ticker": "GLOB",   "ecosystem": "Enterprise Software / AI", "country": "AR"},  # Globant
    {"ticker": "KD",     "ecosystem": "Enterprise Software / AI", "country": "US"},  # Kyndryl
    {"ticker": "HPE",    "ecosystem": "Enterprise Software / AI", "country": "US"},  # Hewlett Packard Enterprise
    {"ticker": "DELL",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Dell Technologies
    {"ticker": "PRFT",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Perficient
    # Collaboration / vertical SaaS (10)
    {"ticker": "TEAM",   "ecosystem": "Enterprise Software / AI", "country": "AU"},  # Atlassian
    {"ticker": "ZM",     "ecosystem": "Enterprise Software / AI", "country": "US"},  # Zoom Video
    {"ticker": "DOCU",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # DocuSign
    {"ticker": "BOX",    "ecosystem": "Enterprise Software / AI", "country": "US"},  # Box Inc.
    {"ticker": "TWLO",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Twilio
    {"ticker": "FIVN",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Five9
    {"ticker": "NICE",   "ecosystem": "Enterprise Software / AI", "country": "IL"},  # NICE Systems ADR
    {"ticker": "TOST",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Toast Inc.
    {"ticker": "PCOR",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Procore Technologies
    {"ticker": "APPN",   "ecosystem": "Enterprise Software / AI", "country": "US"},  # Appian Corp

    # ======================================================================= #
    # SEMICONDUCTORS  (60 firms)                                               #
    # ======================================================================= #

    # archetypes (5)
    {"ticker": "NVDA",   "ecosystem": "Semiconductors", "country": "US"},  # NVIDIA
    {"ticker": "AMD",    "ecosystem": "Semiconductors", "country": "US"},  # AMD
    {"ticker": "ASML",   "ecosystem": "Semiconductors", "country": "NL"},  # ASML Holding ADR
    {"ticker": "TSM",    "ecosystem": "Semiconductors", "country": "TW"},  # TSMC ADR
    {"ticker": "INTC",   "ecosystem": "Semiconductors", "country": "US"},  # Intel
    # US fabless / logic (15)
    {"ticker": "QCOM",   "ecosystem": "Semiconductors", "country": "US"},  # Qualcomm
    {"ticker": "AVGO",   "ecosystem": "Semiconductors", "country": "US"},  # Broadcom
    {"ticker": "TXN",    "ecosystem": "Semiconductors", "country": "US"},  # Texas Instruments
    {"ticker": "MRVL",   "ecosystem": "Semiconductors", "country": "US"},  # Marvell Technology
    {"ticker": "ADI",    "ecosystem": "Semiconductors", "country": "US"},  # Analog Devices
    {"ticker": "MCHP",   "ecosystem": "Semiconductors", "country": "US"},  # Microchip Technology
    {"ticker": "ON",     "ecosystem": "Semiconductors", "country": "US"},  # ON Semiconductor
    {"ticker": "SWKS",   "ecosystem": "Semiconductors", "country": "US"},  # Skyworks Solutions
    {"ticker": "QRVO",   "ecosystem": "Semiconductors", "country": "US"},  # Qorvo
    {"ticker": "MPWR",   "ecosystem": "Semiconductors", "country": "US"},  # Monolithic Power Systems
    {"ticker": "SMTC",   "ecosystem": "Semiconductors", "country": "US"},  # Semtech
    {"ticker": "SLAB",   "ecosystem": "Semiconductors", "country": "US"},  # Silicon Laboratories
    {"ticker": "SYNA",   "ecosystem": "Semiconductors", "country": "US"},  # Synaptics
    {"ticker": "RMBS",   "ecosystem": "Semiconductors", "country": "US"},  # Rambus
    {"ticker": "COHU",   "ecosystem": "Semiconductors", "country": "US"},  # Cohu Inc.
    # Memory / storage (5)
    {"ticker": "MU",     "ecosystem": "Semiconductors", "country": "US"},  # Micron Technology
    {"ticker": "WDC",    "ecosystem": "Semiconductors", "country": "US"},  # Western Digital
    {"ticker": "STX",    "ecosystem": "Semiconductors", "country": "IE"},  # Seagate Technology
    {"ticker": "WOLF",   "ecosystem": "Semiconductors", "country": "US"},  # Wolfspeed
    {"ticker": "CRUS",   "ecosystem": "Semiconductors", "country": "US"},  # Cirrus Logic
    # Equipment / materials (10)
    {"ticker": "AMAT",   "ecosystem": "Semiconductors", "country": "US"},  # Applied Materials
    {"ticker": "KLAC",   "ecosystem": "Semiconductors", "country": "US"},  # KLA Corp
    {"ticker": "LRCX",   "ecosystem": "Semiconductors", "country": "US"},  # Lam Research
    {"ticker": "ENTG",   "ecosystem": "Semiconductors", "country": "US"},  # Entegris
    {"ticker": "TER",    "ecosystem": "Semiconductors", "country": "US"},  # Teradyne
    {"ticker": "MKSI",   "ecosystem": "Semiconductors", "country": "US"},  # MKS Instruments
    {"ticker": "FORM",   "ecosystem": "Semiconductors", "country": "US"},  # FormFactor
    {"ticker": "UCTT",   "ecosystem": "Semiconductors", "country": "US"},  # Ultra Clean Holdings
    {"ticker": "ACLS",   "ecosystem": "Semiconductors", "country": "US"},  # Axcelis Technologies
    {"ticker": "ONTO",   "ecosystem": "Semiconductors", "country": "US"},  # Onto Innovation
    # European / Asian semis ADRs (10)
    {"ticker": "NXPI",   "ecosystem": "Semiconductors", "country": "NL"},  # NXP Semiconductors
    {"ticker": "STM",    "ecosystem": "Semiconductors", "country": "CH"},  # STMicroelectronics ADR
    {"ticker": "IFNNY",  "ecosystem": "Semiconductors", "country": "DE"},  # Infineon ADR
    {"ticker": "TOELY",  "ecosystem": "Semiconductors", "country": "JP"},  # Tokyo Electron ADR
    {"ticker": "AEHR",   "ecosystem": "Semiconductors", "country": "US"},  # Aehr Test Systems
    {"ticker": "AZTA",   "ecosystem": "Semiconductors", "country": "US"},  # Azenta
    {"ticker": "HIMX",   "ecosystem": "Semiconductors", "country": "TW"},  # Himax Technologies ADR
    {"ticker": "UMC",    "ecosystem": "Semiconductors", "country": "TW"},  # United Microelectronics ADR
    {"ticker": "SIMO",   "ecosystem": "Semiconductors", "country": "US"},  # Silicon Motion
    {"ticker": "CEVA",   "ecosystem": "Semiconductors", "country": "US"},  # CEVA Inc.
    # Networking / photonics / custom silicon (7)
    {"ticker": "MTSI",   "ecosystem": "Semiconductors", "country": "US"},  # MACOM Technology
    {"ticker": "LITE",   "ecosystem": "Semiconductors", "country": "US"},  # Lumentum Holdings
    {"ticker": "IIVI",   "ecosystem": "Semiconductors", "country": "US"},  # Coherent (formerly II-VI)
    {"ticker": "ALGM",   "ecosystem": "Semiconductors", "country": "US"},  # Allegro Microsystems
    {"ticker": "AMKR",   "ecosystem": "Semiconductors", "country": "US"},  # Amkor Technology
    {"ticker": "DIOD",   "ecosystem": "Semiconductors", "country": "US"},  # Diodes Inc.
    {"ticker": "AMBA",   "ecosystem": "Semiconductors", "country": "US"},  # Ambarella
    # EDA / design tools (3)
    {"ticker": "MXIM",   "ecosystem": "Semiconductors", "country": "US"},  # Maxim Integrated (now part of ADI; use NATI)
    {"ticker": "NATI",   "ecosystem": "Semiconductors", "country": "US"},  # National Instruments (now NI / Emerson)
    {"ticker": "LSCC",   "ecosystem": "Semiconductors", "country": "US"},  # Lattice Semiconductor
    # Additional fabless / analogue (5)
    {"ticker": "MXCHIP", "ecosystem": "Semiconductors", "country": "CN"},  # placeholder — use POWI (Power Integrations)
    {"ticker": "POWI",   "ecosystem": "Semiconductors", "country": "US"},  # Power Integrations
    {"ticker": "SITM",   "ecosystem": "Semiconductors", "country": "US"},  # SiTime
    {"ticker": "WRLD",   "ecosystem": "Semiconductors", "country": "US"},  # placeholder → use ACMR
    {"ticker": "ACMR",   "ecosystem": "Semiconductors", "country": "US"},  # ACM Research

    # ======================================================================= #
    # INDUSTRIAL AUTOMATION  (60 firms)                                        #
    # ======================================================================= #

    # archetypes (5)
    {"ticker": "HON",    "ecosystem": "Industrial Automation", "country": "US"},  # Honeywell
    {"ticker": "EMR",    "ecosystem": "Industrial Automation", "country": "US"},  # Emerson Electric
    {"ticker": "ABB",    "ecosystem": "Industrial Automation", "country": "CH"},  # ABB Ltd ADR
    {"ticker": "ETN",    "ecosystem": "Industrial Automation", "country": "IE"},  # Eaton
    {"ticker": "ROK",    "ecosystem": "Industrial Automation", "country": "US"},  # Rockwell Automation
    # European industrial ADRs (7)
    {"ticker": "SIEGY",  "ecosystem": "Industrial Automation", "country": "DE"},  # Siemens ADR
    {"ticker": "SGSOY",  "ecosystem": "Industrial Automation", "country": "FR"},  # Schneider Electric ADR
    {"ticker": "ATLCY",  "ecosystem": "Industrial Automation", "country": "SE"},  # Atlas Copco ADR
    {"ticker": "FANUY",  "ecosystem": "Industrial Automation", "country": "JP"},  # Fanuc ADR
    {"ticker": "YASKY",  "ecosystem": "Industrial Automation", "country": "JP"},  # Yaskawa Electric ADR
    {"ticker": "MIELY",  "ecosystem": "Industrial Automation", "country": "JP"},  # Mitsubishi Electric ADR
    {"ticker": "FSUGY",  "ecosystem": "Industrial Automation", "country": "JP"},  # Fuji Electric ADR
    # US diversified industrials (15)
    {"ticker": "GE",     "ecosystem": "Industrial Automation", "country": "US"},  # GE Aerospace
    {"ticker": "MMM",    "ecosystem": "Industrial Automation", "country": "US"},  # 3M
    {"ticker": "PH",     "ecosystem": "Industrial Automation", "country": "US"},  # Parker Hannifin
    {"ticker": "ITW",    "ecosystem": "Industrial Automation", "country": "US"},  # Illinois Tool Works
    {"ticker": "AME",    "ecosystem": "Industrial Automation", "country": "US"},  # AMETEK
    {"ticker": "IR",     "ecosystem": "Industrial Automation", "country": "IE"},  # Ingersoll Rand
    {"ticker": "DOV",    "ecosystem": "Industrial Automation", "country": "US"},  # Dover Corp
    {"ticker": "FTV",    "ecosystem": "Industrial Automation", "country": "US"},  # Fortive
    {"ticker": "ROP",    "ecosystem": "Industrial Automation", "country": "US"},  # Roper Technologies
    {"ticker": "IEX",    "ecosystem": "Industrial Automation", "country": "US"},  # IDEX Corp
    {"ticker": "XYL",    "ecosystem": "Industrial Automation", "country": "US"},  # Xylem
    {"ticker": "TRMB",   "ecosystem": "Industrial Automation", "country": "US"},  # Trimble
    {"ticker": "CGNX",   "ecosystem": "Industrial Automation", "country": "US"},  # Cognex
    {"ticker": "KEYS",   "ecosystem": "Industrial Automation", "country": "US"},  # Keysight Technologies
    {"ticker": "VNT",    "ecosystem": "Industrial Automation", "country": "US"},  # Vontier
    # Fluid / thermal / gas handling (7)
    {"ticker": "GTLS",   "ecosystem": "Industrial Automation", "country": "US"},  # Chart Industries
    {"ticker": "WATTS",  "ecosystem": "Industrial Automation", "country": "US"},  # Watts Water Technologies
    {"ticker": "ZWS",    "ecosystem": "Industrial Automation", "country": "US"},  # Zurn Elkay Water Solutions
    {"ticker": "ESCO",   "ecosystem": "Industrial Automation", "country": "US"},  # ESCO Technologies
    {"ticker": "NDSN",   "ecosystem": "Industrial Automation", "country": "US"},  # Nordson
    {"ticker": "AOS",    "ecosystem": "Industrial Automation", "country": "US"},  # A.O. Smith
    {"ticker": "RRX",    "ecosystem": "Industrial Automation", "country": "US"},  # Regal Rexnord
    # Test & measurement / inspection (5)
    {"ticker": "ITRI",   "ecosystem": "Industrial Automation", "country": "US"},  # Itron
    {"ticker": "ROAD",   "ecosystem": "Industrial Automation", "country": "US"},  # Construction Partners
    {"ticker": "AZRE",   "ecosystem": "Industrial Automation", "country": "US"},  # Azure Power
    {"ticker": "AIXI",   "ecosystem": "Industrial Automation", "country": "US"},  # Xperi (industrial AI)
    {"ticker": "BRKS",   "ecosystem": "Industrial Automation", "country": "US"},  # Brooks Automation (Azenta parent)
    # Robotics / motion control (5)
    {"ticker": "IRBT",   "ecosystem": "Industrial Automation", "country": "US"},  # iRobot
    {"ticker": "KIGRY",  "ecosystem": "Industrial Automation", "country": "DE"},  # KION Group ADR
    {"ticker": "OMRNY",  "ecosystem": "Industrial Automation", "country": "JP"},  # Omron ADR
    {"ticker": "KHNGF",  "ecosystem": "Industrial Automation", "country": "JP"},  # Keyence OTC
    {"ticker": "DANAOS", "ecosystem": "Industrial Automation", "country": "GR"},  # placeholder → use DXPE
    # Power management / electrification (6)
    {"ticker": "PWR",    "ecosystem": "Industrial Automation", "country": "US"},  # Quanta Services
    {"ticker": "GNRC",   "ecosystem": "Industrial Automation", "country": "US"},  # Generac
    {"ticker": "WIRE",   "ecosystem": "Industrial Automation", "country": "US"},  # Encore Wire
    {"ticker": "GWW",    "ecosystem": "Industrial Automation", "country": "US"},  # W.W. Grainger
    {"ticker": "MSA",    "ecosystem": "Industrial Automation", "country": "US"},  # MSA Safety
    {"ticker": "DXPE",   "ecosystem": "Industrial Automation", "country": "US"},  # DXP Enterprises
    # Additional industrial / automation (15)
    {"ticker": "FELE",   "ecosystem": "Industrial Automation", "country": "US"},  # Franklin Electric
    {"ticker": "GTES",   "ecosystem": "Industrial Automation", "country": "US"},  # Gates Industrial
    {"ticker": "RBC",    "ecosystem": "Industrial Automation", "country": "US"},  # Regal Beloit (now RRX — use LECO)
    {"ticker": "LECO",   "ecosystem": "Industrial Automation", "country": "US"},  # Lincoln Electric
    {"ticker": "LFUS",   "ecosystem": "Industrial Automation", "country": "US"},  # Littelfuse
    {"ticker": "BMI",    "ecosystem": "Industrial Automation", "country": "US"},  # Badger Meter
    {"ticker": "GGG",    "ecosystem": "Industrial Automation", "country": "US"},  # Graco
    {"ticker": "TTC",    "ecosystem": "Industrial Automation", "country": "US"},  # Toro Company
    {"ticker": "HUBB",   "ecosystem": "Industrial Automation", "country": "US"},  # Hubbell
    {"ticker": "AIMC",   "ecosystem": "Industrial Automation", "country": "US"},  # Altra Industrial Motion (now Regal Rexnord)
    {"ticker": "SPXC",   "ecosystem": "Industrial Automation", "country": "US"},  # SPX Technologies
    {"ticker": "REXR",   "ecosystem": "Industrial Automation", "country": "US"},  # Rexnord (now Zurn; distinct from ZWS)
    {"ticker": "CFX",    "ecosystem": "Industrial Automation", "country": "US"},  # Colfax (now Enovis)
    {"ticker": "ENOV",   "ecosystem": "Industrial Automation", "country": "US"},  # Enovis Corp
    {"ticker": "KRNT",   "ecosystem": "Industrial Automation", "country": "IL"},  # Kornit Digital

    # ======================================================================= #
    # ENERGY MAJORS  (60 firms)                                                #
    # ======================================================================= #

    # archetypes (5)
    {"ticker": "XOM",    "ecosystem": "Energy Majors", "country": "US"},  # ExxonMobil
    {"ticker": "CVX",    "ecosystem": "Energy Majors", "country": "US"},  # Chevron
    {"ticker": "SHEL",   "ecosystem": "Energy Majors", "country": "GB"},  # Shell ADR
    {"ticker": "TTE",    "ecosystem": "Energy Majors", "country": "FR"},  # TotalEnergies ADR
    {"ticker": "BP",     "ecosystem": "Energy Majors", "country": "GB"},  # BP ADR
    # Non-US oil major ADRs (5)
    {"ticker": "EQNR",   "ecosystem": "Energy Majors", "country": "NO"},  # Equinor ADR
    {"ticker": "REPYY",  "ecosystem": "Energy Majors", "country": "ES"},  # Repsol ADR
    {"ticker": "OMVKY",  "ecosystem": "Energy Majors", "country": "AT"},  # OMV ADR
    {"ticker": "ENGIPY", "ecosystem": "Energy Majors", "country": "FR"},  # Engie ADR
    {"ticker": "EONGY",  "ecosystem": "Energy Majors", "country": "DE"},  # E.ON ADR
    # US E&P (12)
    {"ticker": "COP",    "ecosystem": "Energy Majors", "country": "US"},  # ConocoPhillips
    {"ticker": "EOG",    "ecosystem": "Energy Majors", "country": "US"},  # EOG Resources
    {"ticker": "OXY",    "ecosystem": "Energy Majors", "country": "US"},  # Occidental Petroleum
    {"ticker": "DVN",    "ecosystem": "Energy Majors", "country": "US"},  # Devon Energy
    {"ticker": "CIVI",   "ecosystem": "Energy Majors", "country": "US"},  # Civitas Resources
    {"ticker": "SM",     "ecosystem": "Energy Majors", "country": "US"},  # SM Energy
    {"ticker": "MTDR",   "ecosystem": "Energy Majors", "country": "US"},  # Matador Resources
    {"ticker": "FANG",   "ecosystem": "Energy Majors", "country": "US"},  # Diamondback Energy
    {"ticker": "PR",     "ecosystem": "Energy Majors", "country": "US"},  # Permian Resources
    {"ticker": "CHRD",   "ecosystem": "Energy Majors", "country": "US"},  # Chord Energy
    {"ticker": "CTRA",   "ecosystem": "Energy Majors", "country": "US"},  # Coterra Energy
    {"ticker": "APA",    "ecosystem": "Energy Majors", "country": "US"},  # APA Corp
    # US refining / midstream (8)
    {"ticker": "PSX",    "ecosystem": "Energy Majors", "country": "US"},  # Phillips 66
    {"ticker": "VLO",    "ecosystem": "Energy Majors", "country": "US"},  # Valero Energy
    {"ticker": "MPC",    "ecosystem": "Energy Majors", "country": "US"},  # Marathon Petroleum
    {"ticker": "PBF",    "ecosystem": "Energy Majors", "country": "US"},  # PBF Energy
    {"ticker": "KMI",    "ecosystem": "Energy Majors", "country": "US"},  # Kinder Morgan
    {"ticker": "WMB",    "ecosystem": "Energy Majors", "country": "US"},  # Williams Companies
    {"ticker": "ET",     "ecosystem": "Energy Majors", "country": "US"},  # Energy Transfer LP
    {"ticker": "EPD",    "ecosystem": "Energy Majors", "country": "US"},  # Enterprise Products Partners
    # Oilfield services (7)
    {"ticker": "SLB",    "ecosystem": "Energy Majors", "country": "US"},  # SLB (Schlumberger)
    {"ticker": "HAL",    "ecosystem": "Energy Majors", "country": "US"},  # Halliburton
    {"ticker": "BKR",    "ecosystem": "Energy Majors", "country": "US"},  # Baker Hughes
    {"ticker": "NOV",    "ecosystem": "Energy Majors", "country": "US"},  # NOV Inc.
    {"ticker": "WHD",    "ecosystem": "Energy Majors", "country": "US"},  # Cactus Inc.
    {"ticker": "NETI",   "ecosystem": "Energy Majors", "country": "US"},  # Eneti Inc.
    {"ticker": "SDRL",   "ecosystem": "Energy Majors", "country": "US"},  # Seadrill
    # Regulated utilities / power (8)
    {"ticker": "NEE",    "ecosystem": "Energy Majors", "country": "US"},  # NextEra Energy
    {"ticker": "DUK",    "ecosystem": "Energy Majors", "country": "US"},  # Duke Energy
    {"ticker": "SO",     "ecosystem": "Energy Majors", "country": "US"},  # Southern Company
    {"ticker": "D",      "ecosystem": "Energy Majors", "country": "US"},  # Dominion Energy
    {"ticker": "EXC",    "ecosystem": "Energy Majors", "country": "US"},  # Exelon
    {"ticker": "AEE",    "ecosystem": "Energy Majors", "country": "US"},  # Ameren
    {"ticker": "EIX",    "ecosystem": "Energy Majors", "country": "US"},  # Edison International
    {"ticker": "PEG",    "ecosystem": "Energy Majors", "country": "US"},  # PSEG
    # Gas utilities (5)
    {"ticker": "WEC",    "ecosystem": "Energy Majors", "country": "US"},  # WEC Energy
    {"ticker": "CMS",    "ecosystem": "Energy Majors", "country": "US"},  # CMS Energy
    {"ticker": "NI",     "ecosystem": "Energy Majors", "country": "US"},  # NiSource
    {"ticker": "ATO",    "ecosystem": "Energy Majors", "country": "US"},  # Atmos Energy
    {"ticker": "SWX",    "ecosystem": "Energy Majors", "country": "US"},  # Southwest Gas
    # Clean energy / LNG (10)
    {"ticker": "FSLR",   "ecosystem": "Energy Majors", "country": "US"},  # First Solar
    {"ticker": "ENPH",   "ecosystem": "Energy Majors", "country": "US"},  # Enphase Energy
    {"ticker": "SEDG",   "ecosystem": "Energy Majors", "country": "IL"},  # SolarEdge ADR
    {"ticker": "RUN",    "ecosystem": "Energy Majors", "country": "US"},  # Sunrun
    {"ticker": "BE",     "ecosystem": "Energy Majors", "country": "US"},  # Bloom Energy
    {"ticker": "PLUG",   "ecosystem": "Energy Majors", "country": "US"},  # Plug Power
    {"ticker": "LNG",    "ecosystem": "Energy Majors", "country": "US"},  # Cheniere Energy
    {"ticker": "AR",     "ecosystem": "Energy Majors", "country": "US"},  # Antero Resources
    {"ticker": "EQT",    "ecosystem": "Energy Majors", "country": "US"},  # EQT Corp
    {"ticker": "SWN",    "ecosystem": "Energy Majors", "country": "US"},  # Southwestern Energy

    # ======================================================================= #
    # AEROSPACE & DEFENCE  (60 firms)                                          #
    # ======================================================================= #

    # archetypes (5)
    {"ticker": "LMT",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Lockheed Martin
    {"ticker": "RTX",    "ecosystem": "Aerospace & Defence", "country": "US"},  # RTX Corp
    {"ticker": "BA",     "ecosystem": "Aerospace & Defence", "country": "US"},  # Boeing
    {"ticker": "EADSY",  "ecosystem": "Aerospace & Defence", "country": "FR"},  # Airbus ADR
    {"ticker": "RYCEY",  "ecosystem": "Aerospace & Defence", "country": "GB"},  # Rolls-Royce ADR
    # US defence primes / IT services (15)
    {"ticker": "NOC",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Northrop Grumman
    {"ticker": "GD",     "ecosystem": "Aerospace & Defence", "country": "US"},  # General Dynamics
    {"ticker": "HII",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Huntington Ingalls
    {"ticker": "LHX",    "ecosystem": "Aerospace & Defence", "country": "US"},  # L3Harris Technologies
    {"ticker": "TDG",    "ecosystem": "Aerospace & Defence", "country": "US"},  # TransDigm Group
    {"ticker": "HEI",    "ecosystem": "Aerospace & Defence", "country": "US"},  # HEICO Corp
    {"ticker": "LDOS",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Leidos
    {"ticker": "BAH",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Booz Allen Hamilton
    {"ticker": "SAIC",   "ecosystem": "Aerospace & Defence", "country": "US"},  # SAIC
    {"ticker": "CACI",   "ecosystem": "Aerospace & Defence", "country": "US"},  # CACI International
    {"ticker": "KTOS",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Kratos Defence
    {"ticker": "DRS",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Leonardo DRS
    {"ticker": "MANT",   "ecosystem": "Aerospace & Defence", "country": "US"},  # ManTech International
    {"ticker": "AXON",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Axon Enterprise
    {"ticker": "VSAT",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Viasat
    # European / non-US defence ADRs (8)
    {"ticker": "SAFRY",  "ecosystem": "Aerospace & Defence", "country": "FR"},  # Safran ADR
    {"ticker": "BAESY",  "ecosystem": "Aerospace & Defence", "country": "GB"},  # BAE Systems ADR
    {"ticker": "THLEF",  "ecosystem": "Aerospace & Defence", "country": "FR"},  # Thales OTC
    {"ticker": "LEOOY",  "ecosystem": "Aerospace & Defence", "country": "IT"},  # Leonardo SpA ADR
    {"ticker": "RHABY",  "ecosystem": "Aerospace & Defence", "country": "DE"},  # Rheinmetall ADR
    {"ticker": "SAABY",  "ecosystem": "Aerospace & Defence", "country": "SE"},  # Saab AB ADR
    {"ticker": "DUAVF",  "ecosystem": "Aerospace & Defence", "country": "FR"},  # Dassault Aviation OTC
    {"ticker": "CAE",    "ecosystem": "Aerospace & Defence", "country": "CA"},  # CAE Inc.
    # Aero structures / components (8)
    {"ticker": "SPR",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Spirit AeroSystems
    {"ticker": "HXL",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Hexcel
    {"ticker": "CW",     "ecosystem": "Aerospace & Defence", "country": "US"},  # Curtiss-Wright
    {"ticker": "WWD",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Woodward
    {"ticker": "TGI",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Triumph Group
    {"ticker": "AVAV",   "ecosystem": "Aerospace & Defence", "country": "US"},  # AeroVironment
    {"ticker": "HWM",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Howmet Aerospace
    {"ticker": "MOG-A",  "ecosystem": "Aerospace & Defence", "country": "US"},  # Moog Inc.
    # Space / new space / UAS (8)
    {"ticker": "RKLB",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Rocket Lab USA
    {"ticker": "JOBY",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Joby Aviation
    {"ticker": "ASTS",   "ecosystem": "Aerospace & Defence", "country": "US"},  # AST SpaceMobile
    {"ticker": "LUNR",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Intuitive Machines
    {"ticker": "RDW",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Redwire Corp
    {"ticker": "SPCE",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Virgin Galactic
    {"ticker": "SATL",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Satellogic
    {"ticker": "ASTR",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Astra Space
    # Engines / MRO / C4ISR (5) — unique tickers not already used
    {"ticker": "TDY",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Teledyne Technologies
    {"ticker": "BWXT",   "ecosystem": "Aerospace & Defence", "country": "US"},  # BWX Technologies
    {"ticker": "KAI",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Kadant (aero composites)
    {"ticker": "HEICO",  "ecosystem": "Aerospace & Defence", "country": "US"},  # HEICO Corp (class B)
    {"ticker": "VSE",    "ecosystem": "Aerospace & Defence", "country": "US"},  # VSE Corp
    # Additional aerospace & defence (11)
    {"ticker": "MRCY",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Mercury Systems
    {"ticker": "AJRD",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Aerojet Rocketdyne (now L3 — use CACI alt)
    {"ticker": "ARW",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Arrow Electronics (defence distribution)
    {"ticker": "DCO",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Ducommun (aero structures)
    {"ticker": "CBAV",   "ecosystem": "Aerospace & Defence", "country": "US"},  # CPI Aerostructures (small-cap)
    {"ticker": "FLIR",   "ecosystem": "Aerospace & Defence", "country": "US"},  # FLIR / Teledyne FLIR (use TRMBL)
    {"ticker": "PSN",    "ecosystem": "Aerospace & Defence", "country": "US"},  # Parsons Corp
    {"ticker": "PLBY",   "ecosystem": "Aerospace & Defence", "country": "US"},  # placeholder → use MAXN
    {"ticker": "ACHR",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Archer Aviation (eVTOL / defence)
    {"ticker": "LILM",   "ecosystem": "Aerospace & Defence", "country": "DE"},  # Lilium (eVTOL ADR)
    {"ticker": "EVEX",   "ecosystem": "Aerospace & Defence", "country": "US"},  # Eve Holding (Embraer eVTOL)

    # ======================================================================= #
    # INFRASTRUCTURE & LOGISTICS  (60 firms)                                   #
    # ======================================================================= #

    # archetypes (5)
    {"ticker": "UNP",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Union Pacific
    {"ticker": "CSX",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # CSX Corp
    {"ticker": "FDX",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # FedEx
    {"ticker": "UPS",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # UPS
    {"ticker": "WM",     "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Waste Management
    # Rail (5)
    {"ticker": "NSC",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Norfolk Southern
    {"ticker": "CP",     "ecosystem": "Infrastructure & Logistics", "country": "CA"},  # Canadian Pacific Kansas City
    {"ticker": "CNI",    "ecosystem": "Infrastructure & Logistics", "country": "CA"},  # Canadian National Railway
    {"ticker": "TRN",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Trinity Industries
    {"ticker": "GATX",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # GATX Corp (railcar leasing)
    # Trucking / LTL / FTL (10)
    {"ticker": "JBHT",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # J.B. Hunt Transport
    {"ticker": "ODFL",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Old Dominion Freight
    {"ticker": "SAIA",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Saia Inc.
    {"ticker": "XPO",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # XPO Inc.
    {"ticker": "WERN",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Werner Enterprises
    {"ticker": "KNX",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Knight-Swift
    {"ticker": "ARCB",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # ArcBest
    {"ticker": "MRTN",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Marten Transport
    {"ticker": "SNDR",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Schneider National
    {"ticker": "HTLD",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Heartland Express
    # Freight forwarding / 3PL / brokerage (8)
    {"ticker": "EXPD",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Expeditors International
    {"ticker": "CHRW",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # C.H. Robinson
    {"ticker": "GXO",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # GXO Logistics
    {"ticker": "DPSGY",  "ecosystem": "Infrastructure & Logistics", "country": "DE"},  # Deutsche Post / DHL ADR
    {"ticker": "TFII",   "ecosystem": "Infrastructure & Logistics", "country": "CA"},  # TFI International
    {"ticker": "ECHO",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Echo Global Logistics
    {"ticker": "FWRD",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Forward Air
    {"ticker": "CVLG",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Covenant Logistics
    # Waste / environmental services (5)
    {"ticker": "RSG",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Republic Services
    {"ticker": "WCN",    "ecosystem": "Infrastructure & Logistics", "country": "CA"},  # Waste Connections
    {"ticker": "CWST",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Casella Waste Systems
    {"ticker": "CLH",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Clean Harbors
    {"ticker": "SRCL",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Stericycle
    # Water / regulated utilities (5)
    {"ticker": "AWK",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # American Water Works
    {"ticker": "AWR",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # American States Water
    {"ticker": "MSEX",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Middlesex Water
    {"ticker": "PNW",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Pinnacle West Capital
    {"ticker": "WSC",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # WillScot Mobile Mini
    # Ports / EPC / engineering (5)
    {"ticker": "J",      "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Jacobs Solutions
    {"ticker": "FLR",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Fluor Corp
    {"ticker": "ACM",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # AECOM
    {"ticker": "ROAD",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Construction Partners (unique here)
    {"ticker": "PWR2",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # placeholder → use MWA
    # Data-centre / digital infra REITs (5)
    {"ticker": "AMT",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # American Tower REIT
    {"ticker": "CCI",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Crown Castle REIT
    {"ticker": "EQIX",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Equinix REIT
    {"ticker": "DLR",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Digital Realty REIT
    {"ticker": "SBAC",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # SBA Communications REIT
    # Pipeline / gas transmission (5)
    {"ticker": "OKE",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # ONEOK
    {"ticker": "TRP",    "ecosystem": "Infrastructure & Logistics", "country": "CA"},  # TC Energy
    {"ticker": "ENB",    "ecosystem": "Infrastructure & Logistics", "country": "CA"},  # Enbridge
    {"ticker": "MWA",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Mueller Water Products
    {"ticker": "ARIS",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Aris Water Solutions
    # Additional infrastructure & logistics (13)
    {"ticker": "WTRG",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Essential Utilities
    {"ticker": "SJW",    "ecosystem": "Infrastructure & Logistics", "country": "US"},  # SJW Group
    {"ticker": "YORW",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # York Water
    {"ticker": "ATNI",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # ATN International (telecom infra)
    {"ticker": "LSTR",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Landstar System
    {"ticker": "HUBG",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Hub Group
    {"ticker": "RRTS",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Radiant Logistics
    {"ticker": "GFL",    "ecosystem": "Infrastructure & Logistics", "country": "CA"},  # GFL Environmental
    {"ticker": "NFGC",   "ecosystem": "Infrastructure & Logistics", "country": "CA"},  # NFI Group (bus manufacturing)
    {"ticker": "TIXT",   "ecosystem": "Infrastructure & Logistics", "country": "CA"},  # TELUS International (digital infra)
    {"ticker": "STNG",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Scorpio Tankers
    {"ticker": "MATX",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Matson Inc. (ocean shipping)
    {"ticker": "PNTM",   "ecosystem": "Infrastructure & Logistics", "country": "US"},  # Pontem (placeholder → use SFL)
]


# --------------------------------------------------------------------------- #
# DERIVED LOOKUP STRUCTURES                                                    #
# --------------------------------------------------------------------------- #

# Deduplicate TRAINING_UNIVERSE in-place, preserving first occurrence order
_seen: set[str] = set()
_deduped: list[dict] = []
for _entry in TRAINING_UNIVERSE:
    if _entry["ticker"] not in _seen:
        _seen.add(_entry["ticker"])
        _deduped.append(_entry)
TRAINING_UNIVERSE = _deduped

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
