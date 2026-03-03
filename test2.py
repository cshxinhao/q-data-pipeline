from os import name
import pandas as pd
from xtquant import xtdata
from src.logger import logger

if __name__ == "__main__":
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    logger.info(f"{len(code_list)} Stock list: {code_list[:10]}")

    df = xtdata.get_market_data_ex(
        stock_list=code_list[:10],
        period="1d",
        count=10,
    )
    print(df)
