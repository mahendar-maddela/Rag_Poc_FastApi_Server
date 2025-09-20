# app/services/extractors/pdf_extractor.py
import pdfplumber
import fitz
import pytesseract
from PIL import Image
from io import BytesIO
from .base_extractor import BaseExtractor

class PdfExtractor(BaseExtractor):
    def extract(self, file_bytes: BytesIO):
        """Return extracted text and PDF type (Digital/Scanned)"""
        def detect_pdf_type(pdf_bytes):
            with pdfplumber.open(pdf_bytes) as pdf:
                for page in pdf.pages:
                    if page.extract_text():
                        return "Digital"
            return "Scanned"

        pdf_type = detect_pdf_type(file_bytes)
        text = ""

        if pdf_type == "Digital":
            with pdfplumber.open(file_bytes) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        else:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for i in range(len(doc)):
                page = doc.load_page(i)
                pix = page.get_pixmap()
                img = Image.open(BytesIO(pix.tobytes("png")))
                text += pytesseract.image_to_string(img)

        return text, pdf_type
