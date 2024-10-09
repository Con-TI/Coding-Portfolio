def _create_indicator(p_data, window):
    close, _ , high ,low, _, _, _  = p_data
    window_len = window
    high = high.rolling(window_len).max()
    low = low.rolling(window_len).min()
    sto = (close - low)/(high-low)*100
    sto = sto.fillna(50)
    return sto

def _create_indicator_all(p_data,window):
    return _create_indicator(p_data,window)

def _desc():
    return "sto", "(window_len)"