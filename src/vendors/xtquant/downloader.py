import warnings
from functools import partial
import pandas as pd
from src.logger import logger

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)
    from xtquant import xtdata

xtdata.enable_hello = False


def convert_dt_to_str(dt: pd.Timestamp):
    """
    Convert datetime to string in format "YYYYMMDD" (required by xtquant API).
    """
    return dt.strftime("%Y%m%d")


# def download_holiday():
#     xtdata.download_holiday_data()  # Need R&D VIP


def download_etf():
    xtdata.download_etf_data()


def download_cb():
    xtdata.download_cb_data()


def download_contracts():
    """
    释义: 下载过期（退市）合约信息，过期（退市）标的列表可以通过get_stock_list_in_sector获取
    备注:
    - 同步执行，补充数据完成后返回
    - 过期板块名称可以通过 print([i for i in xtdata.get_sector_list() if "过期" in i]) 查看
    - 下载完成后，可以通过 xtdata.get_instrument_detail() 查看过期（退市）合约信息
    """
    xtdata.download_history_contracts()


def download_sector_data():
    xtdata.download_sector_data()


def download_index_weight():
    """
    Download index weight from XTQuant.
    """
    xtdata.download_index_weight()


def download_1day_bar():
    """
    Download 1day bar data from XTQuant.
    """

    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    period = "1d"

    ## 为了方便用户进行数据管理，xtquant的大部分历史数据都是以压缩形式存储在本地的
    ## 比如行情数据，需要通过download_history_data下载，财务数据需要通过download_financial_data下载
    ## 所以在取历史数据之前，我们需要调用数据下载接口，将数据下载到本地

    xtdata.download_history_data2(
        stock_list=code_list,
        period=period,
        start_time="",
        end_time="",
        callback=partial(on_progress, f"{period} bar"),
        incrementally=True,
    )


def download_1min_bar():
    """
    Download 1min bar data from XTQuant.
    """
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    period = "1m"

    ## 为了方便用户进行数据管理，xtquant的大部分历史数据都是以压缩形式存储在本地的
    ## 比如行情数据，需要通过download_history_data下载，财务数据需要通过download_financial_data下载
    ## 所以在取历史数据之前，我们需要调用数据下载接口，将数据下载到本地

    xtdata.download_history_data2(
        stock_list=code_list,
        period=period,
        start_time="",
        end_time="",
        callback=partial(on_progress, f"{period} bar"),
        incrementally=True,
    )


def download_financial(code_list: list, callback=None):
    """
    Download financial data from XTQuant.
    """
    xtdata.download_financial_data2(
        code_list,
        callback=partial(on_progress, "financial data"),
    )


def on_progress(note: str, data: dict):
    logger.info(f"Download {note} progress: {data}")
