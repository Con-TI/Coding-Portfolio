def _transform_indicator(indicator, params):
    q = params
    return indicator.shift(q)

def _transform_indicator_all(indicator, params):
    return _transform_indicator(indicator, params)

def _desc():
    return "shift", "(shift_num)"