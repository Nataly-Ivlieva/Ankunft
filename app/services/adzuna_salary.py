import httpx
import asyncio
from app.db.session import engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.salary_statistics import SalaryStatistic
from app.models.categories import Category
from app.models.region import Region
from app.config import settings

async def import_salary_data_de(db: AsyncSession):
    categories_result = await db.execute(select(Category))
    categories = categories_result.scalars().all()

    regions_result = await db.execute(select(Region))
    regions = regions_result.scalars().all()

    async with httpx.AsyncClient() as client:
        for cat in categories:
            for reg in regions:
                url = (
                    f"https://api.adzuna.com/v1/api/jobs/{settings.ADZUNA_COUNTRY}/history"
                    f"?app_id={settings.ADZUNA_APP_ID}"
                    f"&app_key={settings.ADZUNA_APP_KEY}"
                    f"&location0=Deutschland"
                    f"&location1={reg.name}"
                    f"&category={cat.tag}"
                    f"&content-type=application/json"
                )
                response = await client.get(url)
                if response.status_code != 200:
                    print(f"Error {cat.tag} in {reg.name}: {response.text}")
                    continue

                data = response.json().get("month", {})
                for month_str, salary in data.items():
                    q = await db.execute(
                        select(SalaryStatistic)
                        .where(SalaryStatistic.category_id == cat.id)
                        .where(SalaryStatistic.region_id == reg.id)
                        .where(SalaryStatistic.month == month_str)
                    )
                    existing = q.scalar_one_or_none()
                    if existing:
                        continue

                    db.add(SalaryStatistic(
                        category_id=cat.id,
                        region_id=reg.id,
                        month=month_str,
                        salary=salary
                    ))

        await db.commit()
    print("Loaded!")

async def main():
    async with AsyncSession(engine) as db:
        await import_salary_data_de(db)

if __name__ == "__main__":
    asyncio.run(main())