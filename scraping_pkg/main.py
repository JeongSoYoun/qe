
from scraping import Scraper
from filter import filter_data

K_MARKETS = ["KOSPI"]
TRADE_INFO = ['거래량/거래대금', '시가총액', '발행주식수/유동비율']

def main():

    scraper = Scraper(trade_info=TRADE_INFO)
    data = []
    for market in K_MARKETS:

        scraper.collect(market=market)
        # data.append(filter_data(data=df))
    
if __name__ == "__main__":

    main()