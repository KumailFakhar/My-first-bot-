import time
import requests
import pandas as pd

# Binance se live price lene ka free tareeqa
def get_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    data = requests.get(url).json()
    return float(data['price'])

print("Bot Start ho gaya... (CTRL+C se band hoga)\n")

prices = []

while True:
    try:
        price = get_price()
        prices.append(price)
        
        # List ko DataFrame me badlo
        df = pd.DataFrame(prices, columns=['price'])
        
        # 2 Moving Average banao
        df['short_avg'] = df['price'].rolling(5).mean()  # 5 price ka average
        df['long_avg'] = df['price'].rolling(20).mean() # 20 price ka average

        if len(prices) > 20:
            short = df['short_avg'].iloc[-1]
            long = df['long_avg'].iloc[-1]

            print(f"Price: {price} | Short Avg: {short:.2f} | Long Avg: {long:.2f}", end=" -> ")

            if short > long:
                print("🟢 BUY Signal")
            else:
                print("🔴 SELL Signal")
        else:
            print(f"Price: {price} - Data jama ho raha hai... {len(prices)}/20")

        time.sleep(3) # har 3 second baad price check

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
