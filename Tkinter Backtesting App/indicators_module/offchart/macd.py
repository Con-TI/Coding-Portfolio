import pandas as pd
def _create_indicator(p_data, window):
    close = p_data[0]
    window_len = window[0]
    ema1 = close.ewm(span=window_len,adjust=False).mean()
    window_len = window[1]
    ema2 = close.ewm(span=window_len,adjust=False).mean()
    macd = ema1-ema2
    window_len = window[2]
    signal = macd.ewm(span=window_len,adjust=False).mean()
    histo = macd-signal
    return histo

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)
    

def _desc():
    return "macd", "(win_len1,win_len2,win_len3)"