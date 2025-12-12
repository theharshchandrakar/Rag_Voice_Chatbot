# pipeline/ingest.py
import pytesseract
from PIL import Image
import os
import glob

# Configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def load_images_from_directory(directory_path: str, extensions=['.png', '.jpg', '.jpeg']):
    """Finds all image paths in the directory."""
    image_paths = []
    directory_path = os.path.normpath(directory_path)
    for ext in extensions:
        search_pattern = os.path.join(directory_path, f"*{ext}")
        image_paths.extend(glob.glob(search_pattern))
    return image_paths

def extract_text(image_path: str) -> str:
    """Performs OCR on a single image."""
    try:
        img = Image.open(image_path)
        custom_config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(img, config=custom_config)
    except Exception as e:
        print(f"[ERROR] processing {image_path}: {e}")
        return ""