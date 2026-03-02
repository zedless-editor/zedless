from contextlib import chdir, contextmanager
from glob import glob
from json import dumps
from os.path import exists
from subprocess import run

import toml

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

def removeSymbolImports(symbol):
    print("remove imports for symbol", symbol)
    editAstAdvanced(
        "crates/",
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

def removeFieldsInDeclarations(identifier):
    print("remove fields and parameters in declarations:", identifier)
    editAstAdvanced(
        "crates/", "rust", [
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

def removeExprArguments(string):
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
                }
            ],
            "stopBy": "end"
        }
    }
    editAstAdvanced(
        "crates/", "rust",
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

bannedCrates = [
    "telemetry"
]

bannedModules = [
    ("web_search_providers", "cloud")
]

bannedFunctions = [
    "report_discovered_project_type_events",
    "send_telemetry",
    "set_authenticated_user_info",
    "telemetry",
    "telemetry_report_accepted_edits",
    "telemetry_report_rejected_edits",
]

bannedStructs = [
    "AiUpsellCard",
    "EditPredictionOnboarding",
    "LlmApiToken",
    "SystemSpecs",
    "Telemetry",
    "TelemetrySettings",
    "TelemetryState",
    "ZedAiOnboarding",
]

bannedArguments = [
    "llm_api_token",
    "telemetry",
]

with chdir("source"):
    cratesToDelete = []
    for crate in bannedCrates:
        if exists(f"crates/{crate}"):
            cratesToDelete.append(crate)

    if len(cratesToDelete) > 0:
        for crate in cratesToDelete:
            print("delete crate:", crate)
            run(["rm", "-rf", f"crates/{crate}/"])

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

    for (crate, mod) in bannedModules:
        print("delete module:", crate, mod)
        deletePatterns(f"crates/{crate}/", "rust", [
            f"mod {mod};"
        ])
        run(["rm", "-f", f"crates/{crate}/src/{mod}.rs"])

    for function in bannedFunctions:
        deleteDeclarations("function_signature_item", function)
        deleteDeclarations("function_item", function)
        deletePatterns("crates/", "rust", [
            f"{function}($$$);",
            f"$_::{function}($$$);",
        ], "expression_statement")
        deletePatternsAdvanced("crates/", "rust", "expression_statement", [
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
        removeSymbolImports(function)

    for struct in bannedStructs:
        deleteDeclarations("struct_item", struct)
        deleteDeclarations("impl_item", struct, "type")
        removeSymbolImports(struct)

    for arg in bannedArguments:
        removeFieldsInDeclarations(arg)
        removeExprArguments(arg)

    nullifyExpressions([
        "telemetry::event!($$$)",
    ], "()", deleteStatements=True)

    deletePatterns("crates/", "rust", [
        "if let $_ = telemetry { $$$ }",
        "if let $_ = telemetry.$_() { $$$ }",
    ])

    deletePatterns("crates/", "rust", [
        "let system_id = $_;",
        "let metrics_id = $_;",
        "if let $_ = system_id { $$$ }",
        "if let $_ = metrics_id { $$$ }",
    ])
