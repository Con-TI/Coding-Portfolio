def _create_indicator(p_data, window):
    low= p_data[3]
    del p_data
    window_len = window
    return low.rolling(window_len).min()

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "min", "(window_len)"