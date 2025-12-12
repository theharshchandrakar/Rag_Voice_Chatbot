# pipeline/chunking.py
from typing import List

def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> List[str]:
    """Splits text into overlapping word chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i : i + chunk_size]
        chunk_str = " ".join(chunk_words)
        if chunk_str:
            chunks.append(chunk_str)
    return chunks