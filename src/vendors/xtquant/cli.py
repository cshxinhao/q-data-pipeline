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


@download.command("holiday")
def download_holiday():
    """
    Download holiday calendar from XTQuant.
    """
    downloader.download_holiday()


@download.command("index-weight")
def download_index_weight():
    """
    Download index weight from XTQuant.
    """
    downloader.download_index_weight()


@cli.group()
def clean():
    pass


if __name__ == "__main__":
    cli()
