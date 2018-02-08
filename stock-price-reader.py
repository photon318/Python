#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 12:37:37 2018

@author: alexz
"""

import pandas as pd
from pandas_datareader import data
from datetime import datetime, timedelta


stocks = pd.read_csv('get_last_prices.csv')

EODDate = datetime.now().date() - timedelta(days=1)
print("Requesting EOD close for {}".format(EODDate))
print()

for index, stock in stocks.iterrows():
    ticker = stock['Symbol']
    bar = data.DataReader(ticker,  "morningstar", EODDate, EODDate)
    close = bar.loc[EODDate.strftime('%Y-%m-%d'):,'Close'].values
#    close = bar.iloc[:1,0].values
    print("{:<10} {:>6.2f}".format(ticker, float(close)));
    

    