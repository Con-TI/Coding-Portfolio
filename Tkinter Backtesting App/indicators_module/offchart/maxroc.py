import numpy as np

def _create_indicator(p_data, params):
    high= p_data[2]
    del p_data
    max_window_len, num_iters, roc_window_len = params
    high = high.rolling(max_window_len).max()
    for i in range(num_iters):
        high = high.pct_change(roc_window_len)
        high[high==np.nan] = 0
    return high

def _create_indicator_all(p_data, params):
    return _create_indicator(p_data, params)

def _desc():
    return "maxroc", "(max_window_len, num_iters, roc_window_len)"