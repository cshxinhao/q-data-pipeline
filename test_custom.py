import pandas as pd
from xtquant import xtdata
from src.logger import logger


def on_progress(data):
    logger.info(f"Download progress: {data}")


if __name__ == "__main__":
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    logger.info(f"{len(code_list)} Stock list: {code_list[:10]}")

    from src.vendors.xtquant.downloader import download_1day_bar, download_1min_bar

    download_1day_bar()
    # download_1min_bar()

    # xtdata.download_holiday_data()
    print("Done download data")
