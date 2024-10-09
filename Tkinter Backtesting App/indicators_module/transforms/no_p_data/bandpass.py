import indicators_module.transforms.no_p_data.highpass as hp
import indicators_module.transforms.no_p_data.super as sp
import numpy as np
import pandas as pd



def _transform_indicator(indicator, params):
    low, upper = params
    band = hp._transform_indicator(indicator,low)
    band = sp._transform_indicator(band, upper)
    return band

def _transform_indicator_all(indicator, params):
    low, upper = params
    band = hp._transform_indicator_all(indicator, low)
    band = sp._transform_indicator_all(indicator, upper)
    return band

def _desc():
    return "bandpass", "(lower_period, upper_period)"
