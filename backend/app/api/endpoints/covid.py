from fastapi import APIRouter, Depends, HTTPException, Query, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import date
import logging

# Configurer le logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from backend.app.core.database import get_db
from backend.app.crud.covid import (
    creer_donnees_covid, obtenir_donnees_covid_par_id, liste_donnees_covid, 
    mettre_a_jour_donnees_covid, supprimer_donnees_covid
)
from backend.app.schemas.schemas import FCovidCreate, FCovidRead
from backend.app.crud.location import obtenir_pays_par_id

router = APIRouter()

# GET - Récupérer la liste des données COVID
@router.get("/", response_model=List[FCovidRead])
async def liste_donnees_covid_endpoint(
    skip: int = 0, 
    limit: int = 100,
    location_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await liste_donnees_covid(
            db, 
            skip=skip, 
            limit=limit,
            location_id=location_id,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )

# GET - Récupérer une donnée COVID par son ID
@router.get("/{covid_fact_id}", response_model=FCovidRead)
async def obtenir_donnees_covid_par_id_endpoint(
    covid_fact_id: int, 
    db: AsyncSession = Depends(get_db)
):

    try:
        logger.info(f"Récupération des données COVID avec ID={covid_fact_id}")
        db_covid = await obtenir_donnees_covid_par_id(db, covid_fact_id)
        if db_covid is None:
            logger.warning(f"Aucun enregistrement COVID trouvé avec ID={covid_fact_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucun enregistrement COVID-19 trouvé avec l'ID {covid_fact_id}"
            )
        return db_covid
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données COVID avec ID={covid_fact_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )

# POST - Créer une nouvelle donnée COVID (JSON)
@router.post("/", response_model=FCovidRead, status_code=status.HTTP_201_CREATED)
async def creer_donnees_covid_endpoint(
    covid_data: FCovidCreate, 
    db: AsyncSession = Depends(get_db)
):
    try:
        # Vérifier si le pays existe
        location = await obtenir_pays_par_id(db, covid_data.location_id)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le pays avec l'ID {covid_data.location_id} n'existe pas dans la base de données"
            )
        
        return await creer_donnees_covid(db, covid_data)
    except Exception as e:
        logger.error(f"Erreur lors de la création des données COVID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )

# POST - Créer une nouvelle donnée COVID (Form)
@router.post("/form", response_model=FCovidRead, status_code=status.HTTP_201_CREATED)
async def creer_donnees_covid_form_endpoint(
    date: date = Form(...),
    location_id: int = Form(...),
    total_cases: Optional[float] = Form(None),
    new_cases: Optional[float] = Form(None),
    total_deaths: Optional[float] = Form(None),
    new_deaths: Optional[float] = Form(None),
    icu_patients: Optional[float] = Form(None),
    hosp_patients: Optional[float] = Form(None),
    total_vaccinations: Optional[float] = Form(None),
    people_vaccinated: Optional[float] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Créer l'objet FCovidCreate à partir des données de formulaire
        covid_data = FCovidCreate(
            date=date,
            location_id=location_id,
            total_cases=total_cases,
            new_cases=new_cases,
            total_deaths=total_deaths,
            new_deaths=new_deaths,
            icu_patients=icu_patients,
            hosp_patients=hosp_patients,
            total_vaccinations=total_vaccinations,
            people_vaccinated=people_vaccinated
        )
        
        # Vérifier si le pays existe
        location = await obtenir_pays_par_id(db, covid_data.location_id)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le pays avec l'ID {covid_data.location_id} n'existe pas dans la base de données"
            )
        
        return await creer_donnees_covid(db, covid_data)
    except Exception as e:
        logger.error(f"Erreur lors de la création des données COVID via formulaire: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}"
        )

# PUT - Mettre à jour une donnée COVID existante
@router.put("/{covid_fact_id}", response_model=FCovidRead)
async def mettre_a_jour_donnees_covid_endpoint(
    covid_fact_id: int,
    covid_data: FCovidCreate,
    db: AsyncSession = Depends(get_db)
):
    """Mettre à jour un enregistrement COVID-19 existant"""
    # Vérifier si le pays existe
    location = await obtenir_pays_par_id(db, covid_data.location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Le pays avec l'ID {covid_data.location_id} n'existe pas dans la base de données"
        )
    
    updated_covid = await mettre_a_jour_donnees_covid(db, covid_fact_id, covid_data)
    if not updated_covid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun enregistrement COVID-19 trouvé avec l'ID {covid_fact_id}"
        )
    return updated_covid

# DELETE - Supprimer une donnée COVID
@router.delete("/{covid_fact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def supprimer_donnees_covid_endpoint(
    covid_fact_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Supprimer un enregistrement COVID-19"""
    result = await supprimer_donnees_covid(db, covid_fact_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun enregistrement COVID-19 trouvé avec l'ID {covid_fact_id}"
        )
    return None