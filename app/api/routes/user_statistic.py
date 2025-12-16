from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_session
from app.models.arbeit_stat import ArbeitStat
from app.models.state_stat import StateStat, ArbeitState as Astate
from app.models.country import Country
from app.models.age import Age
from app.models.protection import Protection
from app.models.genders import Gender
from app.models import KursStat
from app.models.job_geo_statistics import JobGeoStatistic
from app.models.categories import Category
from app.models.salary_statistics import SalaryStatistic
from app.models.region import Region
from app.models.migranten_region import MigrantenRegion

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/migrants/by-region")
async def migrants_by_region(
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await db.execute(
        select(
            Region.name.label("region"),
            MigrantenRegion.zusammen,
            MigrantenRegion.arbeitslos,
        ).join(Region)
    )

    return [
        {
            "region": r.region,
            "zusammen": r.zusammen,
            "arbeitslos": r.arbeitslos,
        }
        for r in result
    ]


@router.get("/arbeit/by-country")
async def arbeit_by_country(
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    q = (
        select(
            Country.name.label("country"),
            ArbeitStat.name.label("type"),
            ArbeitStat.count.label("count"),
        )
        .join(Country, Country.id == ArbeitStat.country_id)
    )

    rows = (await db.execute(q)).all()

    result: dict[str, dict] = {}
    for country, stat_type, count in rows:
        if country not in result:
            result[country] = {
                "country": country,
                "beschaeftigte": 0,
                "teilzeit": 0,
                "unterbeschaeftigte": 0,
            }
        result[country][stat_type.value.lower()] = count

    return list(result.values())


@router.get("/state/by-age")
async def state_by_age(
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    q = (
        select(
            Age.name.label("age"),
            Protection.name.label("protection"),
            StateStat.name.label("state"),
            func.sum(StateStat.count).label("count"),
        )
        .join(Age, StateStat.age_id == Age.id)
        .join(Protection, StateStat.protection_id == Protection.id)
        .group_by(Age.name, Protection.name, StateStat.name)
        .order_by(Age.name)
    )

    rows = (await db.execute(q)).all()

    result: dict[tuple[str, str], dict] = {}
    for age, protection, state, count in rows:
        key = (age, protection)
        if key not in result:
            result[key] = {
                "age": age,
                "protection": protection,
                "arbeitslose": 0,
                "migranten": 0,
            }
        result[key][state.value.lower()] = count

    return list(result.values())


@router.get("/kurs/by-protection")
async def kurs_by_protection(
    protection_id: int | None = None,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    q = (
        select(
            KursStat.name.label("kurs"),
            Protection.name.label("protection"),
            KursStat.count,
        )
        .join(Protection)
    )

    if protection_id:
        q = q.where(KursStat.protection_id == protection_id)

    rows = (await db.execute(q)).all()

    data: dict[str, dict] = {}
    for kurs, protection, count in rows:
        if kurs not in data:
            data[kurs] = {"kurs": kurs}
        data[kurs][protection] = count

    return list(data.values())


@router.get("/jobs/by-region")
async def jobs_by_region(
    category_id: int | None = None,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    q = (
        select(
            Region.name.label("region"),
            Category.label.label("category"),
            func.sum(JobGeoStatistic.count).label("count"),
        )
        .join(Region, JobGeoStatistic.region_id == Region.id)
        .join(Category, JobGeoStatistic.category_id == Category.id)
        .group_by(Region.name, Category.label)
        .order_by(Region.name)
    )

    if category_id:
        q = q.where(JobGeoStatistic.category_id == category_id)

    rows = (await db.execute(q)).all()

    return [
        {
            "region": region,
            "category": category,
            "count": count,
        }
        for region, category, count in rows
    ]


@router.get("/salary")
async def salary_statistics(
    category_id: int | None = None,
    region_id: int | None = None,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    q = (
        select(
            Region.name.label("region"),
            Category.label.label("category"),
            SalaryStatistic.month,
            SalaryStatistic.salary,
        )
        .join(Region, SalaryStatistic.region_id == Region.id)
        .join(Category, SalaryStatistic.category_id == Category.id)
        .order_by(SalaryStatistic.month)
    )

    if category_id:
        q = q.where(SalaryStatistic.category_id == category_id)
    if region_id:
        q = q.where(SalaryStatistic.region_id == region_id)

    rows = (await db.execute(q)).all()

    return [
        {
            "region": r.region,
            "category": r.category,
            "month": r.month,
            "salary": r.salary,
        }
        for r in rows
    ]
