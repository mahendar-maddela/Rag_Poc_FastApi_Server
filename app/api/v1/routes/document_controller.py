from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.authorize import admin_only
from app.services.document_service import DocumentService
from app.schemas.document_schema import DocumentCreateSchema
from app.utils.response import success_response, error_response

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
