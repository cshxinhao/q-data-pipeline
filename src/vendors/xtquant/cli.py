import click
from . import downloader, cleaner, subscriber
from src.logger import setup_logger

logger = setup_logger("xtquant-cli")


@click.group()
def cli():
    pass


@cli.group()
def download():
    pass


@download.command("contracts")
def download_contracts():
    """
    Download expired (delisted) contracts from XTQuant.
    """
    try:
        downloader.download_contracts()
    except Exception as e:
        logger.error(f"Error downloading contracts: {e}")
        raise e
    logger.info("Contracts downloaded.")


@download.command("sector-data")
def download_sector_data():
    """
    Download sector data from XTQuant.
    """
    try:
        downloader.download_sector_data()
    except Exception as e:
        logger.error(f"Error downloading sector data: {e}")
        raise e
    logger.info("Sector data downloaded.")


@download.command("index-weight")
def download_index_weight():
    """
    Download index weight from XTQuant.
    """
    try:
        downloader.download_index_weight()
    except Exception as e:
        logger.error(f"Error downloading index weight: {e}")
        raise e
    logger.info("Index weight downloaded.")


@download.command("bar")
def download_bar():
    """
    Download bar data from XTQuant.
    """
    try:
        downloader.download_1day_bar()
        downloader.download_1min_bar()
    except Exception as e:
        logger.error(f"Error downloading bar data: {e}")
        raise e
    logger.info("1day & 1min Bar data downloaded.")


@download.command("financial")
def download_financial():
    """
    Download financial data from XTQuant.
    """
    try:
        downloader.download_financial()
    except Exception as e:
        logger.error(f"Error downloading financial data: {e}")
        raise e
    logger.info("Financial data downloaded.")


@cli.group()
def clean():
    pass


@clean.command("trade-cal")
def clean_trade_calendar():
    """
    Clean trade calendar from XTQuant.
    """
    try:
        cleaner.clean_trade_calendar()
    except Exception as e:
        logger.error(f"Error cleaning trade calendar: {e}")
        raise e
    logger.info("Trade calendar cleaned.")


@clean.command("identity")
def clean_identity():
    """
    Clean identity from XTQuant.
    """
    try:
        cleaner.clean_identity()
    except Exception as e:
        logger.error(f"Error cleaning identity: {e}")
        raise e
    logger.info("Identity cleaned.")


@clean.command("1day-bar")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def clean_1day_bar(start: str, end: str, replace: bool):
    """
    Clean 1day bar from XTQuant.
    """
    try:
        cleaner.clean_1day_bar(start, end, replace)
    except Exception as e:
        logger.error(f"Error cleaning 1day bar: {e}")
        raise e
    logger.info(f"1day bar cleaned for {start} to {end}.")


@clean.command("1min-bar")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def clean_1min_bar(start: str, end: str, replace: bool):
    """
    Clean 1min bar from XTQuant.
    """
    try:
        cleaner.clean_1min_bar(start, end, replace)
    except Exception as e:
        logger.error(f"Error cleaning 1min bar: {e}")
        raise e
    logger.info(f"1min bar cleaned for {start} to {end}.")


@clean.command("realtime-quote")
@click.option("--date", required=True, help="Date (YYYYMMDD)")
def clean_real_time_quote(date: str):
    """
    Clean real-time quote from XTQuant.
    """
    try:
        cleaner.clean_real_time_quote(date)
    except Exception as e:
        logger.error(f"Error cleaning real-time quote: {e}")
        raise e
    logger.info(f"Real-time quote cleaned for {date}.")


@cli.group()
def subscribe():
    pass


@subscribe.command("realtime-quote")
def subscribe_real_time_quote():
    """
    Subscribe real-time quote data from XTQuant.
    """
    try:
        subscriber.subscribe_realtime_quote()
    except Exception as e:
        logger.error(f"Error subscribing real-time quote: {e}")
        raise e
    logger.info("Real-time quote subscription started.")


if __name__ == "__main__":
    cli()
