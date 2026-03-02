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


class DataRawPath:
    def __init__(self):
        # Base directory for tushare raw data
        self.base_dir = DATA_RAW_DIR / "tushare"
        
        self.trade_calendar_dir = self.base_dir / "trade_calendar"
        self.ticker_mapper_dir = self.base_dir / "ticker_mapper"
        self.bar_dir = self.base_dir / "bar_price"
        self.bar_1min_dir = self.bar_dir / "1min"
        self.bar_1day_dir = self.bar_dir / "1day"
        self.adj_dir = self.base_dir / "adj_factor"

        self.basic_dir = self.base_dir / "basic"


class DataCleanPath:
    def __init__(self):
        # Base directory for clean data
        self.base_dir = DATA_CLEAN_DIR
        
        # Subdirectories for tushare clean data
        self.trade_calendar_dir = self.base_dir / "trade_calendar" / "tushare"
        self.ticker_mapper_dir = self.base_dir / "ticker_mapper" / "tushare"
        self.bar_dir = self.base_dir / "bar_price" / "tushare"
        self.bar_1min_dir = self.bar_dir / "1min" / "tushare"
        self.bar_1day_dir = self.bar_dir / "1day" / "tushare"
        self.adj_dir = self.base_dir / "adj_factor" / "tushare"

        self.cap_dir = self.base_dir / "cap" / "tushare"
        self.valuation_dir = self.base_dir / "valuation" / "tushare"
