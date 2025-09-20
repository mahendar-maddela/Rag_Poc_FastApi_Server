from typing import Tuple
from io import BytesIO

class BaseExtractor:
    def extract(self, file_bytes: BytesIO) -> Tuple[str, str]:
        """
        Extract text and return (raw_text, file_type).
        Each extractor (PDF/Text/Word) will implement this.
        """
        raise NotImplementedError
