import numpy as np
import pandas as pd
def _create_indicator(p_data, window):
    close, _ , high ,low, _, _, _  = p_data
    tr = pd.concat([(high.rolling(window).max()-low.rolling(window).min()),
                    (high.rolling(window).max()-close.shift(1+window)),
                    (low.rolling(window).min()-close.shift(1+window))],axis=1)
    tr = tr.max(axis=1)
    return (close-low.rolling(window).min())/tr

def _create_indicator_all(p_data, window):
    close, _ , high ,low, _, _, _  = p_data
    ret = []
    for i in range(close.shape[1]):
        refc, refh, refl = close.iloc[:,i], high.iloc[:,i], low.iloc[:,i]
        tr = pd.concat([(refh.rolling(window).max()-refl.rolling(window).min()),
                    (refh.rolling(window).max()-refc.shift(1+window)),
                    (refl.rolling(window).min()-refc.shift(1+window))],axis=1)
        tr = tr.max(axis=1)
        ret.append((refc-refl.rolling(window).min())/tr)
    ret = pd.concat(ret,axis=1)
    ret.columns = close.columns
    return ret

def _desc():
    return "trcloselowpct", "(window)"