from llm.llama_client import LlamaClient

def main():
    print("Initializing Jarvis...")
    llm = LlamaClient()
    
    print("Jarvis is ready! Type 'exit' to quit.")
    print("For now, just type your messages (we'll add voice later):")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
                
            response = llm.chat(user_input)
            print(f"Jarvis: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 