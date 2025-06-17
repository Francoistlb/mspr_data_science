from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from sqlalchemy import and_
from datetime import date
from backend.app.models.models import FMpox
from backend.app.schemas.schemas import FMpoxCreate

async def creer_donnees_mpox(db: AsyncSession, mpox_data: FMpoxCreate) -> FMpox:
    db_mpox = FMpox(
        date=mpox_data.date,
        location_id=mpox_data.location_id,
        cases=mpox_data.cases
    )
    db.add(db_mpox)
    await db.commit()
    await db.refresh(db_mpox)
    return db_mpox

async def obtenir_donnees_mpox_par_id(db: AsyncSession, mpox_fact_id: int) -> Optional[FMpox]:
    result = await db.execute(select(FMpox).where(FMpox.mpox_fact_id == mpox_fact_id))
    return result.scalars().first()

async def liste_donnees_mpox(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    location_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[FMpox]:
    query = select(FMpox)
    filters = []
    if location_id:
        filters.append(FMpox.location_id == location_id)
    if start_date:
        filters.append(FMpox.date >= start_date)
    if end_date:
        filters.append(FMpox.date <= end_date)
    if filters:
        query = query.where(and_(*filters))
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def mettre_a_jour_donnees_mpox(db: AsyncSession, mpox_fact_id: int, mpox_data: FMpoxCreate) -> Optional[FMpox]:
    db_mpox = await obtenir_donnees_mpox_par_id(db, mpox_fact_id)
    if db_mpox is None:
        return None
    db_mpox.date = mpox_data.date
    db_mpox.location_id = mpox_data.location_id
    db_mpox.cases = mpox_data.cases
    await db.commit()
    await db.refresh(db_mpox)
    return db_mpox

async def supprimer_donnees_mpox(db: AsyncSession, mpox_fact_id: int) -> bool:
    db_mpox = await obtenir_donnees_mpox_par_id(db, mpox_fact_id)
    if db_mpox is None:
        return False
    await db.delete(db_mpox)
    await db.commit()
    return True