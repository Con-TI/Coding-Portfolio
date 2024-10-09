import numpy as np
import pandas as pd
def _create_indicator(p_data, window):
    close, _ , high ,low, _, _, _  = p_data
    tr = pd.concat([(high-low),(high-close.shift(1)),(low-close.shift(1))],axis=1)
    tr = tr.max(axis=1)
    return tr

def _create_indicator_all(p_data, window):
    close, _ , high ,low, _, _, _  = p_data
    ret = []
    for i in range(close.shape[1]):
        refc, refh, refl = close.iloc[:,i], high.iloc[:,i], low.iloc[:,i]
        tr = pd.concat([(refh-refl),(refh-refc.shift(1)),(refl-refc.shift(1))],axis=1)
        tr = tr.max(axis=1)
        ret.append(tr)
    ret = pd.concat(ret,axis=1)
    ret.columns = close.columns
    return ret

def _desc():
    return "tr", "()"