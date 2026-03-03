import pandas as pd
from pathlib import Path

from src.logger import logger
from .config import (
    DataRawPath,
    DataCleanPath,
)
from src.common.schema import (
    REQ_TRADE_CALENDAR_FIELDS,
    REQ_IDENTITY_FIELDS,
    REQ_1D_BAR_FIELDS,
    REQ_ADJ_FACTOR_FIELDS,
    REQ_CAP_FIELDS,
    REQ_VALUATION_FIELDS,
)


def clean_trade_calendar():
    input_filename = DataRawPath().trade_calendar / "trade_calendar.parquet"
    output_filename = DataCleanPath().trade_calendar / "trade_calendar.parquet"

    # Load data
    try:
        df = pd.read_parquet(input_filename)
    except FileNotFoundError:
        logger.warning(f"File not found: {input_filename}")
        return False

    # Align column names
    df = df.rename(
        columns={
            "cal_date": "calendar_date",
            "pretrade_date": "pre_trade_date",
        }
    )
    df["calendar_date"] = pd.to_datetime(df["calendar_date"])
    df["pre_trade_date"] = pd.to_datetime(df["pre_trade_date"])

    df = df[REQ_TRADE_CALENDAR_FIELDS]
    df.to_parquet(output_filename, index=False)
    return True


def clean_identity():
    input_filename = DataRawPath().ticker_mapper / "ticker_mapper.parquet"
    output_filename = DataCleanPath().identity / "identity.parquet"

    # Load data
    try:
        df = pd.read_parquet(input_filename)
    except FileNotFoundError:
        logger.warning(f"File not found: {input_filename}")
        return False

    # Align column names
    df = df.drop(columns=["symbol"])  # Drop its original symbol
    df = df.rename(
        columns={
            "ts_code": "symbol",
            "name": "chinese_name",
            "enname": "english_name",
            "area": "location",
            "market": "board",
        }
    )
    df["list_date"] = pd.to_datetime(df["list_date"])
    df["delist_date"] = pd.to_datetime(df["delist_date"])
    df["delist_date"] = df["delist_date"].where(~df["delist_date"].isna(), "2099-12-31")

    # Map board to board type
    df["board"] = df["board"].map(
        {
            "主板": "MAIN",
            "创业板": "CHINEXT",
            "科创板": "STAR",
            "北交所": "BSE",
        }
    )

    df = df.reindex(columns=REQ_IDENTITY_FIELDS)
    df.to_parquet(output_filename, index=False)
    return True


def _clean_1day_bar_for_dt(dt: pd.Timestamp, replace: bool = False) -> bool:
    """
    Clean 1day bar data (downloaded by date) from Tushare.
    """

    output_filename = DataCleanPath().bar_1day / f"{dt.strftime('%Y-%m-%d')}.parquet"

    if not replace and output_filename.exists():
        return True

    input_filename = DataRawPath().bar_1day / f"{dt.strftime('%Y-%m-%d')}.parquet"

    # Load data
    try:
        df = pd.read_parquet(input_filename)
    except FileNotFoundError:
        logger.warning(f"File not found: {input_filename}")
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

    df["datetime"] = pd.to_datetime(df["datetime"])

    # Unit
    df["volume"] *= 100
    df["amount"] *= 1000

    # Add columns
    df["vwap"] = df["amount"] / df["volume"]

    # Extract required fields
    df = df.reindex(columns=REQ_1D_BAR_FIELDS)

    df.to_parquet(output_filename, index=False)
    return True


def clean_1day_bar(start_date: str, end_date: str, replace: bool = False):
    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    for dt in dates:
        _clean_1day_bar_for_dt(dt, replace=replace)
        logger.info(f"{dt}: clean 1day bar data done ...")


def _clean_adj_factor_for_dt(dt: pd.Timestamp, replace: bool = False) -> bool:
    """
    Clean adj factor data (downloaded by date) from Tushare.
    """
    output_filename = DataCleanPath().adj_factor / f"{dt.strftime('%Y-%m-%d')}.parquet"

    if not replace and output_filename.exists():
        return True

    input_filename = DataRawPath().adj_factor / f"{dt.strftime('%Y-%m-%d')}.parquet"

    # Load data
    try:
        df = pd.read_parquet(input_filename)
    except FileNotFoundError:
        logger.warning(f"File not found: {input_filename}")
        return False

    # Align column names
    # Rename columns to match AdjFactor model
    # Tushare: trade_date, ts_code, adj_factor
    df = df.rename(
        columns={
            "trade_date": "datetime",
            "ts_code": "symbol",
        }
    )

    df["datetime"] = pd.to_datetime(df["datetime"])

    # Extract required fields
    df = df.reindex(columns=REQ_ADJ_FACTOR_FIELDS)

    df.to_parquet(output_filename, index=False)
    return True


def clean_adj_factor(start_date: str, end_date: str, replace: bool = False):
    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    for dt in dates:
        _clean_adj_factor_for_dt(dt, replace=replace)
        logger.info(f"{dt}: clean adj factor data done ...")


def _clean_cap_for_dt(dt: pd.Timestamp, replace: bool = False) -> bool:
    """
    Clean cap data (downloaded by date) from Tushare.
    """

    output_filename = DataCleanPath().cap / f"{dt.strftime('%Y-%m-%d')}.parquet"

    if not replace and output_filename.exists():
        return True

    input_filename = DataRawPath().basic / f"{dt.strftime('%Y-%m-%d')}.parquet"

    # Load data
    try:
        df = pd.read_parquet(input_filename)
    except FileNotFoundError:
        logger.warning(f"File not found: {input_filename}")
        return False

    # Align column names
    # Rename columns to match Cap model
    # Tushare: trade_date, ts_code, cap
    df = df.rename(
        columns={
            "trade_date": "datetime",
            "ts_code": "symbol",
            "total_share": "shares_out",
            "float_share": "shares_float",
            "free_share": "shares_ff",
            "total_mv": "cap_total",
            "circ_mv": "cap_float",
        }
    )
    df["datetime"] = pd.to_datetime(df["datetime"])

    df["shares_out"] *= 1e4  # From 1w shares to shares
    df["shares_float"] *= 1e4  # From 1w shares to shares
    df["shares_ff"] *= 1e4  # From 1w shares to shares
    df["cap_total"] *= 1e4  # From 1w mv to mv
    df["cap_float"] *= 1e4  # From 1w mv to mv
    df["cap_ff"] = df["close"] * df["shares_ff"]

    # Extract required fields
    df = df.reindex(columns=REQ_CAP_FIELDS)

    df.to_parquet(output_filename, index=False)
    return True


def clean_cap(start_date: str, end_date: str, replace: bool = False):
    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    for dt in dates:
        _clean_cap_for_dt(dt, replace=replace)
        logger.info(f"{dt}: clean cap data done ...")


def _clean_valuation_for_dt(dt: pd.Timestamp, replace: bool = False) -> bool:
    """
    Clean valuation data (downloaded by date) from Tushare.
    """
    output_filename = DataCleanPath().valuation / f"{dt.strftime('%Y-%m-%d')}.parquet"

    if not replace and output_filename.exists():
        return True

    input_filename = DataRawPath().basic / f"{dt.strftime('%Y-%m-%d')}.parquet"

    # Load data
    try:
        df = pd.read_parquet(input_filename)
    except FileNotFoundError:
        logger.info(f"Warning: File not found: {input_filename}")
        return False

    # Align column names
    # Rename columns to match Valuation model
    # Tushare: trade_date, ts_code, pe, pb, ps, ps_ttm, dv_ratio, dv_ttm, total_shares, float_shares
    df = df.rename(
        columns={
            "trade_date": "datetime",
            "ts_code": "symbol",
        }
    )
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Extract required fields
    df = df.reindex(columns=REQ_VALUATION_FIELDS)

    df.to_parquet(output_filename, index=False)
    return True


def clean_valuation(start_date: str, end_date: str, replace: bool = False):
    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    for dt in dates:
        _clean_valuation_for_dt(dt, replace=replace)
        logger.info(f"{dt}: clean valuation data done ...")


# Dataset: concat to dataset and clean


def _load_parquets_under_directory(directory: Path, start_date: str, end_date: str):
    ls = []
    for filename in directory.glob("*.parquet"):
        # To skip the files that are not in the date range
        if pd.Timestamp(filename.stem) < pd.Timestamp(start_date) or pd.Timestamp(
            filename.stem
        ) > pd.Timestamp(end_date):
            continue

        df = pd.read_parquet(filename)
        if not df.empty:
            ls.append(df)

    return pd.concat(ls, axis=0)


def clean_dataset(year: int, replace: bool = False):

    start_date = pd.Timestamp(f"{year}-01-01").strftime("%Y-%m-%d")
    end_date = pd.Timestamp(f"{year}-12-31").strftime("%Y-%m-%d")

    # Path and filename
    output_filename = DataCleanPath().dataset / f"{year}.parquet"

    if not replace and output_filename.exists():
        return True

    # Load data
    logger.info(f"Before concatenating dataset, load components the year {year} ...")
    trade_calendar = pd.read_parquet(
        DataCleanPath().trade_calendar / "trade_calendar.parquet"
    ).sort_values(by="calendar_date")
    identity = pd.read_parquet(
        DataCleanPath().identity / "identity.parquet"
    ).sort_values(by="symbol")
    unadj_1d_bar = _load_parquets_under_directory(
        DataCleanPath().bar_1day, start_date, end_date
    ).sort_values(["datetime", "symbol"])
    adj_factor = _load_parquets_under_directory(
        DataCleanPath().adj_factor, start_date, end_date
    ).sort_values(["datetime", "symbol"])
    cap = _load_parquets_under_directory(
        DataCleanPath().cap, start_date, end_date
    ).sort_values(["datetime", "symbol"])
    valuation = _load_parquets_under_directory(
        DataCleanPath().valuation, start_date, end_date
    ).sort_values(["datetime", "symbol"])

    # Concat
    trade_dates = trade_calendar.query("is_open == 1")["calendar_date"].to_list()
    dataset = (
        pd.concat(
            [
                unadj_1d_bar.loc[unadj_1d_bar["datetime"].isin(trade_dates)].set_index(
                    ["datetime", "symbol"]
                ),
                adj_factor.loc[adj_factor["datetime"].isin(trade_dates)].set_index(
                    ["datetime", "symbol"]
                ),
                cap.loc[cap["datetime"].isin(trade_dates)].set_index(
                    ["datetime", "symbol"]
                ),
                valuation.loc[valuation["datetime"].isin(trade_dates)].set_index(
                    ["datetime", "symbol"]
                ),
            ],
            axis=1,
            join="inner",
        )
        .sort_index()
        .reset_index()
    )
    dataset = pd.merge(
        dataset,
        identity,
        on="symbol",
        how="left",
    ).query("datetime >= list_date and datetime <= delist_date")

    # Adjust the bar
    dataset["open"] = dataset["open"] * dataset["adj_factor"]
    dataset["high"] = dataset["high"] * dataset["adj_factor"]
    dataset["low"] = dataset["low"] * dataset["adj_factor"]
    dataset["close"] = dataset["close"] * dataset["adj_factor"]
    dataset["vwap"] = dataset["vwap"] * dataset["adj_factor"]

    dataset.to_parquet(output_filename, index=False)
    logger.info(f"Done cleaning dataset from {start_date} to {end_date}")
    return True


def clean_listed_days():

    # Load data
    logger.info("Clean listed days ...")
    trade_calendar = pd.read_parquet(
        DataCleanPath().trade_calendar / "trade_calendar.parquet"
    ).sort_values(by="calendar_date")
    ls = []
    for filename in DataCleanPath().dataset.glob("*.parquet"):
        dataset = pd.read_parquet(
            filename,
            columns=["datetime", "symbol", "list_date", "close", "volume", "board"],
        ).sort_values(["datetime", "symbol"])
        ls.append(dataset)
    dataset = pd.concat(ls, axis=0)

    # 000004.SZ and 000005.SZ was IPO before the first trade calendar date
    # Because at that time, they were on trial stage
    # Reset their list_date to the first trade calendar date
    dataset.loc[dataset["symbol"].isin(["000004.SZ", "000005.SZ"]), "list_date"] = (
        trade_calendar.query("is_open == 1").iloc[0]["calendar_date"]
    )

    df_day_count = _add_day_count_columns(dataset, trade_calendar)
    df_day_count.to_parquet(
        DataCleanPath().listed_days / "listed_days.parquet", index=False
    )


def _add_day_count_columns(
    df: pd.DataFrame, trade_calendar: pd.DataFrame
) -> pd.DataFrame:
    """
    Vectorized calculation of:
      - list_days: number of **market-open** days from list_date (inclusive, starts at 1)
      - continuous_trading_days: resets after suspension (gap in open days)
      - suspension_days: number of consecutive missed open market days before current trade

    Parameters:
    -----------
    df : DataFrame with columns ['datetime', 'symbol', 'list_date']
         - datetime: actual trading days of the stock
         - list_date: IPO/listing date per symbol
    trade_calendar : DataFrame with columns ['calendar_date', 'is_open']
         - calendar_date: all potential market dates (sorted)
         - is_open: 1 = market open, 0 = closed/holiday

    Returns:
    --------
    df with added columns: list_days, continuous_trading_days, suspension_days
    """
    df = df.copy()
    trade_calendar = trade_calendar.copy()

    # Ensure datetime types
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["list_date"] = pd.to_datetime(df["list_date"])
    trade_calendar["calendar_date"] = pd.to_datetime(trade_calendar["calendar_date"])

    # Filter only open market days
    trading_days = trade_calendar[trade_calendar["is_open"] == 1].copy()
    trading_days = trading_days.sort_values("calendar_date").reset_index(drop=True)
    trading_days["date_idx"] = trading_days.index  # 0,1,2,... for open days only

    # Create mapping: date → index among open market days
    date_to_idx = pd.Series(
        trading_days["date_idx"].values, index=trading_days["calendar_date"]
    )

    # ────────────────────────────────────────────────
    # Prepare df: only keep rows where stock actually traded
    # ────────────────────────────────────────────────
    df = df.sort_values(["symbol", "datetime"])

    # Map each traded date to its open-day index
    df["date_idx"] = df["datetime"].map(date_to_idx)

    # Remove rows where traded date is not in open calendar (data error)
    df = df.dropna(subset=["date_idx"]).copy()
    df["date_idx"] = df["date_idx"].astype(int)

    # ────────────────────────────────────────────────
    # 1. list_days: count of open market days since (and including) list_date
    # ────────────────────────────────────────────────
    # For each symbol, find the open_idx of its list_date
    df["list_date_idx"] = (
        df.groupby("symbol")["list_date"].transform("first").map(date_to_idx)
    )
    df["list_days"] = df["date_idx"] - df["list_date_idx"] + 1

    # ────────────────────────────────────────────────
    # 2. Gap detection using open_idx differences
    # ────────────────────────────────────────────────
    df["prev_date_idx"] = df.groupby("symbol")["date_idx"].shift(1)

    # Gap = number of **missed open days** between two consecutive trades
    df["gap"] = (df["date_idx"] - df["prev_date_idx"] - 1).fillna(0).astype(int)

    # suspension_days = size of the previous gap (0 if continuous)
    df["suspension_days"] = df["gap"].where(df["gap"] > 0, 0)

    # ────────────────────────────────────────────────
    # 3. Continuous trading days (resets after gap > 0)
    # ────────────────────────────────────────────────
    df["is_reset"] = df["gap"] > 0
    df["segment_id"] = df.groupby("symbol")["is_reset"].cumsum()

    df["continuous_trading_days"] = df.groupby(["symbol", "segment_id"]).cumcount() + 1

    # ────────────────────────────────────────────────
    # Cleanup
    # ────────────────────────────────────────────────
    drop_cols = ["date_idx", "prev_date_idx", "gap", "is_reset", "segment_id"]
    drop_cols = ["prev_date_idx", "gap", "is_reset", "segment_id"]
    drop_cols = []
    df = df.drop(columns=drop_cols, errors="ignore")

    return df
