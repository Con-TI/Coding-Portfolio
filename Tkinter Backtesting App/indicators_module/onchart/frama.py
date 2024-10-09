import numpy as np
import pandas as pd

def _create_indicator(p_data, window):
    close, _, high ,low, _, _, _  = p_data
    del p_data
    alpha_min, alpha_max=0.01,0.99
    window_len = window
    frama = pd.Series(np.zeros(len(close)), index=close.index)
    frama.iloc[:] = np.nan
    try:
        prev = close.iloc[window_len-1]
        
        for t in range(window_len, len(close)):
            high_seg = high[t-window_len:t]
            low_seg = low[t-window_len:t]
            N1 = (high_seg[:window_len//2].max()-low_seg[:window_len//2].min())/(window_len//2)
            N2 = (high_seg[window_len//2:].max()-low_seg[window_len//2:].min())/(window_len//2)
            N3 = (high_seg.max()-low_seg.min())/window_len
            D = np.log((N1+N2)/N3)/np.log(2)
            alpha = np.exp(-4.6*(D-1))
            alpha = max(alpha_min,min(alpha,alpha_max))
            frama.iloc[t] = alpha*close.iloc[t]+(1-alpha)*prev
            prev = frama.iloc[t]
        return frama
    except IndexError:
        return frama

def _create_indicator_all(p_data, window):
    close, _, high ,low, _, _, _  = p_data
    del p_data
    window_len = window
    frama = pd.DataFrame(index=close.index, columns=close.columns)
    frama.iloc[:,:] = np.nan
    for i in range(close.shape[1]):
        p_data = (close.iloc[:,i].dropna(),0,high.iloc[:,i].dropna(),low.iloc[:,i].dropna(),0,0,0)
        indicator = _create_indicator(p_data,window)
        frama.iloc[-len(indicator):,i] = indicator
    return frama
    
def _desc():
    return "frama", "(window_len)"
