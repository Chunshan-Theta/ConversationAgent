def get_value_from_dict_by_multi_name(d: dict, names: [str], default=None):
    for name in names:
        if name in d:
            return d[name]
    return default


def compute_by_string(a, symbol, b):
    pass_token = True
    if symbol != "=":
        a, b = float(a), float(b)
    if symbol == "=":
        if a != b:
            pass_token = False
    elif symbol == ">":
        if not a > b:
            pass_token = False
    elif symbol == "<":
        if not a < b:
            pass_token = False
    elif symbol == "<=":
        if not a < b:
            pass_token = False
    elif symbol == ">=":
        if not a >= b:
            pass_token = False
    return pass_token