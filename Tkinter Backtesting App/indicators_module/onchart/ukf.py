from pykalman import UnscentedKalmanFilter
import pandas as pd
import numpy as np

def _create_indicator(p_data, transition_cov):
    close = p_data[0].dropna()
    del p_data
    kf = UnscentedKalmanFilter(
        initial_state_mean = close.iloc[0],
        initial_state_covariance = 1,
        observation_covariance=1,
        transition_covariance=transition_cov
    )
    state_means,_ = kf.filter(close)
    return pd.Series(state_means.flatten(), index = close.index)

def _create_indicator_all(p_data, transition_cov):
    close = p_data[0]
    cols = close.columns
    del p_data
    close = close.bfill()
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
    
    for close in split_closes:    
        kf = UnscentedKalmanFilter(
            initial_state_mean = close.iloc[0,:].values,
            initial_state_covariance = np.identity(close.shape[1]),
            observation_covariance = np.identity(close.shape[1]),
            transition_covariance=np.identity(close.shape[1])*transition_cov)
        state_means,_ = kf.filter(close)
        state_means = pd.DataFrame(state_means,index=close.index)
        ret.append(state_means)
    
    ret = pd.concat(ret,axis=1)
    ret.columns = cols
    return ret

def _desc():
    return "ukf", "(transition_cov)"
