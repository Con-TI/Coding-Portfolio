from indicators_module.onchart.kf import _create_indicator_all as kf_c_i_a
from indicators_module.onchart.kfsmooth import _create_indicator_all as kfs_c_i_a
from pykalman import KalmanFilter
import pandas as pd
import numpy as np

def _create_indicator(p_data, transition_cov):
    close = p_data[0]
    kf = KalmanFilter(
        transition_matrices = [1],
        observation_matrices = [1],
        initial_state_mean = close.iloc[0],
        initial_state_covariance = 1,
        observation_covariance=1,
        transition_covariance=transition_cov
    )
    state_means,_ = kf.filter(close)
    normal = pd.Series(state_means.flatten(), index = close.index)
    state_means,_ = kf.smooth(close)
    smooth = pd.Series(state_means.flatten(),index=close.index)
    return np.log(smooth)-np.log(normal)

def _create_indicator_all(p_data, transition_cov):
    close = p_data[0]
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
    
    kalmandiff = []
    for close in split_closes:
        normal = kf_c_i_a((close,0),transition_cov)
        smooth = kfs_c_i_a((close,0),transition_cov)
        kalmandiff.append(np.log(smooth) - np.log(normal))
    kalmandiff = pd.concat(kalmandiff,axis=1)
    kalmandiff.columns = cols
    print(kalmandiff)
    return kalmandiff

def _desc():
    return "kalmandiff", "(transition_cov)"