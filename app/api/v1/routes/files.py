from fastapi import APIRouter, HTTPException
from typing import Optional,List
from app.services.file_processor import FileProcessor
from app.db.supabase_client import supabase
import logging, os
from urllib.parse import urlparse
from fastapi import Query


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
    skip_pages: Optional[List[int]] = Query(None, description="Pages to skip, e.g., 4,7,8")
):
    try:
        # Get file metadata
        resp = supabase.table("fileInfo").select("*").eq("id", file_id).single().execute()
        file_info = resp.data
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")

        file_url = file_info.get("file_url")
        file_type = file_info.get("file_type") or _guess_file_type_from_url(file_url)

        if not file_url:
            raise HTTPException(status_code=400, detail="Missing file_url for the file in DB")

        # Process file with skip_pages
        processor = FileProcessor(file_id=file_id, file_url=file_url, file_type=file_type, skip_pages=skip_pages)
        result = processor.process_file()

        return {"status": "success", "data": result}

    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Unexpected error in extract_file_route")
        raise HTTPException(status_code=400, detail=str(e))