# app/services/extractors/text_extractor.py
from io import BytesIO
from .base_extractor import BaseExtractor

class TextExtractor(BaseExtractor):
    def extract(self, file_bytes: BytesIO):
        text = file_bytes.read().decode("utf-8")
        return text, "text"
