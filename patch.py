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
                "kind": "identifier",
                "pattern": symbol
            }
        ],
        {
            "template": "",
            "expandEnd": { "regex": "," }
        }
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

bannedFunctions = [
    "report_discovered_project_type_events",
    "send_telemetry",
    "set_authenticated_user_info",
    "telemetry",
]

bannedStructs = [
    "LlmApiToken",
    "SystemSpecs",
    "Telemetry",
    "TelemetrySettings",
    "TelemetryState",
]

bannedArguments = [
    "llm_api_token",
    "telemetry",
]

with chdir("source"):
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
        "let system_id = $_;",
        "let metrics_id = $_;",
        "if let $_ = system_id { $$$ }",
        "if let $_ = metrics_id { $$$ }",
    ])
