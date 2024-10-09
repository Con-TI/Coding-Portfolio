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
from tabs.allbt import AllStockBtTab

df = pd.read_pickle('datastore/data.pkl')
df5d = pd.read_pickle('datastore/data5d.pkl')
df1wk = pd.read_pickle('datastore/data1wk.pkl')
df1mo = pd.read_pickle('datastore/data1mo.pkl')
matplotlib.use('TkAgg')

class StockCharts:
    def __init__(self, root, df):
        self.close = df['Close']
        self.open = df['Open']
        self.high = df['High']
        self.low = df['Low']
        self.dividend = df['Dividends']
        self.stocksplits = df['Stock Splits']
        self.volume = df['Volume']
        
        self.f = '1d'
        
        root.title("Stock Charts")

        # Initialize notebook
        self.notebook = Notebook(root)
        self.notebook.pack()
        main_frame = Frame(self.notebook)
        self.notebook.add(main_frame, text="Main")
        self.main_master1 = Frame(main_frame)
        self.main_master1.grid(row=0, column=0, pady=10, sticky='nsew')
        self.hold_canv = Canvas(main_frame)
        self.hold_canv.grid(row=0, column=1, sticky='nsew')
        self.hold_canv_scroll = Scrollbar(main_frame, orient='vertical', command=self.hold_canv.yview)
        self.hold_canv_scroll.grid(row=0, column=2, sticky='ns') 
        self.hold_canv.configure(yscrollcommand=self.hold_canv_scroll.set)
        self.main_master2 = Frame(self.hold_canv)
        self.hold_canv.create_window((0,0),window=self.main_master2,anchor='center')
        self.hold_canv.bind('<Configure>', self._update_scroll)
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=5)
        
        indicators_frame = Frame(self.notebook)
        self.notebook.add(indicators_frame, text='Indicators')
        self.indicators_frame_master1 = Frame(indicators_frame)
        self.indicators_frame_master1.grid(row=0, column=0, pady=10, padx=10, sticky='nsew')
        self.indicators_frame_master2 = Frame(indicators_frame)
        self.indicators_frame_master2.grid(row=0, column=1, pady=10, padx=10, sticky='nsew')
        
        bt_frame = Frame(self.notebook)
        self.notebook.add(bt_frame, text='All Stocks Backtest')

        # Main tab

        options = list(df.columns.get_level_values(1).unique())

        l1 = Label(self.main_master1, text='Stock Code: ')
        l1.grid(row=0,column=0)

        self.stock_codes = Combobox(self.main_master1, values=options)
        self.stock_codes.grid(row=0,column=1)
        self.stock_codes.current(0)

        del options

        l2 = Label(self.main_master1, text='y-scale: ')
        l2.grid(row=1,column=0)

        self.y_ax = Combobox(self.main_master1, values=['Linear', 'Log'])
        self.y_ax.grid(row=1,column=1)
        self.y_ax.current(0)

        freq = Label(self.main_master1, text='price freq: ')
        freq.grid(row=2,column=0)
        self.freqb = Combobox(self.main_master1, values=['1d','5d','1wk','1mo'])
        self.freqb.grid(row=2,column=1)
        self.freqb.current(0)

        l3 = Label(self.main_master1, text='price type: ')
        l3.grid(row=3,column=0)

        self.priceform = Combobox(self.main_master1, values=['Normal', 'Heikin Ashi','Kagi','Renko', 'Line Break'])
        self.priceform.grid(row=3,column=1)
        self.priceform.bind("<<ComboboxSelected>>", self._check)
        self.priceform.current(0)

        self.b1 = Button(self.main_master1, text='custom kagi/renko', command = self._cust_kag_renk)
        self.cust_vals_kr = False
        self.editkagirenko1 = Combobox(self.main_master1, values=['pct','ATR','fixed'])
        self.editkagirenko2 = Combobox(self.main_master1, values=[i for i in range(1,100)])

        self.b2 = Button(self.main_master1, text='custom linebreak', command = self._cust_linebreak)
        self.cust_vals_lb = False
        self.editlinebreak = Combobox(self.main_master1, values=[i for i in range(2,100)])

        self.b3 = Button(self.main_master1, text='start date', command=self._enable_cal)
        self.b3.grid(row=4,column=0)

        self.cal = DateEntry(self.main_master1)
        self.cal.config(state='disabled')
        self.cal.grid(row=4,column=1)

        self.b4 = Button(self.main_master1, text='update', command=self._plot)
        self.b4.grid(row=5,column=0, columnspan=2)
        
        self.display_onindicator = Combobox(self.main_master2)
        self.display_onindicator.bind("<<ComboboxSelected>>", self._modify_plot)
        self.disp_onind = Label(self.main_master2, text='On Chart Indicators:')
        self.display_offindicator = Combobox(self.main_master2)
        self.display_offindicator.bind("<<ComboboxSelected>>", self._modify_plot2)
        self.disp_offind = Label(self.main_master2, text='Off Chart Indicators:')
        self.display_offindicator = Combobox(self.main_master2)
        self.display_offindicator.bind("<<ComboboxSelected>>", self._modify_plot2)
        self.disp_offind = Label(self.main_master2, text='Off Chart Indicators:')
        
        separator1 = Separator(self.main_master1, orient='horizontal')
        separator1.grid(row=9, column=0, columnspan=2, pady=20, sticky="WE")
        
        self.buylabel = Label(self.main_master1, text='Buy Conditions')
        self.buylabel.grid(row=10, column=0, columnspan=2)
        self.buycondlist = Listbox(self.main_master1)
        self.buycondlist.grid(row=11, column=0, columnspan=2,padx=10,pady=10, sticky='WE')
        self.cond_entry = Entry(self.main_master1)
        self.cond_entry.grid(row=12, column=0, columnspan=2,padx=10,pady=10)
        self.add_cond_b = Button(self.main_master1, text='Add', command = self._add_cond)
        self.add_cond_b.grid(row=13, column=0, columnspan=2)
        self.del_cond_b = Button(self.main_master1, text='Remove', command = self._del_cond)
        self.del_cond_b.grid(row=14, column=0, columnspan=2)
        
        instruct = Label(self.main_master1, text="Format condition as 'indicator;comparison;value'\nfor e.g. rsi:(50):;<;20. value can be another \nindicator or simply 'price'.")
        instruct.grid(row=15, column=0, columnspan=2, padx=10, pady=(10,0))
        
        separator2 = Separator(self.main_master1, orient='horizontal')
        separator2.grid(row=16, column=0, columnspan=2, pady=(20,10), sticky="WE")
        
        transaction_label = Label(self.main_master1, text='Fees: ')
        transaction_label.grid(row=17, column=0, padx=10, pady=(10,0))
        self.fees_entry = Entry(self.main_master1)
        self.fees_entry.grid(row=17, column=1, padx=10, pady=(10,0))
        l_y_ax_bt = Label(self.main_master1, text='y-scale: ')
        l_y_ax_bt.grid(row=18,column=0, padx=10, pady=(10,0))
        self.y_ax_bt = Combobox(self.main_master1, values=['Linear', 'Log'])
        self.y_ax_bt.grid(row=18,column=1, padx=10, pady=(10,0))
        runbt_label = Label(self.main_master1, text="Run Backtest: ")
        runbt_label.grid(row=19, column=0, padx=10, pady=10)
        self.runbt_mainframe = Button(self.main_master1, text= "▶", command = self._modify_plot_bt)
        self.runbt_mainframe.grid(row=19, column=1, padx=10, pady=10, sticky="WE")
        
        # Main Tab/Custom plots
        self.l_plot_type = Label(self.main_master2, text='Plot Type:')
        self.plot_type = Combobox(self.main_master2, values=['Scatter','Histo','PSD','Integral Transforms'])
        self.plot_type.bind("<<ComboboxSelected>>", self._analysis_plot_type)
        
        self.l_analysis_x = Label(self.main_master2, text='x-axis: ')
        self.analysis_x = Combobox(self.main_master2)
        self.l_analysis_y = Label(self.main_master2, text='y-axis: ')
        self.analysis_y = Combobox(self.main_master2)
        self.l_analysis_var = Label(self.main_master2, text='variable: ')
        self.analysis_var = Combobox(self.main_master2)
        self.b_analysis_plot_update = Button(self.main_master2, text='update', command=self._update_analysis_plot)
        
        # Indicators Tab
        l4 = Label(self.indicators_frame_master1, text="Indicators In Use")
        l4.grid(row=0, column=0, columnspan=2,pady=(10,0))

        self.indicatorslist = Listbox(self.indicators_frame_master1, height=15)
        self.indicatorslist.grid(row=1,column=0,columnspan=2,padx=10,pady=10)
        self.check_ind = False

        l5 = Label(self.indicators_frame_master2, text="On-chart indicator options")
        l5.grid(row=0,column=0,pady=(10,0))

        self.onindtree = Treeview(self.indicators_frame_master2, columns=("Name","Parameters"), show='headings', height=20)
        self.onindtree.heading("Name", text="Name")
        self.onindtree.heading("Parameters", text="Parameters")
        self.onindtree.grid(row=1,column=0,padx=10,pady=10)

        chartinds = [file[:-3] for file in os.listdir('other_proj/customchart/indicators_module/onchart') if file[-3:] == ".py"]
        if len(chartinds) != 0:
            for ind in chartinds:
                module = importlib.import_module(f"indicators_module.onchart.{ind}")
                name, params = module._desc()
                self.onindtree.insert("", END, values=(name, params,))

        l6 = Label(self.indicators_frame_master2, text="Off-chart indicator options")
        l6.grid(row=0,column=1,pady=(10,0))

        self.offindtree = Treeview(self.indicators_frame_master2, columns=("Name","Parameters"), show='headings', height=20)
        self.offindtree.heading("Name", text="Name")
        self.offindtree.heading("Parameters", text="Parameters")
        self.offindtree.grid(row=1,column=1,padx=10,pady=10)

        chartinds = [file[:-3] for file in os.listdir('other_proj/customchart/indicators_module/offchart') if file[-3:] == ".py"]
        if len(chartinds) != 0:
            for ind in chartinds:
                module = importlib.import_module(f"indicators_module.offchart.{ind}")
                name, params = module._desc()
                self.offindtree.insert("", END, values=(name, params,))
                
        l7 = Label(self.indicators_frame_master2, text="Transforms options")
        l7.grid(row=0,column=2,pady=(10,0))    
        
        self.transformstree = Treeview(self.indicators_frame_master2, columns=("Name","Parameters"), show='headings', height=20)
        self.transformstree.heading("Name",text="Name")
        self.transformstree.heading("Parameters", text="Parameters")
        self.transformstree.grid(row=1,column=2,padx=10,pady=10)
            
        chartinds = [file[:-3] for file in os.listdir('other_proj/customchart/indicators_module/transforms/requires_p_data') if file[-3:] == ".py"]
        if len(chartinds) != 0:
            for ind in chartinds:
                module = importlib.import_module(f"indicators_module.transforms.requires_p_data.{ind}")
                name, desc = module._desc()
                self.transformstree.insert("", END, values=(name, desc, ))
        
        chartinds = [file[:-3] for file in os.listdir('other_proj/customchart/indicators_module/transforms/no_p_data') if file[-3:] == ".py"]
        if len(chartinds) != 0:
            for ind in chartinds:
                module = importlib.import_module(f"indicators_module.transforms.no_p_data.{ind}")
                name, desc = module._desc()
                self.transformstree.insert("", END, values=(name, desc, ))
        
        del chartinds, module, name, params, desc

        l8 = Label(self.indicators_frame_master2, text="To add an indicator, add item in format 'Name:Params::'. Parameters need to be specified. \n E.g. sma:(14)::. To transform indicator, add item in format 'Name:Params:Transform:Params2'. \n E.g. rsi:(14):ift:()")
        l8.grid(row=2,column=0,columnspan=3)

        self.indicatorentry = Entry(self.indicators_frame_master1)
        self.indicatorentry.grid(row=2,column=0,columnspan=2,padx=10,pady=10)
        self.b5 = Button(self.indicators_frame_master1, text="Add Item", command=self._add_ind)
        self.b5.grid(row=3,column=0,padx=10,pady=10)
        self.b6 = Button(self.indicators_frame_master1, text="Remove Item", command=self._del_ind)
        self.b6.grid(row=3,column=1,padx=10,pady=10)

        # All Stocks Backtest tab
        bt_tab = AllStockBtTab(bt_frame)

        # Options Pricing tab

        # Execution tab
        exec_tab = 1
        
        # Simulation tab

    def _update_analysis_plot(self, event=None):
        plot_type = self.plot_type.get().lower()
        axes = self.fig2.axes
        if len(axes) != 0:
            for ax in axes:
                self.fig2.delaxes(ax=ax)
        try:
            indicators = {**self.to_plots_onchart, **self.to_plots_offchart}
        except:
            messagebox.showwarning('Input Error', 'No Indicators Found')  
              
        if plot_type == 'scatter':
            x = indicators[self.analysis_x.get()]
            y = indicators[self.analysis_y.get()]
            analysis_chart = self.fig2.add_subplot()
            analysis_chart.scatter(x=x, y=y)
        else:
            var = self.analysis_var.get()
            if plot_type == 'histo':
                analysis_chart = self.fig2.add_subplot()
                sns.histplot(indicators[var], ax=analysis_chart, stat='probability')
            elif plot_type == 'psd':
                analysis_chart = self.fig2.add_subplot()
                analysis_chart.psd(indicators[var])
        self.canvas_main2.draw()
        
    def _analysis_plot_type(self, event=None):
        plot_type = self.plot_type.get().lower()
        if plot_type == 'scatter':
            self.l_analysis_x.grid(row=5,column=1)
            self.analysis_x.grid(row=6,column=1, pady=(0,10))
            self.l_analysis_y.grid(row=5,column=2)
            self.analysis_y.grid(row=6,column=2, pady=(0,10))
            self.b_analysis_plot_update.grid(row=6, column=3, pady=(0,10))
            self.l_analysis_var.grid_remove()
            self.analysis_var.grid_remove()
        else:
            self.l_analysis_x.grid_remove()
            self.analysis_x.grid_remove()
            self.l_analysis_y.grid_remove()
            self.analysis_y.grid_remove()
            self.l_analysis_var.grid(row=5,column=1)
            self.analysis_var.grid(row=6,column=1,pady=(0,10))
            self.b_analysis_plot_update.grid(row=6, column=2, pady=(0,10))

    def _update_scroll(self, event=None):
        self.hold_canv.configure(scrollregion=self.hold_canv.bbox('all'))

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

    def _add_ind(self, event=None):
        item = self.indicatorentry.get()
        if item:
            self.indicatorslist.insert(END, item)
            self.indicatorentry.delete(0, END)
        else:
            messagebox.showwarning("Input Error", "Please enter an item.")

    def _del_ind(self, event=None):
        items = self.indicatorslist.curselection()
        if not items:
            messagebox.showwarning("Selection Error", "Please select an item to remove.")
            return 0
        for index in items[::-1]:
            self.indicatorslist.delete(index)

    def _check(self,event):
        selected = self.priceform.get().lower()
        if (selected == "kagi") or (selected == "renko"):
            self.b1.grid(row=4, column=0)
            self.b2.grid_remove()
            self.editlinebreak.grid_remove()
            if len(self.editkagirenko1.grid_info())==0:
                self.b3.grid(row=5, column=0)
                self.cal.grid(row=5, column=1)
                self.b4.grid(row=6, column=0, columnspan=2)
            else:
                self.b3.grid(row=6, column=0)
                self.cal.grid(row=6, column=1)
                self.b4.grid(row=7, column=0, columnspan=2)
        elif selected == "line break":
            self.b1.grid_remove()
            self.editkagirenko1.grid_remove()
            self.editkagirenko2.grid_remove()
            self.b2.grid(row=4, column=0)            
            self.b3.grid(row=5, column=0)
            self.cal.grid(row=5, column=1)
            self.b4.grid(row=6, column=0, columnspan=2)
        else:
            self.cust_vals_kr = False
            self.cust_vals_lb = False
            self.b1.grid_remove()
            self.b2.grid_remove()
            self.editkagirenko1.grid_remove()
            self.editkagirenko2.grid_remove()
            self.editlinebreak.grid_remove()
            self.b3.grid(row=4, column=0)
            self.cal.grid(row=4, column=1)
            self.b4.grid(row=5, column=0, columnspan=2)

    def _enable_cal(self):
        state = self.cal.state()
        if len(state) == 1:
            self.cal.config(state='enabled')
        else:
            self.cal.config(state='disabled')

    def _cust_linebreak(self):
        self.cust_vals_lb = not self.cust_vals_lb
        if self.cust_vals_lb:
            self.editlinebreak.grid(row=4,column=1)
            self.b3.grid(row=5,column=0)
            self.cal.grid(row=5,column=1)
            self.b4.grid(row=6, column=0, columnspan=2)
        else:
            self.editlinebreak.grid_remove()

    def _cust_kag_renk(self):
        self.cust_vals_kr = not self.cust_vals_kr
        if self.cust_vals_kr:
            self.editkagirenko1.grid(row=4,column=1)
            self.editkagirenko2.grid(row=5,column=1)
            self.b3.grid(row=6,column=0)
            self.cal.grid(row=6,column=1)
            self.b4.grid(row=7, column=0, columnspan=2)
        else:
            self.editkagirenko1.grid_remove()
            self.editkagirenko2.grid_remove()
            self.b3.grid(row=5,column=0)
            self.cal.grid(row=5,column=1)
            self.b4.grid(row=6, column=0, columnspan=2)

    def _modify_plot_bt(self, event=None):
        conditions = self.buycondlist.get(0,END)
        try:
            fee = float(self.fees_entry.get())
        except:
            messagebox.showwarning('Input Error', "Check Fee input")
        axis = self.y_ax_bt.get()
        try:
            self.btchart.cla()
            bt = (self.price_ref.pct_change()+1).shift(-1)
            indicators = {**self.to_plots_onchart, **self.to_plots_offchart}
            keys = [key for key in indicators]
            signals = []
            for cond in conditions:
                ind,comp,val = cond.split(';')
                if str(ind) in keys:
                    ind = indicators[ind]
                else:
                    messagebox.showwarning("Input error", "Check values")
                    return 0
                if str(val) in keys:
                    val = indicators[val]
                elif str(val) == "price":
                    val = self.price_ref
                else:
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
            self.btchart.plot(self.price_ref/self.price_ref.iloc[0], color='k', label='BuyHold', alpha=0.3)
            self.btchart.plot(bt, label='Strategy', color='b')
            self.btchart.set_ylabel(f"{axis} Relative\nWealth")
            self.btchart.set_yscale(f'{axis.lower()}')
            self.btchart.legend()
            self.canvas_main.draw()
        except AttributeError:
            messagebox.showwarning("Data Error", "Please select stock")
        
    def _modify_plot(self, event=None):
        option = self.display_onindicator.get()
        indicators = self.to_plots_onchart
        if option.lower()!='all':
            ind = indicators[option]
            self.chart.cla()
            self.chart.plot(self.chartclose, color='k')
            self.chart.plot(ind)
        else:
            self.chart.cla()
            self.chart.plot(self.chartclose, color='k')
            for name in indicators:
                self.chart.plot(indicators[name], label=name)
            self.chart.legend()
        self.canvas_main.draw()
        
    def _modify_plot2(self, event=None):
        option = self.display_offindicator.get()
        indicators = self.to_plots_offchart
        if option.lower()!='all':
            ind = indicators[option]
            self.chart2.cla()
            self.chart2.plot(ind)
        else:
            self.chart2.cla()
            for name in indicators:
                self.chart2.plot(indicators[name], label=name)
            self.chart2.legend()
        self.canvas_main.draw()

    def _plot(self):
        if hasattr(self, 'canvas_main'):
            self.canvas_main.get_tk_widget().destroy()
            self.toolbar_mainframe.destroy()
            self.canvas_main2.get_tk_widget().destroy()
            self.toolbar_mainframe2.destroy()
            self.separator3.destroy()
            self.analysis_x['values'] = []
            self.analysis_y['values'] = []
            self.analysis_var['values'] = []
            self.display_onindicator['values'] = []
            self.display_offindicator['values'] = []
        
        d1 = self.stock_codes.get()
        d2 = self.y_ax.get()
        d3 = self.priceform.get()
        if not(d1) or not(d2) or not(d3):
            return 0
        fig = Figure(figsize=(12,6), dpi=100)
        gs = GridSpec(12, 5, figure=fig)
        
        d4 = self.freqb.get()
        if d4 == '1d' and d4 != self.f:
            self.close = df['Close']
            self.open = df['Open']
            self.high = df['High']
            self.low = df['Low']
            self.dividend = df['Dividends']
            self.stocksplits = df['Stock Splits']
            self.volume = df['Volume']
            self.f = d4
        elif d4 == '5d' and d4 != self.f:
            self.close = df5d['Close']
            self.open = df5d['Open']
            self.high = df5d['High']
            self.low = df5d['Low']
            self.dividend = df5d['Dividends']
            self.stocksplits = df5d['Stock Splits']
            self.volume = df5d['Volume']
            self.f = d4
        elif d4 == '1wk' and d4 != self.f:
            self.close = df1wk['Close']
            self.open = df1wk['Open']
            self.high = df1wk['High']
            self.low = df1wk['Low']
            self.dividend = df1wk['Dividends']
            self.stocksplits = df1wk['Stock Splits']
            self.volume = df1wk['Volume']
            self.f = d4
        elif d4 =='1mo' and d4!=self.f:
            self.close = df1mo['Close']
            self.open = df1mo['Open']
            self.high = df1mo['High']
            self.low = df1mo['Low']
            self.dividend = df1mo['Dividends']
            self.stocksplits = df1mo['Stock Splits']
            self.volume = df1mo['Volume']
            self.f = d4

        self.price_ref = self.close[d1].dropna()

        p_data = [self.close[d1].dropna(),self.open[d1].dropna(),self.high[d1].dropna(),self.low[d1].dropna(), self.volume[d1].dropna(), self.dividend[d1].dropna(), self.stocksplits[d1].dropna()]
        date = str(self.cal.get_date())
        if len(self.cal.state())!=1:
            p_data = [data[data.index>date] for data in p_data]
        self.chartclose = self._gen_close(d3,d1)
        try:
            if self.chartclose == 0:
                return None
        except:
            pass
        self.chartclose = self.chartclose.dropna()

        indicators = self.indicatorslist.get(0,END)
        if indicators:
            self.to_plots_onchart = {}
            self.to_plots_offchart = {}
            oncharts = [file[:-3] for file in os.listdir("other_proj/customchart/indicators_module/onchart") if file[-3:]==".py"]
            offcharts = [file[:-3] for file in os.listdir("other_proj/customchart/indicators_module/offchart") if file[-3:]==".py"]
            transforms_requiring_no_p_data = [file[:-3] for file in os.listdir("other_proj/customchart/indicators_module/transforms/no_p_data") if file[-3:]==".py"]
            transforms_requiring_p_data = [file[:-3] for file in os.listdir("other_proj/customchart/indicators_module/transforms/requires_p_data") if file[-3:]==".py"]
            try:
                for indicator in indicators:
                    name, params, _, params2 = indicator.split(':')
                    str_params = params
                    str_params2 = params2
                    params = ast.literal_eval(params)
                    if len(params2) != 0:
                        params2 = ast.literal_eval(params2)
                    if len(_) == 0:
                        if name in oncharts:
                            self.display_onindicator['values'] = (*self.display_onindicator['values'], f"{name}:{str_params}:{_}:{str_params2}")
                            module = importlib.import_module(f"indicators_module.onchart.{name}")
                            to_plot = module._create_indicator(p_data,params)
                            self.to_plots_onchart[f"{name}:{str_params}:{_}:{str_params2}"] = to_plot
                        elif name in offcharts:
                            self.display_offindicator['values'] = (*self.display_offindicator['values'], f"{name}:{str_params}:{_}:{str_params2}")
                            module = importlib.import_module(f"indicators_module.offchart.{name}")
                            to_plot = module._create_indicator(p_data,params)
                            self.to_plots_offchart[f"{name}:{str_params}:{_}:{str_params2}"] = to_plot
                    else:                        
                        if name in oncharts:
                            self.display_onindicator['values'] = (*self.display_onindicator['values'], f"{name}:{str_params}:{_}:{str_params2}")
                            module = importlib.import_module(f"indicators_module.onchart.{name}")
                            to_plot = module._create_indicator(p_data,params)
                            if _ in transforms_requiring_p_data:
                                module = importlib.import_module(f"indicators_module.transforms.requires_p_data.{_}")
                                to_plot = module._transform_indicator(to_plot,params2, p_data)
                            elif _ in transforms_requiring_no_p_data:
                                module = importlib.import_module(f"indicators_module.transforms.no_p_data.{_}")
                                to_plot = module._transform_indicator(to_plot,params2)
                            try:
                                if module.TURNS_OFF_CHART:
                                    self.to_plots_offchart[f"{name}:{str_params}:{_}:{str_params2}"] = to_plot    
                                else:
                                    self.to_plots_onchart[f"{name}:{str_params}:{_}:{str_params2}"] = to_plot
                            except:    
                                self.to_plots_onchart[f"{name}:{str_params}:{_}:{str_params2}"] = to_plot
                        elif name in offcharts:
                            self.display_offindicator['values'] = (*self.display_offindicator['values'], f"{name}:{str_params}:{_}:{str_params2}")
                            module = importlib.import_module(f"indicators_module.offchart.{name}")
                            to_plot = module._create_indicator(p_data,params)
                            if _ in transforms_requiring_p_data:
                                module = importlib.import_module(f"indicators_module.transforms.requires_p_data.{_}")
                                to_plot = module._transform_indicator(to_plot,params2, p_data)
                            elif _ in transforms_requiring_no_p_data:
                                module = importlib.import_module(f"indicators_module.transforms.no_p_data.{_}")
                                to_plot = module._transform_indicator(to_plot,params2)
                            self.to_plots_offchart[f"{name}:{str_params}:{_}:{str_params2}"] = to_plot
            except:
                messagebox.showwarning("Indicator error", "Check indicator inputs")
                return 0
            
            
            if len(self.to_plots_onchart) != 0:
                self.display_onindicator['values'] = (*self.display_onindicator['values'], "All")
            if len(self.to_plots_offchart) != 0:
                self.btchart = fig.add_subplot(gs[0:3,:])
                self.btchart.set_ylabel("Relative\nWealth")
                self.chart = fig.add_subplot(gs[3:9,:], sharex=self.btchart)
                self.chart2 = fig.add_subplot(gs[9:,:], sharex=self.chart)
                self.display_offindicator['values'] = (*self.display_offindicator['values'], "All")
            else:
                self.btchart = fig.add_subplot(gs[0:4,:])
                self.btchart.set_ylabel("Relative\nWealth")
                self.chart = fig.add_subplot(gs[4:,:], sharex=self.btchart)

            for name in self.to_plots_onchart:
                self.chart.plot(self.to_plots_onchart[name], label=name)
            for name in self.to_plots_offchart:
                self.chart2.plot(self.to_plots_offchart[name], label=name)

            if (len(self.to_plots_onchart) != 0) and (len(self.to_plots_offchart) != 0):
                self.disp_onind.grid(row=0, column=0)
                self.display_onindicator.grid(row=1,column=0)
                self.disp_offind.grid(row=0, column=1)
                self.display_offindicator.grid(row=1,column=1)
            elif (len(self.to_plots_onchart) != 0):
                self.disp_onind.grid(row=0, column=0)
                self.display_onindicator.grid(row=1,column=0)
                self.disp_offind.grid_remove()
                self.display_offindicator.grid_remove()
            elif (len(self.to_plots_offchart) != 0):
                self.disp_offind.grid(row=0, column=0)
                self.display_offindicator.grid(row=1,column=0)
                self.disp_onind.grid_remove()
                self.display_onindicator.grid_remove()

            if len(self.to_plots_onchart) != 0:            
                self.chart.legend()
            if len(self.to_plots_offchart) != 0:
                self.chart2.legend()    
            
            del indicator, to_plot, module, name, params
            
            self.analysis_x['values'] = [*{**self.to_plots_onchart, **self.to_plots_offchart}]
            self.analysis_y['values'] = [*{**self.to_plots_onchart, **self.to_plots_offchart}]
            self.analysis_var['values'] = [*{**self.to_plots_onchart, **self.to_plots_offchart}]
        else:
            self.chart = fig.add_subplot(gs[:,:])       
            self.display_onindicator.grid_remove()
            self.display_offindicator.grid_remove() 
        del indicators

        self.chart.plot(self.chartclose, color='k', zorder=0)
        self.chart.set_ylabel(f'{d2} Price')
        self.chart.set_yscale(f'{d2.lower()}')

        fig.tight_layout()
        
        self.canvas_main = FigureCanvasTkAgg(fig, master=self.main_master2)
        self.canvas_main.draw()
        self.canvas_main.get_tk_widget().grid(row=2,column=0, columnspan=4)
        
        self.toolbar_mainframe = Frame(master=self.main_master2)
        self.toolbar_mainframe.grid(row=3, column=0, columnspan=4)
        self.toolbar_main = NavigationToolbar2Tk(self.canvas_main, self.toolbar_mainframe)
        self.toolbar_main.update()
        
        width, height = fig.get_size_inches() * fig.dpi
        self.hold_canv.configure(width=int(width))
        
        self.separator3 = Separator(self.main_master2, orient='horizontal')
        self.separator3.grid(row=4, column=0, columnspan=4, pady=20, sticky="WE")
        
        self.fig2 = Figure(figsize=(12,5), dpi=100)
        gs2 = GridSpec(4, 4, figure=self.fig2)
        
        self.l_plot_type.grid(row=5, column=0)
        self.plot_type.grid(row=6, column=0, pady=(0,10))
        
        self.canvas_main2 = FigureCanvasTkAgg(self.fig2, master=self.main_master2)
        self.canvas_main2.draw()
        self.canvas_main2.get_tk_widget().grid(row=7, column=0, columnspan=4)
        
        self.toolbar_mainframe2 = Frame(master=self.main_master2)
        self.toolbar_mainframe2.grid(row=8, column=0, columnspan=4)
        self.toolbar_main2 = NavigationToolbar2Tk(self.canvas_main2, self.toolbar_mainframe2)
        self.toolbar_main2.update()
        
        self.main_master2.update_idletasks()
        self._update_scroll()
        
    def _gen_close(self,price_type,ticker):
        date = str(self.cal.get_date())
        price_type = price_type.lower()
        if price_type=="normal":
            ret = self.close[ticker]
        elif price_type== 'heikin ashi':
            ret = 0.25*(self.close[ticker]+self.open[ticker]+self.high[ticker]+self.low[ticker])
        elif price_type == "line break":
            close = self.close[ticker].dropna()
            start_price = close.iloc[0]
            prices = [start_price]
            dates = [close.index[0]]
            max_p = start_price
            min_p = start_price
            if self.cust_vals_lb == False:
                lim = 3
            else: 
                try:
                    lim = int(self.editlinebreak.get())
                except ValueError:
                    messagebox.showwarning("Input Error", "Please specify all values.")
                    return 0
            for idx,val in zip(close.index[1:],close.values[1:]):
                if len(prices) >= lim + 1:
                    window = prices[-(lim+1):]
                    max_p = max(window)
                    min_p = min(window)
                    if val>max_p:
                        prices.append(val)
                        dates.append(idx)
                    elif val<min_p:
                        prices.append(val)
                        dates.append(idx)
                else:
                    if val>max_p:
                        prices.append(val)
                        dates.append(idx)
                        max_p = val
                    elif val<min_p:
                        prices.append(val)
                        dates.append(idx)
                        min_p = val
            ret = pd.Series(prices, index=dates)
            ret = ret.reindex(close.index).ffill()
        elif price_type == "renko":
            close = self.close[ticker].dropna()
            len_close = close.shape[0]
            start_price = close.iloc[0]
            prices = [start_price]
            dates = [close.index[0]]
            prev = start_price
            if self.cust_vals_kr == False:
                for idx, val in zip(close.index[1:],close.values[1:]):
                    if idx == close.index[-1]:
                        prices.append(val)
                        dates.append(idx)
                        break
                    if val > prev*1.04:
                        prices.append(val)
                        dates.append(idx)
                        prev = val
                    elif val < prev*0.96:
                        prices.append(val)
                        dates.append(idx)
                        prev = val
            else:
                try:
                    method = self.editkagirenko1.get().lower()
                    metric = int(self.editkagirenko2.get())
                except ValueError:
                    messagebox.showwarning("Input Error", "Please specify all values.")
                    return 0
                if method == 'pct':
                    for idx, val in zip(close.index[1:],close.values[1:]):
                        if idx == close.index[-1]:
                            prices.append(val)
                            dates.append(idx)
                            break
                        if val > prev*(1+metric/100):
                            prices.append(val)
                            dates.append(idx)
                            prev = val
                        elif val < prev*(1-metric/100):
                            prices.append(val)
                            dates.append(idx)
                            prev = val
                else:
                    if method == 'fixed':
                        condition = np.arange(len_close)
                        condition[:] = metric
                        condition = pd.Series(condition)
                    elif method == 'atr':
                        condition = self._calc_atr(metric,ticker)
                    for idx, val, cond in zip(close.index[1:],close.values[1:],condition.values[1:]):
                        if idx == close.index[-1]:
                            prices.append(val)
                            dates.append(idx)
                            break
                        if val > prev + cond:
                            prices.append(val)
                            dates.append(idx)
                            prev = val
                        elif val < prev - cond:
                            prices.append(val)
                            dates.append(idx)
                            prev = val
            ret = pd.Series(prices, index=dates)
            ret = ret.reindex(close.index).ffill()
        elif price_type == 'kagi':
            close = self.close[ticker].dropna()
            len_close = close.shape[0]
            start_price = close.iloc[0]
            prices = [start_price]
            dates = [close.index[0]]
            bound = close.iloc[1]
            if bound>start_price:
                bound_type = 1
            else:
                bound_type = -1
            if self.cust_vals_kr == False:
                for idx,val in zip(close.index[2:],close.values[2:]):
                    if idx == close.index[-1]:
                        prices.append(val)
                        dates.append(idx)
                        break
                    if bound_type == 1:
                        if val > bound:
                            bound = val
                        elif val < bound * 0.96:
                            prices.append(bound)
                            dates.append(idx)
                            bound = val
                            bound_type = -1
                    else:
                        if val < bound:
                            bound = val
                        elif val > bound * 1.04:
                            prices.append(bound)
                            dates.append(idx)
                            bound = val
                            bound_type = 1
            else:
                try:
                    method = self.editkagirenko1.get().lower()
                    metric = int(self.editkagirenko2.get())
                except ValueError:
                    messagebox.showwarning("Input Error", "Please specify all values.") 
                    return 0
                if method == 'pct':
                    for idx,val in zip(close.index[2:],close.values[2:]):
                        if idx == close.index[-1]:
                            prices.append(val)
                            dates.append(idx)
                            break
                        if bound_type == 1:
                            if val > bound:
                                bound = val
                            elif val < bound * (1-metric/100):
                                prices.append(bound)
                                dates.append(idx)
                                bound = val
                                bound_type = -1
                        else:
                            if val < bound:
                                bound = val
                            elif val > bound * (1+metric/100):
                                prices.append(bound)
                                dates.append(idx)
                                bound = val
                                bound_type = 1
                else: 
                    if method == 'fixed':
                        condition = np.arange(len_close)
                        condition[:] = metric
                        condition = pd.Series(condition)
                    else:
                        condition = self._calc_atr(metric,ticker)
                    for idx,val,cond in zip(close.index[1:], close.values[1:], condition.values[1:]):
                        if idx == close.index[-1]:
                            prices.append(val)
                            dates.append(idx)
                            break
                        if bound_type == "up":
                            if val > bound:
                                bound = val
                            elif val < bound - cond:
                                prices.append(bound)
                                dates.append(idx)
                                bound = val
                                bound_type = "down"
                        else:
                            if val < bound:
                                bound = val
                            elif val > bound + cond:
                                prices.append(bound)
                                dates.append(idx)
                                bound = val
                                bound_type = "up"
            ret = pd.Series(prices, index=dates)
            ret = ret.reindex(close.index).ffill()
        if len(self.cal.state())==1:
            return ret
        else:
            return ret[ret.index>date]

    def _calc_atr(self,periods,ticker):
        close = self.close[ticker].dropna()
        high = self.high[ticker]
        high = high.iloc[high.index.isin(close.index)]
        low = self.low[ticker]
        low = low.iloc[low.index.isin(close.index)]
        atr = pd.concat([high-low, high-close.shift(), low-close.shift()],axis=1)
        atr = np.max(atr,axis=1)
        atr = atr.rolling(periods).mean()
        return atr

root = Tk()
StockCharts(root,df)
root.mainloop()