from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.services.taxonomy_service import TaxonomyService
from app.schemas.taxonomy_schema import TaxonomyCreate, TaxonomyUpdate, TaxonomyResponse
from app.utils.response import success_response, error_response
from app.core.authorize import admin_only

router = APIRouter()


@router.post("/")
def create_taxonomy(
    data: TaxonomyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only),
):
    try:
        taxonomy = TaxonomyService.create_taxonomy(db, data, user_id=current_user.id)
        print("hello test", taxonomy)
        return success_response(
            "Taxonomy created successfully",
            {
                "id": str(taxonomy.id),
                "level_number": taxonomy.level_number,
                "code": taxonomy.code,
                "display_name": taxonomy.display_name,
                "description": taxonomy.description,
                "is_active": taxonomy.is_active,
            },
            status.HTTP_201_CREATED,
        )
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{taxonomy_id}")
def update_taxonomy(
    taxonomy_id: UUID,
    data: TaxonomyUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only),
):
    try:
        updated = TaxonomyService.update_taxonomy(db, taxonomy_id, data)
        return success_response("Taxonomy updated successfully", updated)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/")
def get_all_taxonomies(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only),
):
    try:
        taxonomies = TaxonomyService.get_all(db)
        return success_response("Taxonomies fetched successfully", taxonomies)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
