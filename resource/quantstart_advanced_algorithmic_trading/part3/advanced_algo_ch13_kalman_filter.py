from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from pykalman import KalmanFilter 

def scatterplot(etfs,price):

    price_length = len(price)
    colour_map = plt.cm.get_cmap('YlorRd')
    colours = np.linspace(0.1,1,price_length)

    scatterplot = plt.scatter(

        price[etfs[0]],
        price[etfs[1]],
        s=30,
        c=colours,
        cmap=colour_map,
        edgecolors='k',
        alpha=0.8
    )
 



if __name__ == "__main__":

    etfs = ['TLT','IEI']
    start_date = "2010-08-01"
    end_date = "2016-08-01"

    tlt_df = pdr.get_data_yahoo(etfs[0],start_date,end_date)
    iei_df = pdr.get_data_yahoo(etfs[1],start_date,end_date)