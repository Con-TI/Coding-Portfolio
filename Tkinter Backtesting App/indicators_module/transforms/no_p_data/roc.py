import numpy as np

TURNS_OFF_CHART = True

def _transform_indicator(indicator, params):
    num_iters,window_len = params
    for i in range(num_iters):
        indicator = indicator.pct_change(window_len)
        indicator[indicator==np.nan] = 0
    return indicator

def _transform_indicator_all(indicator, params):
    return _transform_indicator(indicator, params)

def _desc():
    return "roc", "(num_iters, window_len)"