import requests
import time

def test_coingecko():
    print("Testing CoinGecko API...")
    symbol = "BTC"
    
    # Step 1: Search for ID
    search_url = "https://api.coingecko.com/api/v3/search"
    print(f"Searching for {symbol}...")
    try:
        resp = requests.get(search_url, params={"query": symbol}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        found_coin = None
        for coin in data.get("coins", []):
            if coin["symbol"].upper() == symbol:
                found_coin = coin
                break
        
        if not found_coin:
            print("Could not find coin ID.")
            return

        coin_id = found_coin["id"]
        print(f"Found ID: {coin_id}")
        
        # Step 2: Get Price
        price_url = "https://api.coingecko.com/api/v3/simple/price"
        print(f"Fetching price for {coin_id}...")
        resp = requests.get(price_url, params={"ids": coin_id, "vs_currencies": "usd"}, timeout=10)
        resp.raise_for_status()
        price_data = resp.json()
        
        price = price_data.get(coin_id, {}).get("usd")
        print(f"Price: ${price}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_coingecko()
