import pandas as pd
from xtquant import xtdata
from src.logger import logger


def on_progress(data):
    logger.info(f"Download progress: {data}")


import time


def conv_time(ct):
    """
    conv_time(1476374400000) --> '20161014000000.000'
    """
    local_time = time.localtime(ct / 1000)
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp


if __name__ == "__main__":
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    logger.info(f"{len(code_list)} Stock list: {code_list[:10]}")

    data = xtdata.get_market_data_ex(
        stock_list=code_list[:10],
        period="1d",
        count=10,
    )
    df = pd.concat(data, axis=0).rename_axis(index=["symbol", "datetime"])
    # Beijing is UTC+8
    df["time"] = pd.to_datetime(df["time"], unit="ms") + pd.offsets.Hour(8)

    print(df)

    xtdata.download_history_data2(
        stock_list=code_list[:10],
        period="1m",
        start_time="",
        end_time="",
        callback=on_progress,
        incrementally=True,
    )

    print("Done download data")
