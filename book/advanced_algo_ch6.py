
# QuantStart
# Advanced Algorithmic Trading 
# Michael L. Halls-Moore, PhD
# Chapter 6

import datetime
import pprint
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader as pdr
import pymc3 as pm
import seaborn as sns

def obtain_prices_df(ticker,start_date,end_date):

    df = pdr.get_data_yahoo(ticker, start_date, end_date)
    df["returns"] = df["Adj Close"]/df["Adj Close"].shift(1)
    df.dropna(inplace=True)
    df["log_returns"] = np.log(df["returns"])

    return df

def stochastic_volatility_model(df,samples):

    model = pm.Model()
    log_returns = np.array(df["log_returns"])

    with model: 

        sigma = pm.Exponential('sigma', 50.0, testval = 0.1)
        nu = pm.Exponential('nu', 0.1)
        s = pm.GaussianRandomWalk('s', sigma**-2, shape = len(log_returns))
        logrets = pm.StudentT(

            'logrets',
            nu,
            lam = pm.math.exp(-2.0*s),
            observed = log_returns
        )
    
    print("Fitting the stochastic volatility model...")
    with model:

        trace = pm.sample(samples)

    pm.traceplot(trace, model.vars[:-1])
    plt.show()

def plot(df,ticker):

    df["log_returns"].plot(linewidth = 0.5)
    plt.ylabel("%s daily percentage log returns" %ticker)

    plt.show()


if __name__ == "__main__":

    start_date = datetime.datetime(2006,1,1)
    end_date = datetime.datetime(2015,12,31)
    ticker = "AMZN"
    samples = 2000

    df = obtain_prices_df(ticker = ticker, start_date = start_date, end_date = end_date)
    stochastic_volatility_model(df = df,samples = samples)

    print(df)