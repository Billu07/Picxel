from fastapi import APIRouter

from app.api.v1 import system

router = APIRouter()
router.include_router(system.router)
