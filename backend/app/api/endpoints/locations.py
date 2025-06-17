from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backend.app.core.database import get_db
from backend.app.crud.location import (
    creer_pays, obtenir_pays_par_id, liste_pays, obtenir_pays_par_nom, supprimer_pays
)
from backend.app.schemas.schemas import DLocationCreate, DLocationRead

router = APIRouter()

#Récupérer la liste de tous les pays
@router.get("/", response_model=List[DLocationRead])
async def liste_des_pays_fc(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    locations = await liste_pays(db, skip=skip, limit=limit)
    return locations

#Récupérer les informations d'un pays par son identifiant
@router.get("/{location_id}", response_model=DLocationRead)
async def obtenir_pays_fc(
    location_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_location = await obtenir_pays_par_id(db, location_id)
    if db_location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun pays trouvé avec l'identifiant {location_id}"
        )
    return db_location

#Récupérer les informations d'un pays par son nom exact
@router.get("/nom/{location_name}", response_model=DLocationRead)
async def rechercher_pays_par_nom_fc(
    location_name: str, 
    db: AsyncSession = Depends(get_db)
):
    db_location = await obtenir_pays_par_nom(db, location_name)
    if db_location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun pays nommé '{location_name}' n'a été trouvé"
        )
    return db_location 

#Ajouter un nouveau pays à la base de données
@router.post("/", response_model=DLocationRead, status_code=status.HTTP_201_CREATED)
async def creer_pays_fc(
    location: DLocationCreate, 
    db: AsyncSession = Depends(get_db)
):
    # Vérifier si la location existe déjà
    db_location = await obtenir_pays_par_nom(db, location.location_name)
    if db_location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Le pays '{location.location_name}' existe déjà dans la base de données"
        )
    
    return await creer_pays(db, location)

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def supprimer_pays_fc(
    location_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await supprimer_pays(db, location_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun pays trouvé avec l'identifiant {location_id}"
        )
    return None

