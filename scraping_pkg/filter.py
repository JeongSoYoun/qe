
from scraping import Scraper
import re
from data_manager import Data_Manager

FILTERD_INFO = ['시가총액', '유동비율']
def filter_data(data) -> list:

    """
        시총 
        - 3000억 이상 제외. 

        3년 순이익률
        - 3년 순이익률이 모두 마이너스면 제외.

        거래 대금
        - 300억 미만 제외.
        
        상한가 여부
        
        긴꼬리 여부
    """

    filtered_data = []
    for index in range(len(data)):

        # market_cap
        market_cap = int(re.sub('[^\d]',"",data.loc[index]['시가총액']))

        if market_cap > 3000:
            continue
        
        # 유동비율
        current_ratio = int(re.sub('[^\d]',"",data.loc[index]['유동비율']))
        if current_ratio > 7000: 
            continue
            
        # 3년 순이익률
        profit_3years = data.loc[index]['3년 순이익률']
        for _index in range(len(profit_3years)):
            if profit_3years[_index] == '':
                profit_3years[_index] = 0
        if (
            float(profit_3years[0]) < 0 and  
            float(profit_3years[1]) < 0 and 
            float(profit_3years[2]) < 0
        ):
            continue
        
        ticker = data.loc[index]['티커']
        if filter_market_cap_by_date(ticker=ticker):
        
            filtered_data.append(ticker)
    
    return filtered_data    

def filter_market_cap_by_date(ticker) -> bool:

    df = Data_Manager.get_market_cap_by_date("20210124", "20220125", ticker)
    date = 0
    print(f"filtering {ticker}")
    while date < len(df): 

        if df['거래대금'][date] > 3e10:
            return True
        
        date += 1

if __name__ == "__main__":

    TRADE_INFO = ['거래량/거래대금', '시가총액', '발행주식수/유동비율']

    scraper = Scraper(trade_info=TRADE_INFO)
    df = scraper.collect(limit=10, market="KOSPI")
    filtered_data = filter_data(data=df)

