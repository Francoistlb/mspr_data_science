import pandas as pd
from datetime import datetime
from app.core.database import engine

# Chargement des données
dfc = pd.read_csv('data/covid_processed.csv')

# Conversion de la colonne date en datetime
dfc['date'] = pd.to_datetime(dfc['date'])

# Préparation de d_location
locations_df = pd.DataFrame()
locations_df['location_name'] = dfc['location'].unique()

# Import de la dimension location
locations_df.to_sql('d_location', engine, if_exists='replace', index=True, index_label='location_id')

# Création du mapping pour les clés étrangères de location
location_mapping = pd.read_sql('SELECT location_id, location_name FROM d_location', engine)

# Préparation de f_covid
covid_facts = dfc.merge(
    location_mapping,
    left_on='location',
    right_on='location_name'
)

# Sélection des colonnes pour f_covid
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
f_covid.to_sql('f_covid', engine, if_exists='replace', index=True, index_label='covid_fact_id')





