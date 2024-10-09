import numpy as np

TURNS_OFF_CHART = True

def _transform_indicator(indicator, params):
    indicator = 2*(indicator - indicator.min() + 10**-6)/(indicator.max() - indicator.min() + 2*10**-6)-1
    return 0.5*np.log((1+indicator)/(1-indicator))

def _transform_indicator_all(indicator, params):
    indicator = 2*(indicator-indicator.min(axis=0) + 10**-6)/(indicator.max(axis=0) - indicator.min(axis=0) + 2e-6)-1
    return 0.5*np.log((1+indicator)/(1-indicator))

def _desc():
    return "fisher", "()"