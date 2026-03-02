import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")
# Default paths are relative to current working directory if not specified
DATA_RAW_DIR = Path(os.getenv("DATA_RAW_DIR", "data/raw"))
DATA_CLEAN_DIR = Path(os.getenv("DATA_CLEAN_DIR", "data/clean"))

REQ_TRADE_CALENDAR_FIELDS = [
    "exchange",
    "calendar_date",
    "is_open",
    "pre_trade_date",
]

REQ_IDENTITY_FIELDS = [
    "symbol",
    "chinese_name",
    "english_name",
    "location",
    "sector",
    "industry",
    "board",
    "exchange",
    "list_date",
    "delist_date",
]

REQ_1D_BAR_FIELDS = [
    "datetime",
    "symbol",
    "open",
    "high",
    "low",
    "close",
    "vwap",
    "volume",
    "amount",
]

REQ_ADJ_FACTOR_FIELDS = [
    "datetime",
    "symbol",
    "adj_factor",
]


REQ_CAP_FIELDS = [
    "datetime",
    "symbol",
    "shares_out",
    "shares_float",
    "shares_ff",
    "cap_total",
    "cap_float",
    "cap_ff",
]

REQ_VALUATION_FIELDS = [
    "datetime",
    "symbol",
    "pe",
    "pb",
    "ps",
    "pe_ttm",
    "ps_ttm",
]


class DataRawPath:
    def __init__(self):
        # Base directory for tushare raw data
        self.base_dir = DATA_RAW_DIR / "tushare"

        self.trade_calendar_dir = self.base_dir / "trade_calendar"
        self.ticker_mapper_dir = self.base_dir / "ticker_mapper"
        self.bar_dir = self.base_dir / "bar"
        self.bar_1min_dir = self.bar_dir / "1min"
        self.bar_1day_dir = self.bar_dir / "1day"
        self.adj_factor_dir = self.base_dir / "adj_factor"

        self.basic_dir = self.base_dir / "basic"


class DataCleanPath:
    def __init__(self):
        # Base directory for clean data
        self.base_dir = DATA_CLEAN_DIR

        # Subdirectories for tushare clean data
        self.trade_calendar_dir = self.base_dir / "trade_calendar" / "tushare"
        self.identity_dir = self.base_dir / "identity" / "tushare"
        self.bar_1min_dir = self.base_dir / "bar" / "1min" / "tushare"
        self.bar_1day_dir = self.base_dir / "bar" / "1day" / "tushare"
        self.adj_factor_dir = self.base_dir / "adj_factor" / "tushare"

        self.cap_dir = self.base_dir / "cap" / "tushare"
        self.valuation_dir = self.base_dir / "valuation" / "tushare"
