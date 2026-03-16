import click
from src.logger import setup_logger
from .downloader import FutuDownloader
from . import cleaner

logger = setup_logger(__name__)


@click.group()
def cli():
    pass


@cli.group()
def download():
    pass


@download.command("trade-cal")
@click.option("--market", required=True, help="Market (HK or US)")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
def download_trade_calendar(market: str, start_date: str, end_date: str):
    try:
        with FutuDownloader(market=market) as downloader:
            downloader.donwload_trade_calendar(start_date, end_date)
    except Exception as e:
        logger.error(f"Error downloading trade calendar: {e}")
        raise e


@download.command("hkex-stock-list")
@click.option("--market", required=True, help="Market (HK or US)")
def download_hkex_stock_list(market: str):
    try:
        with FutuDownloader(market=market) as downloader:
            downloader.download_hkex_stock_list()
    except Exception as e:
        logger.error(f"Error downloading HKEX stock list: {e}")
        raise e


@download.command("stock-list")
@click.option("--market", required=True, help="Market (HK or US)")
def download_stock_list(market: str):
    try:
        with FutuDownloader(market=market) as downloader:
            downloader.download_stock_list()
    except Exception as e:
        logger.error(f"Error downloading stock list: {e}")
        raise e


@download.command("plate-list")
@click.option("--market", required=True, help="Market (HK or US)")
def download_plate_list(market: str):
    try:
        with FutuDownloader(market=market) as downloader:
            downloader.download_plate_list()
    except Exception as e:
        logger.error(f"Error downloading plate list: {e}")
        raise e


@download.command("owner-plate")
@click.option("--market", required=True, help="Market (HK or US)")
def download_owner_plate(market: str):
    try:
        with FutuDownloader(market=market) as downloader:
            downloader.download_owner_plate()
    except Exception as e:
        logger.error(f"Error downloading owner plate: {e}")
        raise e


@cli.group()
def clean():
    pass


@clean.command("trade-cal")
@click.option("--market", required=True, help="Market (HK or US)")
def clean_trade_calendar(market: str):
    try:
        cleaner.clean_trade_calendar(market)
    except Exception as e:
        logger.error(f"Error cleaning trade calendar: {e}")
        raise e


@clean.command("identity")
@click.option("--market", required=True, help="Market (HK or US)")
def clean_identity(market: str):
    try:
        cleaner.clean_identity(market)
    except Exception as e:
        logger.error(f"Error cleaning identity: {e}")
        raise e


if __name__ == "__main__":
    cli()
