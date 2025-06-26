#!/usr/bin/env python3
"""
Script principal pour lancer le dashboard COVID-19 & Mpox
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Lancement du dashboard avec préparation automatique des données"""
    
    # Changer vers le répertoire des scripts
    script_dir = Path(__file__).parent / 'scripts'
    os.chdir(script_dir)
    
    print("Lancement du Dashboard COVID-19 & Mpox")
    print("=" * 50)
    
    # Étape 1: Préparer les données
    print("Etape 1: Préparation des données...")
    try:
        result = subprocess.run([sys.executable, 'prepare_data.py'], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la préparation des données: {e}")
        print(e.stderr)
        return False
    
    # Étape 2: Lancer le dashboard
    print("\nEtape 2: Lancement du dashboard...")
    print("Le dashboard sera accessible à l'adresse: http://localhost:8050")
    print("Appuyez sur Ctrl+C pour arrêter le serveur")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'dashboard_moderne.py'], check=True)
    except KeyboardInterrupt:
        print("\nDashboard arrêté par l'utilisateur")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du lancement du dashboard: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        print("\nEn cas de problème, vérifiez que:")
        print("   - Toutes les dépendances sont installées")
        print("   - Vous avez une connexion internet pour télécharger les données")
        print("   - Le port 8050 n'est pas déjà utilisé")
        sys.exit(1) 