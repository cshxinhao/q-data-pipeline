import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default paths are relative to current working directory if not specified
DATA_RAW_DIR = Path(os.getenv("DATA_RAW_DIR", "data/raw"))
DATA_CLEAN_DIR = Path(os.getenv("DATA_CLEAN_DIR", "data/clean"))
DATA_REALTIME_DIR = Path(os.getenv("DATA_REALTIME_DIR", "data/realtime"))


# No need this class
class __DataRawPath:
    def __init__(self):
        # Base directory for xtquant raw data
        self.base_dir = DATA_RAW_DIR / "xtquant"

    def get_custom_path(self, folder_name: str):
        return self._ensure_dir(self.base_dir / folder_name)

    def _ensure_dir(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        return path


class DataRealtimePath:
    def __init__(self):
        # Base directory for real-time data
        self.base_dir = DATA_REALTIME_DIR / "xtquant"

    @property
    def reatime_quote(self):
        return self._ensure_dir(self.base_dir / "realtime_quote")

    def _ensure_dir(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        return path


class DataCleanPath:
    def __init__(self):
        # Base directory for clean data
        self.base_dir = DATA_CLEAN_DIR

    @property
    def reatime_quote(self):
        return self._ensure_dir(self.base_dir / "realtime_quote" / "xtquant")

    @property
    def trade_calendar(self):
        return self._ensure_dir(self.base_dir / "trade_calendar" / "xtquant")

    @property
    def identity(self):
        return self._ensure_dir(self.base_dir / "identity" / "xtquant")

    @property
    def bar_1min(self):
        return self._ensure_dir(self.base_dir / "bar" / "1min" / "xtquant")

    @property
    def bar_1day(self):
        return self._ensure_dir(self.base_dir / "bar" / "1day" / "xtquant")

    @property
    def adj_factor(self):
        return self._ensure_dir(self.base_dir / "adj_factor" / "xtquant")

    @property
    def cap(self):
        return self._ensure_dir(self.base_dir / "cap" / "xtquant")

    @property
    def valuation(self):
        return self._ensure_dir(self.base_dir / "valuation" / "xtquant")

    @property
    def dataset(self):
        return self._ensure_dir(self.base_dir / "dataset" / "xtquant")

    @property
    def listed_days(self):
        return self._ensure_dir(self.base_dir / "listed_days" / "xtquant")

    def get_custom_path(self, folder_name: str):
        return self._ensure_dir(self.base_dir / folder_name / "xtquant")

    def _ensure_dir(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        return path
