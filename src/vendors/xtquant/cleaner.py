import warnings

import pandas as pd
from src.logger import logger
from src.common.schema import (
    REQ_1D_BAR_FIELDS,
    REQ_TRADE_CALENDAR_FIELDS,
    REQ_IDENTITY_FIELDS,
)
from src.vendors.xtquant.config import DataCleanPath

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)
    from xtquant import xtdata

xtdata.enable_hello = False


def convert_dt_to_str(dt: pd.Timestamp):
    """
    Convert datetime to string in format "YYYYMMDD" (required by xtquant API).
    """
    return dt.strftime("%Y%m%d")


def clean_trade_calendar():
    output_filename = DataCleanPath().trade_calendar / "trade_calendar.parquet"

    trading_dates = pd.to_datetime(
        xtdata.get_trading_dates(market="SH", start_time="", end_time="", count=-1),
        unit="ms",
    ) + pd.offsets.Hour(8)
    trading_dates = trading_dates.sort_values()
    first_date, last_date = trading_dates.min(), trading_dates.max()
    df = pd.DataFrame(
        {
            "exchange": "SSE",
            "calendar_date": pd.date_range(first_date, last_date, freq="D"),
            "is_open": 0,
        }
    ).set_index("calendar_date")
    df.loc[trading_dates, "is_open"] = 1
    map2prev_trade_date = dict(zip(trading_dates[1:], trading_dates[:-1]))
    df["pre_trade_date"] = df.index.map(map2prev_trade_date).values
    df["pre_trade_date"] = df["pre_trade_date"].bfill()

    df = df.reset_index()

    df = df[REQ_TRADE_CALENDAR_FIELDS]
    df.to_parquet(output_filename, index=False)


def clean_identity():
    output_filename = DataCleanPath().identity / "identity.parquet"

    # Load data
    stock_list = xtdata.get_stock_list_in_sector("沪深A股")
    data = xtdata.get_instrument_detail_list(stock_list=stock_list)
    df = pd.DataFrame(data).T
    df = df.rename_axis(index="symbol").reset_index()

    # Align column names
    df = df.rename(
        columns={
            "ExchangeID": "exchange",
            "InstrumentName": "chinese_name",
            "OpenDate": "list_date",
            "ExpireDate": "delist_date",
        }
    )

    df["list_date"] = pd.to_datetime(df["list_date"])
    df['delist_date'] = df['delist_date'].map({'99999999': '2099-12-31'})
    df["delist_date"] = pd.to_datetime(df["delist_date"])
    df["delist_date"] = df["delist_date"].where(~df["delist_date"].isna(), "2099-12-31")

    df["exchange"] = df["exchange"].map(
        {
            "SH": "SSE",
            "SZ": "SZSE",
        }
    )

    df = df.reindex(columns=REQ_IDENTITY_FIELDS)
    df.to_parquet(output_filename, index=False)
    return True


def _clean_1day_bar_for_dt(dt: pd.Timestamp, replace: bool = False):
    """
    Clean 1day bar data from XTQuant.
    """

    output_filename = DataCleanPath().bar_1day / f"{dt.strftime('%Y-%m-%d')}.parquet"

    if not replace and output_filename.exists():
        return True

    # Load data
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    data = xtdata.get_market_data_ex(
        stock_list=code_list,
        period="1d",
        start_time=convert_dt_to_str(dt),
        end_time=convert_dt_to_str(dt),
    )
    df = pd.concat(data, axis=0).rename_axis(index=["symbol", "date"]).reset_index()

    # Beijing is UTC+8
    df["datetime"] = pd.to_datetime(df["time"], unit="ms") + pd.offsets.Hour(8)

    # Align column names
    # df = df.rename(columns={})

    # Unit
    df["volume"] *= 100

    # Add columns
    df["vwap"] = df["amount"] / df["volume"]

    # Exrtact required fields
    df = df.reindex(columns=REQ_1D_BAR_FIELDS)

    df.to_parquet(output_filename, index=False)
    return True


def clean_1day_bar(start_date: str, end_date: str, replace: bool = False):
    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    for dt in dates:
        _clean_1day_bar_for_dt(dt, replace=replace)
        logger.info(f"{dt}: clean 1day bar data done ...")
