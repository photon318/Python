#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:47:52 2017
@author: alexz
"""

#import msvcrt
import getpass
import pandas as pd
import sys
import getopt
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


live_trading  = False
max_value  = 0.02
entries_file = ''
trades_log_file = ''

try:
    opts, args = getopt.getopt(sys.argv[1:], "til", ["live-trading=", "entries=", "log-file="])
except getopt.GetoptError:
    print("Usage python Investpedia-automation.py --live-trading=True|False")
    print("--entries=<file.csv>" )
    print("--log-file=<file.csv>" )
    sys.exit(0)


for opt, arg in opts:
    if opt in ("-t", "--live-trading"):
        if (arg == 'True' ):
            live_trading = True
        else:
            live_trading  = False
    elif opt in ("-i", "--entries"):
        entries_file = arg
    elif opt in ("-l", "--log"):
        trades_log_file = arg

print ("Live trading mode: "+str(live_trading))   
print ("Entries commands:" + entries_file)
print ("Log results to:" + trades_log_file)

if trades_log_file == '' :
    print("ATTENTION! Log file is not specified, results will not be recorded!")
        
        
try:    
    w = pd.read_csv('weights.csv', )
    print(w.groupby('C')['C','R'].sum())
except:
    print("W-File parsing error")
    sys.exit(4)
    
#
#w[w['CODE'] == 'RSO']['C'].sum()
#w[w['CODE'] == 'RSO'].loc[:,'LVL':'C']
#    
#   
if  entries_file != '' :
    try:
        long_entries = pd.read_csv(entries_file)
    except:
        print("E-File parsing error")
        sys.exit(2)
else:
        print("No entries file specified!")
        sys.exit(3)
    


password = getpass.getpass(prompt = 'Investopedia account password:')
print('Logging in.....')
client = ita.Account("photon318@gmail.com", password)

PF_state = client.get_portfolio_status()

portfolio = client.get_current_securities()
PF = PortfolioMetrics();
g_alloc =     PF_state.account_val * max_value


r_alloc  = {}
open_pos = {}
actual_orders = []
total_exposed = 0

print("Initial alloc {:.2f}".format(g_alloc))
print("Total order to place {0}".format(len(long_entries)))

for index, order in long_entries.iterrows():
    try:
        code = order['C']
        symbol = order['S']
        price = order['P']
        lvl = int(order['L'])
        ordertype = int(order['T']) # 0 - Market, 1 -Limit
        orderside = DecodeOrderSide(order['R']) # 1 - Long, 2-Sell, 3-Short, 4-BuyToCover
        exit_Z = order['Z'] # Size to exit
        
        
        sc_coef = w[w['C'] == code].iloc[lvl:,w.columns.get_loc("R")].values[0]
        sc_total = w[w['C'] == code].iloc[lvl:,w.columns.get_loc("T")].values[0] 
        unit_alloc = g_alloc * sc_coef 
    
        key = code+'$'+symbol
        keycsv = code+','+symbol
    except Exception:
        print("exception happens")
        print(order);
        break

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

if trades_log_file != '' and live_trading :
    try:
        with open(trades_log_file,'wt') as file:
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