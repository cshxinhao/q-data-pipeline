import time
import pandas as pd

from futu import (
    OpenQuoteContext,
    Market,
    Plate,
    SecurityType,
    RET_OK,
    RET_ERROR,
    KLType,
    AuType,
    KL_FIELD,
    Session,
)
from .config import FUTU_HOST, FUTU_PORT, DataRawPath
from src.logger import setup_logger

logger = setup_logger(__name__)


def _ensure_date_format(date: str):
    return pd.Timestamp(date).strftime("%Y-%m-%d")


class FutuDownloader:
    def __init__(self, market: str):

        assert market in ["HK", "US"], "market must be HK or US"
        self.market = market
        self.futu_market = Market.HK if market == "HK" else Market.US

        self.quote_ctx = OpenQuoteContext(
            host=FUTU_HOST, port=FUTU_PORT, is_encrypt=False
        )
        self.raw_path = DataRawPath(market)
        logger.info("FutuDownloader initialized")

    def __del__(self):
        self.quote_ctx.close()

    def __enter__(self):
        # This runs when you enter the 'with' block
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quote_ctx.close()

    def donwload_trade_calendar(self, start_date: str, end_date: str):
        ret, data = self.quote_ctx.request_trading_days(
            market=self.futu_market,
            start=_ensure_date_format(start_date),
            end=_ensure_date_format(end_date),
            code=None,
        )
        if ret == RET_OK and len(data) > 0:
            df = pd.DataFrame(data)
            s, e = df["time"].min(), df["time"].max()
            filename = self.raw_path.trade_calendar / f"{s}_{e}.parquet"
            df.to_parquet(filename, index=False)
            logger.info(f"Trade calendar saved to {filename}")
        elif len(data) == 0:
            logger.warning(
                f"No trade calendar data available for {start_date} to {end_date}"
            )
        elif ret == RET_ERROR:
            logger.error(f"Failed to download trade calendar: {ret}")
        else:
            logger.error(f"Unknown error: {ret}")

    def download_hkex_stock_list(self):

        # Direct URL (no login needed)
        url = "https://www.hkex.com.hk/eng/services/trading/securities/securitieslists/ListOfSecurities.xlsx"
        try:
            # The file has title rows on top → skip them
            df = pd.read_excel(url, skiprows=2, engine="openpyxl")
            # Save for later use
            filename = self.raw_path.ticker_mapper / "hkex_listed_securities.parquet"
            df.to_parquet(filename, index=False)
            logger.info(f"HKEX stock list saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to download HKEX stock list: {e}")

    def download_stock_list(self):
        ret, df = self.quote_ctx.get_stock_basicinfo(
            self.futu_market, SecurityType.STOCK
        )
        if ret == RET_OK and len(df) > 0:
            filename = self.raw_path.ticker_mapper / "stock_list.parquet"
            df.to_parquet(filename, index=False)
            logger.info(f"Stock list saved to {filename}")
        else:
            logger.error(f"Failed to download stock list: {ret}")

    def download_plate_list(self):
        # Concept list, such as AI, OpenClaw, AppleChain, etc.
        ret, data = self.quote_ctx.get_plate_list(
            market=self.futu_market, plate_class=Plate.CONCEPT
        )
        if ret == RET_OK:
            filename = self.raw_path.plate_list / "concept.parquet"
            data.to_parquet(filename, index=False)
            logger.info(f"Concept plate list saved to {filename}")
        else:
            logger.error(f"Failed to download concept plate list: {ret}")

        # Industry list
        ret, data = self.quote_ctx.get_plate_list(
            market=self.futu_market, plate_class=Plate.INDUSTRY
        )
        if ret == RET_OK:
            filename = self.raw_path.plate_list / "industry.parquet"
            data.to_parquet(filename, index=False)
            logger.info(f"Industry plate list saved to {filename}")
        else:
            logger.error(f"Failed to download industry plate list: {ret}")

        # All list
        ret, data = self.quote_ctx.get_plate_list(
            market=self.futu_market, plate_class=Plate.ALL
        )
        if ret == RET_OK:
            filename = self.raw_path.plate_list / "all.parquet"
            data.to_parquet(filename, index=False)
            logger.info(f"All plate list saved to {filename}")
        else:
            logger.error(f"Failed to download all plate list: {ret}")

    def download_owner_plate(self):

        # It's worth keep a point-in-time record of owner plate
        today = pd.Timestamp.today().strftime("%Y-%m-%d")
        output_filename = self.raw_path.owner_plate / f"{today}.parquet"
        input_filename = self.raw_path.ticker_mapper / "stock_list.parquet"
        stock_list_df = pd.read_parquet(input_filename)
        code_list = stock_list_df["code"].tolist()

        # The API only accept 200 codes at a time
        logger.info(f"Total {len(code_list)} stocks to download owner plate")
        logger.info(
            "FYI: The API only accept 200 codes at a time, need to download by batch"
        )
        ls = []
        for i in range(0, len(code_list), 200):
            ret, data = self.quote_ctx.get_owner_plate(code_list=code_list[i : i + 200])
            if ret == RET_OK:
                ls.append(data)
                logger.info(f"Downloaded owner plate for {i} to {i + 200} stocks")
            else:
                logger.error(f"Failed to download owner plate: {ret}")
            time.sleep(3)
        df = pd.concat(ls, axis=0)

        df.to_parquet(output_filename, index=False)
        logger.info(f"Owner plate saved to {output_filename}")

    def download_1day_bar(self, start_date: str, end_date: str):

        ret, data = self.quote_ctx.request_history_kline(
            code="HK.00001",
        )
        if ret == RET_OK and len(data) > 0:
            filename = self.raw_path.bar_1day / f"{start_date}_{end_date}.parquet"
            data.to_parquet(filename, index=False)
            logger.info(f"1day bar saved to {filename}")
        else:
            logger.error(f"Failed to download 1day bar: {ret}")


if __name__ == "__main__":
    try:
        with FutuDownloader("HK") as downloader:
            downloader.donwload_trade_calendar("2016-01-01", "2026-03-16")
            downloader.download_plate_list()
            downloader.download_hkex_stock_list()
            downloader.download_stock_list()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
