def _create_indicator(p_data, window):
    close, low = p_data[0], p_data[3]
    low = low.rolling(252).min()
    return (close-low)/low

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "52weeklowpct", "()"