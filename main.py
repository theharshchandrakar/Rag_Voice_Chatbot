# main.py
import os
from pathlib import Path
from pipeline.ingest import load_images_from_directory, extract_text
from pipeline.parsing import parse_document
from pipeline.chunking import chunk_text
from pipeline.embedding import generate_embeddings
from pipeline.storage import VectorDB # <--- NEW IMPORT

def main():
    # ... (Setup code remains the same) ...
    PROJECT_ROOT = Path(__file__).resolve().parent
    image_folder = PROJECT_ROOT / 'data' / 'images'
    image_folder_str = str(image_folder)

    # Initialize Vector DB
    print("Initializing Vector Database...")
    vector_db = VectorDB() # Creates the DB connection

    processed_pipeline_data = []

    print(f"\n--- STEP 1: Ingestion ---")
    image_files = load_images_from_directory(image_folder_str)

    for image_path in image_files:
        filename = os.path.basename(image_path)
        print(f"Processing: {filename}")
        
        # Ingest -> Parse -> Chunk -> Embed
        raw_text = extract_text(image_path)
        if not raw_text: continue
        
        structured_doc = parse_document(filename, raw_text)
        structured_doc["chunks"] = chunk_text(structured_doc["content"])
        
        if structured_doc["chunks"]:
            structured_doc["embeddings"] = generate_embeddings(structured_doc["chunks"])
            processed_pipeline_data.append(structured_doc)

    # --- STEP 5: Storage ---
    print("\n--- STEP 5: Storing to Vector DB ---")
    if processed_pipeline_data:
        vector_db.add_documents(processed_pipeline_data)
    else:
        print("No data to add.")

    print("\n--- Pipeline Complete ---")

if __name__ == "__main__":
    main()