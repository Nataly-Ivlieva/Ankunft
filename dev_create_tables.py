import asyncio
import json
from app.db.session import engine, AsyncSession
from sqlalchemy import select
from app.models.base import Base
from app.models.survey import SurveyQuestion
from app.models import state_stat, kurs_stat, arbeit_stat, protection, migranten_region, job_geo_statistics, salary_statistics, categories,  genders, age, user, session, country, region, survey, city
from app.core.security import hash_password
from app.services.adzuna_categories import load_categories

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def fill_reference_data():
    async with AsyncSession(engine) as db:

        reference_data = {
            protection.Protection: ["Richtlinie 2001/55/EG", "Asyl"],
            age.Age: ["15 bis unter 25 Jahre", "25 bis unter 55 Jahre", "55 Jahre und älter"],
            genders.Gender: ["Männer", "Frauen", "Sonstige"],
            region.Region: [
                "Schleswig-Holstein", "Hamburg", "Niedersachsen", "Bremen", "Nordrhein-Westfalen",
                "Hessen", "Rheinland-Pfalz", "Baden-Württemberg", "Bayern", "Saarland", "Berlin",
                "Brandenburg", "Mecklenburg-Vorpommern", "Sachsen", "Sachsen-Anhalt", "Thüringen"
            ]
        }


        for model, values in reference_data.items():
            for value in values:
                q = select(model).where(model.name == value)
                existing = (await db.execute(q)).scalar_one_or_none()
                if not existing:
                    db.add(model(name=value))

        await db.commit()


        q = select(protection.Protection)
        protections = {p.name: p for p in (await db.execute(q)).scalars().all()}


        country_data = [
            ("Ukraine", "Richtlinie 2001/55/EG"),
            ("Arabische Republik Syrien", "Asyl"),
            ("Afghanistan", "Asyl")
        ]


        for country_name, protection_name in country_data:
            q = select(country.Country).where(country.Country.name == country_name)
            existing_country = (await db.execute(q)).scalar_one_or_none()

            if not existing_country:
                db.add(
                    country.Country(
                        name=country_name,
                        protection_id=protections[protection_name].id
                    )
                )

        await db.commit()

        print("→ Lade Adzuna-Kategorien ...")
        await load_categories(db)

async def create_admin():
    async with AsyncSession(engine) as db:
        admin_email = "admin@example.com"
        existing = await db.execute(select(user.User).where(user.User.email == admin_email))
        existing = existing.scalar_one_or_none()
        if not existing:
            admin_user = user.User(
                email=admin_email,
                password_hash=hash_password("admin123"),
                role="admin"
            )
            db.add(admin_user)
            await db.commit()

async def create_questions():
    async with AsyncSession(engine) as db:

        questions = [
            SurveyQuestion(
                step=1,
                question_text="Aus welchem Land sind Sie nach Deutschland gekommen?",
                input_type="select",
                select_api="/api/countries",
                statistic_api="/statistics/arbeit/by-country",
                answer_template=(
                       "💼 In Deutschland arbeiten bereits {employment_total} Menschen aus {country}."
                        "🎓 {courses_total} Personen aus {country} nehmen aktuell an "
                        "Integrations- und Sprachkursen teil."
                ),
                positive_hint="Du bist nicht allein – viele mit ähnlichem Weg haben hier ihren Platz gefunden 💙",
            ),

            SurveyQuestion(
                step=2,
                question_text="Wie alt sind Sie?",
                input_type="select",
                select_api="/api/ages",
                statistic_api="/statistics/state/by-age",
                answer_template=(
                    "📊 In Ihrer Altersgruppe sind bereits {employment_percent}% "
                    "beruflich aktiv."
                    "Der häufigste Schutzstatus ist: {protection}."
                ),
                positive_hint="Dein Alter ist eine Stärke – viele starten genau jetzt 🌱",
            ),

            SurveyQuestion(
                step=3,
                question_text="In welchem Bundesland leben Sie derzeit?",
                input_type="select",
                select_api="/api/regions",
                statistic_api="/statistics/migrants/by-region",
                answer_template=(
                    "📍 In {region} arbeiten bereits {employment_percent}% "
                    "der dort lebenden Migrant:innen."
                ),
                positive_hint="Diese Region bietet gute Voraussetzungen für Integration 🤝",
            ),

            SurveyQuestion(
                step=4,
                question_text="In welchem Berufsfeld möchten Sie arbeiten?",
                input_type="select",
                select_api="/api/categories",
                statistic_api="/statistics/salary",
                answer_template=(
                    "💰 Das durchschnittliche Gehalt in {region} "
                    "für {category} beträgt ca. {salary} € brutto."
                ),
                positive_hint="Viele beginnen klein – und entwickeln sich schnell weiter 📈",
            ),

            SurveyQuestion(
                step=5,
                question_text="In welcher Stadt leben Sie?",
                input_type="select",
                select_api="/api/cities",
                statistic_api="/statistics/jobs/by-city",
                answer_template=(
                    "🔎 Aktuell gibt es {vacancies} offene Stellen "
                    "für {category} in {city}."
                ),
                positive_hint="Das sind echte Chancen – und sie wachsen 🚀",
            ),
        ]

        db.add_all(questions)
        await db.commit()

async def main():
    await create_tables()
    await fill_reference_data()
    await create_admin()
    await create_questions()
    print("Datenbank initialisiert!")

if __name__ == "__main__":
    asyncio.run(main())