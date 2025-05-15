from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from backend.app.models.models import DLocation
from backend.app.schemas.schemas import DLocationCreate


async def creer_pays(db: AsyncSession, location: DLocationCreate) -> DLocation:
    """Créer un nouveau pays"""
    db_location = DLocation(location_name=location.location_name)
    db.add(db_location)
    await db.commit()
    await db.refresh(db_location)
    return db_location


async def obtenir_pays_par_id(db: AsyncSession, location_id: int) -> Optional[DLocation]:
    """Récupérer un pays par son ID"""
    result = await db.execute(select(DLocation).where(DLocation.location_id == location_id))
    return result.scalars().first()


async def obtenir_pays_par_nom(db: AsyncSession, location_name: str) -> Optional[DLocation]:
    """Récupérer un pays par son nom"""
    result = await db.execute(select(DLocation).where(DLocation.location_name == location_name))
    return result.scalars().first()


async def liste_pays(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[DLocation]:
    """Récupérer une liste de pays"""
    result = await db.execute(select(DLocation).offset(skip).limit(limit))
    return result.scalars().all()


async def obtenir_ou_creer_pays(db: AsyncSession, location_name: str) -> DLocation:
    """Récupérer un pays par son nom ou le créer s'il n'existe pas"""
    db_location = await obtenir_pays_par_nom(db, location_name)
    if db_location is None:
        db_location = DLocation(location_name=location_name)
        db.add(db_location)
        await db.commit()
        await db.refresh(db_location)
    return db_location


async def supprimer_pays(db: AsyncSession, location_id: int) -> bool:
    """Supprimer un pays par son ID"""
    db_location = await obtenir_pays_par_id(db, location_id)
    if db_location is None:
        return False
    
    db.delete(db_location)
    await db.commit()
    return True


# Alias pour assurer la compatibilité avec le code existant
create_location = creer_pays
get_location = obtenir_pays_par_id
get_location_by_name = obtenir_pays_par_nom
get_locations = liste_pays
get_or_create_location = obtenir_ou_creer_pays
delete_location = supprimer_pays 