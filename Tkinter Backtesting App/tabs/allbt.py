from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter
from scipy.fft import rfft, rfftfreq
from tkcalendar import DateEntry
import importlib
import os
import ast
from functools import reduce
from operator import mul

class AllStockBtTab:
    def __init__(self, frame):
        self.oncharts = [file[:-3] for file in os.listdir("other_proj/customchart/indicators_module/onchart") if file[-3:]==".py"]
        self.offcharts = [file[:-3] for file in os.listdir("other_proj/customchart/indicators_module/offchart") if file[-3:]==".py"]
        self.transforms_requiring_no_p_data = [file[:-3] for file in os.listdir("other_proj/customchart/indicators_module/transforms/no_p_data") if file[-3:]==".py"]
        self.transforms_requiring_p_data = [file[:-3] for file in os.listdir("other_proj/customchart/indicators_module/transforms/requires_p_data") if file[-3:]==".py"]
        
        self.frame = frame
        self.master1 = Frame(self.frame)
        self.master1.grid(row=0, column=0, pady=10, padx=10, sticky='nsew')
        self.master2 = Frame(self.frame)
        self.master2.grid(row=0, column=1, pady=10, padx=10, sticky='nsew')
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=5)
        p_data = pd.read_pickle('datastore/data.pkl')
        self.p_data = [p_data['Close'],p_data['Open'],p_data['High'],p_data['Low'],p_data['Volume'], p_data['Dividends'], p_data['Stock Splits']]
        '''
        Note: Long-only allowed
        Explanation for each type:
        Simple signal will apply a trading rule to each stock individually.
        The result will be a graph showing what would happen if 100% of capital is allocated to each stock
        over time based on the trading rule. So if there are 900 stocks, 900 plots will be made.
        
        Periodic portfolio will take in a rule that determines portfolio weights. 
        After a specified period of time, the portfolio is readjusted based on the weights.
        The result will be a graph of the portfolio over time.
        
        Non-periodic portfolio will use a portfolio weight rule and exit signals.
        Everytime there is money after exiting a stock, the portfolio weight rule is applied and the portfolio is 
        kept the same until another exit signal is produced.
        
        Pairs will use specified pairs or tuples of stocks to generate signals. 
        The result will be a graph of portfolio value over time.
        
        Options will use options prices, which are first calculated, as the reference data.
        '''
        
        bt_t = Label(self.master1, text='Backtest: ')
        bt_t.grid(row=0, column=0, padx =10)
        self.bt_type = Combobox(self.master1, value=['Simple Signal','Periodic Portfolio','Non-periodic Portfolio','Pairs','Options'])
        
        self.bt_type.grid(row=0,column=1)
        self.bt_type.bind("<<ComboboxSelected>>", self._check)
        
        separator1 = Separator(self.master1, orient='horizontal')
        separator1.grid(row=1, column=0, columnspan=2, pady=20, sticky="WE")
        self.separator2 = Separator(self.master1, orient='horizontal')
        
        self.buylabel = Label(self.master1, text='Buy Conditions')
        self.buycondlist = Listbox(self.master1)
        self.cond_entry = Entry(self.master1)
        self.add_cond_b = Button(self.master1, text='Add', command = self._add_cond)
        self.del_cond_b = Button(self.master1, text='Remove', command = self._del_cond)
        self.fee_label = Label(self.master1, text='Fees: ')
        self.fee = Entry(self.master1)
        self.ax_label = Label(self.master1,text='y-scale: ')
        self.ax_op = Combobox(self.master1, value=['Linear','Log'])
        self.run_bt_label = Label(self.master1, text='Run Backtest: ')
        self.run_bt = Button(self.master1, text="▶",command = self._plot_simple_sig)
        self.return_quantiles = []
        
    def _all_grid_rem(self):
        self.buylabel.grid_remove()
        self.buycondlist.grid_remove()
        self.cond_entry.grid_remove()
        self.add_cond_b.grid_remove()
        self.del_cond_b.grid_remove()
        self.separator2.grid_remove()
        self.fee_label.grid_remove()
        self.fee.grid_remove()
        self.ax_label.grid_remove()
        self.ax_op.grid_remove()
        self.run_bt_label.grid_remove()
        self.run_bt.grid_remove()
    
    def _simple_signal_disp(self):
        self.buylabel.grid(row=2, column=0, columnspan=2)
        self.buycondlist.grid(row=3, column=0, columnspan=2,padx=10,pady=10, sticky='WE')
        self.cond_entry.grid(row=4, column=0, columnspan=2,padx=10,pady=10)
        self.add_cond_b.grid(row=5, column=0, columnspan=2)
        self.del_cond_b.grid(row=6, column=0, columnspan=2)
        self.separator2.grid(row=7, column=0, columnspan=2, pady=20, sticky="WE")
        self.fee_label.grid(row=8,column=0, padx=10)
        self.fee.grid(row=8,column=1, padx=10)
        self.ax_label.grid(row=9,column=0,padx=10,pady=(10,0))
        self.ax_op.grid(row=9,column=1,padx=10,pady=(10,0))
        self.ax_op.current(0)
        self.run_bt_label.grid(row=10,column=0, padx=10,pady=(10,0))
        self.run_bt.grid(row=10,column=1, padx=10,pady=(10,0))
    
    def _check(self,event):
        bt_type = self.bt_type.get().lower()
        if bt_type == 'simple signal':
            self._all_grid_rem()
            self._simple_signal_disp()
        elif bt_type == 'pairs':
            self._all_grid_rem()
        elif bt_type == 'options':
            self._all_grid_rem()
        elif bt_type == 'periodic portfolio':
            self._all_grid_rem()
        elif bt_type == 'non-periodic portfolio':
            self._all_grid_rem()

    def _plot_simple_sig(self, event=None):
        if hasattr(self, 'canvas_main'):
            self.canvas_main.get_tk_widget().destroy()
        axis = self.ax_op.get()
        fig = Figure(figsize=(12,6), dpi=100)
        gs = GridSpec(12, 6, figure=fig)
        self.canvas_main = FigureCanvasTkAgg(fig, master=self.master2)
        self.left_chart = fig.add_subplot(gs[:4,:3])
        self.right_chart = fig.add_subplot(gs[:4,3:])
        self.right_chart.set_yticklabels([])
        
        try:
            fee = float(self.fee.get())
        except:
            messagebox.showwarning('Input Error', "Check Fee input")
            
        indicators = self.buycondlist.get(0,END)
        price = self.p_data[0]
        if indicators:
            signals = []
            bt = (price.pct_change(fill_method=None)+1).shift(-1)
            bt_ref = price
            lens = pd.DataFrame(columns=bt_ref.columns,index=[0])
            av_rets = pd.DataFrame(columns=bt_ref.columns,index=[0])
            print(bt_ref['POOL.JK'].dropna())
            for i in range(price.shape[1]):
                av_rets.iloc[:,i] = bt_ref.iloc[:,i].dropna().iloc[-1]/bt_ref.iloc[:,i].dropna().iloc[0]
                lens.iloc[:,i] = 1/bt_ref.iloc[:,i].dropna().shape[0]
                bt_ref.iloc[:,i] = bt_ref.iloc[:,i]/bt_ref.iloc[:,i].dropna().iloc[0]
            av_rets = (av_rets**lens) - 1
            av_rets = av_rets.transpose().sort_values(0)
            for cond in indicators:
                ind,comp,val = cond.split(';')
                ind = self._get_indicator(ind)
                if val == 'price':
                    val = price
                elif val != 'price':
                    try:
                        val = self._get_indicator(val)
                    except ValueError:
                        try:
                            val = float(val)
                        except:
                            messagebox.showwarning("Input error", "Check values")
                            return 0
                if comp == "==":
                    signal = (ind == val).astype(int)
                elif (comp == ">") or (comp == ">="):
                    signal = (ind > val).astype(int)
                elif (comp == "<") or (comp == "<="):
                    signal = (ind < val).astype(int)
                signals.append(signal)
            signal = reduce(mul, signals)
            fees = 1+((-fee)*(signal.diff().replace(0,np.nan)+1)/2).replace(np.nan,0)
            bt = signal*bt
            bt[bt==0] = 1
            bt = bt*fees
            bt = bt.cumprod()
            # self.right_chart.plot(bt,color='k')
            self.right_chart.set_title('Strategy')
            # self.left_chart.plot(bt_ref,color='k')
            self.left_chart.set_title('Market')
            self.right_chart.set_yscale(f'{axis.lower()}')
            self.left_chart.set_yscale(f'{axis.lower()}')
            self.left_chart.set_ylabel(f'{axis} Returns')
            self.canvas_main.draw()
            self.canvas_main.get_tk_widget().grid(row=0, column=0)
                
    def _get_indicator(self,ind_str):
        name, params, _, params2 = ind_str.split(':')
        str_params = params
        str_params2 = params2
        params = ast.literal_eval(params)
        if len(params2) != 0:
            params2 = ast.literal_eval(params2)  
        if len(_) == 0:
            if name in self.oncharts:
                module = importlib.import_module(f"indicators_module.onchart.{name}")
                indicator = module._create_indicator_all(self.p_data,params)
            elif name in self.offcharts:
                module = importlib.import_module(f"indicators_module.offchart.{name}")
                indicator = module._create_indicator_all(self.p_data,params)
        else:                        
            if name in self.oncharts:
                module = importlib.import_module(f"indicators_module.onchart.{name}")
                indicator = module._create_indicator_all(self.p_data,params)
                if _ in self.transforms_requiring_p_data:
                    module = importlib.import_module(f"indicators_module.transforms.requires_p_data.{_}")
                    indicator = module._transform_indicator(indicator,params2, self.p_data)
                elif _ in self.transforms_requiring_no_p_data:
                    module = importlib.import_module(f"indicators_module.transforms.no_p_data.{_}")
                    indicator = module._transform_indicator(indicator,params2)
            elif name in self.offcharts:
                module = importlib.import_module(f"indicators_module.offchart.{name}")
                indicator = module._create_indicator_all(self.p_data,params)
                if _ in self.transforms_requiring_p_data:
                    module = importlib.import_module(f"indicators_module.transforms.requires_p_data.{_}")
                    indicator = module._transform_indicator(indicator,params2, self.p_data)
                elif _ in self.transforms_requiring_no_p_data:
                    module = importlib.import_module(f"indicators_module.transforms.no_p_data.{_}")
                    indicator = module._transform_indicator(indicator,params2)
        return indicator

    def _add_cond(self, event=None):
        item = self.cond_entry.get()
        if item:
            self.buycondlist.insert(END,item)
            self.cond_entry.delete(0, END)
        else:
            messagebox.showwarning("Input Error", "Please enter an item.")

    def _del_cond(self, event=None):
        items = self.buycondlist.curselection()
        if not items:
            messagebox.showwarning("Selection Error", "Please select an item to remove.")
            return 0
        for index in items[::-1]:
            self.buycondlist.delete(index)