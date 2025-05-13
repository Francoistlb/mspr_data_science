import pandas as pd
from app.core.database import engine

#Chargement des données etl
dfc = pd.read_csv('data/covid_processed.csv')
dfm = pd.read_csv('data/mpox_processed.csv')

dfc.to_sql()





