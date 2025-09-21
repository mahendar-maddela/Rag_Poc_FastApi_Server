# app/services/storage_service.py
from app.db.supabase_client import supabase

class StorageService:
    def __init__(self, bucket: str = "filesMahendar"):
        self.bucket = bucket

    def upload(self, content: str, path: str) -> str:
        """
        Upload string content to Supabase storage and return public URL.
        """
        try:
            # Remove existing file if present
            try:
                supabase.storage.from_(self.bucket).remove([path])
            except Exception:
                pass

            # Upload content
            supabase.storage.from_(self.bucket).upload(path, content.encode("utf-8"))

            # Return public URL
            return supabase.storage.from_(self.bucket).get_public_url(path)
        except Exception as e:
            raise ValueError(f"Failed to upload file to Supabase: {e}")

    def update_file_links(self, file_id: str, rich_link: str, md_link: str,md_content:str,rich_text:str):
        supabase.table("fileInfo").update(
            {
                "extracted_richtext_link": rich_link,
                "extracted_markdown_link": md_link,
                "extracted_markdown_text": md_content,
                "extracted_rich_text":rich_text
            }
        ).eq("id", file_id).execute()
