import os
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.categories import Category
from app.config import settings

ADZUNA_URL = (
    f"https://api.adzuna.com/v1/api/jobs/"
    f"{settings.ADZUNA_COUNTRY}/categories"
    f"?app_id={settings.ADZUNA_APP_ID}"
    f"&app_key={settings.ADZUNA_APP_KEY}"
    f"&content-type=application/json"
)


async def load_categories(db: AsyncSession):
    print("Loading...")

    async with httpx.AsyncClient() as client:
        response = await client.get(ADZUNA_URL)

    if response.status_code != 200:
        raise RuntimeError(f"Error of Adzuna: {response.text}")

    data = response.json()
    categories = data.get("results", [])

    added = 0

    for c in categories:
        label = c.get("label")
        tag = c.get("tag")

        if not label or not tag:
            continue
        q = select(Category).where(Category.tag == tag)
        existing = (await db.execute(q)).scalar_one_or_none()

        if existing:
            continue

        db.add(Category(label=label, tag=tag))
        added += 1

    await db.commit()
    print(f"Loaded: {added}")
