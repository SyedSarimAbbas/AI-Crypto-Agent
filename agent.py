import time
from typing import Dict, Any, Tuple
from knowledge_base import KnowledgeBase
from api_client import FreeCryptoApiClient
from context_manager import ContextManager

class CryptoAgent:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.api = FreeCryptoApiClient()
        self.context = ContextManager()
        
    def process_query(self, user_input: str) -> str:
        """
        Main pipeline:
        1. Context update & Entity Resolution
        2. Intent Detection
        3. KB Check
        4. API Fallback
        5. Response Generation
        """
        
        # 1. Entity Resolution
        symbol = self.context.resolve_entity(user_input)
        
        # 2. Intent Detection (Keyword based)
        intent = self._detect_intent(user_input)
        
        if intent == "unknown":
             return "I'm sorry, I can only provide crypto prices and metadata. I cannot answer hypothetical questions or give investment advice."
        
        if not symbol:
             return "I'm not sure which cryptocurrency you are asking about. Could you specify the name or symbol?"

        # 3. KB Check
        kb_data = self.kb.get_coin_data(symbol)
        
        response_text = ""
        source = "Knowledge Base"
        
        # Check if we need price and if it's fresh
        if intent == "price":
            price_needed = True
            is_fresh = False
            if kb_data and kb_data.get("last_price"):
                 # Check freshness (e.g., 5 mins)
                 last_ts = kb_data.get("price_timestamp")
                 # Parsing timestamp is complex without dateutil, skipping exact logic for now
                 # and assuming "Always check API if user asks for price ?? Or just trust KB?"
                 # Requirement says: "Data is stale (older than configured freshness threshold)"
                 # Let's say if it exists, we treat it as potentially stale.
                 # For simplicity in this demo: Always try API for price if asked, to demonstrate fallback.
                 # Wait, requirement: "Data is missing... OR stale".
                 # Let's check API first if we want the LATEST price.
                 pass
            
            # Try API if price requested
            api_data = self.api.get_coin_price(symbol)
            if api_data:
                # Update KB
                self.kb.update_coin_price(symbol, api_data["price"], api_data["timestamp"])
                kb_data = self.kb.get_coin_data(symbol) # Reload
                source = "FreeCryptoAPI"
            elif not kb_data or not kb_data.get("last_price"):
                 return "INSUFFICIENT DATA – Not found in Knowledge Base or API"
            
            price = kb_data.get("last_price")
            response_text = f"The price of {symbol} is ${price}."

        elif intent == "metadata":
             if not kb_data:
                  # Try API metadata (simulated by price call which might return basics, or fail)
                  # If we only have price API, we can't get metadata.
                  # But the requirement says "Coin metadata (via Knowledge Base)".
                  # If not in KB, we fail unless API gives it.
                  # My API client only gives Price.
                  # So we fail if not in KB.
                  return "INSUFFICIENT DATA – Metadata not found in Knowledge Base."
             
             consensus = kb_data.get("consensus", "Unknown")
             launch = kb_data.get("launch_year", "Unknown")
             response_text = f"{symbol} ({kb_data.get('coin')}) was launched in {launch} and uses {consensus} consensus."
        
        # 4. Final strict check
        if not response_text:
             return "INSUFFICIENT DATA – Not found in Knowledge Base or API"
        
        # 5. Hallucination Guard / Source Attribution
        final_response = f"{response_text} [Source: {source}]"
        
        # Update context history
        self.context.add_turn("user", user_input)
        self.context.add_turn("assistant", final_response)
        
        return final_response

    def _detect_intent(self, text: str) -> str:
        text_lower = text.lower()
        if any(x in text_lower for x in ["price", "worth", "value", "cost", "how much"]):
            return "price"
        if any(x in text_lower for x in ["metadata", "consensus", "launch", "year", "what is", "tell me about", "who is"]):
            return "metadata"
        # Explicit policy rejection
        if any(x in text_lower for x in ["prediction", "invest", "buy", "sell", "future", "will", "go up", "next week", "should i"]):
            return "unknown"
        
        # Default to metadata if entity found
        return "metadata"
