from fastapi import APIRouter, Depends
from app.api.deps import admin_required

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
async def get_stats(user = Depends(admin_required)):
    return {"ok": True, "admin": user.email}
