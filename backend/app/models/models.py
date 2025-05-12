from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey, Numeric, BigInteger, func
)
from backend.app.core.database import Base

class DDate(Base):
    __tablename__ = 'd_date'
    date_id = Column(Integer, primary_key=True)
    full_date = Column(Date, nullable=False)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    quarter = Column(Integer)
    week_of_year = Column(Integer)
    is_weekend = Column(Boolean)
    is_holiday = Column(Boolean)

class DLocation(Base):
    __tablename__ = 'd_location'
    location_id = Column(Integer, primary_key=True)
    iso_code = Column(String(10), nullable=False)
    location_name = Column(String(100), nullable=False)
    continent = Column(String(50))
    region = Column(String(100))
    population = Column(BigInteger)
    population_density = Column(Numeric(10, 2))
    median_age = Column(Numeric(5, 2))
    gdp_per_capita = Column(Numeric(15, 2))

class DPandemic(Base):
    __tablename__ = 'd_pandemic'
    pandemic_id = Column(Integer, primary_key=True)
    pandemic_name = Column(String(50), nullable=False)
    virus_scientific_name = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    pathogen_type = Column(String(50))

class DSource(Base):
    __tablename__ = 'd_source'
    source_id = Column(Integer, primary_key=True)
    source_name = Column(String(100), nullable=False)
    data_format = Column(String(10), nullable=False)
    url = Column(String(255))
    update_frequency = Column(String(50))
    last_updated = Column(DateTime)

class FPandemic(Base):
    __tablename__ = 'f_pandemic'
    pandemic_fact_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('d_location.location_id'), nullable=False)
    date_id = Column(Integer, ForeignKey('d_date.date_id'), nullable=False)
    pandemic_id = Column(Integer, ForeignKey('d_pandemic.pandemic_id'), nullable=False)
    source_id = Column(Integer, ForeignKey('d_source.source_id'))

    total_cases = Column(Numeric(15, 2))
    total_deaths = Column(Numeric(15, 2))
    new_cases = Column(Numeric(15, 2))
    new_deaths = Column(Numeric(15, 2))
    new_cases_smoothed = Column(Numeric(15, 2))
    new_deaths_smoothed = Column(Numeric(15, 2))
    new_cases_per_million = Column(Numeric(15, 2))
    total_cases_per_million = Column(Numeric(15, 2))
    new_cases_smoothed_per_million = Column(Numeric(15, 2))
    new_deaths_per_million = Column(Numeric(15, 2))
    total_deaths_per_million = Column(Numeric(15, 2))
    new_deaths_smoothed_per_million = Column(Numeric(15, 2))
    total_recovered = Column(Numeric(15, 2))
    active_cases = Column(Numeric(15, 2))
    serious_or_critical = Column(Numeric(15, 2))
    total_tests = Column(Numeric(15, 2))
    total_tests_per_1m_population = Column(Numeric(15, 2))
    total_vaccinations = Column(Numeric(15, 2))
    people_vaccinated = Column(Numeric(15, 2))
    people_fully_vaccinated = Column(Numeric(15, 2))
    total_boosters = Column(Numeric(15, 2))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class DVariant(Base):
    __tablename__ = 'd_variant'
    variant_id = Column(Integer, primary_key=True)
    pandemic_id = Column(Integer, ForeignKey('d_pandemic.pandemic_id'))
    variant_name = Column(String(100), nullable=False)
    first_detected_date = Column(Date)
    first_detected_location_id = Column(Integer, ForeignKey('d_location.location_id'))
    description = Column(Text)
    transmissibility_factor = Column(Numeric(5, 2))
    severity_factor = Column(Numeric(5, 2))

class FHealthMeasure(Base):
    __tablename__ = 'f_health_measure'
    measure_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('d_location.location_id'))
    pandemic_id = Column(Integer, ForeignKey('d_pandemic.pandemic_id'))
    date_id = Column(Integer, ForeignKey('d_date.date_id'))

    lockdown_level = Column(Integer)
    school_closing = Column(Integer)
    workplace_closing = Column(Integer)
    cancel_public_events = Column(Integer)
    restrictions_on_gatherings = Column(Integer)
    public_transport_closing = Column(Integer)
    stay_at_home_requirements = Column(Integer)
    restrictions_on_internal_movement = Column(Integer)
    international_travel_controls = Column(Integer)
    facial_coverings = Column(Integer)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
