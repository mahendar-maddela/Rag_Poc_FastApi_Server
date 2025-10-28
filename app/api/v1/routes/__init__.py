from fastapi import APIRouter
from . import files, auth

router = APIRouter()

router.include_router(files.router, prefix="/files", tags=["Files"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
