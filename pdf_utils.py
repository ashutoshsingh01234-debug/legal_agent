import fitz  # PyMuPDF
import easyocr
from io import BytesIO

# Minimum characters required for valid text extraction
MIN_TEXT_LENGTH = 50

# Initialize OCR reader (lazy loading - will be created on first use)
ocr_reader = None


def get_ocr_reader():
    """Lazy load OCR reader to avoid memory issues on startup"""
    global ocr_reader
    if ocr_reader is None:
        ocr_reader = easyocr.Reader(['en'], verbose=False)
    return ocr_reader


def extract_text_from_pdf(file, use_ocr_first=False):
    """
    Extract text from a PDF using multiple strategies:
    1. PyMuPDF (fitz) - Fast, reliable text extraction from text-based PDFs
    2. EasyOCR - Modern OCR for scanned PDFs (pure Python, no system dependencies)

    Args:
        file: PDF file object
        use_ocr_first: If True, skip text extraction and go straight to OCR (for image PDFs)

    Returns:
        dict with keys:
            - 'success': bool indicating if extraction succeeded
            - 'text': extracted text or None
            - 'method': 'fitz', 'ocr', or None
            - 'error': error message if failed
    """

    # Strategy 1: Try PyMuPDF (fitz) first for text extraction
    if not use_ocr_first:
        try:
            file.seek(0)
            pdf_bytes = BytesIO(file.read())
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

            text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                # Extract text with layout preservation
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"

            text = text.strip()
            pdf_document.close()

            if len(text) >= MIN_TEXT_LENGTH:
                return {
                    'success': True,
                    'text': text,
                    'method': 'fitz',
                    'error': None
                }
            # If very little text was extracted, suggest OCR
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
    if use_ocr_first:
        try:
            file.seek(0)
            pdf_bytes = BytesIO(file.read())
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

            ocr_text = ""
            reader = get_ocr_reader()

            # Process each page with OCR
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                # Render page to image at high DPI for better OCR
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better accuracy
                image_data = pix.tobytes("ppm")

                # Run OCR on the page image
                try:
                    result = reader.readtext(pix.tobytes("ppm"), detail=0)
                    if result:
                        page_text = "\n".join(result)
                        if page_text.strip():
                            ocr_text += page_text + "\n"
                except Exception as ocr_error:
                    # Single page OCR failed, continue with next page
                    continue

            ocr_text = ocr_text.strip()
            pdf_document.close()

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
            return {
                'success': False,
                'text': None,
                'method': None,
                'error': f'Error processing PDF with OCR: {str(e)}\n\nPlease try uploading a different file or use manual text input.'
            }
