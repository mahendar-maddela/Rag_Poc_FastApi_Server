from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from app.repositories.taxonomy_repository import TaxonomyRepository
from app.schemas.taxonomy_schema import TaxonomyCreate, TaxonomyUpdate

class TaxonomyService:
    @staticmethod
    def create_taxonomy(db: Session, data: TaxonomyCreate, user_id: UUID):
        return TaxonomyRepository.create(db, data, user_id)

    @staticmethod
    def update_taxonomy(db: Session, taxonomy_id: UUID, data: TaxonomyUpdate):
        taxonomy = TaxonomyRepository.get_by_id(db, taxonomy_id)
        if not taxonomy:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Taxonomy not found")
        return TaxonomyRepository.update(db, taxonomy_id, data)

    @staticmethod
    def get_all(db: Session):
        return TaxonomyRepository.get_all(db)
