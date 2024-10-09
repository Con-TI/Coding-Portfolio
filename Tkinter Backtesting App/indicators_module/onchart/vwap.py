import pandas as pd
def _create_indicator(p_data, window):
    close, vol  = p_data[0], p_data[4]
    del p_data
    window_len = window
    ret = pd.Series(index=close.index)
    for i in range(window,len(close)):
        vol_win = vol.iloc[i-window:i+1]
        close_win = close.iloc[i-window:i+1] 
        ret.iloc[i] = (close_win*vol_win).sum()/vol_win.sum()
    return ret

def _create_indicator_all(p_data, window):
    close, vol  = p_data[0], p_data[4]
    del p_data
    window_len = window
    ret = pd.DataFrame(columns=close.columns,index=close.index)
    for i in range(window,len(close)):
        vol_win = vol.iloc[i-window:i+1,:]
        close_win = close.iloc[i-window:i+1,:] 
        ret.iloc[i,:] = (close_win*vol_win).sum(axis=0)/vol_win.sum(axis=0)
    return ret

def _desc():
    return "vwap", "(window_len)"