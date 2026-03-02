import pandas as pd
from pathlib import Path

from src.logger import logger
from .config import (
    DataRawPath,
    DataCleanPath,
    REQ_TRADE_CALENDAR_FIELDS,
    REQ_IDENTITY_FIELDS,
    REQ_1D_BAR_FIELDS,
    REQ_ADJ_FACTOR_FIELDS,
    REQ_CAP_FIELDS,
    REQ_VALUATION_FIELDS,
)


def clean_trade_calendar():
    input_filename = DataRawPath().trade_calendar_dir / "trade_calendar.parquet"
    output_filename = DataCleanPath().trade_calendar_dir / "trade_calendar.parquet"

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
    df.to_parquet(output_filename)
    return True


def clean_identity():
    input_filename = DataRawPath().ticker_mapper_dir / "ticker_mapper.parquet"
    output_filename = DataCleanPath().identity_dir / "identity.parquet"

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

    df = df.reindex(columns=REQ_IDENTITY_FIELDS)
    df.to_parquet(output_filename)
    return True


def _clean_1day_bar_for_dt(dt: pd.Timestamp, replace: bool = False) -> bool:
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

    output_filename.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_filename)
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
    output_filename = (
        DataCleanPath().adj_factor_dir / f"{dt.strftime('%Y-%m-%d')}.parquet"
    )

    if not replace and output_filename.exists():
        return True

    input_filename = DataRawPath().adj_factor_dir / f"{dt.strftime('%Y-%m-%d')}.parquet"

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

    output_filename.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_filename)
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

    output_filename = DataCleanPath().cap_dir / f"{dt.strftime('%Y-%m-%d')}.parquet"

    if not replace and output_filename.exists():
        return True

    input_filename = DataRawPath().basic_dir / f"{dt.strftime('%Y-%m-%d')}.parquet"

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

    output_filename.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_filename)
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
    output_filename = (
        DataCleanPath().valuation_dir / f"{dt.strftime('%Y-%m-%d')}.parquet"
    )

    if not replace and output_filename.exists():
        return True

    input_filename = DataRawPath().basic_dir / f"{dt.strftime('%Y-%m-%d')}.parquet"

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

    output_filename.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_filename)
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
    output_filename = DataCleanPath().dataset_dir / f"{year}.parquet"
    output_filename.parent.mkdir(parents=True, exist_ok=True)

    if not replace and output_filename.exists():
        return True

    # Load data
    logger.info(
        f"Before concatenating dataset, load components from {start_date} to {end_date} ..."
    )
    trade_calendar = pd.read_parquet(
        DataCleanPath().trade_calendar_dir / "trade_calendar.parquet"
    ).sort_values(by="calendar_date")
    identity = pd.read_parquet(
        DataCleanPath().identity_dir / "identity.parquet"
    ).sort_values(by="symbol")
    unadj_1d_bar = _load_parquets_under_directory(
        DataCleanPath().bar_1day_dir, start_date, end_date
    ).sort_values(["datetime", "symbol"])
    adj_factor = _load_parquets_under_directory(
        DataCleanPath().adj_factor_dir, start_date, end_date
    ).sort_values(["datetime", "symbol"])
    cap = _load_parquets_under_directory(
        DataCleanPath().cap_dir, start_date, end_date
    ).sort_values(["datetime", "symbol"])
    valuation = _load_parquets_under_directory(
        DataCleanPath().valuation_dir, start_date, end_date
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

    dataset.to_parquet(output_filename)
    logger.info(f"Done cleaning dataset from {start_date} to {end_date}")
    return True
