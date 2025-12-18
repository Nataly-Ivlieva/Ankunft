"""
Administrative data import endpoints.

This module defines protected API routes used by administrators
to trigger various data import and synchronization jobs.
All endpoints require admin privileges.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import admin_required
from app.db.session import get_session
from app.services.import_statistic import (
    import_migranten,
    import_arbeit,
    import_kurse,
    import_state_stat,
)
from app.services.adzuna_salary import import_salary_data_de
from app.services.adzuna_count import import_all_geodata
from app.logger import logger

# Router for admin-only import operations
router = APIRouter(prefix="/admin/import", tags=["admin-import"])


@router.post("/salary")
async def run_salary_import(
    user=Depends(admin_required),
    db: AsyncSession = Depends(get_session),
):
    """
    Trigger salary data import for Germany.

    This endpoint starts the process of fetching and storing
    salary-related data. Accessible to administrators only.
    """
    logger.info(f"Admin {user.email} started salary import")

    await import_salary_data_de(db)

    logger.info("Salary import completed")

    return {"status": "ok", "message": "Salary data imported"}


@router.post("/geodata")
async def run_geodata_import(
    user=Depends(admin_required),
    db: AsyncSession = Depends(get_session),
):
    """
    Trigger geolocation data import.

    Imports and updates geographic reference data
    required for other application features.
    """
    logger.info(f"Admin {user.email} started geodata import")

    await import_all_geodata(db)

    logger.info("Geodata import completed")

    return {"status": "ok", "message": "Geodata imported"}


@router.post("/migranten")
async def import_migranten_endpoint(user=Depends(admin_required)):
    """
    Trigger migration statistics import.

    Runs the background job that imports migrant-related
    statistical data.
    """
    logger.info(f"Admin {user.email} started import_migranten()")

    await import_migranten()

    logger.info(f"Admin {user.email} finished import_migranten()")

    return {"status": "ok", "import": "migranten"}


@router.post("/arbeit")
async def import_arbeit_endpoint(user=Depends(admin_required)):
    """
    Trigger employment statistics import.
    """
    logger.info(f"Admin {user.email} started import_arbeit()")

    await import_arbeit()

    logger.info(f"Admin {user.email} finished import_arbeit()")

    return {"status": "ok", "import": "arbeit"}


@router.post("/kurse")
async def import_kurse_endpoint(user=Depends(admin_required)):
    """
    Trigger education/course statistics import.
    """
    logger.info(f"Admin {user.email} started import_kurse()")

    await import_kurse()

    logger.info(f"Admin {user.email} finished import_kurse()")

    return {"status": "ok", "import": "kurse"}


@router.post("/state-stat")
async def import_state_stat_endpoint(user=Depends(admin_required)):
    """
    Trigger state-level statistical data import.
    """
    logger.info(f"Admin {user.email} started import_state_stat()")

    await import_state_stat()

    logger.info(f"Admin {user.email} finished import_state_stat()")

    return {"status": "ok", "import": "state_stat"}
