# pipeline/storage.py
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any

class VectorDB:
    def __init__(self, collection_name: str = "rag_collection"):
        # Initialize the client to save data to a local folder named 'chroma_db'
        self.client = chromadb.PersistentClient(path="chroma_db")
        
        # Create or get the collection (like a table in SQL)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Adds processed documents (with embeddings) to the database.
        """
        if not documents:
            return

        ids = []
        embeddings = []
        metadatas = []
        documents_text = []

        # Loop through your structured data and prepare it for Chroma
        for doc in documents:
            # We need to flatten the data because Chroma stores 1 vector = 1 item
            for i, (chunk, vector) in enumerate(zip(doc["chunks"], doc["embeddings"])):
                
                # Create a unique ID for each chunk (e.g., "doc1_chunk0")
                chunk_id = f"{doc['metadata']['source']}_chunk{i}"
                
                ids.append(chunk_id)
                embeddings.append(vector)
                documents_text.append(chunk)
                metadatas.append(doc["metadata"])

        # Add everything to the database in one go
        if ids:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents_text
            )
            print(f"Successfully added {len(ids)} chunks to ChromaDB.")

    def query(self, query_text: str, n_results: int = 3):
        """
        Searches the database for the most similar chunks.
        Note: We usually need to embed the query first, but Chroma 
        can handle raw text if we set it up with an embedding function.
        For now, we will assume we pass embeddings manually or let Chroma handle it.
        """
        # (We will implement the search logic in the next step!)
        pass