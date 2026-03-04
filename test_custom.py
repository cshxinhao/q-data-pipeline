import pandas as pd
from xtquant import xtdata
from src.logger import logger


def on_progress(data):
    logger.info(f"Download progress: {data}")


if __name__ == "__main__":
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    logger.info(f"{len(code_list)} Stock list: {code_list[:10]}")

    # # Get 1m data
    # data = xtdata.get_market_data_ex(
    #     stock_list=code_list[:10],
    #     period="1m",
    #     count=10,
    # )
    # df = pd.concat(data, axis=0)
    # # Beijing is UTC+8
    # df["time"] = pd.to_datetime(df["time"], unit="ms") + pd.offsets.Hour(8)
    # print(df)

    # # Get tick data
    # data = xtdata.get_market_data_ex(
    #     stock_list=code_list[:10],
    #     period="tick",
    #     count=10,
    # )
    # df = pd.concat(data, axis=0)
    # # Beijing is UTC+8
    # df["time"] = pd.to_datetime(df["time"], unit="ms") + pd.offsets.Hour(8)
    # print(df)

    # Get full-tick data
    data = xtdata.get_full_tick(code_list=code_list[:10])
    print(data)
    df = pd.DataFrame(data).T    
    # Beijing is UTC+8
    df["timetag"] = pd.to_datetime(df["timetag"], unit="ms")
    print(df)

    # xtdata.download_history_data2(
    #     stock_list=code_list,
    #     period="1m",
    #     start_time="",
    #     end_time="",
    #     callback=on_progress,
    #     incrementally=True,
    # )

    # print("Done download data")
