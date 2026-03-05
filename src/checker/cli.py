import click
from . import validator
from .config import CheckerReportPath


@click.group
def check():
    pass


@check.command("duplicate")
@click.option(
    "--market", type=click.Choice(["China"]), required=True, help="Market to check."
)
@click.option(
    "--vendor", type=click.Choice(["tushare"]), required=True, help="Vendor to use."
)
def check_duplicate(market: str, vendor: str):
    df = validator.check_duplicate(market, vendor)
    if df.empty:
        click.echo("No duplicate found.")
    else:
        filename = CheckerReportPath(vendor).base_dir / "duplicate.csv"
        click.echo(f"{len(df)} duplicate found. Saved to {filename}")
        df.to_csv(filename, index=False)


@check.command("null")
@click.option(
    "--market", type=click.Choice(["China"]), required=True, help="Market to check."
)
@click.option(
    "--vendor", type=click.Choice(["tushare"]), required=True, help="Vendor to use."
)
def check_nulls(market: str, vendor: str):
    df = validator.check_nulls(market, vendor)
    if df.empty:
        click.echo("No null found.")
    else:
        filename = CheckerReportPath(vendor).base_dir / "null.csv"
        click.echo(f"{len(df)} null found. Saved to {filename}")
        df.to_csv(filename, index=False)


@check.command("volume")
@click.option(
    "--market", type=click.Choice(["China"]), required=True, help="Market to check."
)
@click.option(
    "--vendor", type=click.Choice(["tushare"]), required=True, help="Vendor to use."
)
def check_volume(market: str, vendor: str):
    df = validator.check_volume(market, vendor)
    if df.empty:
        click.echo("No volume issue found.")
    else:
        filename = CheckerReportPath(vendor).base_dir / "volume.csv"
        click.echo(f"{len(df)} volume issue found. Saved to {filename}")
        df.to_csv(filename, index=False)


@check.command("returns-outlier")
@click.option(
    "--market", type=click.Choice(["China"]), required=True, help="Market to check."
)
@click.option(
    "--vendor", type=click.Choice(["tushare"]), required=True, help="Vendor to use."
)
def check_returns_outlier(market: str, vendor: str):
    df = validator.check_returns_outlier(market, vendor)
    if df.empty:
        click.echo("No returns outlier found.")
    else:
        filename = CheckerReportPath(vendor).base_dir / "returns_outlier.csv"
        click.echo(f"{len(df)} returns outlier found. Saved to {filename}")
        df.sort_values(by=["symbol", "datetime"]).to_csv(filename, index=False)


@check.command("logic-consistency")
@click.option(
    "--market", type=click.Choice(["China"]), required=True, help="Market to check."
)
@click.option(
    "--vendor", type=click.Choice(["tushare"]), required=True, help="Vendor to use."
)
def check_logic_consistency(market: str, vendor: str):
    df = validator.check_logic_consistency(market, vendor)
    if df.empty:
        click.echo("No logic consistency issue found.")
    else:
        filename = CheckerReportPath(vendor).base_dir / "logic_consistency.csv"
        click.echo(f"{len(df)} logic consistency issue found. Saved to {filename}")
        df.to_csv(filename, index=False)


@check.command("cross-check")
def cross_check_between_vendors():
    df = validator.cross_check_between_vendors()
    if df.empty:
        click.echo("No cross check issue found.")
    else:
        filename = (
            CheckerReportPath("cross_check").base_dir
            / "cross_check_inconsistencies.csv"
        )
        click.echo(f"{len(df)} cross check issue found. Saved to {filename}")
        df.to_csv(filename, index=False)


if __name__ == "__main__":
    check()
