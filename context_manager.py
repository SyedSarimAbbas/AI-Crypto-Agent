from typing import List, Dict, Optional
import re

class ContextManager:
    def __init__(self, history_limit: int = 10):
        self.history: List[Dict[str, str]] = []
        self.history_limit = history_limit
        self.last_mentioned_symbol: Optional[str] = None
        # Common crypto symbols for simple detection
        self.known_symbols = {"BTC", "ETH", "SOL", "ADA", "XRP", "DOGE", "DOT", "USDT", "USDC"}

    def add_turn(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.history_limit:
            self.history.pop(0)
        
        # Update last mentioned symbol if found in user content
        found = self._extract_symbol(content)
        if found:
            self.last_mentioned_symbol = found

    def _extract_symbol(self, text: str) -> Optional[str]:
        # Very basic extraction: look for known symbols or full names
        # In a real app, use a more robust NER or mapping
        text_upper = text.upper()
        
        # Direct symbol match ??
        for word in text_upper.split():
            clean_word = word.strip(".,?!")
            if clean_word in self.known_symbols:
                return clean_word
        
        # Name mapping
        name_map = {
            "BITCOIN": "BTC",
            "ETHEREUM": "ETH",
            "SOLANA": "SOL",
            "CARDANO": "ADA",
            "RIPPLE": "XRP",
            "DOGECOIN": "DOGE"
        }
        
        for name, symbol in name_map.items():
            if name in text_upper:
                return symbol
        
        return None

    def resolve_entity(self, text: str) -> Optional[str]:
        """
        Returns the symbol mentioned in the text, or the last mentioned symbol
        if the text contains pronouns like 'it', 'this', 'that'.
        """
        current_symbol = self._extract_symbol(text)
        if current_symbol:
            return current_symbol
        
        # Pronoun resolution
        text_lower = text.lower()
        if any(pronoun in text_lower.split() for pronoun in ["it", "this", "that", "its"]):
            return self.last_mentioned_symbol
        
        return None
