"""
Survey API endpoints.

This module provides endpoints used by the survey flow:
- loading selectable options (countries, ages, regions, etc.)
- returning survey questions
- computing statistics-based answers for each survey step
- generating the final survey summary

All endpoints are read-only and rely on precomputed statistical data.
"""

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user, get_session
from app.models import SalaryStatistic
from app.models import (
    SurveyQuestion,
    Country,
    Region,
    City,
    Age,
    Category,
    Protection,
    ArbeitStat,
    StateStat,
    KursStat,
    MigrantenRegion,
)
from app.models.survey_summary_request import SurveySummaryRequest
from app.models.job_geo_statistics import JobGeoStatistic

router = APIRouter(prefix="/survey", tags=["Survey"])


# =================================================
# Helpers
# =================================================

def render_template(template: str, **kwargs) -> str:
    """
    Safely render a text template using keyword arguments.

    If a required placeholder is missing, returns a readable
    error message instead of raising an exception.
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        return f"Template error: missing {e}"


async def get_country_with_protection(
    db: AsyncSession,
    country_id: int,
) -> Country | None:
    """
    Fetch a country along with its associated protection status.
    """
    res = await db.execute(
        select(Country)
        .options(selectinload(Country.protection))
        .where(Country.id == country_id)
    )
    return res.scalar_one_or_none()


# =================================================
# OPTIONS (used to populate select fields)
# =================================================

@router.get("/options/countries")
async def survey_countries(db: AsyncSession = Depends(get_session)):
    """
    Return a list of available countries for the survey.
    """
    rows = await db.execute(
        select(Country.id, Country.name).order_by(Country.name)
    )
    return [{"id": i, "label": n} for i, n in rows.all()]


@router.get("/options/ages")
async def survey_ages(db: AsyncSession = Depends(get_session)):
    """
    Return available age groups.
    """
    rows = await db.execute(select(Age.id, Age.name).order_by(Age.id))
    return [{"id": i, "label": n} for i, n in rows.all()]


@router.get("/options/regions")
async def survey_regions(db: AsyncSession = Depends(get_session)):
    """
    Return a list of regions (states).
    """
    rows = await db.execute(
        select(Region.id, Region.name).order_by(Region.name)
    )
    return [{"id": i, "label": n} for i, n in rows.all()]


@router.get("/options/cities")
async def survey_cities(
    region_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
    """
    Return cities belonging to the given region.
    """
    rows = await db.execute(
        select(City.id, City.name)
        .where(City.region_id == region_id)
        .order_by(City.name)
    )
    return [{"id": i, "label": n} for i, n in rows.all()]


@router.get("/options/categories")
async def survey_categories(db: AsyncSession = Depends(get_session)):
    """
    Return available job categories.
    """
    rows = await db.execute(
        select(Category.id, Category.label).order_by(Category.label)
    )
    return [{"id": i, "label": n} for i, n in rows.all()]


# =================================================
# QUESTIONS
# =================================================

@router.get("/questions")
async def get_survey_questions(db: AsyncSession = Depends(get_session)):
    """
    Return all survey questions ordered by step.
    """
    rows = await db.execute(
        select(SurveyQuestion).order_by(SurveyQuestion.step)
    )

    return [
        {
            "id": q.id,
            "step": q.step,
            "question_text": q.question_text,
            "input_type": q.input_type,
            "select_api": q.select_api,
            "statistic_api": q.statistic_api,
            "positive_hint": q.positive_hint,
        }
        for q in rows.scalars().all()
    ]


# =================================================
# STATISTICS — STEP 1 (Employment & courses by country)
# =================================================

@router.get("/answer/statistics/arbeit-by-country")
async def statistic_by_country(
    country_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
    """
    Return employment and course statistics for the selected country.
    """
    question = (
        await db.execute(
            select(SurveyQuestion).where(SurveyQuestion.step == 1)
        )
    ).scalar_one()

    country = await get_country_with_protection(db, country_id)
    if not country:
        return {"error": "Country not found"}

    arbeit_rows = await db.execute(
        select(ArbeitStat.name, ArbeitStat.count)
        .where(ArbeitStat.country_id == country_id)
    )

    employment = [
        {"type": r.name.value, "count": int(r.count)}
        for r in arbeit_rows.all()
    ]

    kurs_rows = await db.execute(
        select(KursStat.name, KursStat.count)
        .where(KursStat.protection_id == country.protection_id)
    )

    courses = [
        {"course": n, "count": int(c)}
        for n, c in kurs_rows.all()
    ]

    employment_total = sum(r["count"] for r in employment) or 0
    courses_total = sum(c["count"] for c in courses) or 0

    text = render_template(
        question.answer_template,
        country=country.name,
        employment_total=employment_total,
        courses_total=courses_total,
    )

    return {
        "text": text,
        "positive_hint": question.positive_hint,
        "raw": {
            "country": country.name,
            "employment": employment,
            "courses": courses,
        },
    }


# =================================================
# STATISTICS — STEP 2 (Employment by age & protection)
# =================================================

@router.get("/answer/statistics/state/by-age")
async def statistic_by_age(
    country_id: int = Query(...),
    age_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
    """
    Return employment statistics for a given age group
    and protection status.
    """
    question = (
        await db.execute(
            select(SurveyQuestion).where(SurveyQuestion.step == 2)
        )
    ).scalar_one()

    country = await get_country_with_protection(db, country_id)
    age = await db.get(Age, age_id)

    if not country or not age or not country.protection_id:
        return {"error": "Country, age or protection not found"}

    rows = await db.execute(
        select(StateStat.name, StateStat.count)
        .where(
            StateStat.age_id == age_id,
            StateStat.protection_id == country.protection_id,
        )
    )

    stats = [
        {"type": r.name.value, "count": int(r.count)}
        for r in rows.all()
    ]

    total_migrants = next(
        (r["count"] for r in stats if r["type"] == "Migranten"), 0
    )
    unemployed = next(
        (r["count"] for r in stats if r["type"] == "Arbeitslose"), 0
    )

    employed = max(total_migrants - unemployed, 0)

    employment_percent = (
        round(employed / total_migrants * 100, 1)
        if total_migrants > 0
        else 0
    )

    text = render_template(
        question.answer_template,
        age=age.name,
        protection=country.protection.name if country.protection else "",
        employment_percent=employment_percent,
    )

    return {
        "text": text,
        "positive_hint": question.positive_hint,
        "raw": {
            "age": age.name,
            "protection": country.protection.name if country.protection else "",
            "employment_percent": employment_percent,
        },
    }


# =================================================
# STATISTICS — STEP 3 (Migrants by region)
# =================================================

@router.get("/answer/statistics/migrants/by-region")
async def statistic_by_region(
    region_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
    """
    Return migrant employment statistics for a region.
    """
    question = (
        await db.execute(
            select(SurveyQuestion).where(SurveyQuestion.step == 3)
        )
    ).scalar_one()

    region = await db.get(Region, region_id)
    if not region:
        return {"error": "Region not found"}

    row = await db.execute(
        select(MigrantenRegion)
        .where(MigrantenRegion.region_id == region_id)
    )

    stat = row.scalars().first()

    total = int(stat.zusammen) if stat and stat.zusammen else 0
    unemployed = int(stat.arbeitslos) if stat and stat.arbeitslos else 0
    employed = max(total - unemployed, 0)

    employment_percent = (
        round(employed / total * 100, 1) if total > 0 else 0
    )

    text = render_template(
        question.answer_template,
        region=region.name,
        employment_percent=employment_percent,
    )

    return {
        "text": text,
        "positive_hint": question.positive_hint,
        "raw": {
            "region": region.name,
            "employment_percent": employment_percent,
        },
    }


# =================================================
# STATISTICS — STEP 4 (Salary by region & category)
# =================================================

@router.get("/answer/statistics/salary")
async def statistic_salary(
    region_id: int = Query(...),
    category_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
    """
    Return the latest available salary statistic
    for a given region and job category.
    """
    question = (
        await db.execute(
            select(SurveyQuestion).where(SurveyQuestion.step == 4)
        )
    ).scalar_one()

    region = await db.get(Region, region_id)
    category = await db.get(Category, category_id)

    if not region or not category:
        return {"error": "Invalid parameters"}

    row = await db.execute(
        select(SalaryStatistic)
        .where(
            SalaryStatistic.region_id == region_id,
            SalaryStatistic.category_id == category_id,
        )
        .order_by(desc(SalaryStatistic.month))
        .limit(1)
    )

    stat = row.scalars().first()
    salary = int(stat.salary) if stat and stat.salary else 0

    text = render_template(
        question.answer_template,
        region=region.name,
        category=category.label,
        salary=salary,
    )

    return {
        "text": text,
        "positive_hint": question.positive_hint,
        "raw": {
            "region": region.name,
            "category": category.label,
            "salary": salary,
            "month": stat.month if stat else None,
        },
    }


# =================================================
# STATISTICS — STEP 5 (Job vacancies by city)
# =================================================

@router.get("/answer/statistics/jobs/by-city")
async def statistic_jobs_by_city(
    region_id: int = Query(...),
    category_id: int = Query(...),
    city_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
    """
    Return job vacancy count for a specific city and category.
    """
    question = (
        await db.execute(
            select(SurveyQuestion).where(SurveyQuestion.step == 5)
        )
    ).scalar_one()

    region = await db.get(Region, region_id)
    category = await db.get(Category, category_id)
    city = await db.get(City, city_id)

    if not region or not category or not city:
        return {"error": "Invalid parameters"}

    row = await db.execute(
        select(JobGeoStatistic)
        .where(
            JobGeoStatistic.region_id == region_id,
            JobGeoStatistic.category_id == category_id,
            JobGeoStatistic.city_id == city_id,
        )
    )

    stat = row.scalars().first()
    vacancies = stat.count if stat else 0

    text = render_template(
        question.answer_template,
        category=category.label,
        city=city.name,
        vacancies=vacancies,
    )

    return {
        "text": text,
        "positive_hint": question.positive_hint,
        "raw": {
            "region": region.name,
            "category": category.label,
            "city": city.name,
            "vacancies": vacancies,
        },
    }


# =================================================
# SUMMARY
# =================================================

@router.post("/summary")
async def survey_summary(
    payload: SurveySummaryRequest = Body(...),
    db: AsyncSession = Depends(get_session),
):
    """
    Generate the final survey summary based on user selections.
    """
    country = await get_country_with_protection(db, payload.country_id)
    age = await db.get(Age, payload.age_id)
    region = await db.get(Region, payload.region_id)
    category = await db.get(Category, payload.category_id)
    city = await db.get(City, payload.city_id)

    steps = [
        {"step": 1, "label": "Herkunftsland", "value": country.name if country else ""},
        {"step": 2, "label": "Alter", "value": age.name if age else ""},
        {"step": 3, "label": "Bundesland", "value": region.name if region else ""},
        {"step": 4, "label": "Berufsfeld", "value": category.label if category else ""},
        {"step": 5, "label": "Stadt", "value": city.name if city else ""},
    ]

    return {
        "title": "Vielen Dank 🤍",
        "text": "Ihre Antworten zeigen: Integration ist möglich – Schritt für Schritt.",
        "steps": steps,
    }
