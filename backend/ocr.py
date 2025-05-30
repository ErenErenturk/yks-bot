# ocr.py
from PIL import Image
import pytesseract

# Windows kullanıyorsan burayı set etmen gerekebilir:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image: Image.Image, lang: str = "tur") -> str:
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        return f"OCR hata: {str(e)}"
