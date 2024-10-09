import numpy as np
import pandas as pd
from hurst import compute_Hc

def _create_indicator(p_data, window):
    close = p_data[0]
    window_len = window
    hursts = pd.Series(index=close.index)
    for i in range(window_len, len(close)):
        h, c, data = compute_Hc(close.iloc[i-window_len:i+1])
        hursts.iloc[i] = c
    return hursts

def _create_indicator_all(p_data, window):
    close = p_data[0]
    hursts = []    
    for i in range(close.shape[1]):
        hursts.append(_create_indicator((close.iloc[:,i],0),window))
    hursts = pd.concat(hursts,axis=1)
    hursts.columns = close.columns
    return hursts


def _desc():
    return "hurst_c", "(window_len)"