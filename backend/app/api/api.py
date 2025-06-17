from fastapi import APIRouter
from backend.app.api.endpoints import locations, covid, mpox

api_router = APIRouter()

# Inclusion des différents routers pour chaque partie de l'API
api_router.include_router(
    locations.router,
    prefix="/pays",
    tags=["Pays et localisations"]
)

api_router.include_router(
    covid.router,
    prefix="/covid",
    tags=["Données COVID-19"]
)

api_router.include_router(
    mpox.router,
    prefix="/mpox",
    tags=["Données Mpox"]
)