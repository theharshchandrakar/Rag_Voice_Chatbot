# app.py

import sys
import colorama
from colorama import Fore, Style
from pipeline.retrieval import query_collection
from pipeline.llm import generate_answer

# Initialize colorama for colored text
colorama.init(autoreset=True)

def main():
    print(Fore.CYAN + "\n🤖 --- RAG Voice Chatbot (Powered by Llama 3) ---")
    print(Fore.WHITE + "Type 'exit' to quit.\n")

    while True:
        try:
            # 1. Get User Question
            user_query = input(Fore.YELLOW + "You: " + Style.RESET_ALL)
            
            if user_query.lower() in ['exit', 'quit']:
                print(Fore.CYAN + "Goodbye!")
                break
            
            if not user_query.strip():
                continue

            print(Fore.CYAN + "🔍 Searching knowledge base...")

            # 2. Retrieve Context (Phase 2)
            # We get the top 5 chunks to give the LLM enough info
            results = query_collection(user_query, n_results=5)
            
            if not results:
                print(Fore.RED + "❌ No relevant information found in the database.")
                continue

            # Extract just the text content from the results
            context_chunks = [res['context'] for res in results]

            print(Fore.CYAN + "🧠 Thinking (Llama 3)...")

            # 3. Generate Answer (Phase 3)
            answer = generate_answer(user_query, context_chunks)

            # 4. Display Result
            print("\n" + Fore.GREEN + "🤖 AI: " + Style.RESET_ALL + answer)
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")

if __name__ == "__main__":
    main()