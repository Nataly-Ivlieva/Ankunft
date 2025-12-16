#  Ankunft+ 🇩🇪

Web application to guide migrants through integration steps in Germany.

## Tech stack
- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Frontend: React + TypeScript
- Auth: JWT

## Features
- Step-by-step survey
- Dynamic statistics based on answers
- Regional and city-based data
- Clean UX with positive guidance

## Run locally
### Backend
```bash
uvicorn app.main:app --reload
cd frontend
npm install
npm run dev

