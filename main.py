from agent import CryptoAgent
import sys

def main():
    print("Initializing Crypto Agent...")
    print("Local Knowledge Base: Loaded")
    print("API Client: Ready (Mock Mode: " + str(CryptoAgent().api.use_mock) + ")")
    print("\nWelcome! specific queries I can answer:")
    print("- 'Tell me about Bitcoin'")
    print("- 'What is its price?'")
    print("- 'Price of Solana'")
    print("(Type 'exit' to quit)\n")

    agent = CryptoAgent()

    while True:
        try:
            user_input = input("User: ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            response = agent.process_query(user_input)
            print(f"Agent: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
