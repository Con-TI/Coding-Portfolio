def _create_indicator(p_data, params):
    close = p_data[0]
    window_len = params[0]
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
    
    window_len = params[1]
    rsilow = rsi.rolling(window_len).min()
    rsihigh = rsi.rolling(window_len).max()
    storsi = 100*(rsi-rsilow)/(rsihigh-rsilow)
    storsi = storsi.fillna(50)
    
    return storsi

def _create_indicator_all(p_data, params):
    return _create_indicator(p_data, params)

def _desc():
    return "storsi", "(rsi_window_len,sto_window_len)"