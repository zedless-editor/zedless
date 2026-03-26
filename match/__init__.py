def all(*items):
    items = list(filterEmptyRules(items))
    return {
        "all": items
    } if len(items) != 1 else items[0]

def any(*items):
    items = list(filterEmptyRules(items))
    return {
        "any": items
    } if len(items) != 1 else items[0]

def filterEmptyRules(rules):
    return filter(lambda x: x != {}, rules)
