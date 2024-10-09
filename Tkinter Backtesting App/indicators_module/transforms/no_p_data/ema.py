def _transform_indicator(indicator, window):
    window_len = window
    return indicator.ewm(span=window_len,adjust=False).mean()

def _transform_indicator_all(indicator, window):
    return _transform_indicator(indicator, window)


def _desc():
    return "ema", "(window_len)"