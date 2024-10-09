import indicators_module.offchart.daysdiv as daysdiv
def _create_indicator(p_data, window):
    days_div_ser = daysdiv._create_indicator(p_data,window)
    return (days_div_ser==0).rolling(252).sum()

def _create_indicator_all(p_data, window):
    days_div_ser = daysdiv._create_indicator_all(p_data,window)
    return (days_div_ser==0).rolling(252).sum()

def _desc():
    return "divfreq", "()"