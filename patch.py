from contextlib import chdir
from subprocess import run

def editAst(target, language, pattern, rewrite, selector=None):
    args = [
        "ast-grep", "run", "--update-all",
        "--lang", language,
        "--pattern", pattern,
        "--rewrite", rewrite,
        "--color", "never"
    ]
    if selector:
        args.extend(["--selector", selector])
    run(args + [target])

def deletePatterns(target, language, patterns, selector=None):
    for pattern in patterns:
        print("delete", pattern)
        editAst(target, language, pattern, "", selector)

with chdir("source"):
    deletePatterns("crates/", "rust", [
        "telemetry::event!($$$);",
    ])
