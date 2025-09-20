from fastapi import APIRouter
from . import files

router = APIRouter()

router.include_router(files.router, prefix="/files", tags=["Files"])