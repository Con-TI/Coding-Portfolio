import numpy as np
def _create_indicator(p_data, window):
    close  = p_data[0]
    del p_data
    window_len = window
    change = np.log(close) - np.log(close.shift(1))
    change = change - change.rolling(window_len).mean()
    return change.rolling(window_len).std()
    
def _create_indicator_all(p_data, window):
    return _create_indicator(p_data,window)

def _desc():
    return "volatility", "(window)"