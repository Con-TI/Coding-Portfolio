import numpy as np

TURNS_OFF_CHART = True

def _transform_indicator(indicator, params):
    window_len, q = params
    indicator = (indicator - indicator.rolling(window_len).quantile(q))/(indicator.rolling(window_len).quantile(1-q)-indicator.rolling(window_len).quantile(q))*10-5
    ift = (np.exp(indicator*2)-1)/(np.exp(indicator*2)+1)
    return ift

def _transform_indicator_all(indicator,params):
    window_len, q = params
    indicator = (indicator - indicator.rolling(window_len).quantile(q))/(indicator.rolling(window_len).quantile(1-q)-indicator.rolling(window_len).quantile(q))*10-5
    ift = (np.exp(indicator*2)-1)/(np.exp(indicator*2)+1)
    return ift

def _desc():
    return "rollingift", "(window_len, lower_quantile)"