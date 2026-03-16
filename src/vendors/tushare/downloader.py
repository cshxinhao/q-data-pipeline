from functools import lru_cache
from pathlib import Path
import time
from typing import Callable

import pandas as pd
from tqdm import tqdm
import tushare as ts

from .config import TUSHARE_TOKEN, DataRawPath
from src.logger import logger


@lru_cache(maxsize=1)
def get_pro():
    return ts.pro_api(TUSHARE_TOKEN)


def convert_dt_to_str(dt: pd.Timestamp):
    """
    Convert datetime to string in format "YYYYMMDD" (required by tushare API).
    """
    return dt.strftime("%Y%m%d")


def try_n_times(task: Callable, n: int, seconds: int, **kwargs):
    count = 0
    while True:
        try:
            result = task(**kwargs)
            return result
        except Exception as e:
            logger.error(e)
            count += 1
            if count >= n:
                return None
            time.sleep(seconds)


def download_trade_calendar(start_date: str, end_date: str):
    """
    Download trade calendar from Tushare.

    Suggest download full history every time.
    """
    # Init the interface
    pro = get_pro()

    trade_calendar = pro.trade_cal(
        exchange="",
        start_date=convert_dt_to_str(pd.Timestamp(start_date)),
        end_date=convert_dt_to_str(pd.Timestamp(end_date)),
    )

    # Preprocess
    trade_calendar["cal_date"] = pd.to_datetime(trade_calendar.loc[:, "cal_date"])
    trade_calendar["pretrade_date"] = pd.to_datetime(
        trade_calendar.loc[:, "pretrade_date"]
    )
    trade_calendar.sort_values(by="cal_date", inplace=True)

    # Save
    filename = DataRawPath().trade_calendar / "trade_calendar.parquet"
    trade_calendar.to_parquet(filename, index=False)


def download_ticker_mapper():
    # Init the interface
    pro = get_pro()

    listed = pro.stock_basic(
        exchange="",
        list_status="L",
        fields="ts_code,symbol,name,area,industry,fullname,enname,market,exchange,list_status,list_date,delist_date,is_hs,act_name,act_ent_type",
    )

    delisted = pro.stock_basic(
        exchange="",
        list_status="D",
        fields="ts_code,symbol,name,area,industry,fullname,enname,market,exchange,list_status,list_date,delist_date,is_hs,act_name,act_ent_type",
    )

    paused = pro.stock_basic(
        exchange="",
        list_status="P",
        fields="ts_code,symbol,name,area,industry,fullname,enname,market,exchange,list_status,list_date,delist_date,is_hs,act_name,act_ent_type",
    )

    # Concat all
    ticker_mapper: pd.DataFrame = pd.concat([listed, delisted, paused], axis=0)

    # Preprocess
    ticker_mapper["list_date"] = pd.to_datetime(ticker_mapper.loc[:, "list_date"])
    ticker_mapper["delist_date"] = pd.to_datetime(ticker_mapper.loc[:, "delist_date"])

    # To save
    filename = DataRawPath().ticker_mapper / "ticker_mapper.parquet"
    ticker_mapper.to_parquet(filename, index=False)


def _download_bar_for_dt(dt: pd.Timestamp):
    pro = get_pro()
    df = pro.daily(trade_date=convert_dt_to_str(dt))
    if df.shape[0] > 0:
        df["trade_date"] = pd.to_datetime(df.loc[:, "trade_date"])
    return df


def download_1day_bar(start_date: str, end_date: str, replace: bool = False):
    """
    Download 1day bar price from Tushare.

    The tushare API suggests download bar day by day.
    """
    # Create folder
    file_path = DataRawPath().bar_1day

    for dt in reversed(pd.date_range(start_date, end_date, freq="B")):
        filename = file_path / f"{dt.strftime('%Y-%m-%d')}.parquet"
        if filename.exists() and not replace:
            logger.info(f"{dt}: No need to download 1day bar, already exists ...")
            continue
        df = try_n_times(
            _download_bar_for_dt,
            n=5,
            seconds=30,
            dt=dt,
        )

        if df is None:
            logger.error(f"{dt}: download 1day bar failed downloading ...")
            continue

        df.to_parquet(filename, index=False)
        logger.info(f"{dt}: download 1day bar successful ...")

        time.sleep(1)


def _download_adj_factor_for_dt(dt: pd.Timestamp):
    pro = get_pro()
    df = pro.adj_factor(trade_date=convert_dt_to_str(dt))
    if df.shape[0] > 0:
        df["trade_date"] = pd.to_datetime(df.loc[:, "trade_date"])

    return df


def download_adj_factor(start_date: str, end_date: str, replace: bool = False):
    """
    Download adj factor from Tushare.

    The tushare API suggests download adj factor day by day.
    """
    # Create folder
    file_path = DataRawPath().adj_factor

    for dt in reversed(pd.date_range(start_date, end_date, freq="B")):
        filename = file_path / f"{dt.strftime('%Y-%m-%d')}.parquet"
        if filename.exists() and not replace:
            logger.info(f"{dt}: No need to download adj factor, already exists ...")
            continue
        df = try_n_times(
            _download_adj_factor_for_dt,
            n=5,
            seconds=30,
            dt=dt,
        )
        if df is None:
            logger.error(f"{dt}: download adj factor failed downloading ...")
            continue

        df.to_parquet(filename, index=False)
        logger.info(f"{dt}: download adj factor successful ...")

        time.sleep(30)


def _download_basic_for_dt(dt: pd.Timestamp):
    pro = get_pro()
    df = pro.daily_basic(trade_date=convert_dt_to_str(dt))
    if df.shape[0] > 0:
        df["trade_date"] = pd.to_datetime(df.loc[:, "trade_date"])
    return df


def download_basic(start_date: str, end_date: str, replace: bool = False):
    """
    Download basic data from Tushare.

    The tushare API suggests download basic data day by day.
    """
    # Create folder
    file_path = DataRawPath().basic

    for dt in reversed(pd.date_range(start_date, end_date, freq="B")):
        filename = file_path / f"{dt.strftime('%Y-%m-%d')}.parquet"
        if filename.exists() and not replace:
            logger.info(f"{dt}: No need to download basic data, already exists ...")
            continue
        df = try_n_times(
            _download_basic_for_dt,
            n=5,
            seconds=30,
            dt=dt,
        )

        if df is None:
            logger.error(f"{dt}: download basic data failed downloading ...")
            continue

        df.to_parquet(filename, index=False)
        logger.info(f"{dt}: download basic data successful ...")

        time.sleep(10)


def download_indices():
    pro = get_pro()
    markets = ["MSCI", "CSI", "SSE", "SZSE", "CICC", "SW", "OTH"]
    for mkt in markets:
        df = pro.index_basic(market=mkt)
        if df.shape[0] > 0:
            filename = DataRawPath().indices / f"{mkt}.parquet"
            df.to_parquet(filename, index=False)
            logger.info(f"{mkt}: download index basic data successful ...")


def _download_index_constituent_for_month(index_code: str, year: int, month: int):
    pro = get_pro()
    start_date = f"{year:04d}{month:02d}01"
    end_date = f"{year:04d}{month:02d}31"

    df = pro.index_weight(
        index_code=index_code,
        start_date=start_date,
        end_date=end_date,
    )
    if df.shape[0] > 0:
        df["trade_date"] = pd.to_datetime(df.loc[:, "trade_date"])
    return df


def download_index_constituent(start_date: str, end_date: str, replace: bool = False):
    """
    Download index constituent from Tushare.

    The tushare API suggests download index constituent day by day.
    """

    pro = get_pro()

    indices = {
        "CSI300": "000300.SH",
        "CSI500": "000905.SH",
        "CSI800": "000906.SH",
        "CSI1000": "000852.SH",
        "CSI2000": "932000.CSI",
        "CSIA500": "000510.CSI",
    }
    for name, code in indices.items():
        filepath = DataRawPath().index_constituent / name
        filepath.mkdir(parents=True, exist_ok=True)

        # Query the list date of the index
        index_basic = pro.index_basic(ts_code=code)
        list_date = pd.Timestamp(index_basic.loc[:, "list_date"].values[0])
        logger.info(f"{name} list date: {list_date}")

        for dt in pd.date_range(start_date, end_date, freq="MS"):
            year = dt.year
            month = dt.month
            if dt < list_date:
                continue
            filename = filepath / f"{year:04d}{month:02d}.parquet"
            if filename.exists() and not replace:
                logger.info(
                    f"{name} & {dt}: No need to download index constituent, already exists ..."
                )
                continue

            df = _download_index_constituent_for_month(
                index_code=code,
                year=year,
                month=month,
            )
            if df.shape[0] > 0:
                df.to_parquet(
                    filename,
                    index=False,
                )
                logger.info(f"{name} & {dt}: download index constituent successful ...")
            else:
                logger.warning(f"{name} & {dt}: No index constituent data ...")

            time.sleep(1)

        logger.info(f"{name}: Done")
