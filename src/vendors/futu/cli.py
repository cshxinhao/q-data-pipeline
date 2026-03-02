import click

@click.group()
def cli():
    pass

@cli.group()
def download():
    pass

@cli.group()
def clean():
    pass

if __name__ == "__main__":
    cli()
