#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:47:52 2017
@author: alexz
"""

#import sys
#import msvcrt
import getpass
import pandas as pd
from InvestopediaApi import ita

class PortfolioMetrics:
    total = 0;
    win = 0;
    loss = 0;
    exposure_gross = 0;
    exposure_at_cost = 0;
    

password = getpass.getpass(prompt = 'Investopedia account password:')
print('Logging in.....')
client = ita.Account("photon318@gmail.com", password)

PF_state = client.get_portfolio_status()

portfolio = client.get_current_securities()
PF = PortfolioMetrics();

open_trades = client.get_open_trades()
for open_trade in open_trades:
    print("{0} {1} {2} {3} {4}".format(
            open_trade.date_time, 
            open_trade.description, 
            open_trade.symbol, 
            open_trade.quantity, 
            ita.get_quote(open_trade.symbol)
            ))
    
w = pd.read_csv('weights.csv', )
w.groupby('C')['C','R'].sum()
#
#w[w['CODE'] == 'RSO']['C'].sum()
#w[w['CODE'] == 'RSO'].loc[:,'LVL':'C']
#    
#    
long_entries = pd.read_csv('long_entries.csv')
##X = dataset.iloc[:, :-1].values
##y = dataset.iloc[:, 3].values
g_alloc =     PF_state.account_val * 0.01;

print("Initial {:.2f}".format(g_alloc))
live_trading  = False

total_exposed = 0
for index, order in long_entries.iterrows():
    code = order['C']
    symbol = order['S']
    price = order['P']
    lvl = order['L']
    ordertype = order['T']
    
    sc_coef = w[w['C'] == code].iloc[lvl:,w.columns.get_loc("R")].values[0]
    sc_total = w[w['C'] == code].iloc[lvl:,w.columns.get_loc("T")].values[0] 

    unit_alloc = g_alloc * sc_coef 
    total_exposed += unit_alloc
    size =   int(round(unit_alloc / price, 0))      
    print("Located {:.2f}".format(total_exposed))
    if ordertype == 0:
        print('Placing Market order for {0} Buy {1} {2}'.format(symbol, size, sc_coef))
        if live_trading: 
            client.trade(symbol, ita.Action.buy, size, duration=ita.Duration.day_order)
    else:
        print('Placing Limit order for {0} Buy {1} Limit {2} {3}'.format(symbol, size, price, sc_coef))
        if live_trading:
            client.trade(symbol, ita.Action.buy, size, "Limit", price, duration=ita.Duration.day_order)
        
#    
#    
#    Buying 10 shares of Google (GOOG) at market price:
#
#client.trade("GOOG", ita.Action.buy, 10)
#Selling 10 shares of Google at market price:
#
#client.trade("GOOG", ita.Action.sell, 10)
#Shorting 10 shares of Google:
#
#    class Action(Enum):
#    buy = 1
#    sell = 2
#    short = 3
#    cover = 4
#
#
#class Duration(Enum):
#    day_order = 1
#    good_cancel = 2

#cent.trade("GOOG", ita.Action.short, 10)
#Buying 10 shares of Google with a limit order at $500
#client.trade("GOOG", ita.Action.SellShort, 10, "Limit", 500)
#
#short_entries = pd.read_csv('short_entries.csv')
##X = dataset.iloc[:, :-1].values
##y = dataset.iloc[:, 3].values
#for index, short_order in short_entries.iterrows():
#    symbol = short_order['Symbol']
#    price = short_order['Price']
#    size = short_order['Size']
#    coef = short_order['Coef']
#    print('Placing trade for', symbol)
#    client.trade(symbol, ita.Action.short, size, "Limit", price)


    
    
    
    
    
    
