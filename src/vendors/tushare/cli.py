import click
from . import downloader
from . import cleaner


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
    downloader.download_trade_calendar(start_date=start, end_date=end)


@download.command("ticker-mapper")
def download_ticker_mapper():
    downloader.download_ticker_mapper()


@download.command("1day-bar-price")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", is_flag=True, default=False, help="Replace existing files")
def download_1day_bar_price(start, end, replace):
    downloader.download_1day_bar_price(start_date=start, end_date=end, replace=replace)


@download.command("adj-factor")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", is_flag=True, default=False, help="Replace existing files")
def download_adj_factor(start, end, replace):
    downloader.download_adj_factor(start_date=start, end_date=end, replace=replace)


@download.command("basic")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", is_flag=True, default=False, help="Replace existing files")
def download_basic(start, end, replace):
    downloader.download_basic(start_date=start, end_date=end, replace=replace)


@cli.group()
def clean():
    pass


@clean.command("1day-bar-price")
@click.option("--start", required=True, help="Start date (YYYYMMDD)")
@click.option("--end", required=True, help="End date (YYYYMMDD)")
@click.option("--replace", is_flag=True, default=False, help="Replace existing files")
def clean_1day_bar_price(start, end, replace):
    cleaner.clean_1day_bar_range(start_date=start, end_date=end, replace=replace)


if __name__ == "__main__":
    cli()
