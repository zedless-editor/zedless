from contextlib import chdir
from json import dumps
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

def editAstAdvanced(target, language, rules, rewrite, mode="all"):
    args = [
        "ast-grep", "scan", "--update-all",
        "--inline-rules", dumps({
            "id": "inline",
            "language": language,
            "rule": {
                mode: rules
            },
            "fix": rewrite
        }),
        "--color", "never"
    ]
    run(args + [target])

def deletePatterns(target, language, patterns, selector=None):
    for pattern in patterns:
        print("delete", pattern)
        editAst(target, language, pattern, "", selector)

def deleteDeclarations(kind, name, identifierField="name"):
    print("delete declarations:", kind, name)
    editAstAdvanced(
        "crates/",
        "rust",
        [
            {
                "kind": kind
            },
            {
                "has": {
                    "field": identifierField,
                    "pattern": name
                }
            }
        ],
        {
            "template": "",
            "expandStart": {
                "any": [
                    { "kind": "line_comment" },
                    { "kind": "attribute_item" }
                ]
            }
        },
    )

def removeSymbolImports(symbol):
    print("remove imports for symbol", symbol)
    editAst(
        "crates/",
        "rust",
        f"use $CRATE::{{$$$BEFORE, {symbol}, $$$AFTER}};",
        f"use $CRATE::{{$$$BEFORE, $$$AFTER}};",
        "use_declaration"
    )
    deletePatterns("crates/", "rust", [
        f"use $CRATE::{symbol};"
    ], selector="use_declaration")

def nullifyExpressions(patterns, empty, deleteStatements=False):
    if deleteStatements:
        deletePatterns("crates/", "rust", [f"{p};" for p in patterns])
    for pattern in patterns:
        print("nullify expression", pattern)
        editAst(
            "crates/",
            "rust",
            pattern,
            empty
        )

bannedPublicFunctions = [
    "send_telemetry",
]

with chdir("source"):
    for function in bannedPublicFunctions:
        deletePatterns("crates/", "rust", [
            f"pub fn {function}($$$) -> $_;",
            f"pub fn {function}($$$);",
        ], "function_signature_item")
        deletePatterns("crates/", "rust", [
            f"pub fn {function}($$$) -> $_ {{$$$}}",
            f"pub fn {function}($$$) {{$$$}}",
        ], "function_item")
        deletePatterns("crates/", "rust", [
            f"{function}($$$);",
            f"$_::{function}($$$);",
        ], "expression_statement")
        removeSymbolImports(function)

    nullifyExpressions([
        "telemetry::event!($$$)",
    ], "()", deleteStatements=True)
