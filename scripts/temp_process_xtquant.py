import pandas as pd
from src.vendors.xtquant.config import DataCleanPath


count = 0
for filename in DataCleanPath().bar_1day.glob("*.parquet"):
    df = pd.read_parquet(filename)
    df = df.dropna(subset=["open", "high", "low", "close"])
    df.to_parquet(filename, index=False)
    count += 1
    if count % 100 == 0:
        print(f"Processed {count} files.")
