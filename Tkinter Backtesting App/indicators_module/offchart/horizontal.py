import numpy as np
import pandas as pd
from hurst import compute_Hc

def _create_indicator(p_data, y_val):
    close = p_data[0]
    line = pd.Series(index=close.index)
    line.iloc[:] = y_val
    return line

def _create_indicator_all(p_data, y_val):
    close = p_data[0]
    line = pd.DataFrame(columns=close.columns, index=close.index)
    line.iloc[:,:] = y_val
    return line

def _desc():
    return "horizontal", "(y_val)"