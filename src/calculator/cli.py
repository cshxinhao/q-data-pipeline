# To calculate some commonly used fields, for downstream use.
import click
import pandas as pd
from src.calculator.config import CalculatorOutputPath
from src.logger import setup_logger

logger = setup_logger(__name__)


@click.group()
def cli():
    pass


@cli.group()
def calc():
    pass


@calc.command("ml-common")
@click.option("--market", default="China", help="Market to calculate.")
def calc_ml_common(market: str):
    if market == "China":
        from src.vendors.tushare.config import DataCleanPath

        logger.info(f"Loading data from {DataCleanPath().dataset}")
        df = pd.read_parquet(
            DataCleanPath().dataset,
            columns=[
                "datetime",
                "symbol",
                "open",
                "high",
                "low",
                "close",
                "vwap",
                "volume",
                "amount",
                "cap_total",
                "industry",
                "board",
            ],
        ).set_index(["datetime", "symbol"])

    else:
        raise NotImplementedError(f"Market {market} not implemented.")

    logger.info("Calculating adv & forward returns.")

    # Calculate adv
    df["adv"] = df["amount"].unstack().rolling(window=20).mean().stack()

    # Calculate forward returns
    for combo in [("close", 0), ("open", 1), ("vwap", 1)]:
        field, delay = combo
        px2d = df[field].unstack()
        df[f"{field}_fr1d_delay{delay}d"] = (
            px2d.shift(-1 - delay) / px2d.shift(-delay) - 1
        ).stack()
        df[f"{field}_fr2d_delay{delay}d"] = (
            px2d.shift(-2 - delay) / px2d.shift(-delay) - 1
        ).stack()
        df[f"{field}_fr3d_delay{delay}d"] = (
            px2d.shift(-3 - delay) / px2d.shift(-delay) - 1
        ).stack()
        df[f"{field}_fr5d_delay{delay}d"] = (
            px2d.shift(-5 - delay) / px2d.shift(-delay) - 1
        ).stack()
        df[f"{field}_fr10d_delay{delay}d"] = (
            px2d.shift(-10 - delay) / px2d.shift(-delay) - 1
        ).stack()
        df[f"{field}_fr20d_delay{delay}d"] = (
            px2d.shift(-20 - delay) / px2d.shift(-delay) - 1
        ).stack()

    df = df.reset_index()

    df.to_parquet(
        CalculatorOutputPath().ml_common_data / "ml_common_data.parquet",
        index=False,
    )
    logger.info(
        f"ml_common_data.parquet saved to {CalculatorOutputPath().ml_common_data}"
    )


if __name__ == "__main__":
    cli()
