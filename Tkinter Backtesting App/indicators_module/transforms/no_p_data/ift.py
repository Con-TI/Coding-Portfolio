import numpy as np

TURNS_OFF_CHART = True

def _transform_indicator(indicator, params):
    q = params
    indicator = (indicator - indicator.quantile(q))/(indicator.quantile(1-q)-indicator.quantile(q))*10-5
    ift = (np.exp(indicator*2)-1)/(np.exp(indicator*2)+1)
    return ift

def _transform_indicator_all(indicator, params):
    q = params
    indicator = (indicator-indicator.quantile(q,axis=0))/(indicator.quantile(1-q,axis=0)-indicator.quantile(q,axis=0))*10-5
    ift = (np.exp(indicator*2)-1)/(np.exp(indicator*2)+1)
    return ift

def _desc():
    return "ift", "(lower_quantile)"