
# Machine Learning for Trading 2nd Edition
# Stefan Jansen

from pathlib import Path
from dotenv import load_dotenv
import requests
from io import BytesIO
from zipfile import ZipFile, BadZipFile

import numpy as np 
import pandas as pd
import pandas_datareader.data as web
import os
from sklearn.datasets import fetch_openml

load_dotenv()
DATA_PATH = Path('assets.h5')
API_KEY = os.getenv('NASDAQ_API_KEY')
DATA = ['nasdaq', 'sp500', 'us']


class Data_Manager:

    def store_data(self, name: str) -> None: 

        if name == "nasdaq":

            """
            wiki_prices.csv download link
            - login to NASDAQ
            - https://data.nasdaq.com/tables/WIKIP/WIKI-PRICES/export

            wiki_stocks.csv link
            - https://github.com/PacktPublishing/Machine-Learning-for-Algorithmic-Trading-Second-Edition/blob/master/data/wiki_stocks.csv
            """

            df = (pd.read_csv(
                'wiki_prices.csv', 
                parse_dates=['date'],
                index_col=['date', 'ticker'],
                infer_datetime_format=True
            ).sort_index())
            with pd.HDFStore(DATA_PATH) as store:
                store.put('quandl/wiki/prices', df)

            df = pd.read_csv('wiki_stocks.csv')
            with pd.HDFStore(DATA_PATH) as store:
                store.put('quandl/wiki/stocks', df)

        elif name == "sp500":

            df = web.DataReader(name='SP500', data_source='fred', start=2009).squeeze().to_frame('close')
            with pd.HDFStore(DATA_PATH) as store:
                store.put('sp500/fred', df)

            url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            df = pd.read_html(url, header=0)[0]
            df.columns = ['ticker', 'name', 'sec_filings', 'gics_sector', 'gics_sub_industry',
                    'location', 'first_added', 'cik', 'founded']
            df = df.drop('sec_filings', axis=1).set_index('ticker')

            with pd.HDFStore(DATA_PATH) as store:
                store.put('sp500/stocks', df)

        elif name == "us":

            """
            us_equities_meta_data.csv link
            - https://github.com/PacktPublishing/Machine-Learning-for-Algorithmic-Trading-Second-Edition/blob/master/data/us_equities_meta_data.csv
            """

            df = pd.read_csv('us_equities_meta_data.csv')
            
            with pd.HDFStore(DATA_PATH) as store:
                store.put('us_equities/stocks', df.set_index('ticker'))
            
            
if __name__ == '__main__':

    data_manager = Data_Manager()
    for data in DATA:

        data_manager.store_data(name=data)
