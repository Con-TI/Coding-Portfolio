import numpy as np

TURNS_OFF_CHART = True

def _transform_indicator(indicator, window):
    indicator = indicator-indicator.mean()
    return np.sign(indicator)*np.log(np.abs(indicator)+1)

def _transform_indicator_all(indicator,window):
    indicator = indicator-indicator.mean(axis=0)
    return np.sign(indicator)*np.log(np.abs(indicator)+1)

def _desc():
    return "signlog", "()"