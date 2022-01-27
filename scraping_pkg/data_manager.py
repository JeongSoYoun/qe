
from traceback import format_exception
from h11 import Data
from matplotlib.pyplot import close
from pykrx import stock as krx
from utils import Utils

class Data_Manager:

    @staticmethod
    def get_ticker(date: str = None, market: str = "KOSPI") -> list:

        """
            Args
            - date: If not passed, default would be today's date
            - market: default="KOSPI" (KOSPI | KOSDAQ | KONEX | ALL)

            Returns
            - List of Ticker
        """

        return krx.get_market_ticker_list(date=date, market=market)

    @staticmethod
    def get_transaction_amount(ticker=None, freq='d') -> list :
        
        (_from, _to) = Utils.get_date()
        df = krx.get_market_cap_by_date(
            _from, 
            _to, 
            ticker=ticker, 
            freq=freq
        )

        return df['거래대금'].values.tolist()

    @staticmethod 
    def is_upper_limit(ticker: str = None, freq: str ='d'):

        (_from,_to) = Utils.get_date()
        df = krx.get_market_ohlcv_by_date(
                fromdate=_from,
                todate=_to,
                ticker=ticker,
                freq=freq
            )
        start_price = df['시가'].tolist()
        close_price = df['종가'].tolist()

        return start_price,close_price

    @staticmethod
    def is_tail(ticker: str = None):
        pass

    @staticmethod
    def get_ticker_name(ticker: str) -> str :

        return krx.get_market_ticker_name(ticker=ticker)


if __name__ == "__main__":
    
    # print(Data_Manager().get_ticker())
    df = Data_Manager.is_upper_limit(ticker='005930')
    start_price = df['시가'].tolist()
    close_price = df['종가'].tolist()
    print(df)
    print('시가')
    print(start_price)
    print('종가')
    print(close_price)
    print(Utils.pct_change(
        price_1=start_price[0],
        price_2=close_price[1]
    ))
    for index in range(len(df)-1):
        if (
            Utils.pct_change(
                price_1=start_price[index],
                price_2=close_price[index+1]
            ) > 28.5
        ):

            print("true")