import uvicorn
import sys
import asyncio
from pathlib import Path
import time

# Ajouter le répertoire parent au PYTHONPATH pour permettre les imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.app.init_db import init_db

async def setup():
    """Initialiser la base de données"""
    print("🔧 Initialisation de la base de données...")
    await init_db()
    print("✅ Base de données initialisée avec succès.")

if __name__ == "__main__":
    # Afficher un message de bienvenue
    print("""
    🚀 Démarrage de l'API COVID-19 & Mpox
    ====================================
    
    Projet MSPR Data Science - EPSI
    """)
    
    # Exécuter l'initialisation de la base de données
    asyncio.run(setup())
    
    print("\n📌 Informations importantes :")
    print("  • URL de l'API : http://localhost:8000")
    print("  • Documentation : http://localhost:8000/docs")
    print("  • Endpoints API : http://localhost:8000/api/...")
    print("\n⏳ Démarrage du serveur...")
    time.sleep(1)  # Petite pause pour laisser le temps de lire
    
    # Démarrer l'API
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 