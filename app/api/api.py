from fastapi import APIRouter
from app.api.routes.admin_import import router as admin_import_router
from app.api.routes.user_statistic import router as user_statistic_router
from app.api.routes.user_questionary import router as survey

api_router = APIRouter()
api_router.include_router(admin_import_router)
api_router.include_router(user_statistic_router)
api_router.include_router(survey)
