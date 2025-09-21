# # app/services/file_processor.py
# import requests
# import markdownify
# from io import BytesIO
# from .extractors.pdf_extractor import PdfExtractor
# from .extractors.text_extractor import TextExtractor
# from app.services.storage_db_service import StorageService

# class FileProcessor:
#     def __init__(self, file_id: str, file_url: str, file_type: str):
#         self.file_id = file_id
#         self.file_url = file_url
#         self.file_type = file_type.lower()
#         self.storage = StorageService()

#     def _download_file(self) -> BytesIO:
#         response = requests.get(self.file_url)
#         if response.status_code != 200:
#             raise ValueError("Failed to download file")
#         return BytesIO(response.content)

#     def _get_extractor(self):
#         if self.file_type == "application/pdf":
#             return PdfExtractor()
#         elif self.file_type == "text":
#             return TextExtractor()
#         else:
#             raise ValueError(f"Unsupported file type: {self.file_type}")

#     def process_file(self) -> dict:
#         file_bytes = self._download_file()
#         extractor = self._get_extractor()

#         # Extract text
#         text_content, detected_type = extractor.extract(file_bytes)

#         # Convert to Markdown
#         md_content = markdownify.markdownify(text_content, heading_style="ATX")

#         # Upload files and get public URLs
#         rich_url = self.storage.upload(text_content, f"{self.file_id}_richtext.txt")
#         md_url = self.storage.upload(md_content, f"{self.file_id}_extracted.md")

#         # Update DB
#         self.storage.update_file_links(self.file_id, rich_url, md_url,md_content)

#         return {
#             "file_id": self.file_id,
#             "file_type": detected_type,
#             "extracted_richtext_link": rich_url,
#             "extracted_markdown_link": md_url
#         }


import requests
import markdownify
from io import BytesIO
from .extractors.pdf_extractor import PdfExtractor
from .extractors.text_extractor import TextExtractor
from app.services.storage_db_service import StorageService
from typing import Optional,List


class FileProcessor:
    def __init__(self, file_id: str, file_url: str, file_type: str, skip_pages: Optional[List[int]] = None):
        self.file_id = file_id
        self.file_url = file_url
        self.file_type = file_type.lower()
        self.skip_pages = skip_pages or []
        self.storage = StorageService()

    def _download_file(self) -> BytesIO:
        response = requests.get(self.file_url)
        if response.status_code != 200:
            raise ValueError("Failed to download file")
        return BytesIO(response.content)

    def _get_extractor(self):
        if self.file_type == "application/pdf":
            return PdfExtractor(skip_pages=self.skip_pages)
        elif self.file_type == "text":
            return TextExtractor()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

    def process_file(self) -> dict:
        file_bytes = self._download_file()
        extractor = self._get_extractor()

        # Extract text
        # text_content, rich_text = extractor.extract(file_bytes)
        markdown_text, rich_text, detected_type = extractor.extract(file_bytes)

        # Convert to Markdown
        md_content = markdownify.markdownify(markdown_text, heading_style="ATX")

        # Upload files and get public URLs
        rich_url = self.storage.upload(rich_text, f"{self.file_id}_richtext.txt")
        md_url = self.storage.upload(md_content, f"{self.file_id}_extracted.md")

        # Update DB
        self.storage.update_file_links(self.file_id, rich_url, md_url,md_content ,rich_text)

        return {
            "file_id": self.file_id,
            "file_type": detected_type,
            "extracted_richtext_link": rich_url,
            "extracted_markdown_link": md_url
        }


