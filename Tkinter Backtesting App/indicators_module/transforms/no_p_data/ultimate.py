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
    c1 = (1+c2-c3)/4
    ultimate = indicator
    for i in range(4, len(indicator)):
        ultimate.iloc[i] = (1-c1)*indicator.iloc[i] + (2*c1-c2)*indicator.iloc[i-1] - (c1+c3)*indicator.iloc[i-2] + c2*ultimate.iloc[i-1] + c3*ultimate.iloc[i-2]      
    ret.iloc[(len(ret)-len(ultimate)):] = ultimate
    return ret

def _transform_indicator_all(indicator, params):
    ret = pd.DataFrame(index= indicator.index, columns = indicator.columns)
    ret.iloc[:,:] = np.nan
    for i in range(ret.shape[1]):
        ind = _transform_indicator(indicator.iloc[:,i],params)
        ret.iloc[-len(ind):,i] = ind
    return ret
        

def _desc():
    return "ultimate", "(upper_period)"