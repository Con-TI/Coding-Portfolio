import pandas as pd
import numpy as np
def _create_indicator(p_data, window):
    dividends = p_data[5]
    days = pd.Series(index=dividends.index)
    div_present = False
    for i in range(len(dividends)):
        if dividends.iloc[i]>0:
            days.iloc[i] = 0
            div_present = True
        else:
            if not div_present:
                days.iloc[i] = np.nan
            else:
                days.iloc[i] = days.iloc[i-1] + 1
    return days

def _create_indicator_all(p_data, window):
    dividends = p_data[5]
    ret = []
    for i in range(dividends.shape[1]):
        ret.append(_create_indicator((0,0,0,0,0,dividends.iloc[:,i]),window))
    ret = pd.concat(ret, axis=1)
    ret.columns = dividends.columns
    return ret

def _desc():
    return "daysdiv", "()"