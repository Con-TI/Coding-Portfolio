import numpy as np
def _create_indicator(p_data, num_iters):
    close  = p_data[0]
    return np.log(close)-np.log(close.shift(1))

def _create_indicator_all(p_data, num_iters):
    return _create_indicator(p_data,num_iters)
    

def _desc():
    return "logret", "()"