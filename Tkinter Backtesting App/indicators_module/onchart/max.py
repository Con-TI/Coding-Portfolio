def _create_indicator(p_data, window):
    high = p_data[2]
    del p_data
    window_len = window
    return high.rolling(window_len).max()

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "max", "(window_len)"