"""
Script de test pour vérifier le chargement de DATABASE_URL
"""
# Importer le module database pour déclencher le print
import sys
import os

# Ajouter le répertoire parent au chemin Python pour permettre l'importation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Maintenant on peut importer depuis le répertoire parent
from database import DATABASE_URL

print(f"DATABASE_URL = {DATABASE_URL}")
print("Test terminé. Vérifiez l'URL de la base de données ci-dessus.") 