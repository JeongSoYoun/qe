
from traceback import format_exception
from h11 import Data
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
    def get_market_cap_by_date(ticker=None, freq='d') -> list :
        
        (_from, _to) = Utils.calculate_date()
        df = krx.get_market_cap_by_date(
            _from, 
            _to, 
            ticker=ticker, 
            freq=freq
        )

        return df['거래대금'].values.tolist()

    @staticmethod
    def get_ticker_name(ticker: str) -> str :

        return krx.get_market_ticker_name(ticker=ticker)

if __name__ == "__main__":
    
    # print(Data_Manager().get_ticker())
    print(Data_Manager.get_market_cap_by_date(
        fromdate='20210127',
        todate='20220127',
        ticker='005930'
    ))