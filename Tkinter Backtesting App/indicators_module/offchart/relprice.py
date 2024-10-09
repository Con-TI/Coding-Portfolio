def _create_indicator(p_data, window):
    close = p_data[0]
    window_len = window
    sma = close.rolling(window_len).mean()
    return close/sma

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "relprice", "(window_len)"