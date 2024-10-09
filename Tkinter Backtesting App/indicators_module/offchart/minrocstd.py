import numpy as np

def _create_indicator(p_data, params):
    low= p_data[3]
    del p_data
    min_window_len, num_iters, roc_window_len, std_window_len = params
    indicator = low.rolling(min_window_len).min()
    for i in range(num_iters):
        indicator = indicator.pct_change(roc_window_len)
        indicator[indicator==np.nan] = 0
    indicator = indicator.rolling(std_window_len).std()
    indicator[indicator==np.nan] = 0
    return indicator

def _create_indicator_all(p_data, params):
    return _create_indicator(p_data, params)

def _desc():
    return "minrocstd", "(min_window_len, num_iters, roc_window_len, std_window_len)"