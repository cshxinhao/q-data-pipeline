import warnings

import pandas as pd
from xtquant.xtdata import get_local_data, get_market_data_ex
from src.logger import logger
from src.common.schema import (
    REQ_1D_BAR_FIELDS,
    REQ_TICK_QUOTE_FIELDS,
    REQ_TRADE_CALENDAR_FIELDS,
    REQ_IDENTITY_FIELDS,
)
from src.vendors.xtquant.config import DataRealtimePath, DataCleanPath

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
    df["delist_date"] = df["delist_date"].map({"99999999": "2099-12-31"})
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

    # Drop records with null [open, high, low, close]
    df = df.dropna(subset=["open", "high", "low", "close"])

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


def _clean_1min_bar_for_dt(dt: pd.Timestamp, replace: bool = False):
    """
    Clean 1min bar data from XTQuant.
    """

    output_filename = DataCleanPath().bar_1min / f"{dt.strftime('%Y-%m-%d')}.parquet"

    if not replace and output_filename.exists():
        return True

    # Load data
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    data = xtdata.get_market_data_ex(
        stock_list=code_list,
        period="1m",
        start_time=convert_dt_to_str(dt),
        end_time=convert_dt_to_str(dt),
    )
    df = pd.concat(data, axis=0).rename_axis(index=["symbol", "date"]).reset_index()

    # # Test
    # data = xtdata.get_market_data_ex(stock_list=['600519.SH', '300750.SZ'], period="1m")
    # data = xtdata.get_market_data(stock_list=['600519.SH', '300750.SZ'], period="1m")
    # data = xtdata.get_local_data(stock_list=['600519.SH', '300750.SZ'], period="1m")

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


def clean_1min_bar(start_date: str, end_date: str, replace: bool = False):
    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    for dt in dates:
        _clean_1min_bar_for_dt(dt, replace=replace)
        logger.info(f"{dt}: clean 1min bar data done ...")


def clean_real_time_quote(date: str):
    """
    Clean real-time quote data from XTQuant.
    """
    date_str = pd.Timestamp(date).strftime("%Y%m%d")
    input_path = DataRealtimePath().reatime_quote / date_str
    output_filename = DataCleanPath().reatime_quote / f"{date_str}.parquet"

    df = pd.read_parquet(
        input_path,  # All the parquet files under this path
        columns=[
            "stock_code",
            "time",
            "lastPrice",
            "pvolume",
            "lastClose",
            "stockStatus",
            "transactionNum",
            "askPrice1",
            "askPrice2",
            "askPrice3",
            "askPrice4",
            "askPrice5",
            "askVol1",
            "askVol2",
            "askVol3",
            "askVol4",
            "askVol5",
            "bidPrice1",
            "bidPrice2",
            "bidPrice3",
            "bidPrice4",
            "bidPrice5",
            "bidVol1",
            "bidVol2",
            "bidVol3",
            "bidVol4",
            "bidVol5",
        ],
    )
    df["time"] = pd.to_datetime(df["time"], unit="ms") + pd.offsets.Hour(8)
    df = df.sort_values(by=["time", "stock_code"])

    # stockStatus: 3=continuous-session, 8=closing-auction, 5=closed, ??0,7

    # Drop duplicated rows
    df = df.drop_duplicates(keep="first")  # Drop fully duplicated rows

    # Align column names
    df = df.rename(
        columns={
            "stock_code": "symbol",
            "time": "datetime",
            "lastPrice": "last_price",
            "pvolume": "volume",
            "lastClose": "last_close",
            "stockStatus": "stock_status",
            "transactionNum": "transaction_num",
            "askPrice1": "ask_px1",
            "askPrice2": "ask_px2",
            "askPrice3": "ask_px3",
            "askPrice4": "ask_px4",
            "askPrice5": "ask_px5",
            "askVol1": "ask_vol1",
            "askVol2": "ask_vol2",
            "askVol3": "ask_vol3",
            "askVol4": "ask_vol4",
            "askVol5": "ask_vol5",
            "bidPrice1": "bid_px1",
            "bidPrice2": "bid_px2",
            "bidPrice3": "bid_px3",
            "bidPrice4": "bid_px4",
            "bidPrice5": "bid_px5",
            "bidVol1": "bid_vol1",
            "bidVol2": "bid_vol2",
            "bidVol3": "bid_vol3",
            "bidVol4": "bid_vol4",
            "bidVol5": "bid_vol5",
        }
    )

    df = df.reindex(columns=REQ_TICK_QUOTE_FIELDS)

    df.to_parquet(output_filename, index=False)
    logger.info(f"{date_str}: clean real-time quote data done ...")
    return True
