def _create_indicator(p_data, window):
    vol = p_data[4]
    del p_data
    return vol

def _create_indicator_all(p_data, window):
    return _create_indicator(p_data, window)

def _desc():
    return "vol", "()"