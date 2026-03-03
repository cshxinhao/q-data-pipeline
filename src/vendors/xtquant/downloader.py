import pandas as pd
from xtquant import xtdata
from src.logger import logger


def convert_dt_to_str(dt: pd.Timestamp):
    """
    Convert datetime to string in format "YYYYMMDD" (required by xtquant API).
    """
    return dt.strftime("%Y%m%d")


def download_holiday():
    xtdata.download_holiday_data()


def download_index_weight():
    """
    Download index weight from XTQuant.
    """
    xtdata.download_index_weight()


def download_sector_data():
    xtdata.download_sector_data()


def download_1day_bar():
    """
    Download 1day bar data from XTQuant.
    """

    code_list = ["000001.SZ"]
    period = "1d"

    ## 为了方便用户进行数据管理，xtquant的大部分历史数据都是以压缩形式存储在本地的
    ## 比如行情数据，需要通过download_history_data下载，财务数据需要通过download_financial_data下载
    ## 所以在取历史数据之前，我们需要调用数据下载接口，将数据下载到本地

    xtdata.download_history_data2(
        stock_list=code_list,
        period=period,
        start_time='',
        end_time='',
        callback=on_progress,
        incrementally=True,
    )


def download_financial(code_list: list, callback=None):
    """
    Download financial data from XTQuant.
    """
    xtdata.download_financial_data2(code_list, callback=callback)


def on_progress(data):
    logger.info(f"Download progress: {data}")
