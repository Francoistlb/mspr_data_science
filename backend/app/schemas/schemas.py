from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# ----------- d_date -----------
class DDateBase(BaseModel):
    full_date: date
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]
    quarter: Optional[int]
    week_of_year: Optional[int]
    is_weekend: Optional[bool]

class DDateCreate(DDateBase):
    pass

class DDateRead(DDateBase):
    date_id: int
    class Config:
        orm_mode = True

# ----------- d_location -----------
class DLocationBase(BaseModel):
    location_name: str

class DLocationCreate(DLocationBase):
    pass

class DLocationRead(DLocationBase):
    location_id: int
    class Config:
        orm_mode = True

# ----------- f_covid -----------
class FCovidBase(BaseModel):
    date_id: int
    location_id: int
    total_cases: Optional[float]
    new_cases: Optional[float]
    total_deaths: Optional[float]
    new_deaths: Optional[float]
    icu_patients: Optional[float]
    hosp_patients: Optional[float]
    total_vaccinations: Optional[float]
    people_vaccinated: Optional[float]

class FCovidCreate(FCovidBase):
    pass

class FCovidRead(FCovidBase):
    covid_fact_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
