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
    
    
def DecodeOrderSide(side_code):
    if side_code == 1:
        return ita.Action.buy
    elif side_code == 2:
        return ita.Action.sell
    elif side_code == 3:
        return ita.Action.short
    elif side_code == 4: 
        return ita.Action.cover
    else:
        return 0


password = getpass.getpass(prompt = 'Investopedia account password:')
print('Logging in.....')
client = ita.Account("photon318@gmail.com", password)

PF_state = client.get_portfolio_status()

portfolio = client.get_current_securities()
PF = PortfolioMetrics();
#
#open_trades = client.get_open_trades()
#for open_trade in open_trades:
#    print("{0} {1} {2} {3} {4}".format(
#            open_trade.date_time, 
#            open_trade.description, 
#            open_trade.symbol, 
#            open_trade.quantity, 
#            ita.get_quote(open_trade.symbol)
#            ))
#


live_trading  = True
max_value  = 0.02
    
w = pd.read_csv('weights.csv', )
w.groupby('C')['C','R'].sum()

#
#w[w['CODE'] == 'RSO']['C'].sum()
#w[w['CODE'] == 'RSO'].loc[:,'LVL':'C']
#    
#    
long_entries = pd.read_csv('entries-2018-06-01.csv')
g_alloc =     PF_state.account_val * max_value

print("Initial {:.2f}".format(g_alloc))

r_alloc  = {}
open_pos = {}
actual_orders = []

total_exposed = 0

for index, order in long_entries.iterrows():
    code = order['C']
    symbol = order['S']
    price = order['P']
    lvl = order['L']
    ordertype = order['T'] # 0 - Market, 1 -Limit
    orderside = DecodeOrderSide(order['R']) # 1 - Long, 2-Sell, 3-Short, 4-BuyToCover
    exit_Z = order['Z'] # Size to exit
    
    sc_coef = w[w['C'] == code].iloc[lvl:,w.columns.get_loc("R")].values[0]
    sc_total = w[w['C'] == code].iloc[lvl:,w.columns.get_loc("T")].values[0] 
    unit_alloc = g_alloc * sc_coef 

    key = code+'$'+symbol
    keycsv = code+','+symbol

    if exit_Z == 0 :
        size =   int(round(unit_alloc / price, 0))      

        prev_size = 0
        if key in open_pos :
            prev_size = open_pos[key]
        open_pos[key] = prev_size + size
        
        t_alloc = 0
        if key in r_alloc :
            t_alloc = r_alloc[key]
        r_alloc[key] = t_alloc + ( size *  price )

        total_exposed += unit_alloc

        actual_orders.append(keycsv +','+str(lvl)+','+str(orderside)+','+str(ordertype)+',' + str(size)+','+str(price))
    else:
        size = exit_Z
    
    if ordertype == 0:
        print('{0} Placing {1} Market order for {2} {3} {4}'.format(code, orderside, symbol, size, sc_coef))
        if live_trading: 
            if not client.trade(symbol, orderside, size, duration=ita.Duration.day_order):
                print("failed")
    else:
        print('{0} Placing {1} Limit order for {2} {3} Limit {4} {5}'.format(code, orderside, symbol, size, price, sc_coef))
        if live_trading:
            if not client.trade(symbol, orderside, size, "Limit", price, duration=ita.Duration.day_order):
                print("failed")


print("Total allocated {:.2f}".format(total_exposed))

print(r_alloc)

try:
    with open('actual-2018-06-01.csv','wt') as file:
        for line in actual_orders:
            file.write(line)
            file.write('\n')
except Exception:
    print("Write actual orders to file failed")


        
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