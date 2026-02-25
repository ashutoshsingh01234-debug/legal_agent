import fitz  # PyMuPDF
import easyocr
from io import BytesIO
import streamlit as st

# Minimum characters required for valid text extraction
MIN_TEXT_LENGTH = 50


# ---------------------------------------------------------
# CACHED OCR LOADER (loads only once in Streamlit)
# ---------------------------------------------------------
@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(['en'], verbose=False)


# ---------------------------------------------------------
# MAIN EXTRACTION FUNCTION
# ---------------------------------------------------------
def extract_text_from_pdf(file, use_ocr_first=False):
    """
    Extract text from a PDF using:
    1. PyMuPDF (fast for text-based PDFs)
    2. EasyOCR (for scanned PDFs)

    Args:
        file: Uploaded file object from Streamlit
        use_ocr_first: Force OCR even if text exists

    Returns:
        dict: { success, text, method, error }
    """

    # Read PDF once
    try:
        file.seek(0)
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        return {
            'success': False,
            'text': None,
            'method': None,
            'error': f'Could not read PDF: {str(e)}'
        }

    # ---------------------------------------------------------
    # STRATEGY 1: PyMuPDF TEXT EXTRACTION
    # ---------------------------------------------------------
    if not use_ocr_first:
        try:
            text_chunks = []

            for page in pdf_document:
                page_text = page.get_text()
                if page_text:
                    text_chunks.append(page_text)

            extracted_text = "\n".join(text_chunks).strip()

            if len(extracted_text) >= MIN_TEXT_LENGTH:
                return {
                    'success': True,
                    'text': extracted_text,
                    'method': 'fitz',
                    'error': None
                }

            elif len(extracted_text) > 0:
                return {
                    'success': False,
                    'text': None,
                    'method': None,
                    'error': 'Very little text extracted. Try enabling OCR.'
                }

            else:
                return {
                    'success': False,
                    'text': None,
                    'method': None,
                    'error': 'No text extracted. Try enabling OCR.'
                }

        except Exception as e:
            return {
                'success': False,
                'text': None,
                'method': None,
                'error': f'Error extracting text: {str(e)}'
            }

    # ---------------------------------------------------------
    # STRATEGY 2: OCR EXTRACTION
    # ---------------------------------------------------------
    try:
        reader = get_ocr_reader()
        ocr_text_chunks = []

        for page in pdf_document:
            # Lower DPI for faster OCR (1.3x is optimal)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3))
            img_bytes = pix.tobytes("ppm")

            result = reader.readtext(img_bytes, detail=0)
            if result:
                ocr_text_chunks.append("\n".join(result))

        final_text = "\n".join(ocr_text_chunks).strip()

        if len(final_text) >= MIN_TEXT_LENGTH:
            return {
                'success': True,
                'text': final_text,
                'method': 'ocr',
                'error': None
            }

        return {
            'success': False,
            'text': None,
            'method': None,
            'error': 'OCR extracted very little text.'
        }

    except Exception as e:
        return {
            'success': False,
            'text': None,
            'method': None,
            'error': f'OCR error: {str(e)}'
        }