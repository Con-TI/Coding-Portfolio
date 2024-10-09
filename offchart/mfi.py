def _create_indicator(p_data, window):
    close, vol = p_data[0], p_data[4]
    turn = close*vol
    window_len = window
    diffs = turn.diff()
    is_gain = diffs>=0
    is_loss = diffs<0
    gain, loss = diffs, -diffs
    gain[is_loss] = 0 
    loss[is_gain] = 0
    gain = gain.rolling(window_len).mean()
    loss = loss.rolling(window_len).mean()
    rs = gain/loss
    rsi = 100-100/(1+rs)
    rsi = rsi.fillna(50)
    return rsi

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "mfi", "(window_len)"