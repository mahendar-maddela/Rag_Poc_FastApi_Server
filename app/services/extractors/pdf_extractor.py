# # app/services/extractors/pdf_extractor.py
# import pdfplumber
# import fitz
# import pytesseract
# from PIL import Image
# from io import BytesIO
# from .base_extractor import BaseExtractor


# this is text extraction from digital PDFs using pdfplumber and fitz
# class PdfExtractor(BaseExtractor):
#     def extract(self, file_bytes: BytesIO):
#         """Return extracted text and PDF type (Digital/Scanned)"""
#         def detect_pdf_type(pdf_bytes):
#             with pdfplumber.open(pdf_bytes) as pdf:
#                 for page in pdf.pages:
#                     if page.extract_text():
#                         return "Digital"
#             return "Scanned"

#         pdf_type = detect_pdf_type(file_bytes)
#         text = ""

#         if pdf_type == "Digital":
#             with pdfplumber.open(file_bytes) as pdf:
#                 for page in pdf.pages:
#                     text += page.extract_text() or ""
#         else:
#             doc = fitz.open(stream=file_bytes, filetype="pdf")
#             for i in range(len(doc)):
#                 page = doc.load_page(i)
#                 pix = page.get_pixmap()
#                 img = Image.open(BytesIO(pix.tobytes("png")))
#                 text += pytesseract.image_to_string(img)

#         return text, pdf_type

# this is skip pages in digital PDFs
# import pdfplumber
# import fitz
# import pytesseract
# from PIL import Image
# from io import BytesIO
# from typing import Optional, List
# from .base_extractor import BaseExtractor

# class PdfExtractor(BaseExtractor):
#     def __init__(self, skip_pages: Optional[List[int]] = None):
#         """
#         skip_pages: List of 1-based page numbers to skip
#         """
#         self.skip_pages = skip_pages or []

#     def extract(self, file_bytes: BytesIO):
#         """
#         Extract text from PDF.
#         Returns: (extracted_text, pdf_type)
#         pdf_type: 'Digital' or 'Scanned'
#         """
#         pdf_type = self._detect_pdf_type(file_bytes)
#         text = ""

#         if pdf_type == "Digital":
#             text = self._extract_digital_pdf(file_bytes)
#         else:
#             text = self._extract_scanned_pdf(file_bytes)

#         return text, pdf_type

#     def _detect_pdf_type(self, pdf_bytes: BytesIO) -> str:
#         """Detect if PDF is Digital or Scanned"""
#         with pdfplumber.open(pdf_bytes) as pdf:
#             for i, page in enumerate(pdf.pages, start=1):
#                 if i in self.skip_pages:
#                     continue
#                 if page.extract_text():
#                     return "Digital"
#         return "Scanned"

#     def _extract_digital_pdf(self, pdf_bytes: BytesIO) -> str:
#         """Extract text and tables from digital PDF"""
#         text = ""
#         with pdfplumber.open(pdf_bytes) as pdf:
#             for i, page in enumerate(pdf.pages, start=1):
#                 if i in self.skip_pages:
#                     continue

#                 # Extract text (headers, paragraphs)
#                 page_text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
#                 text += page_text + "\n"

#                 # Extract tables
#                 tables = page.extract_tables()
#                 for table in tables:
#                     for row in table:
#                         text += "\t".join([str(cell) if cell else "" for cell in row]) + "\n"
#         return text

#     def _extract_scanned_pdf(self, pdf_bytes: BytesIO) -> str:
#         """Extract text from scanned PDF using OCR"""
#         text = ""
#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")
#         for i in range(len(doc)):
#             if (i + 1) in self.skip_pages:  # fitz is 0-indexed
#                 continue

#             page = doc.load_page(i)
#             pix = page.get_pixmap()
#             img = Image.open(BytesIO(pix.tobytes("png")))

#             # OCR with layout preservation
#             custom_config = r'--oem 3 --psm 6'
#             text += pytesseract.image_to_string(img, config=custom_config) + "\n"

#         return text



# extracting the skip pages with morkdown and rich text

# app/services/extractors/pdf_extractor.py
# import pdfplumber
# import fitz
# import pytesseract
# from PIL import Image
# from io import BytesIO
# from typing import Optional, List
# from .base_extractor import BaseExtractor


# class PdfExtractor(BaseExtractor):
#     def __init__(self, skip_pages: Optional[List[int]] = None):
#         """
#         skip_pages: List of 1-based page numbers to skip
#         """
#         self.skip_pages = skip_pages or []

#     def extract(self, file_bytes: BytesIO):
#         """
#         Extract text from PDF and return markdown + rich text.
#         Returns: (markdown_text, rich_text, pdf_type)
#         """
#         pdf_type = self._detect_pdf_type(file_bytes)

#         if pdf_type == "Digital":
#             markdown_text, rich_text = self._extract_digital_pdf(file_bytes)
#         else:
#             markdown_text, rich_text = self._extract_scanned_pdf(file_bytes)

#         return markdown_text, rich_text, pdf_type

#     def _detect_pdf_type(self, pdf_bytes: BytesIO) -> str:
#         """Detect if PDF is Digital or Scanned"""
#         with pdfplumber.open(pdf_bytes) as pdf:
#             for i, page in enumerate(pdf.pages, start=1):
#                 if i in self.skip_pages:
#                     continue
#                 if page.extract_text():
#                     return "Digital"
#         return "Scanned"

#     def _extract_digital_pdf(self, pdf_bytes: BytesIO):
#         """Extract text, tables, and images from digital PDF into markdown + rich text"""
#         markdown = []
#         rich_text = []

#         with pdfplumber.open(pdf_bytes) as pdf:
#             for i, page in enumerate(pdf.pages, start=1):
#                 if i in self.skip_pages:
#                     continue

#                 # Add page heading
#                 markdown.append(f"# Page Number {i}\n")
#                 rich_text.append(f"=== Page Number {i} ===\n")

#                 # --- Extract normal text ---
#                 page_text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
#                 if page_text.strip():
#                     lines = page_text.splitlines()
#                     for line in lines:
#                         if line.isupper() or len(line.split()) <= 4:
#                             markdown.append(f"## {line.strip()}")
#                             rich_text.append(f"[HEADER] {line.strip()}")
#                         else:
#                             markdown.append(line.strip())
#                             rich_text.append(line.strip())
#                     markdown.append("\n")
#                     rich_text.append("\n")

#                 # --- Extract tables ---
#                 tables = page.extract_tables()
#                 for table in tables:
#                     markdown.append(self._format_table_markdown(table))
#                     rich_text.append(self._format_table_richtext(table))
#                     markdown.append("\n")
#                     rich_text.append("\n")

#                 # --- Add placeholder for images/diagrams ---
#                 # if page.images:
#                 #     for idx, _ in enumerate(page.images, start=1):
#                 #         markdown.append(f"![Image_Page{i}_{idx}](#)")
#                 #         rich_text.append(f"[Image_Page{i}_{idx}]")

#         return "\n".join(markdown), "\n".join(rich_text)

#     def _extract_scanned_pdf(self, pdf_bytes: BytesIO):
#         """Extract text + OCR images into markdown + rich text"""
#         markdown = []
#         rich_text = []

#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")
#         for i in range(len(doc)):
#             if (i + 1) in self.skip_pages:
#                 continue

#             # Add page heading
#             markdown.append(f"# Page Number {i+1}\n")
#             rich_text.append(f"=== Page Number {i+1} ===\n")

#             page = doc.load_page(i)
#             pix = page.get_pixmap()
#             img = Image.open(BytesIO(pix.tobytes("png")))

#             # OCR text
#             custom_config = r'--oem 3 --psm 6'
#             ocr_text = pytesseract.image_to_string(img, config=custom_config)

#             if ocr_text.strip():
#                 markdown.append(ocr_text.strip())
#                 rich_text.append(ocr_text.strip())

#             # Insert image placeholder
#             markdown.append(f"![Scanned_Page_{i+1}](#)")
#             rich_text.append(f"[Scanned_Page_{i+1}]")

#         return "\n".join(markdown), "\n".join(rich_text)

#     def _format_table_markdown(self, table):
#         """Convert extracted table into markdown table"""
#         if not table:
#             return ""
#         md = []
#         headers = table[0]
#         md.append("| " + " | ".join([h if h else "" for h in headers]) + " |")
#         md.append("| " + " | ".join(["---"] * len(headers)) + " |")
#         for row in table[1:]:
#             md.append("| " + " | ".join([str(c) if c else "" for c in row]) + " |")
#         return "\n".join(md)

#     def _format_table_richtext(self, table):
#         """Convert extracted table into simple rich text format"""
#         if not table:
#             return ""
#         rt = []
#         for row in table:
#             rt.append("\t".join([str(c) if c else "" for c in row]))
#         return "\n".join(rt)



import pdfplumber
import fitz
import pytesseract
from PIL import Image
from io import BytesIO
from typing import Optional, List
from .base_extractor import BaseExtractor
import yaml
import re

class PdfExtractor(BaseExtractor):
    def __init__(self, skip_pages: Optional[List[int]] = None, rules_path: str = "cleaning_rules.yml"):
        """
        skip_pages: List of 1-based page numbers to skip
        """
        self.skip_pages = skip_pages or []
        with open(rules_path, "r", encoding="utf-8") as f:
            self.cleaning_rules = yaml.safe_load(f)

    def extract(self, file_bytes: BytesIO):
        """
        Extract text from PDF and return markdown + rich text.
        Returns: (markdown_text, rich_text, pdf_type)
        """
        pdf_type = self._detect_pdf_type(file_bytes)
        
        if pdf_type == "Digital":
            markdown_text, rich_text = self._extract_digital_pdf(file_bytes)
        else:
            markdown_text, rich_text = self._extract_scanned_pdf(file_bytes)

        # Apply cleaning rules
        markdown_text = self._clean_text(markdown_text)
        rich_text = self._clean_text(rich_text)

        return markdown_text, rich_text, pdf_type

    def _detect_pdf_type(self, pdf_bytes: BytesIO) -> str:
        """Detect if PDF is Digital or Scanned"""
        with pdfplumber.open(pdf_bytes) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                if i in self.skip_pages:
                    continue
                if page.extract_text():
                    return "Digital"
        return "Scanned"

    def _extract_digital_pdf(self, pdf_bytes: BytesIO):
        """Extract text, tables, and images from digital PDF into markdown + rich text"""
        markdown = []
        rich_text = []
        normal_text = []

        with pdfplumber.open(pdf_bytes) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                if i in self.skip_pages:
                    continue

                # Add page heading
                markdown.append(f"# Page Number {i}\n")
                rich_text.append(f"=== Page Number {i} ===\n")

                # --- Extract normal text ---
                page_text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
                if page_text.strip():
                    lines = page_text.splitlines()
                    for line in lines:
                        if line.isupper() or len(line.split()) <= 4:
                            markdown.append(f"## {line.strip()}")
                            rich_text.append(f"[HEADER] {line.strip()}")
                        else:
                            markdown.append(line.strip())
                            rich_text.append(line.strip())
                    markdown.append("\n")
                    rich_text.append("\n")

                # --- Extract tables ---
                tables = page.extract_tables()
                for table in tables:
                    markdown.append(self._format_table_markdown(table))
                    rich_text.append(self._format_table_richtext(table))
                    markdown.append("\n")
                    rich_text.append("\n")

        return "\n".join(markdown), "\n".join(rich_text)

    def _extract_scanned_pdf(self, pdf_bytes: BytesIO):
        """Extract text + OCR images into markdown + rich text"""
        markdown = []
        rich_text = []

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for i in range(len(doc)):
            if (i + 1) in self.skip_pages:
                continue

            # Add page heading
            markdown.append(f"# Page Number {i+1}\n")
            rich_text.append(f"=== Page Number {i+1} ===\n")

            page = doc.load_page(i)
            pix = page.get_pixmap()
            img = Image.open(BytesIO(pix.tobytes("png")))

            # OCR text
            custom_config = r'--oem 3 --psm 6'
            ocr_text = pytesseract.image_to_string(img, config=custom_config)

            if ocr_text.strip():
                markdown.append(ocr_text.strip())
                rich_text.append(ocr_text.strip())

            # Insert image placeholder
            markdown.append(f"![Scanned_Page_{i+1}](#)")
            rich_text.append(f"[Scanned_Page_{i+1}]")

        return "\n".join(markdown), "\n".join(rich_text)

    def _format_table_markdown(self, table):
        """Convert extracted table into markdown table"""
        if not table:
            return ""
        md = []
        headers = table[0]
        md.append("| " + " | ".join([h if h else "" for h in headers]) + " |")
        md.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in table[1:]:
            md.append("| " + " | ".join([str(c) if c else "" for c in row]) + " |")
        return "\n".join(md)

    def _format_table_richtext(self, table):
        """Convert extracted table into simple rich text format"""
        if not table:
            return ""
        rt = []
        for row in table:
            rt.append("\t".join([str(c) if c else "" for c in row]))
        return "\n".join(rt)

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""

        # Iterate through all rule categories
        for category, rules in self.cleaning_rules.get("cleaning_rules", {}).items():
            for rule in rules:
                pattern = rule.get("pattern")
                replacement = rule.get("replacement", "")
                try:
                    text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
                except re.error as e:
                    print(f"[Warning] Invalid regex in {category}: {pattern} ({e})")

        return text.strip()
