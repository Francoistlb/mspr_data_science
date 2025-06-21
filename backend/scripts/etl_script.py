import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import requests
from io import StringIO
import kagglehub

# Création du répertoire pour stocker les données
if not os.path.exists('data'):
    os.makedirs('data')

# URLs des données (sources publiques pour COVID-19 et mpox)
COVID_DATA_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
# MPOX_DATA_URL = "https://7rydd2v2ra.execute-api.eu-central-1.amazonaws.com/web/lastest.csv"
MPOX_KAGGLE_DATASET = "utkarshx27/mpox-monkeypox-data"

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

    # Effacer les doublons 
    covid_df.drop_duplicates(inplace=True)
    
    return covid_df

def load_and_clean_mpox_data():
    """Charger et nettoyer les données mpox/monkeypox"""
    try:
        # Télécharger les données depuis Kaggle
        print(f"Téléchargement des données mpox depuis Kaggle dataset {MPOX_KAGGLE_DATASET}...")
        dataset_path = kagglehub.dataset_download(MPOX_KAGGLE_DATASET)
        print(f"Données téléchargées dans: {dataset_path}")
        
        # Trouver le fichier CSV principal dans le dossier téléchargé
        csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
        if not csv_files:
            print("Aucun fichier CSV trouvé dans les données téléchargées.")
            return None
            
        # Utiliser le premier fichier CSV trouvé
        mpox_file = os.path.join(dataset_path, csv_files[0])
        print(f"Utilisation du fichier: {mpox_file}")
        
        # Copier le fichier dans notre dossier data
        mpox_df = pd.read_csv(mpox_file)
        mpox_df.to_csv('data/mpox_data.csv', index=False)
        print("Données mpox copiées dans data/mpox_data.csv")
        
        # Afficher les colonnes disponibles pour le débogage
        print("Colonnes disponibles dans le fichier Kaggle:")
        print(mpox_df.columns.tolist())
        
        # Colonnes requises selon le modèle FMpox
        required_cols = [
            'location', 'date', 
            'total_cases', 'total_deaths', 'new_cases', 'new_deaths', 
            'new_cases_smoothed', 'new_deaths_smoothed', 
            'new_cases_per_million', 'total_cases_per_million', 
            'new_cases_smoothed_per_million', 'new_deaths_per_million', 
            'total_deaths_per_million', 'new_deaths_smoothed_per_million'
        ]

        # Vérifier quelles colonnes sont présentes et lesquelles manquent
        available_cols = [col for col in required_cols if col in mpox_df.columns]
        missing_cols = [col for col in required_cols if col not in mpox_df.columns]

        # Afficher un avertissement si des colonnes sont absentes
        if missing_cols:
            print(f"⚠️ Attention : les colonnes suivantes sont absentes du fichier CSV et seront ignorées : {missing_cols}")

        # Garder uniquement les colonnes disponibles parmi les requises
        mpox_clean_df = mpox_df[available_cols].copy()


        # Conversion de la date (si présente)
        if 'date' in mpox_clean_df.columns:
            mpox_clean_df['date'] = pd.to_datetime(mpox_clean_df['date'], errors='coerce')
        else:
            print("⚠️ Colonne 'date' absente : aucune conversion possible.")

        # Remplacement des valeurs manquantes (NaN)
        mpox_clean_df = mpox_clean_df.fillna(0)

        # drop les doublons :
        mpox_clean_df.drop_duplicates(inplace=True)


    except Exception as e:
        print(f"Erreur lors du traitement des données mpox: {e}")
        return None
    
    return mpox_clean_df

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
        if 'location' in mpox_df.columns and 'total_cases' in mpox_df.columns:
            mpox_by_country = mpox_df.groupby('location')['total_cases'].sum().reset_index()
            top_mpox = mpox_by_country.sort_values('total_cases', ascending=False).head(10)
            sns.barplot(x='total_cases', y='location', data=top_mpox)
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
                mpox_by_country.columns = ['location', 'Count']
                top_mpox = mpox_by_country.head(10)
                sns.barplot(x='Count', y='location', data=top_mpox)
                plt.title('Distribution des cas de mpox par pays')
                plt.xlabel('Nombre de cas')
                plt.ylabel('Pays')
    
    # 4. Comparaison COVID-19 vs mpox (si possible)
    plt.subplot(2, 2, 4)
    # Cette visualisation dépend de la structure des données mpox
    if covid_df is not None and mpox_df is not None and 'location' in mpox_df.columns and 'total_cases' in mpox_df.columns:
        # Trouver les pays communs aux deux datasets
        common_countries = set(covid_df['location'].unique()).intersection(set(mpox_df['location'].unique()))
        if common_countries:
            # Sélectionner quelques pays communs (max 5)
            selected_countries = list(common_countries)[:5]
            
            # Créer un dataframe comparatif
            compare_data = []
            
            for country in selected_countries:
                covid_cases = covid_df[covid_df['location'] == country]['total_cases'].max()
                mpox_cases = mpox_df[mpox_df['location'] == country]['total_cases'].max()
                
                compare_data.append({
                    'Pays': country,
                    'COVID-19': covid_cases if not pd.isna(covid_cases) else 0,
                    'Mpox': mpox_cases if not pd.isna(mpox_cases) else 0
                })
            
            compare_df = pd.DataFrame(compare_data)
            compare_df = compare_df.melt(id_vars=['Pays'], var_name='Maladie', value_name='Cas')
            
            # Graphique
            sns.barplot(x='Pays', y='Cas', hue='Maladie', data=compare_df)
            plt.title('Comparaison COVID-19 vs Mpox')
            plt.ylabel('Nombre total de cas')
            plt.yscale('log')  # Échelle logarithmique pour mieux voir les différences
            plt.legend(title='')
        else:
            plt.text(0.5, 0.5, "Comparaison impossible : aucun pays commun entre les datasets", 
                    horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
            plt.axis('off')
    else:
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