import pytesseract
from pdf2image import convert_from_bytes
from pypdf import PdfReader

# Set your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ashut\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(file):
    """
    Extract text from a PDF using:
    1. Direct text extraction (pypdf)
    2. OCR fallback (pdf2image + pytesseract)
    """

    # Try direct extraction first
    try:
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        if text.strip():
            return text.strip()

    except Exception:
        pass  # fallback to OCR

    # OCR fallback
    try:
        file.seek(0)
        images = convert_from_bytes(file.read())

        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img, lang="eng") + "\n"

        return ocr_text.strip()

    except Exception as e:
        return f"OCR failed: {str(e)}"
