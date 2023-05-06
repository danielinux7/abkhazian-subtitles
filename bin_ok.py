import json

# Load the JSON data for Binance and OKEx
with open('binance.json', 'r') as f:
    binance_data = json.load(f)
with open('okex.json', 'r') as f:
    okex_data = json.load(f)

# Create a dictionary to store the prices of each trading pair
prices = {}
for ticker in binance_data:
    symbol = ticker['symbol']
    price = float(ticker['price'])
    prices[symbol] = {'binance': price}
for ticker in okex_data:
    symbol = ticker['symbol']
    price = float(ticker['price'])
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
