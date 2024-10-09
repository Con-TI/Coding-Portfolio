import numpy as np

TURNS_OFF_CHART = True

def _transform_indicator(indicator, params):
    num_iters, roc_window_len, std_window_len = params
    for i in range(num_iters):
        indicator = indicator.pct_change(roc_window_len)
        indicator[indicator==np.nan] = 0
    indicator = indicator.rolling(std_window_len).std()
    indicator[indicator==np.nan] = 0
    return indicator
    
def _transform_indicator_all(indicator, params):
    return _transform_indicator(indicator,params)

def _desc():
    return "rocstd", "(num_iters, roc_window_len, std_window_len)"