import pandas as pd
from xtquant import xtdata
from src.logger import logger


def on_progress(data):
    logger.info(f"Download progress: {data}")


if __name__ == "__main__":
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    logger.info(f"{len(code_list)} Stock list: {code_list[:10]}")

    # # Download the stock one by one
    # success_count = 0
    # fail_count = 0

    # for stock in code_list:
    #     try:
    #         data = xtdata.download_history_data(
    #             stock,
    #             period="1d",
    #             incrementally=True,
    #         )
    #         success_count += 1
    #         logger.info(f"{stock}: download history data successful ...")
    #     except Exception as e:
    #         fail_count += 1
    #         logger.error(f"{stock}: download history data failed, Error: {e}")

    # xtdata.download_history_data2(
    #     stock_list=code_list,
    #     period="1d",
    #     callback=on_progress,
    #     incrementally=True,
    # )

    # xtdata.download_sector_data()
    xtdata.download_financial_data2(code_list, callback=on_progress)
