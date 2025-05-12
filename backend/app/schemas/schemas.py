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
    is_holiday: Optional[bool]

class DDateCreate(DDateBase):
    date_id: int

class DDateRead(DDateBase):
    date_id: int
    class Config:
        orm_mode = True

# ----------- d_location -----------
class DLocationBase(BaseModel):
    iso_code: str
    location_name: str
    continent: Optional[str]
    region: Optional[str]
    population: Optional[int]
    population_density: Optional[float]
    median_age: Optional[float]
    gdp_per_capita: Optional[float]

class DLocationCreate(DLocationBase):
    pass

class DLocationRead(DLocationBase):
    location_id: int
    class Config:
        orm_mode = True

# ----------- d_pandemic -----------
class DPandemicBase(BaseModel):
    pandemic_name: str
    virus_scientific_name: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    description: Optional[str]
    pathogen_type: Optional[str]

class DPandemicCreate(DPandemicBase):
    pass

class DPandemicRead(DPandemicBase):
    pandemic_id: int
    class Config:
        orm_mode = True

# ----------- d_source -----------
class DSourceBase(BaseModel):
    source_name: str
    data_format: str
    url: Optional[str]
    update_frequency: Optional[str]
    last_updated: Optional[datetime]

class DSourceCreate(DSourceBase):
    pass

class DSourceRead(DSourceBase):
    source_id: int
    class Config:
        orm_mode = True

# ----------- f_pandemic -----------
class FPandemicBase(BaseModel):
    location_id: int
    date_id: int
    pandemic_id: int
    source_id: Optional[int]
    total_cases: Optional[float]
    total_deaths: Optional[float]
    new_cases: Optional[float]
    new_deaths: Optional[float]
    new_cases_smoothed: Optional[float]
    new_deaths_smoothed: Optional[float]
    new_cases_per_million: Optional[float]
    total_cases_per_million: Optional[float]
    new_cases_smoothed_per_million: Optional[float]
    new_deaths_per_million: Optional[float]
    total_deaths_per_million: Optional[float]
    new_deaths_smoothed_per_million: Optional[float]
    total_recovered: Optional[float]
    active_cases: Optional[float]
    serious_or_critical: Optional[float]
    total_tests: Optional[float]
    total_tests_per_1m_population: Optional[float]
    total_vaccinations: Optional[float]
    people_vaccinated: Optional[float]
    people_fully_vaccinated: Optional[float]
    total_boosters: Optional[float]

class FPandemicCreate(FPandemicBase):
    pass

class FPandemicRead(FPandemicBase):
    pandemic_fact_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

# ----------- d_variant -----------
class DVariantBase(BaseModel):
    pandemic_id: Optional[int]
    variant_name: str
    first_detected_date: Optional[date]
    first_detected_location_id: Optional[int]
    description: Optional[str]
    transmissibility_factor: Optional[float]
    severity_factor: Optional[float]

class DVariantCreate(DVariantBase):
    pass

class DVariantRead(DVariantBase):
    variant_id: int
    class Config:
        orm_mode = True

# ----------- f_health_measure -----------
class FHealthMeasureBase(BaseModel):
    location_id: Optional[int]
    pandemic_id: Optional[int]
    date_id: Optional[int]
    lockdown_level: Optional[int]
    school_closing: Optional[int]
    workplace_closing: Optional[int]
    cancel_public_events: Optional[int]
    restrictions_on_gatherings: Optional[int]
    public_transport_closing: Optional[int]
    stay_at_home_requirements: Optional[int]
    restrictions_on_internal_movement: Optional[int]
    international_travel_controls: Optional[int]
    facial_coverings: Optional[int]

class FHealthMeasureCreate(FHealthMeasureBase):
    pass

class FHealthMeasureRead(FHealthMeasureBase):
    measure_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
