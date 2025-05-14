from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Numeric, ForeignKey, func
)
from backend.app.core.database import Base

class DLocation(Base):
    """Dimension géographique pour stocker les localisations uniques"""
    __tablename__ = 'd_location'
    
    location_id = Column(Integer, primary_key=True)
    location_name = Column(String(100), nullable=False, unique=True)  # Nom du pays/région

class FCovid(Base):
    """Table de faits principale pour les données COVID"""
    __tablename__ = 'f_covid'
    
    covid_fact_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)  # Format: YYYY-MM-DD
    location_id = Column(Integer, ForeignKey('d_location.location_id'), nullable=False)
    
    # Métriques de cas et décès
    total_cases = Column(Numeric(15, 2))
    new_cases = Column(Numeric(15, 2))
    total_deaths = Column(Numeric(15, 2))
    new_deaths = Column(Numeric(15, 2))
    
    # Métriques hospitalières
    icu_patients = Column(Numeric(15, 2))
    hosp_patients = Column(Numeric(15, 2))
    
    # Métriques de vaccination
    total_vaccinations = Column(Numeric(15, 2))
    people_vaccinated = Column(Numeric(15, 2))
    
    # Métadonnées
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class FMpox(Base):
    """Table de faits pour les données MPOX (variole du singe)"""
    __tablename__ = 'f_mpox'

    mpox_fact_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    location_id = Column(Integer, ForeignKey('d_location.location_id'), nullable=False)

    # Métriques similaires à f_covid
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

    # Métadonnées
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())