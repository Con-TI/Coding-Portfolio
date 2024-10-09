from indicators_module.onchart.kf import _create_indicator_all as _kf_c_i_a
from indicators_module.onchart.kf import _create_indicator as _kf_c_i
from pykalman import KalmanFilter
import numpy as np
import pandas as pd

def _create_indicator(p_data, ema_window):
    close = p_data[0]
    del p_data
    ema = close.ewm(span=ema_window,adjust=False).mean()
    kf = _kf_c_i((close,0),0.01)
    print(ema,kf)
    return np.sign(kf-ema)

def _create_indicator_all(p_data, ema_window):
    close = p_data[0]
    del p_data
    ema = close.ewm(span=ema_window,adjust=False).mean()
    kf = _kf_c_i_a((close,0),0.01)
    kf.columns = ema.columns
    return np.sign(kf-ema)

def _desc():
    return "trender", "(ema_window)"