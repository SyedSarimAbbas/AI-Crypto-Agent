from api_client import FreeCryptoApiClient
import sys

def verify():
    print("Verifying CoinGecko API integration...")
    client = FreeCryptoApiClient()
    
    # Test with Bitcoin
    symbol = "BTC"
    print(f"Fetching price for {symbol}...")
    data = client.get_coin_price(symbol)
    
    if data and "price" in data:
        print(f"SUCCESS: {symbol} Price: ${data['price']}")
        print(f"Timestamp: {data['timestamp']}")
    else:
        print(f"FAILURE: Could not fetch price for {symbol}")
        if data and "source" in data:
             print(f"WARNING: Result came from Mock API: {data['source']}")

if __name__ == "__main__":
    verify()
