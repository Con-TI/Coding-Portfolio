def _create_indicator(p_data, window):
    close  = p_data[0]
    window_len = window
    diffs = close.diff()
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

def _create_indicator_all(p_data,window):
    return _create_indicator(p_data,window)

def _desc():
    return "rsi", "(window_len)"