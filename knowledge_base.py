import json
import os
from typing import Optional, Dict, Any

class KnowledgeBase:
    def __init__(self, kb_path: str = "crypto_kb.json"):
        self.kb_path = kb_path
        self.data: Dict[str, Any] = self._load_kb()

    def _load_kb(self) -> Dict[str, Any]:
        if not os.path.exists(self.kb_path):
            return {}
        try:
            with open(self.kb_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding {self.kb_path}, starting with empty KB.")
            return {}

    def save_kb(self):
        with open(self.kb_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_coin_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        return self.data.get(symbol.upper())

    def update_coin_price(self, symbol: str, price: float, timestamp: str):
        symbol = symbol.upper()
        if symbol not in self.data:
            # If coin doesn't exist, we might create a partial record or error depending on policy.
            # For now, we'll create a partial record if we have an API hit.
            self.data[symbol] = {
                "symbol": symbol,
                "coin": symbol, # Default to symbol if name unknown
                "launch_year": None,
                "consensus": None
            }
        
        self.data[symbol]["last_price"] = price
        self.data[symbol]["price_timestamp"] = timestamp
        self.save_kb()

    def add_fresh_coin_data(self, symbol: str, data: Dict[str, Any]):
        """Adds or merges new data for a coin from API."""
        symbol = symbol.upper()
        if symbol not in self.data:
             self.data[symbol] = {}
        
        self.data[symbol].update(data)
        self.save_kb()
