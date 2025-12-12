# pipeline/embedding.py
from sentence_transformers import SentenceTransformer
from typing import List

# Load model once when this module is imported
print("Loading Embedding Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    """Converts text chunks to vectors."""
    if not chunks:
        return []
    vectors = model.encode(chunks)
    return [v.tolist() for v in vectors]