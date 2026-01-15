import unittest
from agent import CryptoAgent
from knowledge_base import KnowledgeBase
import os

class TestCryptoAgent(unittest.TestCase):
    def setUp(self):
        # Use a temporary test file to avoid overwriting production KB
        self.test_kb_path = "test_crypto_kb.json"
        
        # Initialize agent but swap out the KB
        self.agent = CryptoAgent()
        self.agent.kb = KnowledgeBase(kb_path=self.test_kb_path)
        
        # Reset Test KB data
        self.agent.kb.data = {
            "BTC": {
                "coin": "Bitcoin",
                "symbol": "BTC",
                "launch_year": 2009,
                "consensus": "Proof of Work"
            }
        }
    
    def tearDown(self):
        # Clean up test file
        if os.path.exists(self.test_kb_path):
            os.remove(self.test_kb_path)
    
    def test_kb_hit_metadata(self):
        print("\n[Test] KB Hit Metadata")
        response = self.agent.process_query("Tell me about Bitcoin")
        print(f"Response: {response}")
        self.assertIn("Proof of Work", response)
        self.assertIn("Source: Knowledge Base", response)

    def test_context_resolution(self):
        print("\n[Test] Context Resolution")
        self.agent.process_query("Tell me about Bitcoin")
        response = self.agent.process_query("What is its price?")
        print(f"Response: {response}")
        self.assertIn("BTC", response) # Should mention BTC or price of it
        # Note: Might verify API fallback if price not in KB
        # Since I reset KB, price is missing, so it should hit API/Mock
        self.assertTrue("MockAPI" in response or "Source: FreeCryptoAPI" in response)

    def test_api_fallback_new_coin(self):
        print("\n[Test] API Fallback (New Coin)")
        response = self.agent.process_query("What is the price of Solana?")
        print(f"Response: {response}")
        self.assertIn("SOL", response)
        self.assertIn("Source: FreeCryptoAPI", response)
        # Verify it persisted to KB
        kb_check = self.agent.kb.get_coin_data("SOL")
        self.assertIsNotNone(kb_check)
        self.assertIn("last_price", kb_check)

    def test_rejection_policy(self):
        print("\n[Test] Rejection Policy")
        response = self.agent.process_query("Will Bitcoin go up next week?")
        print(f"Response: {response}")
        self.assertIn("I cannot answer hypothetical questions", response)

if __name__ == "__main__":
    unittest.main()
