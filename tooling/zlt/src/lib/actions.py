from glob import glob
from subprocess import run
import fnmatch

import click

def deleteFileGlob(fileglob):
    for file in glob(fileglob, recursive=True):
        yield DeleteAction(file)

def handleConflicts(conflictSettings):
    status = run(["git", "status", "--porcelain=v1"], capture_output=True)
    status.check_returncode()
    fileActions = set()
    for line in status.stdout.splitlines():
        l = line.decode()
        fileActions.add((
            l[0],
            l[1],
            l[3:],
        ))
    for (ourAction, theirAction, fn) in fileActions:
        for fileglob in conflictSettings["ourFiles"]:
            if fnmatch.fnmatch(fn, fileglob) and ourAction != " ":
                yield RestoreOursAction(fn, ourAction == "D")
        for fileglob in conflictSettings["acceptTheirDeletions"]:
            if fnmatch.fnmatch(fn, fileglob) and ourAction == "U" and theirAction == "D":
                yield DeleteAction(fn)

class Action:
    def print(self):
        pass
    def apply(self):
        pass

class MultiAction(Action):
    def __init__(self, actions):
        self.__actions = actions
    def print(self):
        count = len(self.__actions)
        if count == 1:
            self.__actions[0].print()
        else:
            click.echo(f"Group of {count} actions:")
            for action in self.__actions:
                print("  ", end="")
                action.print()
    def apply(self):
        for action in self.__actions:
            action.apply()

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
        super().__init__(["git", "rm", "-rf", "--", path])
        self.__path = path
    def print(self):
        click.echo("Delete: "+click.style(self.__path, fg="red"))

class RestoreOursAction(MultiAction):
    def __init__(self, file, deletedByUs=False):
        self.__file = file
        if deletedByUs:
            super().__init__([
                DeleteAction(file)
            ])
        else:
            super().__init__([
                CommandAction(["git", "checkout", "--ours", "--", file]),
                CommandAction(["git", "add", "--", file]),
            ])
    def print(self):
        click.echo("Restore: "+click.style(self.__file, fg="cyan"))
