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
