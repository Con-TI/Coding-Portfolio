from indicators_module.offchart.tr import _create_indicator as tr_c_i
from indicators_module.offchart.tr import _create_indicator_all as tr_c_i_a
import numpy as np
import pandas as pd
def _create_indicator(p_data, window):
    tr = tr_c_i(p_data,window)
    atr = tr.rolling(window).mean()
    return atr

def _create_indicator_all(p_data, window):
    tr = tr_c_i_a(p_data,window)
    atr = tr.rolling(window).mean()
    return atr

def _desc():
    return "atr", "(window_len)"