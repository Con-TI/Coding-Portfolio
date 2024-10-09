def _create_indicator(p_data, window):
    vol = p_data[4]
    window_len = window
    sma = vol.rolling(window_len).mean()
    return vol/sma

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "relvol", "(window_len)"