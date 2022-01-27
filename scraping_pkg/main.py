
from scraping import Scraper
from filter import filter_data

K_MARKETS = ["KOSPI", "KOSDAQ"]
TRADE_INFO = ['거래량/거래대금', '시가총액', '발행주식수/유동비율']

def main():

    scraper = Scraper(trade_info=TRADE_INFO)
    filtered_data = {}
    for market in K_MARKETS:

        df = scraper.collect(limit=50, market=market)
        filtered_data[market] = filter_data(data=df)
    
    print(filtered_data)

if __name__ == "__main__":

    main()