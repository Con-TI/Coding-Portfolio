import pandas as pd
def _create_indicator(p_data, window):
    split = p_data[6]
    days = pd.Series(index=split.index)
    split_present = False
    for i in range(len(split)):
        if split.iloc[i]>0:
            days.iloc[i] = 0
            split_present = True
        else:
            if not split_present:
                days.iloc[i] = 0
            else:
                days.iloc[i] = days.iloc[i-1] + 1
    return days

def _create_indicator_all(p_data, window):
    split = p_data[6]
    ret = []
    for i in range(split.shape[1]):
        ret.append(_create_indicator((0,0,0,0,0,0,split.iloc[:,i]),window))
    ret = pd.concat(ret, axis=1)
    ret.columns = split.columns
    return ret

def _desc():
    return "dayssplit", "()"