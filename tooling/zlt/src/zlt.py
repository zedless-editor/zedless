import click

from commands.apply import apply

@click.group()
def cli():
    pass

cli.add_command(apply)

if __name__ == "__main__":
    cli()
