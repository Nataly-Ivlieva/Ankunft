from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import desc
from app.models import SalaryStatistic

from app.api.deps import get_current_user, get_session
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
)
from app.models.survey_summary_request import SurveySummaryRequest
from app.models.job_geo_statistics import JobGeoStatistic
from app.models import MigrantenRegion

router = APIRouter(prefix="/survey", tags=["Survey"])


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def render_template(template: str, **kwargs) -> str:
    try:
        return template.format(**kwargs)
    except KeyError as e:
        return f"Template error: missing {e}"


async def get_country_with_protection(
    db: AsyncSession,
    country_id: int,
) -> Country | None:
    res = await db.execute(
        select(Country)
        .options(selectinload(Country.protection))
        .where(Country.id == country_id)
    )
    return res.scalar_one_or_none()


# -------------------------------------------------
# OPTIONS
# -------------------------------------------------

@router.get("/options/countries")
async def survey_countries(db: AsyncSession = Depends(get_session)):
    rows = await db.execute(
        select(Country.id, Country.name).order_by(Country.name)
    )
    return [{"id": i, "label": n} for i, n in rows.all()]


@router.get("/options/ages")
async def survey_ages(db: AsyncSession = Depends(get_session)):
    rows = await db.execute(select(Age.id, Age.name).order_by(Age.id))
    return [{"id": i, "label": n} for i, n in rows.all()]


@router.get("/options/regions")
async def survey_regions(db: AsyncSession = Depends(get_session)):
    rows = await db.execute(
        select(Region.id, Region.name).order_by(Region.name)
    )
    return [{"id": i, "label": n} for i, n in rows.all()]


@router.get("/options/cities")
async def survey_cities(
    region_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
    rows = await db.execute(
        select(City.id, City.name)
        .where(City.region_id == region_id)
        .order_by(City.name)
    )
    return [{"id": i, "label": n} for i, n in rows.all()]


@router.get("/options/categories")
async def survey_categories(db: AsyncSession = Depends(get_session)):
    rows = await db.execute(
        select(Category.id, Category.label).order_by(Category.label)
    )
    return [{"id": i, "label": n} for i, n in rows.all()]


# -------------------------------------------------
# QUESTIONS
# -------------------------------------------------

@router.get("/questions")
async def get_survey_questions(db: AsyncSession = Depends(get_session)):
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


# -------------------------------------------------
# STATISTICS — STEP 1
# -------------------------------------------------

@router.get("/answer/statistics/arbeit-by-country")
async def statistic_by_country(
    country_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
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


# -------------------------------------------------
# STATISTICS — STEP 2
# -------------------------------------------------

@router.get("/answer/statistics/state/by-age")
async def statistic_by_age(
    country_id: int = Query(...),
    age_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
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
        (r["count"] for r in stats if r["type"] == "Migranten"),
        0,
    )
    unemployed = next(
        (r["count"] for r in stats if r["type"] == "Arbeitslose"),
        0,
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
            "total_migrants": total_migrants,
            "unemployed": unemployed,
            "employed": employed,
            "employment_percent": employment_percent,
            "stats": stats,
        },
    }


@router.get("/answer/statistics/migrants/by-region")
async def statistic_by_region(
    region_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
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

    zusammen = int(stat.zusammen) if stat and stat.zusammen else 0
    arbeitslos = int(stat.arbeitslos) if stat and stat.arbeitslos else 0
    employed = max(zusammen - arbeitslos, 0)

    employment_percent = (
        round(employed / zusammen * 100, 1)
        if zusammen > 0
        else 0
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
            "total_migrants": zusammen,
            "unemployed": arbeitslos,
            "employed": employed,
            "employment_percent": employment_percent,
        },
    }


@router.get("/answer/statistics/salary")
async def statistic_salary(
    region_id: int = Query(...),
    category_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
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
# -------------------------------------------------
# STATISTICS — STEP 5 (JOBS BY CITY)
# -------------------------------------------------

@router.get("/answer/statistics/jobs/by-city")
async def statistic_jobs_by_city(
    region_id: int = Query(...),
    category_id: int = Query(...),
    city_id: int = Query(...),
    db: AsyncSession = Depends(get_session),
):
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



# -------------------------------------------------
# SUMMARY
# -------------------------------------------------

@router.post("/summary")
async def survey_summary(
    payload: SurveySummaryRequest = Body(...),
    db: AsyncSession = Depends(get_session),
):
    country = await get_country_with_protection(db, payload.country_id)
    age = await db.get(Age, payload.age_id)
    region = await db.get(Region, payload.region_id)
    category = await db.get(Category, payload.category_id)
    city = await db.get(City, payload.city_id)

    steps = []

    steps.append({
        "step": 1,
        "label": "Herkunftsland",
        "value": country.name if country else "",
    })

    steps.append({
        "step": 2,
        "label": "Alter",
        "value": age.name if age else "",
    })

    steps.append({
        "step": 3,
        "label": "Bundesland",
        "value": region.name if region else "",
    })

    steps.append({
        "step": 4,
        "label": "Berufsfeld",
        "value": category.label if category else "",
    })

    steps.append({
        "step": 5,
        "label": "Stadt",
        "value": city.name if city else "",
    })

    return {
        "title": "Vielen Dank 🤍",
        "text": "Ihre Antworten zeigen: Integration ist möglich – Schritt für Schritt.",
        "steps": steps,
    }
