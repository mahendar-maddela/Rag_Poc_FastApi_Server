from fastapi import APIRouter
from . import files, auth,taxonomy_levels_controller,document_controller

router = APIRouter()

router.include_router(files.router, prefix="/files", tags=["Files"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(taxonomy_levels_controller.router, prefix="/taxonomy", tags=["Taxonomy  Levels"])
router.include_router(document_controller.router, prefix="/documents", tags=["Documents"])


