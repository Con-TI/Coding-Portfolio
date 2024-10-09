import numpy as np
import pandas as pd

def _transform_indicator(indicator, params):
    ret = pd.Series(index=indicator.index)
    indicator = indicator.dropna()
    period = params
    a = np.exp(-np.sqrt(2)*np.pi/period)
    b = 2*a*np.cos(np.sqrt(2)*180/period)
    c2 = b
    c3 = -a**2
    c1 = (1-c2-c3)/4
    high = indicator
    high.iloc[:4] = 0
    for i in range(4, len(indicator)):
        high.iloc[i] = c1*(indicator.iloc[i]-2*indicator.iloc[i-1]+indicator.iloc[i-2]) + c2*high.iloc[i-1] + c3*high.iloc[i-2]        
    high.iloc[:4] = np.nan
    ret.iloc[(len(ret)-len(high)):] = high
    return ret

def _transform_indicator_all(indicator, params):
    ret = pd.DataFrame(index=indicator.index, columns = indicator.columns)
    ret.iloc[:,:] = np.nan
    for i in range(ret.shape[1]):
        ind = _transform_indicator(indicator.iloc[:,i],params)
        ret.iloc[-len(ind):,i] = ind
    return ret

def _desc():
    return "highpass", "(lower_period)"