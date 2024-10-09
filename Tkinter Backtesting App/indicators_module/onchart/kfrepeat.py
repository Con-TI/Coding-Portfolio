from pykalman import KalmanFilter
import pandas as pd
import numpy as np

def _create_indicator(p_data, params):
    close = p_data[0]
    transition_cov, num_repeat = params
    del p_data
    kf = KalmanFilter(
        transition_matrices = [1],
        observation_matrices = [1],
        initial_state_mean = close.iloc[0],
        initial_state_covariance = 1,
        observation_covariance=1,
        transition_covariance=transition_cov
    )
    for i in range(num_repeat):
        state_means,_ = kf.filter(close)
        close = pd.Series(state_means.flatten(), index = close.index)    
    return pd.Series(state_means.flatten(), index = close.index)

def _create_indicator_all(p_data, params):
    close = p_data[0]
    transition_cov, num_repeat = params
    del p_data
    close = close.bfill()
    cols = close.columns
    num_stocks = close.shape[1]
    split_closes = []
    if num_stocks>30:
        end_num = 30*(num_stocks//30)
        for i in range(0,num_stocks,30):
            split_closes.append(close.iloc[:,i:i+30])
            if i == end_num:
                split_closes.append(close.iloc[:,i:])
    else:
        split_closes.append(close)
    del close
    
    ret = []
    
    for i in range(num_repeat):
        for close in split_closes:    
            kf = KalmanFilter(
                transition_matrices = np.identity(close.shape[1]),
                observation_matrices = np.identity(close.shape[1]),
                initial_state_mean = close.iloc[0,:].values,
                initial_state_covariance = np.identity(close.shape[1]),
                observation_covariance = np.identity(close.shape[1]),
                transition_covariance=np.identity(close.shape[1])*transition_cov)
            state_means,_ = kf.filter(close)
            state_means = pd.DataFrame(state_means,index=close.index)
            ret.append(state_means)
        ret = pd.concat(ret,axis=1)
        ret.columns = cols
        close=ret
        split_closes = []
        if num_stocks>30:
            end_num = 30*(num_stocks//30)
            for i in range(0,num_stocks,30):
                split_closes.append(close.iloc[:,i:i+30])
                if i == end_num:
                    split_closes.append(close.iloc[:,i:])
        else:
            split_closes.append(close)
    
    return ret

def _desc():
    return "kfrepeat", "(transition_cov, num_repeat)"