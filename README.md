# Projet d'analyse COVID-19 et Mpox

Ce projet permet d'extraire, transformer, charger et visualiser les données mondiales sur le COVID-19 et le Mpox (anciennement connu sous le nom de monkeypox).

## Fonctionnalités

- Téléchargement automatique des données depuis des sources fiables
- Nettoyage et transformation des données
- Stockage des données dans une base PostgreSQL
- Génération de visualisations comparatives
- Dashboard interactif pour explorer les données
- API REST pour accéder aux données
- Comparaison des tendances entre COVID-19 et Mpox

## Structure du projet

```
mspr_data_science/
│
├── backend/                # API et gestion des données
│   ├── app/
│   │   ├── main.py        # Point d'entrée FastAPI
│   │   ├── models/        # Modèles SQLAlchemy
│   │   ├── schemas/       # Schémas Pydantic
│   │   ├── crud/         # Opérations CRUD
│   │   ├── api/          # Routes API
│   │   └── core/         # Configuration
│   │
│   ├── scripts/          # Scripts utilitaires
│   │   ├── import_db.py  # Import des données
│   │   ├── etl_script.py # Scripts ETL
│   │   └── dashboard.py  # Dashboard Plotly
│   │
│   ├── data/            # Données source
│   │   └── covid_processed.csv
│   │
│   └── requirements.txt  # Dépendances Python
│
└── README.md            # Documentation
```

## Prérequis

- Python 3.8 ou supérieur
- PostgreSQL
- pip (gestionnaire de paquets Python)

## Installation

1. Cloner le projet
```bash
git clone https://github.com/Francoistlb/mspr_data_science.git
cd mspr_data_science
```

2. Configuration de l'environnement backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/MacOS
pip install -r requirements.txt
```

3. Configuration de la base de données
- Créer un fichier `.env` dans le dossier backend :
```env
DATABASE_URL=postgresql://user:password@localhost:5432/mspr_db
```

## Préparation des données (ETL)

1. Exécuter le processus ETL pour télécharger et transformer les données :
```bash
python run.py etl
python run.py analisys
```

Cette étape va :
- Télécharger les données brutes COVID-19 et Mpox
- Nettoyer et transformer les données
- Générer les fichiers CSV traités dans le dossier `data/`

## Mise en place de la base de données

1. Installer PostgreSQL et pgAdmin (sous Windows)

2. Créer et initialiser la base de données :
```bash
/mspr_data_science
python -m backend.app.create_database
python -m backend.app.init_db
```

3. Importer les données préparées :
```bash
python run.py import
```

## Utilisation

Le projet propose plusieurs modes d'utilisation via le script `run.py` :

```bash
python run.py [commande]
```

Commandes disponibles :
- `etl` : Exécution des scripts ETL (préparation des données)
- `import` : Import des données préparées dans la base
- `dashboard` : Lancement du dashboard Plotly
- `start_analysis` : Démarrage de l'analyse des données

### API Backend

Pour lancer l'API :
```bash
cd backend
uvicorn app.main:app --reload
```

L'API sera accessible à :
- Interface : http://localhost:8000
- Documentation Swagger : http://localhost:8000/docs
- Documentation ReDoc : http://localhost:8000/redoc

### Dashboard

Le dashboard interactif comprend trois onglets :

1. **COVID-19**
   - Évolution temporelle des cas/décès/hospitalisations
   - Comparaison entre pays
   - Filtres par pays, métrique et plage de dates

2. **Mpox**
   - Distribution mondiale des cas (carte)
   - Comparaison entre pays
   - Filtres par pays

3. **Comparaison**
   - Tendances temporelles
   - Échelle logarithmique pour comparer les deux maladies
   - Filtres par pays

## Structure des données

### COVID-19
Les données proviennent de "Our World in Data" et contiennent :
- Nombre total de cas par pays
- Nouveaux cas quotidiens
- Décès totaux et nouveaux
- Données sur les hospitalisations
- Données sur la vaccination

### Mpox
Les données proviennent du projet Global.health et contiennent :
- Cas confirmés par pays
- Dates de confirmation
- Distribution géographique

## Développement

- Les modèles de données sont dans `backend/app/models/`
- Les schémas Pydantic sont dans `backend/app/schemas/`
- Les opérations CRUD sont dans `backend/app/crud/`
- Les routes API sont dans `backend/app/api/endpoints/`
- La configuration est dans `backend/app/core/`

## Remarques

Ce projet est à des fins éducatives et d'analyse. Les données sont régulièrement mises à jour par leurs sources respectives. 
