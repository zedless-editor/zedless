def functionCall(name):
    return {
        "kind": "call_expression",
        "has": {
            "kind": "identifier",
            "pattern": name
        }
    }


def functionDefinition(name):
    return {
        "kind": "function_item",
        "has": {
            "field": "name",
            "pattern": name
        }
    }

def insideMethodCall(name):
    return {
        "inside": {
            "kind": "arguments",
            "inside": {
                "kind": "call_expression",
                "has": {
                    "kind": "field_expression",
                    "has": {
                        "kind": "field_identifier",
                        "regex": f"^{name}$"
                    }
                }
            }
        }
    }
