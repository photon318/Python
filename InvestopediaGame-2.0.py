#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:47:52 2017
@author: alexz
"""

# TO DO: 
# 1. Implelemt importing of scales form base aplication and applying them to Investopedia account (IA).
#    In scales must be ratio and scale level. Rest is caclulated based on allocations in IA
# 2. Implement importing of exit siganls from base application
#3. Use adju prices for % chg

#import sys
#import msvcrt
import getpass
import pandas as pd
from InvestopediaApi import ita
from pandas_datareader import data
from datetime import datetime, timedelta

class PortfolioMetrics:
    total = 0;
    win = 0;
    loss = 0;
    exposure_gross = 0;
    exposure_at_cost = 0;
    

def print_status ( status ):
    print()
    print("{:<20} {:> 15,.2f},$".format("Account Value:",status.account_val))
    print("{:<20} {:> 15,.2f},$".format("Buying Power:", status.buying_power))
    print("{:<20} {:> 15,.2f},$".format("Cash:", status.cash))
    print("{:<20} {:> 15,.2f},%".format("Annual Return:", status.annual_return))
    print()
    return;
    
def print_shares_header ()   :
    table_format = "{:<10} {:<50} {:>6} {:>10} {:>10}"
    print(table_format.format("Symbol", "Description", "Shares", "Total PNL", "DayChg %"))
    table_uformat = "{:-<10} {:-<50} {:->6} {:->10} {:->10}"
    print(table_uformat.format("", "", "", "", ""))
    return;

def print_portfolio_section (securities, metrics, isShort) :
    days_offests = (3,3,2,2,2,2,3)
    for sec in securities:
        if sec.symbol == "BTI1":
            continue
        if isShort:
            piece  = (sec.purchase_price-sec.current_price)*sec.quantity
        else:
            piece  = (sec.current_price-sec.purchase_price)*sec.quantity
        metrics.total += piece
        metrics.exposure_gross += sec.quantity * sec.current_price
        metrics.exposure_at_cost += sec.quantity * sec.purchase_price
        if piece > 0:
            metrics.win += piece
        else:
            metrics.loss += piece
    
        prev_close_date = datetime.now().date() - timedelta(days=days_offests[datetime.now().date().weekday()])
        prev_close = data.DataReader(sec.symbol,  "morningstar", prev_close_date, prev_close_date).loc[prev_close_date.strftime('%Y-%m-%d'):,'Close'].values
        
        day_chg =  (sec.current_price / prev_close -1 ) * 100
        print("{:<10} {:<50} {:>6,.0f} {:>10,.2f} {:>10,.2f}".format(
                sec.symbol
                ,sec.description
                ,sec.quantity
                ,piece
#                ,sec.current_price 
#                ,float(prev_close)
                ,float(day_chg)))
    print()
    return;

def print_statistics(PF, status) :
    print("{:-<79}".format(""))
    print("Exp.C: {:.2f}  Exp.G: {:.2f} Delta: {:.2f}".format(PF.exposure_at_cost, PF.exposure_gross, PF.exposure_gross-PF.exposure_at_cost))
    print()
    print("Total PNL: {:.2f}  Win: {:.2f} Loss: {:.2f}".format(PF.total, PF.win, PF.loss))
    print()
    print("Gross Exposured,$:  {:.2f}".format(PF.exposure_gross))
    print("Gross Exposure:     {:.2f}%".format(PF.exposure_gross/status.account_val*100))
    print("Exposured at Cost,$:{:.2f}".format(PF.exposure_at_cost))
    print("Exposure at Cost,%: {:.2f}%".format(PF.exposure_at_cost/status.account_val*100))
    print()
    print("M1:                 {:.2f}".format(status.account_val-PF.exposure_gross))
    print("M2:                 {:.2f}".format(status.account_val-status.cash))
    return;



password = getpass.getpass(prompt = 'Investopedia account password:')
print('Logging in.....')
client = ita.Account("photon318@gmail.com", password)

PF_state = client.get_portfolio_status()
print_status(PF_state)

portfolio = client.get_current_securities()


PF = PortfolioMetrics();

print("Long Portfolio")
print_shares_header()
print_portfolio_section(portfolio.bought, PF, isShort=False)

print("Short Portfolio")
print_shares_header()
print_portfolio_section(portfolio.shorted, PF, isShort=True)
 
print_statistics(PF, PF_state)


open_trades = client.get_open_trades()
for open_trade in open_trades:
    print("{0} {1} {2} {3} {4}".format(
            open_trade.date_time, 
            open_trade.description, 
            open_trade.symbol, 
            open_trade.quantity, 
            ita.get_quote(open_trade.symbol)
            ))
    
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

    
    
    
    
    
