import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_RAW_DIR = Path(os.getenv("DATA_RAW_DIR", "data/raw"))
BASE_CLEAN_DIR = Path(os.getenv("DATA_CLEAN_DIR", "data/clean"))

DATA_RAW_DIR = BASE_RAW_DIR / "futu"
DATA_CLEAN_DIR = BASE_CLEAN_DIR / "futu"
