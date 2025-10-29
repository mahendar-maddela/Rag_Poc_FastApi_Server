from sqlalchemy.orm import Session
from uuid import UUID
from app.models.taxonomy_levels import TaxonomyLevel
from app.schemas.taxonomy_schema import TaxonomyCreate, TaxonomyUpdate

class TaxonomyRepository:
    @staticmethod
    def create(db: Session, data: TaxonomyCreate, user_id: UUID):
        new_item = TaxonomyLevel(**data.dict(), created_by_user_id=user_id)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    @staticmethod
    def get_by_id(db: Session, taxonomy_id: UUID):
        return db.query(TaxonomyLevel).filter(TaxonomyLevel.id == taxonomy_id).first()

    @staticmethod
    def update(db: Session, taxonomy_id: UUID, data: TaxonomyUpdate):
        taxonomy = db.query(TaxonomyLevel).filter(TaxonomyLevel.id == taxonomy_id).first()
        if taxonomy:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(taxonomy, key, value)
            db.commit()
            db.refresh(taxonomy)
        return taxonomy

    @staticmethod
    def get_all(db: Session):
        return db.query(TaxonomyLevel).filter(TaxonomyLevel.is_active == True).all()
