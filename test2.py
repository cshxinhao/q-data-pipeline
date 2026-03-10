from os import name
import pandas as pd
from src.logger import logger

if __name__ == "__main__":
    # from src.checker.validator import cross_check_between_vendors

    # cross_check_between_vendors()

    from src.vendors.xtquant.cleaner import clean_real_time_quote
    clean_real_time_quote("20260309")