from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# URL de connexion PostgreSQL (modifie selon ta config)
DATABASE_URL = os.getenv("DATABASE_URL")

# Vérifier si DATABASE_URL est bien chargé
if not DATABASE_URL:
    raise ValueError("DATABASE_URL n'est pas défini dans le fichier .env")

# Créer l'engine SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Créer une session asynchrone
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Définir la base pour les modèles
Base = declarative_base()

# Fonction pour récupérer une session DB
async def get_db():
    async with SessionLocal() as session:
        yield session
