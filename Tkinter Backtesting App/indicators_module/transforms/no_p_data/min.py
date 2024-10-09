def _transform_indicator(indicator, params):
    window_len = params
    return indicator.rolling(window_len).min()

def _transform_indicator_all(indicator, params):
    return _transform_indicator(indicator,params)

def _desc():
    return "min", "(window_len)"