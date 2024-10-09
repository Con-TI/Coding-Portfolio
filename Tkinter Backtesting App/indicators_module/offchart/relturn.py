def _create_indicator(p_data, window):
    close, vol = p_data[0],p_data[4]
    turn = close*vol
    window_len = window
    sma = turn.rolling(window_len).mean()
    return turn/sma

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "relturn", "(window_len)"