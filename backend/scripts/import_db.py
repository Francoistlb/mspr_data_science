import os
import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def get_sync_db():
    # Récupérer l'URL de la base de données depuis les variables d'environnement
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL n'est pas défini dans le fichier .env")
    
    # Convertir l'URL async en URL sync (remplacer postgresql+asyncpg par postgresql+psycopg2)
    SYNC_DATABASE_URL = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    
    # Créer une connexion synchrone
    engine = create_engine(SYNC_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def main():
    # Chargement des données
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'covid_processed.csv')
    dfc = pd.read_csv(data_path)

    # Conversion de la colonne date en datetime
    dfc['date'] = pd.to_datetime(dfc['date'])

    # Obtenir une session de base de données
    db: Session = get_sync_db()
    
    try:
        # Supprimer les tables existantes dans le bon ordre
        print("Suppression des anciennes tables...")
        db.execute(text("DROP TABLE IF EXISTS f_covid"))
        db.execute(text("DROP TABLE IF EXISTS d_location"))
        db.commit()

        # Préparation et import de d_location
        print("Import de la table d_location...")
        locations_df = pd.DataFrame({'location_name': dfc['location'].unique()})
        locations_df.to_sql('d_location', db.bind, if_exists='fail', index=True, index_label='location_id')

        # Récupération des IDs de location
        location_mapping = pd.read_sql('SELECT location_id, location_name FROM d_location', db.bind)

        # Préparation des données COVID avec les clés étrangères
        covid_facts = dfc.merge(
            location_mapping,
            left_on='location',
            right_on='location_name'
        )

        # Sélection des colonnes finales pour f_covid
        f_covid = covid_facts[[
            'date',
            'location_id',
            'total_cases',
            'new_cases',
            'total_deaths',
            'new_deaths',
            'icu_patients',
            'hosp_patients',
            'total_vaccinations',
            'people_vaccinated'
        ]]

        # Import de la table de faits
        print("Import de la table f_covid...")
        f_covid.to_sql('f_covid', db.bind, if_exists='fail', index=True, index_label='covid_fact_id')
        
        # Commit des changements
        db.commit()
        print("Import des données terminé avec succès!")
        
    except Exception as e:
        print(f"Erreur lors de l'import : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()















