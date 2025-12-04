import click
from lib.actions import deleteFileGlob, handleConflicts
from lib.config import CONFIG

@click.command()
def apply():
    actions = []
    for g in CONFIG["deleteFileGlobs"]:
        actions.extend(deleteFileGlob(g))
    actions.extend(handleConflicts(CONFIG["conflicts"]))
    if len(actions) == 0:
        print("Nothing to do.")
        exit(0)
    print("Will perform actions:")
    for action in actions:
        action.print()
    if click.confirm(f"Apply {len(actions)} actions?"):
        for action in actions:
            action.apply()
    else:
        print("Cancelled")
