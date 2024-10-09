def _create_indicator(p_data, window):
    close = p_data[0]
    del p_data
    window_len = window
    return close.ewm(span=window_len,adjust=False).mean()

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)
    

def _desc():
    return "ema", "(window_len)"