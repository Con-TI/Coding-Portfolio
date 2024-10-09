def _transform_indicator(indicator, window):
    window_len = window
    return indicator.rolling(window_len).mean()

def _transform_indicator_all(indicator, window):
    return _transform_indicator(indicator,window)

def _desc():
    return "sma", "(window_len)"