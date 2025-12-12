# pipeline/retrieval.py

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

# --- Configuration ---
# NOTE: This must use the exact same model name as pipeline/embedding.py
# If the models mismatch, the vectors will not be comparable!
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "rag_collection"

# --- Initialization ---
# Load the embedding model (used to convert the user's question into a vector)
try:
    print(f"Loading Embedding Model: {EMBEDDING_MODEL_NAME}")
    query_embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
except Exception as e:
    print(f"[ERROR] Could not load SentenceTransformer: {e}")
    # Setting to None will prevent the functions from running
    query_embedder = None


def query_collection(query_text: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """
    Connects to ChromaDB, embeds the query, and performs a semantic search.
    
    :param query_text: The user's question.
    :param n_results: The number of top-k results to return.
    :return: A list of dictionaries containing the relevant context chunks.
    """
    if not query_embedder:
        return [{"error": "Embedding model failed to load. Cannot perform search."}]
    
    # 1. Connect to the Existing ChromaDB
    try:
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        print(f"[ERROR] Could not connect to ChromaDB: {e}")
        return [{"error": "Database connection failed."}]

    # 2. Embed the Query
    # Convert the user's question into a vector using the same model
    query_vector = query_embedder.encode(query_text).tolist()

    # 3. Perform the Semantic Search
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results,
        include=['documents', 'metadatas', 'distances']
    )
    
    # 4. Format the Output
    # Chroma returns data in a nested, confusing structure (list of lists).
    # We flatten it into a clean list of dictionaries for easier use in the next phase.
    
    formatted_results = []
    
    if results and results.get('documents') and results['documents'][0]:
        
        # We only need the first result list [0], as we only sent one query vector
        
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        
        for doc, meta, dist in zip(documents, metadatas, distances):
            formatted_results.append({
                "context": doc,
                "source": meta.get('source', 'Unknown'),
                "distance": dist  # Lower distance means better match (0 is perfect)
            })

    return formatted_results