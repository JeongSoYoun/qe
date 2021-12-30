import datetime
import pprint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import pymc3 as pd
import seaborn as sns

def obtain_prices_df(ticker,start_date,end_date):

    df = pdr.get_data_yahoo(ticker, start_date, end_date)
    df["returns"] = df["Adj Close"]/df["Adj Close"].shift(1)
    df.dropna(inplace=True)
    df["log_returns"] = np.log(df["returns"])

    return df

def plot(df,ticker):

    df["log_returns"].plot(linewidth = 0.5)
    plt.ylabel("%s daily percentage log returns" %ticker)

    plt.show()


if __name__ == "__main__":

    start_date = datetime.datetime(2006,1,1)
    end_date = datetime.datetime(2015,12,31)
    ticker = "AMZN"

    df = obtain_prices_df(ticker = ticker, start_date = start_date, end_date = end_date)

    print(df)
    plot(df,ticker)