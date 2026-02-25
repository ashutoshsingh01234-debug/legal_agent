import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from pypdf import PdfReader

# Set your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ashut\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Minimum characters required for valid text extraction
MIN_TEXT_LENGTH = 50  # Lowered for scanned PDFs which may have less structured text


def extract_text_from_pdf(file, use_ocr_first=False):
    """
    Extract text from a PDF using multiple strategies:
    1. pdfplumber (pure Python, works everywhere - for text-based PDFs)
    2. OCR fallback (pdf2image + pytesseract - for scanned PDFs, only if explicitly requested)

    Args:
        file: PDF file object
        use_ocr_first: If True, skip pdfplumber and go straight to OCR (useful for known scanned documents)

    Returns:
        dict with keys:
            - 'success': bool indicating if extraction succeeded
            - 'text': extracted text or None
            - 'method': 'pdfplumber', 'ocr', or None
            - 'error': error message if failed
    """

    # Strategy 1: Try pdfplumber first (pure Python solution, works everywhere)
    if not use_ocr_first:
        try:
            file.seek(0)
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

                text = text.strip()
                if len(text) >= MIN_TEXT_LENGTH:
                    return {
                        'success': True,
                        'text': text,
                        'method': 'pdfplumber',
                        'error': None
                    }
                # If pdfplumber extracted very little text and user didn't request OCR,
                # return error suggesting they check the OCR checkbox
                elif len(text) > 0:
                    return {
                        'success': False,
                        'text': None,
                        'method': None,
                        'error': 'Very little text was extracted. This might be a scanned PDF.\n\n'
                                'Try checking the "Force OCR processing" checkbox to extract text from scanned documents.'
                    }
                else:
                    # No text extracted at all
                    return {
                        'success': False,
                        'text': None,
                        'method': None,
                        'error': 'No text could be extracted from the PDF using standard methods.\n\n'
                                'If this is a scanned PDF, try checking the "Force OCR processing" checkbox.\n'
                                'Otherwise, the PDF may be corrupted or empty.'
                    }

        except Exception as e:
            return {
                'success': False,
                'text': None,
                'method': None,
                'error': f'Could not read PDF file: {str(e)}\n\nPlease check that the file is a valid PDF.'
            }

    # Strategy 2: OCR for scanned images (only if explicitly requested via use_ocr_first=True)
    try:
        file.seek(0)
        images = convert_from_bytes(file.read(), dpi=300)  # Higher DPI for better OCR accuracy

        ocr_text = ""
        for page_num, img in enumerate(images):
            # Apply OCR with English language support
            # For Indian legal documents, you could add 'hin' for Hindi if needed
            page_text = pytesseract.image_to_string(img, lang="eng")

            if page_text.strip():
                ocr_text += page_text + "\n"

        ocr_text = ocr_text.strip()

        if len(ocr_text) >= MIN_TEXT_LENGTH:
            return {
                'success': True,
                'text': ocr_text,
                'method': 'ocr',
                'error': None
            }
        else:
            # OCR extracted very little text
            return {
                'success': False,
                'text': None,
                'method': None,
                'error': 'The PDF appears to be empty or could not be processed with OCR.\n\n'
                        'Please check:\n'
                        '- The PDF is not corrupted\n'
                        '- The PDF contains readable content\n'
                        '- Try uploading a different file'
            }

    except Exception as e:
        error_msg = str(e).lower()

        # Provide specific error message based on exception type
        if 'poppler' in error_msg or 'page count' in error_msg:
            return {
                'success': False,
                'text': None,
                'method': None,
                'error': 'Poppler is not installed, which is required for OCR processing.\n\n'
                        'To use OCR for scanned PDFs:\n\n'
                        '**Option A (Recommended):** Install via Chocolatey:\n'
                        '`choco install poppler`\n\n'
                        '**Option B (Manual):** Download from:\n'
                        'https://github.com/oschwartz10612/poppler-windows/releases/\n'
                        'Extract and add to Windows PATH.\n\n'
                        'After installing, restart your IDE and try again.'
            }
        elif 'tesseract' in error_msg or 'tesseract is not installed' in error_msg:
            return {
                'success': False,
                'text': None,
                'method': None,
                'error': 'OCR engine (Tesseract) is not properly installed. '
                        'Please reinstall from: https://github.com/UB-Mannheim/tesseract/wiki'
            }
        else:
            return {
                'success': False,
                'text': None,
                'method': None,
                'error': f'Error processing PDF: {str(e)}'
            }


