import pandas as pd
import importlib
def _create_indicator(p_data, params):
    close = p_data[0]
    name, ind_params, window = params
    module = importlib.import_module(f"indicators_module.offchart.{name}")
    indicator = module._create_indicator(p_data,ind_params)
    indicator = (indicator-indicator.min())/(indicator.max()-indicator.min())
    del p_data
    ret = pd.Series(index=close.index)
    for i in range(window,len(close)):
        ind_win = indicator.iloc[i-window:i+1]
        close_win = close.iloc[i-window:i+1] 
        ret.iloc[i] = (close_win*ind_win).sum()/ind_win.sum()
    return ret

def _create_indicator_all(p_data, params):
    close = p_data[0]
    name, ind_params, window = params
    module = importlib.import_module(f"indicators_module.offchart.{name}")
    indicator = module._create_indicator_all(p_data,ind_params)
    del p_data
    ret = pd.DataFrame(columns=close.columns,index=close.index)
    for i in range(window,len(close)):
        ind_win = indicator.iloc[i-window:i+1]
        ind_win = (ind_win - ind_win.min(axis=0))/(ind_win.max(axis=0)-ind_win.min(axis=0)+ 1.0e-6) + 1.0e-6
        close_win = close.iloc[i-window:i+1] 
        ret.iloc[i] = (close_win*ind_win).sum(axis=0)/ind_win.sum(axis=0)
    return ret

def _desc():
    return "customwap", "(indicator_name,(ind_params), window_len)"