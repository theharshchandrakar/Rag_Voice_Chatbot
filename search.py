# search.py

import sys
from pipeline.retrieval import query_collection

def run_search_interface():
    """
    Interactive command-line interface for querying the vector database.
    """
    print("\n--- RAG Retrieval Interface (Phase 2) ---")
    print("Database: chroma_db | Model: all-MiniLM-L6-v2")
    print("Type 'exit' or 'quit' to end the session.")
    
    while True:
        try:
            # Get user input
            user_query = input("\nEnter your question > ")
            
            if user_query.lower() in ['exit', 'quit']:
                print("\nSession ended. Goodbye!")
                break
            
            if not user_query.strip():
                continue
            
            # --- 1. Call the Retrieval Logic ---
            print(f"Searching for '{user_query}'...")
            
            # Request the top 3 results from the database
            results = query_collection(user_query, n_results=3)

            # --- 2. Display the Results ---
            if results and results[0].get('error'):
                print(f"[CRITICAL ERROR] {results[0]['error']}")
                continue

            if not results:
                print("No relevant documents found in the database.")
            else:
                print("\n--- Retrieval Results (Top 3 Matches) ---")
                
                for i, result in enumerate(results):
                    # Distance: The lower the number, the closer the vector match (0 is perfect)
                    distance = result.get('distance', 'N/A')
                    source = result.get('source', 'N/A')
                    context = result.get('context', 'N/A')
                    
                    print(f"\n[{i+1}] Source: {source} | Similarity Score (Distance): {distance:.4f}")
                    print("-----------------------------------------------------------------")
                    print(context)
                    
        except KeyboardInterrupt:
            print("\nSession ended by user (Ctrl+C). Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            
if __name__ == "__main__":
    run_search_interface()