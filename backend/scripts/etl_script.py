import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import requests
from io import StringIO

# Création du répertoire pour stocker les données
if not os.path.exists('data'):
    os.makedirs('data')

# URLs des données (sources publiques pour COVID-19 et mpox)
COVID_DATA_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
MPOX_DATA_URL = "https://7rydd2v2ra.execute-api.eu-central-1.amazonaws.com/web/"

def download_data(url, filename):
    """Télécharger les données à partir de l'URL spécifiée"""
    print(f"Téléchargement des données depuis {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifier si la requête a réussi
        
        with open(f"data/{filename}", 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Données enregistrées dans data/{filename}")
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")
        return False

def load_and_clean_covid_data():
    """Charger et nettoyer les données COVID-19"""
    if not os.path.exists('data/covid_data.csv'):
        success = download_data(COVID_DATA_URL, 'covid_data.csv')
        if not success:
            return None
    
    # Chargement des données
    covid_df = pd.read_csv('data/covid_data.csv')
    
    # Nettoyage et transformation
    # Sélection des colonnes pertinentes
    cols_to_keep = ['date', 'location', 'total_cases', 'new_cases', 
                    'total_deaths', 'new_deaths', 'icu_patients',
                    'hosp_patients', 'total_vaccinations', 'people_vaccinated']
    
    covid_df = covid_df[[col for col in cols_to_keep if col in covid_df.columns]]
    
    # Conversion de la date
    covid_df['date'] = pd.to_datetime(covid_df['date'])
    
    # Remplacement des valeurs manquantes
    covid_df = covid_df.fillna({
        'new_cases': 0,
        'new_deaths': 0
    })
    
    return covid_df

def load_and_clean_mpox_data():
    """Charger et nettoyer les données mpox/monkeypox"""
    if not os.path.exists('data/mpox_data.csv'):
        success = download_data(MPOX_DATA_URL, 'mpox_data.csv')
        if not success:
            return None
    
    # Chargement des données
    try:
        mpox_df = pd.read_csv('data/mpox_data.csv')
        
        # Nettoyage et transformation
        # Selon la structure des données, nous pouvons avoir besoin d'ajuster ce code
        if 'Date_confirmation' in mpox_df.columns:
            mpox_df['Date_confirmation'] = pd.to_datetime(mpox_df['Date_confirmation'], errors='coerce')
        
        if 'Country' in mpox_df.columns and 'City' in mpox_df.columns:
            # Agréger les données par pays et par date
            mpox_grouped = mpox_df.groupby(['Country', pd.Grouper(key='Date_confirmation', freq='D')]).size().reset_index(name='cases')
            return mpox_grouped
        else:
            print("Les colonnes attendues ne sont pas présentes. Vérification du schema des données...")
            print(mpox_df.columns.tolist())
            return mpox_df
    except Exception as e:
        print(f"Erreur lors du traitement des données mpox: {e}")
        # Essai avec une structure différente
        return pd.read_csv('data/mpox_data.csv')

def generate_visualizations(covid_df, mpox_df):
    """Générer des visualisations pour les deux jeux de données"""
    # Configurer les styles de plot
    sns.set(style="whitegrid")
    plt.figure(figsize=(15, 10))
    
    # 1. Évolution des cas COVID-19 dans le temps
    if covid_df is not None:
        # Filtrer quelques pays majeurs pour la lisibilité
        major_countries = ['France', 'United States', 'United Kingdom', 'Germany', 'China', 'India', 'Brazil']
        filtered_df = covid_df[covid_df['location'].isin(major_countries)]
        
        plt.subplot(2, 2, 1)
        for country in major_countries:
            country_data = filtered_df[filtered_df['location'] == country]
            if not country_data.empty:
                plt.plot(country_data['date'], country_data['total_cases'], label=country)
        
        plt.title('Évolution des cas COVID-19')
        plt.xlabel('Date')
        plt.ylabel('Nombre total de cas')
        plt.legend()
        plt.tight_layout()
        
        # 2. Taux de vaccination COVID-19
        plt.subplot(2, 2, 2)
        latest_data = covid_df.sort_values('date').groupby('location').last().reset_index()
        # Filtrer pour n'avoir que les pays avec des données de vaccination
        vacc_data = latest_data[latest_data['people_vaccinated'].notna()]
        top_vacc = vacc_data.sort_values('people_vaccinated', ascending=False).head(10)
        
        sns.barplot(x='people_vaccinated', y='location', data=top_vacc)
        plt.title('Pays avec le plus de personnes vaccinées')
        plt.xlabel('Nombre de personnes vaccinées')
        plt.ylabel('Pays')
    
    # 3. Distribution des cas de mpox par pays
    if mpox_df is not None:
        plt.subplot(2, 2, 3)
        
        # Adaptation en fonction de la structure réelle des données
        if 'Country' in mpox_df.columns and 'cases' in mpox_df.columns:
            mpox_by_country = mpox_df.groupby('Country')['cases'].sum().reset_index()
            top_mpox = mpox_by_country.sort_values('cases', ascending=False).head(10)
            sns.barplot(x='cases', y='Country', data=top_mpox)
            plt.title('Pays avec le plus de cas de mpox')
            plt.xlabel('Nombre de cas')
            plt.ylabel('Pays')
        else:
            # Adaptation si la structure est différente
            print("Tentative d'adaptation pour visualiser les données mpox...")
            # Chercher les colonnes potentielles
            country_col = next((col for col in mpox_df.columns if 'country' in col.lower() or 'nation' in col.lower()), None)
            if country_col:
                mpox_by_country = mpox_df[country_col].value_counts().reset_index()
                mpox_by_country.columns = ['Country', 'Count']
                top_mpox = mpox_by_country.head(10)
                sns.barplot(x='Count', y='Country', data=top_mpox)
                plt.title('Distribution des cas de mpox par pays')
                plt.xlabel('Nombre de cas')
                plt.ylabel('Pays')
    
    # 4. Comparaison COVID-19 vs mpox (si possible)
    plt.subplot(2, 2, 4)
    # Cette visualisation dépend de la structure des données mpox
    # Pour l'instant, on ajoute un texte explicatif
    plt.text(0.5, 0.5, "Comparaison COVID-19 vs mpox\n(Nécessite plus de données ou un format commun)", 
            horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('data/covid_mpox_visualizations.png')
    print("Visualisations enregistrées dans data/covid_mpox_visualizations.png")

def main():
    print("Début du processus ETL pour COVID-19 et mpox...")
    
    # Extraction et transformation des données
    covid_df = load_and_clean_covid_data()
    mpox_df = load_and_clean_mpox_data()
    
    # Sauvegarde des données transformées
    if covid_df is not None:
        covid_df.to_csv('data/covid_processed.csv', index=False)
        print("Données COVID-19 transformées enregistrées dans data/covid_processed.csv")
    
    if mpox_df is not None:
        mpox_df.to_csv('data/mpox_processed.csv', index=False)
        print("Données mpox transformées enregistrées dans data/mpox_processed.csv")
    
    # Génération des visualisations
    if covid_df is not None or mpox_df is not None:
        generate_visualizations(covid_df, mpox_df)
    
    print("Processus ETL terminé.")

if __name__ == "__main__":
    main() 