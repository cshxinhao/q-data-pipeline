from typing import List, Union
from datetime import date, datetime
import pyarrow.parquet as pq
import pandas as pd
import numpy as np


# ----------------------------------------------------------------------------------------------------------------
# Basic Check: for each vendor separately


def check_duplicate(market: str, vendor: str) -> pd.DataFrame:
    # Load the data
    if market == "China" and vendor == "tushare":
        from src.vendors.tushare.config import DataCleanPath

        data = pd.read_parquet(
            DataCleanPath().dataset,
            columns=[
                "datetime",
                "symbol",
                "open",
                "high",
                "low",
                "close",
                "vwap",
                "volume",
                "exchange",
            ],
        )
    else:
        # TODO: Add global duplicate check for other markets
        raise NotImplementedError(
            f"Duplicate check not implemented for market {market}"
        )

    if data.empty:
        return pd.DataFrame()

    # Check for duplicate index
    dups = data.duplicated(subset=["datetime", "symbol"])
    return data[dups]


def check_nulls(market: str, vendor: str) -> pd.DataFrame:

    CORE_FIELDS = [
        "datetime",
        "symbol",
        "open",
        "high",
        "low",
        "close",
        "vwap",
        "adj_factor",
        "volume",
        "amount",
        "shares_out",
        "cap_total",
        "board",
        "exchange",
    ]

    if market == "China" and vendor == "tushare":
        from src.vendors.tushare.config import DataCleanPath

        data = pd.read_parquet(
            DataCleanPath().dataset,
            columns=CORE_FIELDS,
        )
    else:
        # TODO: Add global nulls check for other markets
        raise NotImplementedError(f"Nulls check not implemented for market {market}")

    if data.empty:
        return pd.DataFrame()

    # Check for null values
    nulls = data.isnull().any(axis=1)
    return data[nulls]


def check_volume(market: str, vendor: str) -> pd.DataFrame:

    if market == "China" and vendor == "tushare":
        from src.vendors.tushare.config import DataCleanPath

        data = pd.read_parquet(
            DataCleanPath().dataset,
            columns=[
                "datetime",
                "symbol",
                "close",
                "volume",
                "amount",
            ],
        )
    else:
        # TODO: Add global volume check for other markets
        raise NotImplementedError(f"Volume check not implemented for market {market}")

    if data.empty:
        return pd.DataFrame()

    # Check for zero volume (suspicious for active stocks)
    zero_vol = data[(data["volume"] == 0) | (data["amount"] == 0)]
    return zero_vol


def check_logic_consistency(market: str, vendor: str) -> pd.DataFrame:

    # Load the data
    if market == "China" and vendor == "tushare":
        from src.vendors.tushare.config import DataCleanPath

        data = pd.read_parquet(
            DataCleanPath().dataset,
            columns=[
                "datetime",
                "symbol",
                "open",
                "high",
                "low",
                "close",
                "vwap",
                "volume",
                "amount",
            ],
        )
    else:
        # TODO: Add global logic consistency check for other markets
        raise NotImplementedError(
            f"Logic consistency check not implemented for market {market}"
        )

    if data.empty:
        return pd.DataFrame()

    required = ["open", "high", "low", "close", "vwap", "volume"]
    # Relax requirement: only check what is present?
    # But 'high >= low' requires both.
    # Let's check essential OHLC.
    if not all(col in data.columns for col in required):
        # Try to check partial?
        # For now, return empty if essential columns missing to avoid crash
        return pd.DataFrame()

    inconsistencies = []

    # Check High: High >= Open, High >= Close, High >= Low
    mask_high = (
        (data["high"] < data["open"])
        | (data["high"] < data["close"])
        | (data["high"] < data["low"])
    )

    if mask_high.any():
        inv_high = data[mask_high].copy()
        inv_high["reason"] = "High < Open/Close/Low"
        inconsistencies.append(inv_high)

    # # Check Low: Low <= Open, Low <= Close
    mask_low = (data["low"] > data["open"]) | (data["low"] > data["close"])

    if mask_low.any():
        inv_low = data[mask_low].copy()
        inv_low["reason"] = "Low > Open/Close"
        inconsistencies.append(inv_low)

    # Volume >= 0
    mask_vol = data["volume"] < 0
    if mask_vol.any():
        inv_vol = data[mask_vol].copy()
        inv_vol["reason"] = "Volume < 0"
        inconsistencies.append(inv_vol)

    # Amount >= 0
    if "amount" in data.columns:
        mask_amt = data["amount"] < 0
        if mask_amt.any():
            inv_amt = data[mask_amt].copy()
            inv_amt["reason"] = "Amount < 0"
            inconsistencies.append(inv_amt)

    # VWAP Logic
    if "vwap" in data.columns:
        tolerance = 1e-4
        mask_vwap = (data["vwap"] < data["low"] * (1 - tolerance)) | (
            data["vwap"] > data["high"] * (1 + tolerance)
        )

        if mask_vwap.any():
            inv_vwap = data[mask_vwap].copy()
            inv_vwap["reason"] = "VWAP out of [Low, High]"
            inconsistencies.append(inv_vwap)

    if inconsistencies:
        return pd.concat(inconsistencies)

    return pd.DataFrame()


def check_returns_outlier(market: str, vendor: str) -> pd.DataFrame:

    if market == "China" and vendor == "tushare":
        from .china_rules import calculate_price_limit, get_board_type
        from src.vendors.tushare.config import DataCleanPath

        data = pd.read_parquet(DataCleanPath().listed_days / "listed_days.parquet")

        if data.empty:
            return pd.DataFrame()

        if "board" not in data.columns:
            data["board"] = data["symbol"].apply(get_board_type)
        data["limit"] = calculate_price_limit(data)

        # Calculate percentage change
        data["abs_pct_change"] = data.groupby("symbol")["close"].pct_change().abs()

        # Check against limit
        tolerance = 0.2 / 100  # 0.2% tolerance

        # Identify violations
        mask_violation = (data["abs_pct_change"] > data["limit"] + tolerance) & (
            data["limit"] != np.inf
        )
        return data.loc[mask_violation]

    else:
        # TODO: Add global price limit check for other markets, like Taiwan, Korea
        raise NotImplementedError(
            f"Price limit check not implemented for market {market}"
        )


def check_network_delay(market: str, vendor: str, date: str) -> pd.DataFrame:
    if market == "China" and vendor == "xtquant":
        from src.vendors.xtquant.config import DataCleanPath

        date_str = pd.Timestamp(date).strftime("%Y%m%d")
        data = pd.read_parquet(DataCleanPath().reatime_quote / f"{date_str}.parquet")
        if data.empty:
            return pd.DataFrame()

    # Calculate network delay stats
    # TODO: discrepancy between datetime, receive_datetime, produce_datetime and consume_datetime


def __check_continuity(
    data: pd.DataFrame,
    start: Union[date, datetime],
    end: Union[date, datetime],
    calendar: List[date],
) -> List[str]:

    if data.empty:
        return [d.isoformat() for d in calendar if start <= d <= end]

    # Ensure index is datetime
    if not isinstance(data.index, pd.DatetimeIndex):
        if "dt" in data.columns:
            data = data.set_index("dt")
        else:
            raise ValueError("Data must have datetime index or 'dt' column")

    # Get unique dates from data
    data_dates = set(data.index.normalize().date)

    # Filter calendar for range
    start_date = start.date() if isinstance(start, datetime) else start
    end_date = end.date() if isinstance(end, datetime) else end

    expected_dates = [d for d in calendar if start_date <= d <= end_date]

    missing = []
    for d in expected_dates:
        if d not in data_dates:
            missing.append(d.isoformat())

    return missing


# ----------------------------------------------------------------------------------------------------------------
# Advanced Check: cross-check between vendors


def cross_check_between_vendors() -> pd.DataFrame:
    """
    Cross-check data between two vendors to find discrepancies.
    """

    # TODO: hardcode for now, will be configurable in the future
    vendor1 = "tushare"
    vendor2 = "xtquant"
    start = "2026-01-01"
    end = None

    # ----------------------------------------------------------------------------------------------------------------
    # TODO: Check trade calendar

    # ----------------------------------------------------------------------------------------------------------------
    # TODO: Check identity

    # ----------------------------------------------------------------------------------------------------------------
    # Check 1day bar
    from src.vendors.tushare.config import DataCleanPath as TusharePath
    from src.vendors.xtquant.config import DataCleanPath as XTPath

    filters = [("datetime", ">=", pd.Timestamp(start))]
    filenames = [
        filename
        for filename in TusharePath().bar_1day.glob("*.parquet")
        if pq.read_metadata(filename).num_rows > 0
        and pd.Timestamp(filename.stem) >= pd.Timestamp(start)
    ]
    df1 = pd.read_parquet(filenames, filters=filters)
    filenames = [
        filename
        for filename in XTPath().bar_1day.glob("*.parquet")
        if pq.read_metadata(filename).num_rows > 0
        and pd.Timestamp(filename.stem) >= pd.Timestamp(start)
    ]
    df2 = pd.read_parquet(filenames, filters=filters)

    # check SH and SZ stocks only
    df1 = df1.loc[df1["symbol"].str.endswith(("SH", "SZ"))]
    df2 = df2.loc[df2["symbol"].str.endswith(("SH", "SZ"))]

    # main key: datetime, symbol
    df1 = df1.set_index(["datetime", "symbol"])
    df2 = df2.set_index(["datetime", "symbol"])
    outer_key = df1.index.union(df2.index)
    df1 = df1.reindex(outer_key)
    df2 = df2.reindex(outer_key)

    # since vwap is calculated using amount & volume, no need to check alone
    df1 = df1.drop(columns=["vwap"])
    df2 = df2.drop(columns=["vwap"])

    # round to economical meaningful precision
    cols = ["open", "high", "low", "close"]
    df1[cols] = df1[cols].round(3)
    df2[cols] = df2[cols].round(3)

    cols = ["volume", "amount"]
    df1[cols] = df1[cols] // 100 * 100  # To the 100
    df2[cols] = df2[cols] // 100 * 100  # To the 100

    # volume & amount are hard to match 100%
    # as long as the discrepancy is within 1% tolerance
    # just accept it
    tolerance = 0.01  # 1% tolerance
    mask_violation = (df1["volume"] <= df2["volume"] * (1 + tolerance)) & (
        df1["volume"] >= df2["volume"] * (1 - tolerance)
    )
    df1.loc[mask_violation, "volume"] = df2.loc[mask_violation, "volume"]
    df1.loc[mask_violation, "amount"] = df2.loc[mask_violation, "amount"]

    # values
    inconsistencies = df1.compare(df2, result_names=(vendor1, vendor2)).reset_index()
    return inconsistencies
