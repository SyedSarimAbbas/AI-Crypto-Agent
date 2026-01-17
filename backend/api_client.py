import os
import requests
import random
import time
import re
from typing import Optional, Dict, Any

class FreeCryptoApiClient:
    BASE_URL = "https://api.coincap.io/v2/assets" # Fallback/Legacy
    COINGECKO_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = None # CoinGecko free tier needs no key
        self.use_mock = False
        self.id_cache = {} # Cache symbol -> coin_id mapping
        print(f"[System] Initialized FreeCryptoApiClient (Provider: CoinGecko)")

    def get_coin_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetches the current price of a coin using CoinGecko API.
        """
        if self.use_mock:
            return self._mock_get_price(symbol)
        
        # Real API Implementation
        data = self._real_get_price(symbol)
        if not data:
             print(f"[API] Fallback to mock for {symbol}")
             return self._mock_get_price(symbol)
        return data

    def _get_coin_id(self, symbol: str) -> Optional[str]:
        """Resolves a symbol (e.g. BTC) to CoinGecko ID (e.g. bitcoin)"""
        if symbol.upper() in self.id_cache:
            return self.id_cache[symbol.upper()]
            
        try:
            # Search for the coin
            response = requests.get(
                f"{self.COINGECKO_URL}/search", 
                params={"query": symbol},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            for coin in data.get("coins", []):
                if coin["symbol"].upper() == symbol.upper():
                    # Found exact match
                    self.id_cache[symbol.upper()] = coin["id"]
                    return coin["id"]
            return None
        except Exception as e:
            print(f"[API Error] Failed to resolve ID for {symbol}: {e}")
            return None

    def _real_get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        try:
            coin_id = self._get_coin_id(symbol)
            if not coin_id:
                print(f"[API] Could not resolve CoinGecko ID for {symbol}")
                return None

            response = requests.get(
                f"{self.COINGECKO_URL}/simple/price", 
                params={
                    "ids": coin_id,
                    "vs_currencies": "usd"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if coin_id not in data:
                return None
                
            price = data[coin_id].get("usd")
            
            if price is None:
                return None

            return {
                "symbol": symbol.upper(),
                "price": float(price),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        except Exception as e:
            print(f"[API Error] Failed to fetch price for {symbol}: {e}")
            return None

    def _mock_get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Simulates an API response."""
        time.sleep(0.5)

        known_mocks = {
            "BTC": 43500.00,
            "ETH": 2300.00,
            "SOL": 95.00,
            "ADA": 0.55,
            "XRP": 0.60,
            "DOGE": 0.08
        }

        symbol_upper = symbol.upper()
        
        if symbol_upper in known_mocks:
            base_price = known_mocks[symbol_upper]
        else:
            seed = sum(ord(c) for c in symbol_upper)
            random.seed(seed)
            base_price = random.uniform(0.1, 1000.0)
            random.seed() 

        variation = base_price * random.uniform(-0.02, 0.02)
        price = base_price + variation
        return {
            "symbol": symbol_upper,
            "price": round(price, 2),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source": "MockAPI (Estimate)"
        }

    def get_coin_metadata(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetches metadata (description) for a coin using CoinGecko API.
        """
        coin_id = self._get_coin_id(symbol)
        if not coin_id:
            return None

        try:
            url = f"{self.COINGECKO_URL}/coins/{coin_id}"
            params = {
                "localization": "false",
                "tickers": "false",
                "market_data": "false",
                "community_data": "false",
                "developer_data": "false",
                "sparkline": "false"
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            description = data.get("description", {}).get("en", "")
            clean_desc = self._clean_html(description)
            
            # Get first paragraph or first 500 chars
            if "\n" in clean_desc:
                clean_desc = clean_desc.split("\n")[0]
            
            if len(clean_desc) > 500:
                clean_desc = clean_desc[:497] + "..."

            return {
                "description": clean_desc,
                "founders": [] # CoinGecko doesn't easily provide a structured founder list in simple calls
            }
        except Exception as e:
            print(f"[API Error] Failed to fetch metadata for {symbol}: {e}")
            return None

    def _clean_html(self, raw_html: str) -> str:
        """Removes HTML tags from a string."""
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
