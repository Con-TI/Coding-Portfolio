import numpy as np
def _create_indicator(p_data, params):
    close  = p_data[0]
    num_iters, window_len = params
    for i in range(num_iters):
        close = close.pct_change(window_len)
        close[close==np.nan] = 0
    return close

def _create_indicator_all(p_data, params):
    return _create_indicator(p_data, params)

def _desc():
    return "roc", "(num_iters, window_len)"