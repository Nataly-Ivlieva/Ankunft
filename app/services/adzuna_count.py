import asyncio
import httpx

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import engine
from app.models.region import Region
from app.models.categories import Category
from app.models.city import City
from app.models.job_geo_statistics import JobGeoStatistic
from app.config import settings


async def fetch_with_retry(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
                response = await client.get(url)
            return response

        except httpx.ReadTimeout:
            print(f"⏳ Timeout on attempt {attempt+1}/{retries}: {url}")

            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                print("❌ API did not respond after retries")
                return None


async def import_job_geodata(db, region: Region, category: Category):
    url = (
        f"https://api.adzuna.com/v1/api/jobs/de/geodata"
        f"?app_id={settings.ADZUNA_APP_ID}"
        f"&app_key={settings.ADZUNA_APP_KEY}"
        f"&location0=Deutschland"
        f"&location1={region.name}"
        f"&category={category.tag}"
    )

    response = await fetch_with_retry(url)

    if not response:
        print(f"⚠️ Failed: {region.name} — {category.tag}")
        return

    if response.status_code != 200:
        print(f"⚠️ Error {response.status_code} in {region.name}: {response.text}")
        return

    data = response.json()
    locations = data.get("locations", [])

    for loc in locations:
        count = loc.get("count")
        city_name = loc["location"]["area"][-1]

        q = select(City).where(
            City.name == city_name,
            City.region_id == region.id
        )
        city = (await db.execute(q)).scalar_one_or_none()

        if not city:
            city = City(name=city_name, region_id=region.id)
            db.add(city)
            await db.flush()  # получаем ID

        stat = JobGeoStatistic(
            category_id=category.id,
            region_id=region.id,
            city_id=city.id,
            count=count
        )
        db.add(stat)

    await db.commit()
    print(f"✓ {region.name} — {category.tag} imported")


async def import_all_geodata(db):
    regions = (await db.execute(select(Region))).scalars().all()
    categories = (await db.execute(select(Category))).scalars().all()

    for region in regions:
        if not region.name:
            print("⚠️ Region without name, skipping")
            continue

        for category in categories:
            await import_job_geodata(db, region, category)

async def main():
    async with AsyncSession(engine, expire_on_commit=False) as db:
        await import_all_geodata(db)


if __name__ == "__main__":
    asyncio.run(main())
