from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain.schema import Document
import requests
import logging


class ChunkService:
    """
    Service to fetch Markdown files and split them into structured or hybrid chunks.
    Supports:
        - Structural chunking (by headers)
        - Hybrid chunking (structural + fixed-size chunks with overlap)
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize chunk service.
        Args:
            chunk_size (int): Maximum number of characters per chunk.
            overlap (int): Number of overlapping characters between chunks.
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def fetch_markdown(self, md_url: str) -> str:
        """
        Fetch markdown content from a URL.
        Args:
            md_url (str): URL of the Markdown file.
        Returns:
            str: Markdown text content.
        """
        try:
            response = requests.get(md_url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch Markdown from {md_url}: {e}")
            raise RuntimeError(f"Error fetching Markdown: {e}")

    def structural_chunking(self, markdown_text: str) -> List[Document]:
        """
        Structural chunking based on Markdown headers (#, ##, ###).
        Args:
            markdown_text (str): Raw Markdown content.
        Returns:
            List[Document]: List of LangChain Document objects.
        """
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        return splitter.split_text(markdown_text)

    def hybrid_chunking(self, markdown_text: str) -> List[Document]:
        """
        Hybrid chunking: combines structural splitting and fixed-size chunks with overlap.
        Useful for large documents and RAG pipelines.
        Args:
            markdown_text (str): Raw Markdown content.
        Returns:
            List[Document]: List of LangChain Document objects.
        """
        # Step 1: Split by structure (headers)
        structural_docs = self.structural_chunking(markdown_text)

        # Step 2: Split each structural chunk into smaller chunks (size + overlap)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.overlap,
            separators=["\n\n", "\n", " ", ""],
        )

        hybrid_docs: List[Document] = []
        for doc in structural_docs:
            split_docs = splitter.split_documents([doc])
            hybrid_docs.extend(split_docs)

        return hybrid_docs

    def to_json(self, docs: List[Document]) -> List[dict]:
        """
        Convert LangChain Document objects to JSON-ready dictionaries.
        Args:
            docs (List[Document]): List of Document objects.
        Returns:
            List[dict]: List of dicts with id, metadata, and content.
        """
        return [
            {
                "id": i + 1,
                "metadata": doc.metadata,
                "content": doc.page_content,
            }
            for i, doc in enumerate(docs)
        ]

    def to_markdown(self, docs: List[Document]) -> str:
        """
        Convert LangChain Document objects to a single Markdown string.
        Args:
            docs (List[Document]): List of Document objects.
        Returns:
            str: Combined Markdown text separated by '---' for clarity.
        """
        return "\n\n---\n\n".join([doc.page_content for doc in docs])
