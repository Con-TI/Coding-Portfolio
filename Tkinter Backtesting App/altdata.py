import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pandas as pd

driver = webdriver.Firefox()
driver.maximize_window()
wait = WebDriverWait(driver,3)
countries = ['indonesia','united-states','japan','united-kingdom','china','australia','switzerland','canada','india','south-korea','euro-area','new-zealand','norway','sweden','hong-kong','singapore','malaysia','brazil']
metrics = ['interest-rate']
# metrics = ['harmonised-inflation-rate-mom',
#            'producer-price-inflation-mom',
#            'import-prices',
#            'export-prices',
#            'retail-sales',
#            'gasoline-prices',
#            'price-to-rent-ratio',
#            'residential-property-prices',
#            'consumer-confidence',
#            'business-confidence',
#            'manufacturing-pmi',
#            'unemployment-rate',
#            'gold-reserves',
#            'terms-of-trade',]
for metric in metrics:
    series = []
    for country in countries:
        link = f"https://tradingeconomics.com/{country}/{metric}"
        driver.get(link)
        time.sleep(1)
        max_val = float(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_ctl00_ctl02_Panel1"]/div/div[3]/table/tbody/tr/td[4]'))).text)
        min_val = float(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_ctl00_ctl02_Panel1"]/div/div[3]/table/tbody/tr/td[5]'))).text)
        maxlen = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="dateSpansDiv"]/a[4]')))
        maxlen.click()
        time.sleep(1)
        line = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/div[5]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[3]/div/button')))
        line.click()
        time.sleep(1)
        line = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/div[5]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[3]/div/div/div[5]/button')))
        line.click()
        dots = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/div[5]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div[1]/div/button[4]')))
        dots.click()
        full = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="fullscreenOption"]')))
        full.click()
        time.sleep(1)
        del maxlen, line, dots, full

        path = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'g g path')))[0].get_attribute('outerHTML')
        soup = BeautifulSoup(path, 'html.parser')
        path = soup.find('path').attrs['d']
        path = [part for part in path.split(' ')]
        path = [(float(path[3*i+1]),float(path[3*i+2])) for i in range(int(len(path)/3))]

        date_toggle = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="dateInputsToggle"]')))
        date_toggle.click()
        time.sleep(0.2)
        start_date = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/div[5]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[5]/input[1]')))
        end_date = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/div[5]/div/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[5]/input[2]')))
        start_date = datetime.strptime(start_date.get_attribute('value'), '%Y-%b-%d')
        end_date = datetime.strptime(end_date.get_attribute('value'), '%Y-%b-%d')
        date_toggle.click()
        days = (end_date-start_date).days

        start_x = path[0][0]
        end_x = path[-1][0]
        dates = []
        for x,_ in path:
            dates.append(start_date + timedelta(days=int((x-start_x)/(end_x-start_x)*float(days))))

        ys = [y for _,y in path]
        max_y = min(ys)
        min_y = max(ys)
        nums = []
        for _,y in path:
            nums.append(round(4*(min_val+(y-min_y)/(max_y-min_y)*(max_val-min_val)))/4)

        df = pd.Series(nums,index=pd.DatetimeIndex(dates),name=country)
        x = df.diff()!=0
        x = x.shift(-1) | x
        df[~x] = np.nan
        df = df.dropna()
        series.append(df)
    df = pd.concat(series,axis=1).ffill()
    df.to_pickle(f'datastore/{metric}.pkl')
driver.quit()