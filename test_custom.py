from src.vendors.tushare.cleaner import clean_dataset

if __name__ == "__main__":
    for year in range(2012, 2027):
        clean_dataset(year=year, replace=True)
