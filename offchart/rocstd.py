import numpy as np
def _create_indicator(p_data, params):
    num_iters, roc_window_len, std_window_len = params
    close  = p_data[0]
    for i in range(num_iters):
        close = close.pct_change(roc_window_len)
        close[close==np.nan] = 0
    close = close.rolling(std_window_len).std()
    close[close==np.nan] = 0
    return close

def _create_indicator_all(p_data, params):
    return _create_indicator(p_data, params)

def _desc():
    return "rocstd", "(num_iters, roc_window_len, std_window_len)"