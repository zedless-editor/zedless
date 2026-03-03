from contextlib import chdir, contextmanager
from glob import glob
from json import dumps
from os.path import exists
from subprocess import run
from config import CONFIG

import toml

import match
import match.rust

@contextmanager
def editTomlDocument(file):
    def callback(v):
        with open(file, "w") as f:
            toml.dump(v, f)
    value = None
    with open(file, "r") as f:
        value = toml.load(f)
    if value:
        yield value, callback

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

def deletePatternsAdvanced(target, language, kind, patterns):
    print("delete advanced", kind)
    editAstAdvanced(
        target,
        language,
        [
            { "kind": kind },
            { "any": patterns }
        ],
        "",
        mode="all"
    )

def deleteDeclarations(kind, name, identifierField="name", target="crates/"):
    print("delete declarations:", kind, name)
    editAstAdvanced(
        target,
        "rust",
        [
            {
                "kind": kind
            },
            {
                "has": {
                    "field": identifierField,
                    "regex": f"^{name}$"
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

def removeSymbolImports(symbol, target="crates/"):
    print("remove imports for symbol", symbol)
    editAstAdvanced(
        target,
        "rust",
        [
            {
                "inside": { "kind": "use_list" },
                "any": [
                    {
                        "kind": "identifier",
                        "pattern": symbol
                    },
                    {
                        "kind": "scoped_identifier",
                        "has": {
                            "field": "name",
                            "pattern": symbol
                        }
                    }
                ],
            }
        ],
        {
            "template": "",
            "expandEnd": { "regex": "," }
        }
    )
    deletePatterns("crates/", "rust", [
        f"use $CRATE::{symbol};",
        f"pub use $CRATE::{symbol};",
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

def removeFieldsInDeclarations(identifier, target="crates/"):
    print("remove fields and parameters in declarations:", identifier)
    editAstAdvanced(
        target,
        "rust",
        [
            {
                "all": [
                    { "kind": "field_declaration" },
                    { "has": { "field": "name", "regex": f"^{identifier}$" } }
                ]
            },
            {
                "all": [
                    { "kind": "parameter"},
                    { "has": { "field": "pattern", "pattern": identifier } }
                ]
            },
        ],
        {
            "template": "",
            "expandStart": {
                "any": [
                    { "kind": "line_comment" },
                    { "kind": "attribute_item" }
                ]
            },
            "expandEnd": { "regex": "," }
        },
        mode="any"
    )

def removeExprArguments(string, target="crates/"):
    print("remove expression arguments:", string)
    matchingIdentifier = {
        "kind": "identifier",
        "pattern": string
    }
    matchingCallExpression = {
        "kind": "call_expression",
        "has": {
            "any": [
                matchingIdentifier,
                {
                    "kind": "field_expression",
                    "pattern": f"$_.{string}"
                },
                {
                    "kind": "field_expression",
                    "pattern": f"{string}.$_"
                },
                {
                    "kind": "field_expression",
                    "pattern": f"$_.{string}().$_"
                },
            ]
        }
    }
    matchingSome = {
        "kind": "call_expression",
        "pattern": "Some($_)",
        "has": {
            "kind": "arguments",
            "has": {
                "any": [
                    matchingIdentifier,
                    matchingCallExpression
                ]
            }
        }
    }
    matchingReferenceExpression = {
        "kind": "reference_expression",
        "has": matchingIdentifier
    }
    editAstAdvanced(
        target,
        "rust",
        [
            {
                "inside": {
                    "any": [
                        { "kind": "arguments" },
                        { "kind": "field_initializer_list" }
                    ]
                }
            },
            {
                "any": [
                    matchingIdentifier,
                    matchingCallExpression,
                    matchingSome,
                    matchingReferenceExpression,
                    {
                        "kind": "shorthand_field_initializer",
                        "has": matchingIdentifier
                    },
                    {
                        "kind": "field_initializer",
                        "has": {
                            "any": [
                                matchingIdentifier,
                                matchingCallExpression,
                                matchingSome,
                                matchingReferenceExpression,
                                {
                                    "kind": "field_identifier",
                                    "regex": f"^{string}$"
                                },
                            ]
                        }
                    }
                ]
            }
        ],
        {
            "template": "",
            "expandEnd": { "regex": "," }
        },
        mode="all"
    )

with chdir("source"):
    cratesToDelete = []
    for crate in CONFIG.bannedCrates:
        if exists(f"crates/{crate}"):
            cratesToDelete.append(crate)

    if len(cratesToDelete) > 0:
        for crate in cratesToDelete:
            print("delete crate:", crate)
            run(["rm", "-rf", f"crates/{crate}/"])

        deletePatterns("crates/", "rust", [f"use {crate}::$_;" for crate in cratesToDelete])
        with editTomlDocument("Cargo.toml") as (data, write):
            data["workspace"]["members"] = list(filter(
                lambda m: m.removeprefix("crates/") not in cratesToDelete,
                data["workspace"]["members"]
            ))
            for crate in cratesToDelete:
                if crate in data["workspace"]["dependencies"]:
                    del data["workspace"]["dependencies"][crate]
                for prof in data["profile"]:
                    if "package" in data["profile"][prof] and crate in data["profile"][prof]["package"]:
                        del data["profile"][prof]["package"][crate]
            write(data)

        for manifest in glob("crates/*/Cargo.toml"):
            with editTomlDocument(manifest) as (data, write):
                for crate in cratesToDelete:
                    if "dependencies" in data and crate in data["dependencies"]:
                        del data["dependencies"][crate]
                write(data)

    for (crate, mod) in CONFIG.bannedModules:
        print("delete module:", crate, mod)
        deletePatterns(f"crates/{crate}/", "rust", [
            f"mod {mod};"
        ])
        run(["rm", "-f", f"crates/{crate}/src/{mod}.rs"])

    for (target, cfg) in CONFIG.perDirectory.items():
        for function in cfg.bannedFunctions:
            deleteDeclarations("function_signature_item", function, target=target)
            deleteDeclarations("function_item", function, target=target)
            deletePatterns(target, "rust", [
                f"{function}($$$);",
                f"$_::{function}($$$);",
            ], "expression_statement")
            deletePatternsAdvanced(target, "rust", "expression_statement", [
                {
                    "has": {
                        "kind": "call_expression",
                        "has": {
                            "kind": "field_expression",
                            "has": {
                                "kind": "field_identifier",
                                "regex": f"^{function}$"
                            }
                        }
                    }
                }
            ])
            removeSymbolImports(function, target=target)
    
        for struct in cfg.bannedStructs:
            deleteDeclarations("struct_item", struct, target=target)
            deleteDeclarations("impl_item", struct, identifierField="type", target=target)
            removeSymbolImports(struct)
    
        for arg in cfg.bannedArguments:
            removeFieldsInDeclarations(arg, target=target)
            removeExprArguments(arg, target=target)

    nullifyExpressions([
        "telemetry::event!($$$)",
    ], "()", deleteStatements=True)

    deletePatterns("crates/", "rust", [
        "if let $_ = telemetry { $$$ }",
        "if let $_ = telemetry.$_() { $$$ }",
        "telemetry.$_($$$);",
        "let (telemetry, is_via_ssh) = { $$$ };"
    ])
    
    deleteDeclarations("let_declaration", "telemetry", "pattern")

    deletePatterns("crates/", "rust", [
        "let system_id = $_;",
        "let metrics_id = $_;",
        "if let $_ = system_id { $$$ }",
        "if let $_ = metrics_id { $$$ }",
    ])

    deletePatterns("crates/web_search_providers/", "rust", [
        "register_zed_web_search_provider($$$)"
    ])
