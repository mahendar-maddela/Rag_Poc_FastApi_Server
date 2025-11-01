from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException,Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.authorize import admin_only
from app.services.document_service import DocumentService
from app.schemas.document_schema import DocumentCreateSchema
from app.utils.response import success_response, error_response
from app.services.file_processor import FileProcessor
from typing import Optional, List



from app.models.user import User

router = APIRouter()


@router.post("/upload")
def upload_document(
    title: str = Form(...),
    language: str = Form(...),
    visibility: str = Form(...),
    taxonomyId: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    try:
        data = DocumentCreateSchema(
            title=title,
            language=language,
            visibility=visibility,
            taxonomyId=taxonomyId,
        )

        result = DocumentService.upload_document(
            db=db, file=file, data=data, user=current_user
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_all_documents(
    db: Session = Depends(get_db),
):
    try:
        documents = DocumentService.get_all_documents(db)
        return success_response("Taxonomy created successfully", documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{file_id}")
def get_file_metadata(file_id: str, db: Session = Depends(get_db)):
    """Fetch single document with signed S3 URL"""
    try:
        data = DocumentService.get_file_metadata(db, file_id)
        return {"status": "success", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/extract/{file_id}")
def extract_file(file_id: str, skip_pages: Optional[List[int]] = Query(None), db: Session = Depends(get_db)):
    """Extract text/markdown from file"""
    try:
        doc = DocumentService.get_file_metadata(db, file_id)
        processor = FileProcessor(file_id, doc["file_url"], doc["file_type"], skip_pages)
        result = processor
        return {"status": "success", "data": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))