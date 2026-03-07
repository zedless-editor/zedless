def functionCall(name):
    return {
        "kind": "call_expression",
        "has": {
            "kind": "identifier",
            "pattern": name
        }
    }


def functionCallWith(identifier=None, withinArguments=None, matchRecursive=True):
    extraRules = []
    if identifier:
        extraRules.append({
            "has": identifier
        })
    if withinArguments:
        extraRules.append({
            "has": {
                "kind": "arguments",
                "has": withinArguments | ({
                    "stopBy": "end"
                } if matchRecursive else {})
            }
        })
    return {
        "kind": "call_expression",
        "all": extraRules
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

def implDefinition(name):
    return {
        "kind": "impl_item",
        "has": {
            "field": "type",
            "regex": f"^{name}$"
        }
    }

def structDefinition(name):
    return {
        "kind": "struct_item",
        "has": {
            "field": "name",
            "regex": f"^{name}$"
        }
    }
