from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Boolean, Numeric, ForeignKey, func
)
from backend.app.core.database import Base

class DDate(Base):
    """Dimension temporelle pour stocker les dates uniques"""
    __tablename__ = 'd_date'
    
    date_id = Column(Integer, primary_key=True)
    full_date = Column(Date, nullable=False, unique=True)  # Date complète pour jointure
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    
    # Champs optionnels utiles pour l'analyse
    quarter = Column(Integer)
    week_of_year = Column(Integer)
    is_weekend = Column(Boolean)

class DLocation(Base):
    """Dimension géographique pour stocker les localisations uniques"""
    __tablename__ = 'd_location'
    
    location_id = Column(Integer, primary_key=True)
    location_name = Column(String(100), nullable=False, unique=True)  # Nom du pays/région

class FCovid(Base):
    """Table de faits principale pour les données COVID"""
    __tablename__ = 'f_covid'
    
    covid_fact_id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey('d_date.date_id'), nullable=False)
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
