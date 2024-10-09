from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
from io import StringIO
import yfinance as yf
from time import sleep

# def find_stock_codes():
#     driver = webdriver.Chrome()
#     wait = WebDriverWait(driver,10)
#     idx = "https://www.idx.co.id/en/market-data/stocks-data/stock-list"
#     driver.get(idx)
#     sleep(10)
#     # sleep(5)
#     driver.execute_script("window.open('');")
#     driver.switch_to.window(driver.window_handles[1])
#     select_element = wait.until(EC.presence_of_element_located((By.TAG_NAME,"select")))
#     select = Select(select_element)
#     select.select_by_visible_text("All")
#     table_element = wait.until(EC.presence_of_element_located((By.TAG_NAME,"table")))
#     table_html = table_element.get_attribute('outerHTML')
#     df = pd.read_html(StringIO(table_html))[0]
#     stock_codes = df.iloc[:,1].to_list()
#     listing_years = [int(string[-4:]) for string in df.iloc[:,3].to_list()]
#     return pd.Series(stock_codes), pd.Series(listing_years)

# stock_codes, listing_years = find_stock_codes()
cols = list(pd.read_pickle('datastore/data.pkl').columns.get_level_values(1).unique())

# stock_codes = [f"{code}.JK" for code in stock_codes]
cols.sort()
stock_codes = cols
tickers = [yf.Ticker(code).history(period='max') for code in stock_codes]
opens = pd.concat([ticker['Open'] for ticker in tickers],axis=1)
opens.columns = pd.MultiIndex.from_tuples([('Open',code) for code in stock_codes])
closes = pd.concat([ticker['Close'] for ticker in tickers],axis=1)
closes.columns = pd.MultiIndex.from_tuples([('Close',code) for code in stock_codes])
highs = pd.concat([ticker['High'] for ticker in tickers],axis=1)
highs.columns = pd.MultiIndex.from_tuples([('High',code) for code in stock_codes])
lows = pd.concat([ticker['Low'] for ticker in tickers],axis=1)
lows.columns = pd.MultiIndex.from_tuples([('Low',code) for code in stock_codes])
volume = pd.concat([ticker['Volume'] for ticker in tickers],axis=1)
volume.columns = pd.MultiIndex.from_tuples([('Volume',code) for code in stock_codes])
divs = pd.concat([ticker['Dividends'] for ticker in tickers],axis=1)
divs.columns = pd.MultiIndex.from_tuples([('Dividends',code) for code in stock_codes])
stocksplits = pd.concat([ticker['Stock Splits'] for ticker in tickers],axis=1)
stocksplits.columns = pd.MultiIndex.from_tuples([('Stock Splits',code) for code in stock_codes])
df = pd.concat([opens,closes,highs,lows,volume,divs,stocksplits],axis=1)
df.to_pickle('datastore/data.pkl')

tickers = [yf.Ticker(code).history(period='max', interval='5d') for code in stock_codes]
opens = pd.concat([ticker['Open'] for ticker in tickers],axis=1)
opens.columns = pd.MultiIndex.from_tuples([('Open',code) for code in stock_codes])
closes = pd.concat([ticker['Close'] for ticker in tickers],axis=1)
closes.columns = pd.MultiIndex.from_tuples([('Close',code) for code in stock_codes])
highs = pd.concat([ticker['High'] for ticker in tickers],axis=1)
highs.columns = pd.MultiIndex.from_tuples([('High',code) for code in stock_codes])
lows = pd.concat([ticker['Low'] for ticker in tickers],axis=1)
lows.columns = pd.MultiIndex.from_tuples([('Low',code) for code in stock_codes])
volume = pd.concat([ticker['Volume'] for ticker in tickers],axis=1)
volume.columns = pd.MultiIndex.from_tuples([('Volume',code) for code in stock_codes])
divs = pd.concat([ticker['Dividends'] for ticker in tickers],axis=1)
divs.columns = pd.MultiIndex.from_tuples([('Dividends',code) for code in stock_codes])
stocksplits = pd.concat([ticker['Stock Splits'] for ticker in tickers],axis=1)
stocksplits.columns = pd.MultiIndex.from_tuples([('Stock Splits',code) for code in stock_codes])
df = pd.concat([opens,closes,highs,lows,volume,divs,stocksplits],axis=1)
df.to_pickle('datastore/data5d.pkl')

tickers = [yf.Ticker(code).history(period='max', interval='1wk') for code in stock_codes]
opens = pd.concat([ticker['Open'] for ticker in tickers],axis=1)
opens.columns = pd.MultiIndex.from_tuples([('Open',code) for code in stock_codes])
closes = pd.concat([ticker['Close'] for ticker in tickers],axis=1)
closes.columns = pd.MultiIndex.from_tuples([('Close',code) for code in stock_codes])
highs = pd.concat([ticker['High'] for ticker in tickers],axis=1)
highs.columns = pd.MultiIndex.from_tuples([('High',code) for code in stock_codes])
lows = pd.concat([ticker['Low'] for ticker in tickers],axis=1)
lows.columns = pd.MultiIndex.from_tuples([('Low',code) for code in stock_codes])
volume = pd.concat([ticker['Volume'] for ticker in tickers],axis=1)
volume.columns = pd.MultiIndex.from_tuples([('Volume',code) for code in stock_codes])
divs = pd.concat([ticker['Dividends'] for ticker in tickers],axis=1)
divs.columns = pd.MultiIndex.from_tuples([('Dividends',code) for code in stock_codes])
stocksplits = pd.concat([ticker['Stock Splits'] for ticker in tickers],axis=1)
stocksplits.columns = pd.MultiIndex.from_tuples([('Stock Splits',code) for code in stock_codes])
df = pd.concat([opens,closes,highs,lows,volume,divs,stocksplits],axis=1)
df.to_pickle('datastore/data1wk.pkl')

tickers = [yf.Ticker(code).history(period='max', interval='1mo') for code in stock_codes]
opens = pd.concat([ticker['Open'] for ticker in tickers],axis=1)
opens.columns = pd.MultiIndex.from_tuples([('Open',code) for code in stock_codes])
closes = pd.concat([ticker['Close'] for ticker in tickers],axis=1)
closes.columns = pd.MultiIndex.from_tuples([('Close',code) for code in stock_codes])
highs = pd.concat([ticker['High'] for ticker in tickers],axis=1)
highs.columns = pd.MultiIndex.from_tuples([('High',code) for code in stock_codes])
lows = pd.concat([ticker['Low'] for ticker in tickers],axis=1)
lows.columns = pd.MultiIndex.from_tuples([('Low',code) for code in stock_codes])
volume = pd.concat([ticker['Volume'] for ticker in tickers],axis=1)
volume.columns = pd.MultiIndex.from_tuples([('Volume',code) for code in stock_codes])
divs = pd.concat([ticker['Dividends'] for ticker in tickers],axis=1)
divs.columns = pd.MultiIndex.from_tuples([('Dividends',code) for code in stock_codes])
stocksplits = pd.concat([ticker['Stock Splits'] for ticker in tickers],axis=1)
stocksplits.columns = pd.MultiIndex.from_tuples([('Stock Splits',code) for code in stock_codes])
df = pd.concat([opens,closes,highs,lows,volume,divs,stocksplits],axis=1)
df.to_pickle('datastore/data1mo.pkl')
