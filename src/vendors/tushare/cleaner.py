import pandas as pd
from tqdm import tqdm

from .config import DataRawPath, DataCleanPath

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

REQ_TRADE_CALENDAR_FIELDS = [
    "datetime",
    "symbol",
    "is_trading",
]


def clean_1day_bar(dt: pd.Timestamp, replace: bool = False) -> bool:
    """
    Clean 1day bar data (downloaded by date) from Tushare.
    """
    
    output_filename = (
        DataCleanPath().bar_1day_dir / f"{dt.strftime('%Y-%m-%d')}.parquet"
    )

    if not replace and output_filename.exists():
        return True

    input_filename = DataRawPath().bar_1day_dir / f"{dt.strftime('%Y-%m-%d')}.parquet"

    # Load data
    try:
        df = pd.read_parquet(input_filename)
    except FileNotFoundError:
        print(f"Warning: File not found: {input_filename}")
        return False

    # Align column names
    # Rename columns to match Bar model
    # Tushare: trade_date, open, high, low, close, vol, amount
    df = df.rename(
        columns={
            "trade_date": "datetime",
            "ts_code": "symbol",
            "vol": "volume",
        }
    )

    # Unit
    df["volume"] *= 100
    df["amount"] *= 1000

    # Add columns
    df["vwap"] = df["amount"] / df["volume"]

    output_filename.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_filename)
    return True


def clean_1day_bar_range(start_date: str, end_date: str, replace: bool = False):
    dates = pd.date_range(start=start_date, end=end_date)
    for dt in tqdm(dates):
        clean_1day_bar(dt, replace=replace)
