def _create_indicator(p_data, window):
    close  = p_data[0]
    del p_data
    window_len = window
    return close.rolling(window_len).mean()

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "sma", "(window_len)"