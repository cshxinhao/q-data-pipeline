import importlib

import click


class VendorLazyGroup(click.Group):
    def list_commands(self, ctx: click.Context):
        return ["tushare", "xtquant", "futu", "checker", "calculator"]

    def get_command(self, ctx: click.Context, cmd_name: str):
        if cmd_name == "tushare":
            module = importlib.import_module("src.vendors.tushare.cli")
            return module.cli
        if cmd_name == "xtquant":
            module = importlib.import_module("src.vendors.xtquant.cli")
            return module.cli
        if cmd_name == "futu":
            module = importlib.import_module("src.vendors.futu.cli")
            return module.cli
        if cmd_name == "checker":
            module = importlib.import_module("src.checker.cli")
            return module.cli
        if cmd_name == "calculator":
            module = importlib.import_module("src.calculator.cli")
            return module.cli
        return None


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]}, cls=VendorLazyGroup
)
def cli():
    """Q data pipeline command line interface."""


if __name__ == "__main__":
    cli()
