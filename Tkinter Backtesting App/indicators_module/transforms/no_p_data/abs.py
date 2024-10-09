import numpy as np

def _transform_indicator(indicator, params):
    return np.abs(indicator)

def _transform_indicator_all(indicator, params):
    return _transform_indicator(indicator, params)

def _desc():
    return "abs", "()"