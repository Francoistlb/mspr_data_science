#!/usr/bin/env python3
"""
Script pour préparer les données avant le lancement du dashboard
"""

import os
import sys
import subprocess
import pandas as pd
from datetime import datetime

def check_dependencies():
    """Vérifier que toutes les dépendances sont installées"""
    required_packages = [
        'pandas', 'numpy', 'dash', 'plotly', 'requests', 'kagglehub'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Packages manquants: {', '.join(missing_packages)}")
        print("Installation des dépendances...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("Dépendances installées avec succès!")
    else:
        print("Toutes les dépendances sont installées")

def create_data_directory():
    """Créer le répertoire de données s'il n'existe pas"""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Répertoire 'data' créé")
    else:
        print("Répertoire 'data' existe déjà")

def run_etl():
    """Exécuter le script ETL"""
    print("Exécution du script ETL...")
    try:
        # Importer et exécuter le script ETL
        import etl_script
        etl_script.main()
        print("Script ETL exécuté avec succès!")
        return True
    except Exception as e:
        print(f"Erreur lors de l'exécution de l'ETL: {e}")
        return False

def verify_data():
    """Vérifier que les données ont été générées correctement"""
    required_files = ['covid_processed.csv', 'mpox_processed.csv']
    
    for file in required_files:
        file_path = os.path.join('data', file)
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                print(f"OK {file}: {len(df)} lignes, {len(df.columns)} colonnes")
                
                # Afficher un aperçu des colonnes
                print(f"   Colonnes: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
                
                # Afficher les premières lignes
                print(f"   Aperçu: {df.head(2).to_string()}")
                print()
            except Exception as e:
                print(f"Erreur lors de la lecture de {file}: {e}")
        else:
            print(f"Fichier manquant: {file}")
            return False
    
    return True

def main():
    """Fonction principale"""
    print("Préparation des données pour le dashboard...")
    print("=" * 50)
    
    # Vérifier les dépendances
    check_dependencies()
    print()
    
    # Créer le répertoire de données
    create_data_directory()
    print()
    
    # Vérifier si les données existent déjà
    if os.path.exists('data/covid_processed.csv') and os.path.exists('data/mpox_processed.csv'):
        print("Les données transformées existent déjà")
        if verify_data():
            print("Données prêtes pour le dashboard!")
            return True
        else:
            print("Données corrompues, régénération...")
    
    # Exécuter l'ETL
    if run_etl():
        print()
        if verify_data():
            print("Données prêtes pour le dashboard!")
            return True
    
    print("Echec de la préparation des données")
    return False

if __name__ == '__main__':
    success = main()
    if success:
        print("\nVous pouvez maintenant lancer le dashboard avec:")
        print("python dashboard_moderne.py")
    else:
        print("\nVérifiez les erreurs ci-dessus et réessayez") 