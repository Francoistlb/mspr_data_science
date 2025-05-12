# MSPR Data Science - Backend API

Ce projet est l'API backend pour le projet MSPR Data Science.

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. Cloner le projet (si ce n'est pas déjà fait)
```bash
git clone <votre-repo>
cd mspr_data_science/backend
```

2. Créer un environnement virtuel Python
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## Configuration

1. Créer un fichier `.env` à la racine du dossier backend avec les variables suivantes :
```env
DATABASE_URL=postgresql://user:password@localhost:5432/mspr_db
```

## Structure du Projet

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py               # Point d'entrée FastAPI
│   ├── models/              # Modèles SQLAlchemy
│   ├── schemas/             # Schémas Pydantic
│   ├── crud/               # Opérations CRUD
│   ├── api/                # Routes API
│   │   └── endpoints/
│   └── core/              # Configuration
│
├── requirements.txt        # Dépendances Python
└── README.md              # Ce fichier
```

## Lancement du serveur

1. Activer l'environnement virtuel (si ce n'est pas déjà fait)
```bash
# Windows
.\venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate
```

2. Lancer le serveur
```bash
uvicorn app.main:app --reload
```

Le serveur sera accessible à l'adresse : http://localhost:8000

Documentation API :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Développement

- Les modèles de données sont définis dans `app/models/`
- Les schémas Pydantic sont dans `app/schemas/`
- Les opérations CRUD sont dans `app/crud/`
- Les routes API sont dans `app/api/endpoints/`
- La configuration est dans `app/core/` 