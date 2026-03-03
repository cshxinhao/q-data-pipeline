import pandas as pd
from xtquant import xtdata
from src.logger import logger


def convert_dt_to_str(dt: pd.Timestamp):
    """
    Convert datetime to string in format "YYYYMMDD" (required by xtquant API).
    """
    return dt.strftime("%Y%m%d")


def _clean_1day_bar(dt: pd.Timestamp, replace: bool = False):
    """
    Clean 1day bar data from XTQuant.
    """
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    logger.info(f"{len(code_list)} Stock list: {code_list[:10]}")

    df = xtdata.get_market_data_ex(
        stock_list=code_list,
        period="1d",
        start_time=convert_dt_to_str(dt),
        end_time=convert_dt_to_str(dt),
    )


def clean_1day_bar(dt: pd.Timestamp, replace: bool = False):

    pass


def clean_trade_calendar():

    trade_calendar = xtdata.get_trading_calendar(market="SH")


def clean_identity():
    stock_list = xtdata.get_stock_list_in_sector("沪深A股")
    identity = xtdata.get_instrument_detail_list(stock_list=stock_list)
