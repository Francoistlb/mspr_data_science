#!/usr/bin/env python3
"""
Script principal pour démarrer l'analyse des données COVID-19 et Mpox.
Ce script exécute l'ETL puis lance le dashboard interactif.
"""

import os
import sys
import subprocess

def main():
    print("=== Démarrage de l'analyse COVID-19 et Mpox ===")
    
    # Vérifier si le dossier de données existe, sinon le créer
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Dossier 'data' créé.")
    
    # Exécuter l'ETL si nécessaire
    if not os.path.exists('data/covid_processed.csv') or not os.path.exists('data/mpox_processed.csv'):
        print("\n=== Démarrage du processus ETL ===")
        try:
            import scripts.etl_script as etl_script
            etl_script.main()
            print("Processus ETL terminé avec succès.")
        except Exception as e:
            print(f"Erreur pendant l'ETL: {e}")
            sys.exit(1)
    else:
        print("\nLes données transformées existent déjà. Utilisation des données existantes.")
        print("Pour forcer la mise à jour des données, supprimez les fichiers dans le dossier 'data'.")
    
    # Démarrer le dashboard
    print("\n=== Démarrage du dashboard interactif ===")
    print("Le dashboard sera accessible à l'adresse: http://127.0.0.1:8050/")
    print("Appuyez sur Ctrl+C pour arrêter le dashboard.")
    
    try:
        import dashboard as dashboard
        dashboard.app.run(debug=False)
    except KeyboardInterrupt:
        print("\nDashboard arrêté par l'utilisateur.")
    except Exception as e:
        print(f"\nErreur pendant l'exécution du dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 