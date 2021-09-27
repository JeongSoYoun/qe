import api_key as key
import pyupbit as upbit
import rsi as get_rsi
import bolinger
import read_data as read
import time
import base_model as base 

def main():

    coin_list = read.coin_list()
    interval = "day"
    count = 200
    to = None

    for coin in coin_list: 

        time.sleep(1)
        df = read.coin_data(coin, interval, count, to)

        rsi = get_rsi.relative_strength(14, count, df)
        bolinger_df = bolinger.calculate_band(20, df)

        last_index = str(df.index[count-1])

        change = base.get_diff(df,coin,interval,count,to,last_index)
        price_change = change[0]
        volume_change = change[1]

        print(coin, "->" , base.price(coin), "KRW / " \
            "Price Change:", price_change,"% ", "Volume_Change:", volume_change,"%")
        
        print("RSI: ", rsi)

        if bolinger.signal(count,bolinger_df) == "sell" and rsi > 70:

            print("SELL SIGNAL!", coin)

        elif bolinger.signal(count,bolinger_df) == "buy" and rsi < 30:

            print("BUY SIGNAL!", coin)




if __name__ == '__main__':

    main()