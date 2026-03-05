from os import name
import pandas as pd
from src.logger import logger

if __name__ == "__main__":
    from src.checker.validator import cross_check_between_vendors

    cross_check_between_vendors()
