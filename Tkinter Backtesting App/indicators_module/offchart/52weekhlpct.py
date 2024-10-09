def _create_indicator(p_data, window):
    high, low = p_data[2], p_data[3]
    high = high.rolling(252).max()
    low = low.rolling(252).min()
    return (high-low)/low

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "52weekhlpct", "()"