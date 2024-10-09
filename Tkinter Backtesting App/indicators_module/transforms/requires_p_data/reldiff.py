import pandas as pd
import importlib
import os

TURNS_OFF_CHART = True

def  _transform_indicator(indicator1, params, p_data):
    name, ind_params = params
    oncharts = [file[:-3] for file in os.listdir("other_proj/tests/customchart/indicators_module/onchart") if file[-3:]==".py"]
    offcharts = [file[:-3] for file in os.listdir("other_proj/tests/customchart/indicators_module/offchart") if file[-3:]==".py"]
    if name in oncharts:
        module = importlib.import_module(f"indicators_module.onchart.{name}")
    elif name in offcharts:
        module = importlib.import_module(f"indicators_module.offchart.{name}")
    indicator2 = module._create_indicator(p_data,ind_params)
    del p_data
    ret = (indicator1-indicator2)/indicator1
    return ret

def _desc():
    return "reldiff", "(indicator_name,(ind_params))"