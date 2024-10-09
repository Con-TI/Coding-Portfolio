import numpy as np

def _create_indicator(p_data, params):
    low= p_data[3]
    del p_data
    min_window_len, num_iters, roc_window_len = params
    low = low.rolling(min_window_len).min()
    for i in range(num_iters):
        low = low.pct_change(roc_window_len)
        low[low==np.nan] = 0
    return low

def _create_indicator_all(p_data, params):
    return _create_indicator(p_data, params)

def _desc():
    return "minroc", "(min_window_len, num_iters, roc_window_len)"