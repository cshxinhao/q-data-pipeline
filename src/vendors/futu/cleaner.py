import pandas as pd
from src.logger import logger
from .config import DataCleanPath, DataRawPath
from src.common.schema import (
    REQ_TRADE_CALENDAR_FIELDS,
    REQ_IDENTITY_FIELDS,
    REQ_1D_BAR_FIELDS,
    REQ_ADJ_FACTOR_FIELDS,
    REQ_CAP_FIELDS,
    REQ_VALUATION_FIELDS,
)


def clean_trade_calendar(market: str):

    assert market in ["US", "HK"], f"market must be US or HK, but got {market}"
    if market == "HK":
        exchange = "HKEX"
    else:
        raise NotImplementedError(f"market {market} is not implemented")

    input_path = DataRawPath(market).trade_calendar
    output_filename = DataCleanPath(market).trade_calendar / "trade_calendar.parquet"

    # Load data
    df = pd.read_parquet(input_path)

    # Convert types
    df["exchange"] = exchange
    df["time"] = pd.to_datetime(df["time"])
    df = df.rename(
        columns={
            "time": "calendar_date",
            "trade_date_type": "hkex_trade_date_type",
        }
    )
    df["is_open"] = 1
    df["pre_trade_date"] = df["calendar_date"].shift(1)
    whole_calendar_dates = pd.date_range(
        df["calendar_date"].min(), df["calendar_date"].max(), freq="D"
    )
    df = df.set_index("calendar_date").reindex(whole_calendar_dates).reset_index()
    df["is_open"] = df["is_open"].fillna(0).astype(int)
    df["pre_trade_date"] = df["pre_trade_date"].bfill()
    df.loc[0, "pre_trade_date"] = None

    df = df.reindex(columns=REQ_TRADE_CALENDAR_FIELDS + ["hkex_trade_date_type"])
    df.to_parquet(output_filename, index=False)
    logger.info(f"Trade calendar cleaned and saved to {output_filename}")
    return True


def clean_identity(market: str):
    assert market in ["US", "HK"], f"market must be US or HK, but got {market}"
    if market == "HK":
        exchange = "HKEX"
    else:
        raise NotImplementedError(f"market {market} is not implemented")

    output_filename = DataCleanPath(market).identity / "identity.parquet"

    final_df = None
    # ---------------------------------------------------------------------------------
    # HKEX info
    input_filename1 = (
        DataRawPath(market).ticker_mapper / "hkex_listed_securities.parquet"
    )

    # Load data
    df = pd.read_parquet(input_filename1)
    df = df.loc[df["Category"].eq("Equity")]

    # Convert types
    df = df.rename(
        columns={
            "Name of Securities": "english_name",
            "Sub-Category": "board",
            "Board Lot": "round_lot",
            "ISIN": "isin",
        }
    )
    df["symbol"] = df["Stock Code"].astype(str).str.zfill(5) + f".{market}"
    df["exchange"] = exchange
    final_df = df.copy()

    # ---------------------------------------------------------------------------------
    # Futu info
    input_filename2 = DataRawPath(market).ticker_mapper / "stock_list.parquet"
    df = pd.read_parquet(input_filename2)
    df["listing_date"] = pd.to_datetime(df["listing_date"])
    df = df.rename(
        columns={
            "lot_size": "round_lot",
            "name": "chinese_name",
            "listing_date": "list_date",
            "exchange_type": "board",
        }
    )
    df["symbol"] = df["code"].str.split(".").str[1] + f".{market}"

    final_df = final_df.merge(
        df[["symbol", "chinese_name", "list_date"]], on="symbol", how="left"
    )

    final_df = final_df.reindex(columns=REQ_IDENTITY_FIELDS)
    final_df.to_parquet(output_filename, index=False)
    logger.info(f"Identity cleaned and saved to {output_filename}")
    return True
