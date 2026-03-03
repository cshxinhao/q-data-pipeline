import click
import pandas as pd
from xtquant import xtdata
from . import downloader


@click.group()
def cli():
    pass


@cli.group()
def download():
    pass


@download.command("trade-cal")
@click.argument("--start", type=str, help="Start date (YYYYMMDD)")
@click.argument("--end", type=str, help="End date (YYYYMMDD)")
def download_trade_calendar(start: str, end: str):
    """
    Download trade calendar from XTQuant.
    """
    downloader.download_trade_calendar(start, end)


@cli.group()
def clean():
    pass


if __name__ == "__main__":
    cli()
