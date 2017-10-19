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

#import sys
#import msvcrt
import getpass
from InvestopediaApi import ita

password = getpass.getpass(prompt = 'Investopedia account password:')
print('Logging in.....')
client = ita.Account("photon318@gmail.com", password)

status = client.get_portfolio_status()
print()
print("{:<20} {:> 15,.2f},$".format("Account Value:",status.account_val))
print("{:<20} {:> 15,.2f},$".format("Buying Power:", status.buying_power))
print("{:<20} {:> 15,.2f},$".format("Cash:", status.cash))
print("{:<20} {:> 15,.2f},%".format("Annual Return:", status.annual_return))


print()
print("Portfolio")

portfolio = client.get_current_securities()

bought_securities = portfolio.bought
shorted_securities = portfolio.shorted
options = portfolio.options

table_format = "{:<10} {:<50} {:>6} {:>10}"
print(table_format.format("Symbol", "Description", "Shares", "Total PNL"))
table_uformat = "{:-<10} {:-<50} {:->6} {:->10}"
print(table_uformat.format("", "", "", ""))


total = 0
win = 0
loss = 0
exposure_gross = 0
exposure_at_cost = 0

for bought in bought_securities:
    piece  = (bought.current_price-bought.purchase_price)*bought.quantity
    total += piece
    exposure_gross += bought.quantity * bought.current_price
    exposure_at_cost += bought.quantity * bought.purchase_price
    if piece > 0:
        win += piece
    else:
        loss += piece
    print("{:<10} {:<50} {:>6,.0f} {:>10,.2f}".format(
            bought.symbol
            ,bought.description
            ,bought.quantity
            ,(bought.current_price-bought.purchase_price)*bought.quantity))
    
    
    
print("{:-<100}".format(""))
print("Exp.C: {:.2f}  Exp.G: {:.2f} Delta: {:.2f}".format(exposure_at_cost, exposure_gross, exposure_gross-exposure_at_cost))
print()
print("Total PNL: {:.2f}  Win: {:.2f} Loss: {:.2f}".format(total, win, loss))
print()
print("Gross Exposured,$:  {:.2f}".format(exposure_gross))
print("Gross Exposure:     {:.2f}%".format(exposure_gross/status.account_val*100))
print("Exposured at Cost,$:{:.2f}".format(exposure_at_cost))
print("Exposure at Cost,%: {:.2f}%".format(exposure_at_cost/status.account_val*100))
print()
print("M1:                 {:.2f}".format(status.account_val-exposure_gross))
print("M2:                 {:.2f}".format(status.account_val-status.cash))
#    print(bought.symbol, bought.description, bought.purchase_price, bought.current_price, (bought.current_price-bought.purchase_price)*bought.quantity )
 

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
#client.trade("GOOG", ita.Action.short, 10)
#Buying 10 shares of Google with a limit order at $500
#
#client.trade("GOOG", ita.Action.buy, 10, "Limit", 500)