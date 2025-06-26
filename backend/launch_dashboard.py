#!/usr/bin/env python3
"""
Script de lancement du Dashboard COVID-19 & Mpox
Version finale - Sans bugs
"""

import os
import sys
import subprocess
from pathlib import Path

def check_data_files():
    """Vérifier que les fichiers de données existent"""
    data_dir = Path(__file__).parent / 'scripts' / 'data'
    
    covid_file = data_dir / 'covid_processed.csv'
    mpox_file = data_dir / 'mpox_processed.csv'
    
    if not covid_file.exists():
        print("❌ Fichier covid_processed.csv manquant")
        print("💡 Exécutez d'abord le script ETL pour générer les données")
        return False
    
    if not mpox_file.exists():
        print("⚠️ Fichier mpox_processed.csv manquant - données Mpox non disponibles")
    
    print("✅ Fichiers de données trouvés")
    return True

def launch_dashboard():
    """Lancer le dashboard"""
    try:
        # Changer vers le répertoire des scripts
        script_dir = Path(__file__).parent / 'scripts'
        os.chdir(script_dir)
        
        print("🚀 Lancement du Dashboard COVID-19 & Mpox")
        print("=" * 50)
        
        # Vérifier les données
        if not check_data_files():
            return False
        
        # Lancer le dashboard
        print("\n📊 Démarrage du serveur...")
        print("🌐 Le dashboard sera accessible à l'adresse: http://localhost:8050")
        print("⏹️ Appuyez sur Ctrl+C pour arrêter le serveur")
        print("-" * 50)
        
        # Lancer le dashboard final
        subprocess.run([sys.executable, 'dashboard_final.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard arrêté par l'utilisateur")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = launch_dashboard()
    if not success:
        print("\n💡 Solutions possibles:")
        print("   1. Vérifiez que les données sont générées (exécutez l'ETL)")
        print("   2. Vérifiez que le port 8050 n'est pas utilisé")
        print("   3. Vérifiez que toutes les dépendances sont installées")
        sys.exit(1) 