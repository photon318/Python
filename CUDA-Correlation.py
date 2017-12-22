#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 20:05:04 2017

@author: alexz
"""
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

os.chdir("/Users/Alexz/Documents/Github/Python")

data = pd.read_csv("Rates2017.csv");

corr = data.loc[:,['AUD','BGN','CAD','CHF','CNY','CZK','DKK','EUR','GBP','IRR','ISK',
                   'JPY','KGS','KWD','KZT','MDL','NOK','NZD','PLN','RUB','SEK','SGD','TRY','UAH','USD','XDR']].corr()

pd.plotting.scatter_matrix(corr)

sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax)



# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(8, 8))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
