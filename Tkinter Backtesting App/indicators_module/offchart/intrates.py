'''
For this indicator, this is the list of possible country names:
['indonesia', 'united-states', 'japan', 'united-kingdom', 'china',
       'australia', 'switzerland', 'canada', 'india', 'south-korea',
       'euro-area', 'new-zealand', 'norway', 'sweden', 'hong-kong',
       'singapore', 'malaysia', 'brazil']
'''
import pandas as pd

def _create_indicator(p_data, country_name):
    close = p_data[0]
    df = pd.read_pickle('datastore/interest-rate.pkl')[country_name].dropna()
    df = df.tz_localize('UTC')
    df = df.tz_convert('Asia/Bangkok')
    ret = pd.Series(index = close.index)
    ret = ret.combine_first(df)
    ret = ret.ffill()
    return ret
    
def _create_indicator_all(p_data, country_name):
    close = p_data[0]
    rets = []
    df = pd.read_pickle('datastore/interest-rate.pkl')[country_name].dropna()
    df = df.tz_localize('UTC')
    df = df.tz_convert('Asia/Bangkok')
    ret = pd.Series(index = close.index)
    ret = ret.combine_first(df)
    ret = ret.ffill()
    for i in range(close.shape[1]):
        rets.append(ret)
    rets = pd.concat(rets, axis=1)
    rets.columns = close.columns
    return rets


def _desc():
    return "intrates", "(country_name)"