import pandas as pd
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import engine
from app.models.region import Region
from app.models.migranten_region import MigrantenRegion

from app.models.country import Country
from app.models.arbeit_stat import ArbeitStat, ArbeitState

from app.models.protection import Protection
from app.models.kurs_stat import KursStat

from app.models.genders import Gender
from app.models.age import Age
from app.models.protection import Protection
from app.models.state_stat import StateStat
from app.models.state_stat import ArbeitState
from app.models.arbeit_stat import ArbeitState as Astate

EXCEL_FILE = "data/Statistic.xlsx"
SHEET_REG = "migranten_region"
SHEET_ARB = "arbeitsmarkt"
SHEET_KUR = "Kursen"
SHEET_STATE = "Stat_migr"

async def get_or_create(db: AsyncSession, model, field: str, value: str):
    q = select(model).where(getattr(model, field) == value)
    obj = (await db.execute(q)).scalar_one_or_none()
    if obj:
        return obj

    obj = model(**{field: value})
    db.add(obj)
    await db.flush()
    return obj


async def import_state_stat():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_STATE)
    df.columns = [str(c).strip().lower() for c in df.columns]

    async with AsyncSession(engine, expire_on_commit=False) as db:

        for _, row in df.iterrows():

            gender = None
            if not pd.isna(row.get("genders")):
                gender = await get_or_create(db, Gender, "name", row["genders"].strip())

            age = None
            if not pd.isna(row.get("age")):
                age = await get_or_create(db, Age, "name", row["age"].strip())

            protection = await get_or_create(
                db, Protection, "name", row["protection"].strip()
            )

            name = row["name"].strip()
            if name not in ("Migranten", "Arbeitslose"):
                print(f"⚠️ Unknown state: {name}")
                continue

            count = float(str(row["count"]).replace(" ", ""))

            q = select(StateStat).where(
                StateStat.name == name,
                StateStat.protection_id == protection.id,
                StateStat.gender_id == (gender.id if gender else None),
                StateStat.age_id == (age.id if age else None),
            )

            stat = (await db.execute(q)).scalar_one_or_none()

            if stat:
                stat.count = count
            else:
                stat = StateStat(
                    name=name,
                    protection_id=protection.id,
                    gender_id=gender.id if gender else None,
                    age_id=age.id if age else None,
                    count=count
                )
                db.add(stat)

        await db.commit()
        print("✓ StateStat imported successfully")


async def import_kurse():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_KUR)
    df.columns = [c.strip().lower() for c in df.columns]

    async with AsyncSession(engine, expire_on_commit=False) as db:

        for _, row in df.iterrows():
            protection = await get_or_create(
                db, Protection, "name", row["protection"].strip()
            )

            count = float(str(row["count"]).replace(" ", ""))

            q = select(KursStat).where(
                KursStat.name == row["name"],
                KursStat.protection_id == protection.id
            )

            existing = (await db.execute(q)).scalar_one_or_none()

            if existing:
                existing.count = count
            else:
                db.add(KursStat(
                    name=row["name"],
                    count=count,
                    protection_id=protection.id
                ))

        await db.commit()
        print("✓ KursStat upserted")


async def import_arbeit():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_ARB)

    async with AsyncSession(engine, expire_on_commit=False) as db:
        for _, row in df.iterrows():

            country = await get_or_create(
                db, Country, "name", str(row["country"]).strip()
            )

            raw_name = str(row["name"]).replace("\xa0", " ").strip()

            try:
                name = Astate(raw_name)
            except ValueError:
                print(f"⚠️ Unknown ArbeitState: {raw_name!r}")
                continue

            count = float(str(row["count"]).replace(" ", ""))

            q = select(ArbeitStat).where(
                ArbeitStat.country_id == country.id,
                ArbeitStat.name == name
            )

            existing = (await db.execute(q)).scalar_one_or_none()

            if existing:
                existing.count = count
            else:
                db.add(ArbeitStat(
                    country_id=country.id,
                    name=name,
                    count=count
                ))

        await db.commit()
        print("✓ ArbeitStat upserted")



async def import_migranten():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_REG)
    df.columns = [str(c).strip() for c in df.columns]

    async with AsyncSession(engine, expire_on_commit=False) as db:
        regions = (await db.execute(select(Region))).scalars().all()
        region_map = {r.name: r for r in regions}

        zusammen_row = df[df["type"] == "migranten"].iloc[0]
        arbeitslos_row = df[df["type"] == "arbeitslos"].iloc[0]

        for col in df.columns:
            if col == "type":
                continue

            region = region_map.get(col)
            if not region:
                print(f"⚠️ Region not found: {col}")
                continue

            zusammen = (
                float(str(zusammen_row[col]).replace(" ", ""))
                if not pd.isna(zusammen_row[col]) else None
            )

            arbeitslos = (
                float(str(arbeitslos_row[col]).replace(" ", ""))
                if not pd.isna(arbeitslos_row[col]) else None
            )

            q = select(MigrantenRegion).where(
                MigrantenRegion.region_id == region.id
            )

            existing = (await db.execute(q)).scalar_one_or_none()

            if existing:
                existing.zusammen = zusammen
                existing.arbeitslos = arbeitslos
            else:
                db.add(MigrantenRegion(
                    region_id=region.id,
                    zusammen=zusammen,
                    arbeitslos=arbeitslos
                ))

        await db.commit()
        print("✓ MigrantenRegion upserted")



if __name__ == "__main__":
    asyncio.run(import_migranten())
    asyncio.run(import_arbeit())
    asyncio.run(import_kurse())
    asyncio.run(import_state_stat())
