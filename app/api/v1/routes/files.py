from fastapi import APIRouter, HTTPException
from typing import Optional, List
from app.services.file_processor import FileProcessor
from app.db.supabase_client import supabase
from app.services.yaml_process import YamlFileProcessor
import logging, os
from urllib.parse import urlparse
from fastapi import Query
from pydantic import BaseModel
from app.services.storage_db_service import StorageService
from app.services.chunk_service import ChunkService
from app.db.ai_model_client import groq_client
import requests


# from app.services.file_service import extract_file


router = APIRouter()

# @router.get("/extract_file/{file_id}")
# def extract_file_route(file_id: str):
#     try:
#         result = extract_file(file_id)
#         return {"status": "success", "data": result}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


@router.get("/api_key")
def getApiKey():
    return "hello ajhbdhasv kbsha"


# @router.get("/extract_file/{file_id}")
# def extract_file_route(file_id: str):
#     try:
#         print(f"Processing file with ID: {file_id}")
#         # Get file metadata
#         resp = supabase.table("fileInfo").select("*").eq("id", file_id).single().execute()
#         file_info = resp.data
#         if not file_info:
#             raise HTTPException(status_code=404, detail="File not found")

#         file_url = file_info.get("file_url")
#         file_type = file_info.get("file_type") or _guess_file_type_from_url(file_url)

#         if not file_url:
#             raise HTTPException(status_code=400, detail="Missing file_url for the file in DB")

#         # Process file
#         processor = FileProcessor(file_id=file_id, file_url=file_url, file_type=file_type)
#         result = processor.process_file()

#         return {"status": "success", "data": result}

#     except HTTPException:
#         raise
#     except Exception as e:
#         logging.exception("Unexpected error in extract_file_route")
#         raise HTTPException(status_code=400, detail=str(e))


def _guess_file_type_from_url(url: Optional[str]) -> str:
    if not url:
        return "pdf"
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    return ext or "pdf"


@router.get("/extract_file/{file_id}")
def extract_file_route(
    file_id: str,
    skip_pages: Optional[List[int]] = Query(
        None, description="Pages to skip, e.g., 4,7,8"
    ),
):
    try:
        # Get file metadata
        resp = (
            supabase.table("fileInfo").select("*").eq("id", file_id).single().execute()
        )
        file_info = resp.data
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")

        file_url = file_info.get("file_url")
        file_type = file_info.get("file_type") or _guess_file_type_from_url(file_url)

        if not file_url:
            raise HTTPException(
                status_code=400, detail="Missing file_url for the file in DB"
            )

        # Process file with skip_pages
        processor = FileProcessor(
            file_id=file_id,
            file_url=file_url,
            file_type=file_type,
            skip_pages=skip_pages,
        )
        result = processor.process_file()

        return {"status": "success", "data": result}

    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Unexpected error in extract_file_route")
        raise HTTPException(status_code=400, detail=str(e))


class UserRuleRequest(BaseModel):
    extract: str


@router.post("/user_rule_yml")
def user_rules_yml(request: UserRuleRequest):
    try:
        yaml_content = YamlFileProcessor.create_yaml_from_extract(request.extract)
        return {"yaml": yaml_content}
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Unexpected error in user rules yml creation")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/clean_file/{file_id}")
def clean_extracted_file_user_rules(file_id: str):
    try:
        # Fetch file metadata from Supabase
        resp = (
            supabase.table("fileInfo").select("*").eq("id", file_id).single().execute()
        )
        file_info = resp.data
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")

        md_url = file_info.get("extracted_markdown_link")
        if not md_url:
            raise HTTPException(status_code=400, detail="Missing Markdown link in DB")

        # Fetch Markdown content
        resp = requests.get(md_url, timeout=10)
        if resp.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Failed to fetch Markdown content"
            )
        md_content = resp.text

        # Clean Markdown
        cleaned_md = YamlFileProcessor.clean_md_text(md_content)

        # Upload cleaned Markdown
        storage = StorageService()
        new_md_url = storage.upload(cleaned_md, f"{file_id}_cleaned.md")

        # Update Supabase
        supabase.table("fileInfo").update(
            {
                "extracted_markdown_link": new_md_url,
                "extracted_markdown_text": cleaned_md,
            }
        ).eq("id", file_id).execute()

        return {"markdown_url": new_md_url, "status": "file cleaned with user rules"}

    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Unexpected error in cleaning Markdown")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/chunk_file/{file_id}")
def chunk_file(file_id: str, method: str = "structural"):
    try:
        print(f"Method: {method}")

        # Fetch file metadata from Supabase
        resp = supabase.table("fileInfo").select("*").eq("id", file_id).single().execute()
        file_info = resp.data
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")

        md_url = file_info.get("extracted_markdown_link")
        if not md_url:
            raise HTTPException(status_code=400, detail="Missing Markdown link in DB")

        # Fetch markdown content
        chunk_service = ChunkService()
        markdown_text = chunk_service.fetch_markdown(md_url)

        # Chunk the text
        if method == "structural":
            docs = chunk_service.structural_chunking(markdown_text)
        elif method == "hybrid":
            docs = chunk_service.hybrid_chunking(markdown_text)
        else:
            raise HTTPException(status_code=400, detail="Invalid chunking method")

        # Split docs into smaller batches to avoid request too large
        chunks_for_ai = []
        current_chunk = ""

        for doc in docs:
            doc_text = doc.page_content
            if len(current_chunk) + len(doc_text) > 1500:
                chunks_for_ai.append(current_chunk)
                current_chunk = doc_text
            else:
                current_chunk += "\n\n" + doc_text

        if current_chunk:
            chunks_for_ai.append(current_chunk)

        # Generate summaries for each batch
        all_summaries = []
        for chunk in chunks_for_ai:
            response = groq_client.responses.create(
                model="openai/gpt-oss-120b",
                input=f"Summarize the following content in short explanation:\n{chunk}"
            )
            summary_text = response.output_text if hasattr(response, "output_text") else str(response)
            all_summaries.append(summary_text)

        # Combine summaries into a final summary
        final_summary = "\n\n".join(all_summaries)

        # Return JSON + Markdown + Final Summary
        return {
            "summary": final_summary,
            "json": chunk_service.to_json(docs),
            "markdown": chunk_service.to_markdown(docs),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))