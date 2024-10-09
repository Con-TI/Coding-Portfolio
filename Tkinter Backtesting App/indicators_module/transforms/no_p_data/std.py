import numpy as np
TURNS_OFF_CHART = True

def _transform_indicator(indicator, params):
    window_len = params
    indicator = indicator.rolling(window_len).std()
    return indicator.dropna()
    
def _transform_indicator_all(indicator, params):
    window_len = params
    indicator = indicator.rolling(window_len).std()
    return indicator
def _desc():
    return "std", "(window_len)"