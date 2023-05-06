import requests

# Make API requests for ticker data
binance_url = 'https://api.binance.com/api/v3/ticker/price'
okex_url = 'https://www.okex.com/api/v5/market/tickers?instType=SPOT'
while True:
    try:
        binance_response = requests.get(binance_url)
        okex_response = requests.get(okex_url)
        break
    except requests.exceptions.RequestException as e:
        print(f"Failed to get data. {str(e)}. Retrying in 5 seconds...")
binance_data = binance_response.json()
okex_data = okex_response.json()

# Create a dictionary to store the prices of each trading pair
prices = {}
for ticker in binance_data:
    symbol = ticker['symbol']
    price = float(ticker['price'])
    prices[symbol] = {'binance': price}
for ticker in okex_data['data']:
    symbol = ticker['instId'].replace('-', '')
    price = float(ticker['last'])
    if symbol in prices:
      prices[symbol]['okex'] = price

# Iterate over all possible pairs and find profitable spreads
text = ""
for pair in prices.keys():
    if 'okex' in prices[pair] and 'binance' in prices[pair]:
        okex_price = prices[pair]['okex']
        binance_price = prices[pair]['binance']
        spread = abs(round(okex_price - binance_price, 2))
        if spread > 1:
            text += pair+": OKEx = "+str(okex_price)+", Binance = "+str(binance_price)+", spread = "+str(spread)+"\n"
print(text)
