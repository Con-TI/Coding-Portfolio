import pandas as pd
def _create_indicator(p_data, window):
    close, high = p_data[0], p_data[2]
    high = high.rolling(252).max()
    return (high-close)/high

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "52weekhighpct", "()"