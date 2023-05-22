from fastapi import APIRouter
from api import payments, settings

router = APIRouter()

router.include_router(payments.router)
router.include_router(settings.router)