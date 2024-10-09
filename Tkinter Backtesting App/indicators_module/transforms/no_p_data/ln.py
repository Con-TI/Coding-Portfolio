import numpy as np

TURNS_OFF_CHART = True

def _transform_indicator(indicator, params):
    return np.log(indicator)

def _transform_indicator_all(indicator, params):
    return _transform_indicator(indicator, params)


def _desc():
    return "ln", "()"