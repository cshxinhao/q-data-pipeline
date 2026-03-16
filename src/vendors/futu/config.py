import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables
FUTU_HOST = os.getenv("FUTU_HOST", "127.0.0.1")
FUTU_PORT = int(os.getenv("FUTU_PORT", 11111))

# Default paths are relative to current working directory if not specified
DATA_RAW_DIR = Path(os.getenv("DATA_RAW_DIR", "data/raw"))
DATA_CLEAN_DIR = Path(os.getenv("DATA_CLEAN_DIR", "data/clean"))


VENDOR_NAME = "futu"


class DataRawPath:
    def __init__(self, market: str):
        # Base directory for futu raw data
        assert market in ["HK", "US"], f"market {market} is not implemented"
        self.base_dir = DATA_RAW_DIR / VENDOR_NAME / market.lower()

    @property
    def plate_list(self):
        return self._ensure_dir(self.base_dir / "plate_list")

    @property
    def trade_calendar(self):
        return self._ensure_dir(self.base_dir / "trade_calendar")

    @property
    def ticker_mapper(self):
        return self._ensure_dir(self.base_dir / "ticker_mapper")

    @property
    def bar_1min(self):
        return self._ensure_dir(self.base_dir / "bar" / "1min")

    @property
    def bar_1day(self):
        return self._ensure_dir(self.base_dir / "bar" / "1day")

    @property
    def adj_factor(self):
        return self._ensure_dir(self.base_dir / "adj_factor")

    @property
    def owner_plate(self):
        return self._ensure_dir(self.base_dir / "owner_plate")

    def get_custom_path(self, folder_name: str):
        return self._ensure_dir(self.base_dir / folder_name)

    def _ensure_dir(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        return path


class DataCleanPath:
    def __init__(self, market: str):
        # Base directory for clean data
        assert market in ["HK", "US"], f"market {market} is not implemented"
        self.base_dir = DATA_CLEAN_DIR / market.lower()

    @property
    def trade_calendar(self):
        return self._ensure_dir(self.base_dir / "trade_calendar" / VENDOR_NAME)

    @property
    def identity(self):
        return self._ensure_dir(self.base_dir / "identity" / VENDOR_NAME)

    @property
    def bar_1min(self):
        return self._ensure_dir(self.base_dir / "bar" / "1min" / VENDOR_NAME)

    @property
    def bar_1day(self):
        return self._ensure_dir(self.base_dir / "bar" / "1day" / VENDOR_NAME)

    @property
    def adj_factor(self):
        return self._ensure_dir(self.base_dir / "adj_factor" / VENDOR_NAME)

    @property
    def cap(self):
        return self._ensure_dir(self.base_dir / "cap" / VENDOR_NAME)

    @property
    def valuation(self):
        return self._ensure_dir(self.base_dir / "valuation" / VENDOR_NAME)

    @property
    def dataset(self):
        return self._ensure_dir(self.base_dir / "dataset" / VENDOR_NAME)

    @property
    def listed_days(self):
        return self._ensure_dir(self.base_dir / "listed_days" / VENDOR_NAME)

    def get_custom_path(self, folder_name: str):
        return self._ensure_dir(self.base_dir / folder_name / VENDOR_NAME)

    def _ensure_dir(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        return path
