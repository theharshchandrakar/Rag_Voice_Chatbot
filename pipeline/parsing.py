# pipeline/parsing.py
import os
import datetime
from typing import Dict, Any

def parse_document(filename: str, raw_text: str) -> Dict[str, Any]:
    """Wraps raw text into a structured dictionary."""
    clean_text = raw_text.strip()
    return {
        "metadata": {
            "source": filename,
            "file_type": os.path.splitext(filename)[1],
            "created_at": datetime.datetime.now().isoformat(),
            "char_count": len(clean_text)
        },
        "content": clean_text
    }