import numpy as np
import importlib
import os

TURNS_OFF_CHART = False

def _transform_indicator(indicator, params, p_data):
    global TURNS_OFF_CHART
    no_p_data = [file[:-3] for file in os.listdir('other_proj/tests/customchart/indicators_module/transforms/no_p_data')]
    requires_p_data = [file[:-3] for file in os.listdir('other_proj/tests/customchart/indicators_module/transforms/requires_p_data')]
    for infotuple in params:
        name, transparams = infotuple
        if name in no_p_data:
            module = importlib.import_module(f'indicators_module.transforms.no_p_data.{name}')
            indicator = module._transform_indicator(indicator, transparams)
        elif name in requires_p_data:
            module = importlib.import_module(f'indicators_module.transforms.requires_p_data.{name}')
            indicator = module._transform_indicator(indicator, transparams, p_data)
        try:
            if module.TURNS_OFF_CHART:
                TURNS_OFF_CHART = True
        except:
            pass
    return indicator

def _transform_indicator_all(indicators, params, p_data):
    no_p_data = [file[:-3] for file in os.listdir('other_proj/tests/customchart/indicators_module/transforms/no_p_data')]
    requires_p_data = [file[:-3] for file in os.listdir('other_proj/tests/customchart/indicators_module/transforms/requires_p_data')]
    ret_indicators = []
    for infotuple in params:
        name, transparams = infotuple
        for i in range(indicators.shape(1)):
            indicator = indicators.iloc[:,i]
            if name in no_p_data:
                module = importlib.import_module(f'indicators_module.transforms.no_p_data.{name}')
                indicator = module._transform_indicator(indicator, transparams)
            elif name in requires_p_data:
                module = importlib.import_module(f'indicators_module.transforms.requires_p_data.{name}')
                indicator = module._transform_indicator(indicator, transparams, p_data)
            indicators.iloc[:,i] = indicator
    return ret_indicators

def _desc():
    return "combine", "((transform1,(params1)),...,(transform2,(params2)))"