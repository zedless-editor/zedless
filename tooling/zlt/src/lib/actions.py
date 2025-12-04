from glob import glob
from subprocess import run

import click

def deleteFileGlob(fileglob):
    for file in glob(fileglob, recursive=True):
        yield DeleteAction(file)

class Action:
    def print(self):
        pass
    def apply(self):
        pass

class CommandAction(Action):
    def __init__(self, args):
        self.__args = args
        super().__init__()
    def print(self):
        click.echo(f"Run command: {str(self.__args)}")
    def apply(self):
        run(self.__args)

class DeleteAction(CommandAction):
    def __init__(self, path):
        super().__init__(["rm", "-rf", path])
        self.__path = path
    def print(self):
        click.echo("Delete: "+click.style(f"{self.__path}", fg="red"))
