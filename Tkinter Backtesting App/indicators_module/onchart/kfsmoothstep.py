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
    
    ret = pd.Series(index=close.index)
    for i in range(len(close)):
        state_means,_ = kf.smooth(close.iloc[:i+1])
        state_means = state_means.flatten()
        ret.iloc[i] = state_means[-1]
    return ret

def _create_indicator_all(p_data, transition_cov):
    close = p_data[0]
    close = close.bfill()
    kf = KalmanFilter(
        transition_matrices = np.identity(close.shape[1]),
        observation_matrices = np.identity(close.shape[1]),
        initial_state_mean = close.iloc[0,:].values,
        initial_state_covariance = np.identity(close.shape[1]),
        observation_covariance = np.identity(close.shape[1]),
        transition_covariance=np.identity(close.shape[1])*0.01)
    
    ret = pd.DataFrame(index=close.index)
    for i in range(len(close)):
        state_means,_ = kf.smooth(close.iloc[:i+1,:])
        ret.iloc[i,:] = state_means[-1,:]
    return state_means

def _desc():
    return "kfsmoothstep", "(transition_cov)"