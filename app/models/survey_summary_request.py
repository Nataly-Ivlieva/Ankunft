from pydantic import BaseModel

class SurveySummaryRequest(BaseModel):
    country_id: int
    age_id: int
    region_id: int
    category_id: int
    city_id: int
