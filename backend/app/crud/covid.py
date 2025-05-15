from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional, Dict, Any
from sqlalchemy import func, and_
from datetime import date
from backend.app.models.models import FCovid, DLocation
from backend.app.schemas.schemas import FCovidCreate
from backend.app.crud.location import obtenir_ou_creer_pays


async def creer_donnees_covid(db: AsyncSession, covid_data: FCovidCreate) -> FCovid:
    """Créer un nouvel enregistrement de données COVID"""
    db_covid = FCovid(
        date=covid_data.date,
        location_id=covid_data.location_id,
        total_cases=covid_data.total_cases,
        new_cases=covid_data.new_cases,
        total_deaths=covid_data.total_deaths,
        new_deaths=covid_data.new_deaths,
        icu_patients=covid_data.icu_patients,
        hosp_patients=covid_data.hosp_patients,
        total_vaccinations=covid_data.total_vaccinations,
        people_vaccinated=covid_data.people_vaccinated
    )
    db.add(db_covid)
    await db.commit()
    await db.refresh(db_covid)
    return db_covid


async def creer_donnees_covid_avec_pays(
    db: AsyncSession, 
    covid_data: Dict[str, Any],
    location_name: str
) -> FCovid:
    """Créer un enregistrement COVID avec création automatique du pays si nécessaire"""
    # Récupérer ou créer le pays
    location = await obtenir_ou_creer_pays(db, location_name)
    
    # Construire l'objet FCovidCreate avec les données
    covid_create = FCovidCreate(
        date=covid_data.get("date"),
        location_id=location.location_id,
        total_cases=covid_data.get("total_cases"),
        new_cases=covid_data.get("new_cases"),
        total_deaths=covid_data.get("total_deaths"),
        new_deaths=covid_data.get("new_deaths"),
        icu_patients=covid_data.get("icu_patients"),
        hosp_patients=covid_data.get("hosp_patients"),
        total_vaccinations=covid_data.get("total_vaccinations"),
        people_vaccinated=covid_data.get("people_vaccinated")
    )
    
    # Créer l'enregistrement COVID
    return await creer_donnees_covid(db, covid_create)


async def obtenir_donnees_covid_par_id(db: AsyncSession, covid_fact_id: int) -> Optional[FCovid]:
    """Récupérer un enregistrement COVID par son ID"""
    result = await db.execute(select(FCovid).where(FCovid.covid_fact_id == covid_fact_id))
    return result.scalars().first()


async def liste_donnees_covid(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    location_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[FCovid]:
    """Récupérer une liste d'enregistrements COVID avec filtres optionnels"""
    query = select(FCovid)
    
    # Appliquer les filtres si fournis
    filters = []
    if location_id:
        filters.append(FCovid.location_id == location_id)
    if start_date:
        filters.append(FCovid.date >= start_date)
    if end_date:
        filters.append(FCovid.date <= end_date)
    
    if filters:
        query = query.where(and_(*filters))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def obtenir_statistiques_covid(
    db: AsyncSession,
    location_id: Optional[int] = None
) -> Dict[str, Any]:
    """Récupérer des statistiques agrégées sur les données COVID"""
    # Construit la requête de base
    query = select(
        func.sum(FCovid.total_cases).label("total_cases"),
        func.sum(FCovid.total_deaths).label("total_deaths"),
        func.max(FCovid.date).label("latest_date")
    )
    
    # Ajouter le filtre de location si fourni
    if location_id:
        query = query.where(FCovid.location_id == location_id)
    
    result = await db.execute(query)
    stats = result.fetchone()
    
    # Récupérer les statistiques de vaccination les plus récentes
    vax_query = select(
        func.sum(FCovid.total_vaccinations).label("total_vaccinations"),
        func.sum(FCovid.people_vaccinated).label("people_vaccinated")
    )
    
    if location_id:
        vax_query = vax_query.where(FCovid.location_id == location_id)
    
    vax_result = await db.execute(vax_query)
    vax_stats = vax_result.fetchone()
    
    # Combiner tous les résultats
    return {
        "total_cases": stats.total_cases if stats else 0,
        "total_deaths": stats.total_deaths if stats else 0,
        "latest_date": stats.latest_date if stats else None,
        "total_vaccinations": vax_stats.total_vaccinations if vax_stats else 0,
        "people_vaccinated": vax_stats.people_vaccinated if vax_stats else 0
    }


async def obtenir_evolution_temporelle_covid(
    db: AsyncSession,
    location_id: Optional[int] = None,
    metric: str = "total_cases",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[Dict[str, Any]]:
    """Récupérer une série temporelle pour une métrique spécifique"""
    # Vérifier que la métrique est valide
    valid_metrics = ["total_cases", "new_cases", "total_deaths", "new_deaths", 
                    "icu_patients", "hosp_patients", "total_vaccinations", "people_vaccinated"]
    
    if metric not in valid_metrics:
        raise ValueError(f"Métrique invalide. Doit être l'une de: {', '.join(valid_metrics)}")
    
    # Construction de la requête de base
    query = select(
        FCovid.date,
        FCovid.location_id,
        getattr(FCovid, metric).label("value")
    )
    
    # Joindre avec la table de location pour obtenir les noms
    query = query.join(DLocation, FCovid.location_id == DLocation.location_id)
    query = query.add_columns(DLocation.location_name)
    
    # Appliquer les filtres
    filters = []
    if location_id:
        filters.append(FCovid.location_id == location_id)
    if start_date:
        filters.append(FCovid.date >= start_date)
    if end_date:
        filters.append(FCovid.date <= end_date)
    
    if filters:
        query = query.where(and_(*filters))
    
    # Ordonner par date
    query = query.order_by(FCovid.date)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    # Formatage des résultats
    return [
        {
            "date": row.date.isoformat(),
            "location_id": row.location_id,
            "location_name": row.location_name,
            "value": float(row.value) if row.value is not None else None,
            "metric": metric
        }
        for row in rows
    ]


async def supprimer_donnees_covid(db: AsyncSession, covid_fact_id: int) -> bool:
    """Supprimer un enregistrement COVID par son ID"""
    db_covid = await obtenir_donnees_covid_par_id(db, covid_fact_id)
    if db_covid is None:
        return False
    
    db.delete(db_covid)
    await db.commit()
    return True


async def mettre_a_jour_donnees_covid(
    db: AsyncSession, 
    covid_fact_id: int, 
    covid_data: FCovidCreate
) -> Optional[FCovid]:
    """Mettre à jour un enregistrement COVID existant"""
    # Vérifier si l'enregistrement existe
    db_covid = await obtenir_donnees_covid_par_id(db, covid_fact_id)
    if db_covid is None:
        return None
    
    # Mettre à jour les attributs
    db_covid.date = covid_data.date
    db_covid.location_id = covid_data.location_id
    db_covid.total_cases = covid_data.total_cases
    db_covid.new_cases = covid_data.new_cases
    db_covid.total_deaths = covid_data.total_deaths
    db_covid.new_deaths = covid_data.new_deaths
    db_covid.icu_patients = covid_data.icu_patients
    db_covid.hosp_patients = covid_data.hosp_patients
    db_covid.total_vaccinations = covid_data.total_vaccinations
    db_covid.people_vaccinated = covid_data.people_vaccinated
    
    # Persister les modifications
    await db.commit()
    await db.refresh(db_covid)
    return db_covid


# Alias pour assurer la compatibilité avec le code existant
create_covid_record = creer_donnees_covid
create_covid_record_with_location = creer_donnees_covid_avec_pays
get_covid_record = obtenir_donnees_covid_par_id
get_covid_records = liste_donnees_covid
get_covid_stats = obtenir_statistiques_covid
get_covid_time_series = obtenir_evolution_temporelle_covid
delete_covid_record = supprimer_donnees_covid
update_covid_record = mettre_a_jour_donnees_covid 