import click
from . import downloader, cleaner
from src.logger import setup_logger

logger = setup_logger("tushare-cli")


@click.group()
def cli():
    pass


@cli.group()
def download():
    pass


@download.command("trade-cal")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
def download_trade_cal(start, end):
    try:
        downloader.download_trade_calendar(start_date=start, end_date=end)
    except Exception as e:
        logger.error(f"Error downloading trade calendar: {e}")
        raise e
    logger.info("Trade calendar downloaded.")


@download.command("ticker-mapper")
def download_ticker_mapper():
    try:
        downloader.download_ticker_mapper()
    except Exception as e:
        logger.error(f"Error downloading ticker mapper: {e}")
        raise e
    logger.info("Ticker mapper downloaded.")


@download.command("1day-bar")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def download_1day_bar(start, end, replace):
    try:
        downloader.download_1day_bar(start_date=start, end_date=end, replace=replace)
    except Exception as e:
        logger.error(f"Error downloading 1day bar: {e}")
        raise e
    logger.info("1day bar downloaded.")


@download.command("adj-factor")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def download_adj_factor(start, end, replace):
    try:
        downloader.download_adj_factor(start_date=start, end_date=end, replace=replace)
    except Exception as e:
        logger.error(f"Error downloading adj factor: {e}")
        raise e
    logger.info("Adj factor downloaded.")


@download.command("basic")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def download_basic(start, end, replace):
    try:
        downloader.download_basic(start_date=start, end_date=end, replace=replace)
    except Exception as e:
        logger.error(f"Error downloading basic data: {e}")
        raise e
    logger.info("Basic data downloaded.")


@download.command("indices")
def download_indices():
    try:
        downloader.download_indices()
    except Exception as e:
        logger.error(f"Error downloading indices: {e}")
        raise e
    logger.info("Indices downloaded.")


@download.command("index-constituent")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def download_index_constituent(start, end, replace):
    try:
        downloader.download_index_constituent(
            start_date=start, end_date=end, replace=replace
        )
    except Exception as e:
        logger.error(f"Error downloading index weights: {e}")
        raise e
    logger.info("Index weights downloaded.")


@cli.group()
def clean():
    pass


@clean.command("trade-cal")
def clean_trade_cal():
    try:
        cleaner.clean_trade_calendar()
    except Exception as e:
        logger.error(f"Error cleaning trade calendar: {e}")
        raise e
    logger.info("Trade calendar cleaned.")


@clean.command("identity")
def clean_identity():
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
def clean_1day_bar_price(start, end, replace):
    try:
        cleaner.clean_1day_bar(start_date=start, end_date=end, replace=replace)
    except Exception as e:
        logger.error(f"Error cleaning 1day bar: {e}")
        raise e
    logger.info("1day bar cleaned.")


@clean.command("adj-factor")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def clean_adj_factor(start, end, replace):
    try:
        cleaner.clean_adj_factor(start_date=start, end_date=end, replace=replace)
    except Exception as e:
        logger.error(f"Error cleaning adj factor: {e}")
        raise e
    logger.info("Adj factor cleaned.")


@clean.command("cap")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def clean_cap(start, end, replace):
    try:
        cleaner.clean_cap(start_date=start, end_date=end, replace=replace)
    except Exception as e:
        logger.error(f"Error cleaning cap: {e}")
        raise e
    logger.info("Cap cleaned.")


@clean.command("valuation")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def clean_valuation(start, end, replace):
    try:
        cleaner.clean_valuation(start_date=start, end_date=end, replace=replace)
    except Exception as e:
        logger.error(f"Error cleaning valuation: {e}")
        raise e
    logger.info("Valuation cleaned.")


@clean.command("dataset")
@click.option("--year", required=True, help="Year (YYYY)")
@click.option("--replace", type=bool, required=True, help="Replace existing files")
def clean_dataset(year, replace):
    try:
        cleaner.clean_dataset(year=year, replace=replace)
    except Exception as e:
        logger.error(f"Error cleaning dataset: {e}")
        raise e
    logger.info("Dataset cleaned.")


@clean.command("listed-days")
def clean_listed_days():
    try:
        cleaner.clean_listed_days()
    except Exception as e:
        logger.error(f"Error cleaning listed days: {e}")
        raise e
    logger.info("Listed days cleaned.")


if __name__ == "__main__":
    cli()
