from pykalman import KalmanFilter
import pandas as pd
import numpy as np

def _transform_indicator(indicator, transition_cov):
    ret = pd.Series(index=indicator.index)
    kf = KalmanFilter(
        transition_matrices = [1],
        observation_matrices = [1],
        initial_state_mean = indicator.dropna().iloc[0],
        initial_state_covariance = 1,
        observation_covariance=1,
        transition_covariance=transition_cov
    )
    state_means,_ = kf.filter(indicator.dropna())
    state_means = state_means.flatten()
    ret.iloc[(len(ret)-len(state_means)):] = pd.Series(state_means)
    return ret

def _transform_indicator_all(indicator, transition_cov):
    indicator = indicator.bfill()
    cols = indicator.columns
    num_stocks = indicator.shape[1]
    split = []
    if num_stocks>30:
        end_num = 30*(num_stocks//30)
        for i in range(0,num_stocks,30):
            split.append(indicator.iloc[:,i:i+30])
            if i == end_num:
                split.append(indicator.iloc[:,i:])
    else:
        split.append(indicator)
    del indicator
    
    ret = []
    
    for ind in split:    
        kf = KalmanFilter(
            transition_matrices = np.identity(ind.shape[1]),
            observation_matrices = np.identity(ind.shape[1]),
            initial_state_mean = ind.iloc[0,:].values,
            initial_state_covariance = np.identity(ind.shape[1]),
            observation_covariance = np.identity(ind.shape[1]),
            transition_covariance=np.identity(ind.shape[1])*transition_cov)
        state_means,_ = kf.filter(ind)
        state_means = pd.DataFrame(state_means,index=ind.index)
        ret.append(state_means)
    
    ret = pd.concat(ret,axis=1)
    ret.columns = cols
    return ret

def _desc():
    return "kf", "(transition_cov)"
