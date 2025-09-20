import requests
import pdfplumber
from io import BytesIO
import markdownify
from app.db.supabase_client import supabase


def extract_file(file_id: str):
    """
    1. Fetch file metadata from Supabase (get file_url).
    2.  PDF from file_url.
    3. Extract rich text.
    4. Extract to Markdown.
    5. Upload extracted files back to Supabase.
    6. Return links.
    """
    # 1. Get file link from Supabase table
    file_data = (
        supabase.table("fileInfo").select("file_url","file_type").eq("id", file_id).single().execute()
    )   

    if not file_data.data:
        raise ValueError("File not found in Supabase")

    file_url = file_data.data["file_url"]

    # 2. Download PDF
    response = requests.get(file_url)
    if response.status_code != 200:
        raise ValueError("Failed to download file from Supabase storage")

    pdf_bytes = BytesIO(response.content)

    # 3. Extract text using pdfplumber
    extracted_text = ""
    with pdfplumber.open(pdf_bytes) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() or ""

    # 4. Convert to Markdown
    markdown_content = markdownify.markdownify(extracted_text, heading_style="ATX")

    # 5. Upload extracted results to Supabase storage
    bucket = "filesMahendar"

    rich_text_path = f"{file_id}_richtext.txt"
    markdown_path = f"{file_id}_extracted.md"

    supabase.storage.from_(bucket).upload(rich_text_path, extracted_text.encode("utf-8"))
    supabase.storage.from_(bucket).upload(markdown_path, markdown_content.encode("utf-8"))

    rich_text_link = supabase.storage.from_(bucket).get_public_url(rich_text_path)
    markdown_link = supabase.storage.from_(bucket).get_public_url(markdown_path)

    # 6. Update DB with new links
    supabase.table("fileInfo").update(
        {
            "extracted_richtext_link": rich_text_link,
            "extracted_markdown_link": markdown_link,
        }
    ).eq("id", file_id).execute()

    return {
        "file_id": file_id,
        "extracted_richtext_link": rich_text_link,
        "extracted_markdown_link": markdown_link,
    }
