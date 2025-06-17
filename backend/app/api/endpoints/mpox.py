from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date

from backend.app.core.database import get_db
from backend.app.crud.mpox import (
    creer_donnees_mpox, obtenir_donnees_mpox_par_id, liste_donnees_mpox,
    mettre_a_jour_donnees_mpox, supprimer_donnees_mpox
)
from backend.app.schemas.schemas import FMpoxCreate, FMpoxRead
from backend.app.crud.location import obtenir_pays_par_id

router = APIRouter()

@router.get("/", response_model=List[FMpoxRead])
async def liste_donnees_mpox_endpoint(
    skip: int = 0,
    limit: int = 100,
    location_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    return await liste_donnees_mpox(db, skip, limit, location_id, start_date, end_date)

@router.get("/{mpox_fact_id}", response_model=FMpoxRead)
async def obtenir_donnees_mpox_par_id_endpoint(
    mpox_fact_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_mpox = await obtenir_donnees_mpox_par_id(db, mpox_fact_id)
    if db_mpox is None:
        raise HTTPException(status_code=404, detail="Donnée Mpox non trouvée")
    return db_mpox

@router.post("/", response_model=FMpoxRead, status_code=status.HTTP_201_CREATED)
async def creer_donnees_mpox_endpoint(
    mpox_data: FMpoxCreate,
    db: AsyncSession = Depends(get_db)
):
    location = await obtenir_pays_par_id(db, mpox_data.location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Le pays avec l'ID {mpox_data.location_id} n'existe pas dans la base de données"
        )
    return await creer_donnees_mpox(db, mpox_data)

@router.put("/{mpox_fact_id}", response_model=FMpoxRead)
async def mettre_a_jour_donnees_mpox_endpoint(
    mpox_fact_id: int,
    mpox_data: FMpoxCreate,
    db: AsyncSession = Depends(get_db)
):
    """Mettre à jour un enregistrement Mpox existant"""
    location = await obtenir_pays_par_id(db, mpox_data.location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Le pays avec l'ID {mpox_data.location_id} n'existe pas dans la base de données"
        )
    updated_mpox = await mettre_a_jour_donnees_mpox(db, mpox_fact_id, mpox_data)
    if not updated_mpox:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun enregistrement Mpox trouvé avec l'ID {mpox_fact_id}"
        )
    return updated_mpox

@router.delete("/{mpox_fact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def supprimer_donnees_mpox_endpoint(
    mpox_fact_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Supprimer un enregistrement Mpox"""
    result = await supprimer_donnees_mpox(db, mpox_fact_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun enregistrement Mpox trouvé avec l'ID {mpox_fact_id}"
        )
    return None