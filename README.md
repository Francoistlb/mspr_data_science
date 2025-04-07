# Projet d'analyse COVID-19 et Mpox

Ce projet permet d'extraire, transformer, charger et visualiser les données mondiales sur le COVID-19 et le Mpox (anciennement connu sous le nom de monkeypox).

## Fonctionnalités

- Téléchargement automatique des données depuis des sources fiables
- Nettoyage et transformation des données
- Génération de visualisations comparatives
- Dashboard interactif pour explorer les données
- Comparaison des tendances entre COVID-19 et Mpox

## Prérequis

- Python 3.6 ou supérieur
- Les bibliothèques suivantes:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - requests
  - dash
  - plotly

## Installation

1. Clonez ce dépôt sur votre machine locale
2. Installez les dépendances:

```
pip install -r requirements.txt
```

## Utilisation

### Option 1: Script de démarrage complet

Pour démarrer l'analyse complète (ETL + dashboard), exécutez:

```
python start_analysis.py
```

Le script va:
1. Vérifier si les données existent, sinon les télécharger et les transformer
2. Lancer le dashboard interactif accessible à l'adresse http://127.0.0.1:8050/

### Option 2: Exécution des composants individuellement

Pour exécuter seulement le processus ETL:

```
python etl_script.py
```

Pour lancer seulement le dashboard (après avoir exécuté l'ETL):

```
python dashboard.py
```

## Structure des données

### COVID-19
Les données COVID-19 proviennent de "Our World in Data" et contiennent:
- Nombre total de cas par pays
- Nouveaux cas quotidiens
- Décès totaux et nouveaux
- Données sur les hospitalisations
- Données sur la vaccination

### Mpox
Les données Mpox proviennent du projet Global.health et contiennent:
- Cas confirmés par pays
- Dates de confirmation
- Distribution géographique

## Dashboard interactif

Le dashboard interactif comprend trois onglets:

1. **COVID-19**: Visualisation des données COVID-19 avec:
   - Évolution temporelle des cas/décès/hospitalisations
   - Comparaison entre pays
   - Filtres par pays, métrique et plage de dates

2. **Mpox**: Visualisation des données Mpox avec:
   - Distribution mondiale des cas (carte)
   - Comparaison entre pays
   - Filtres par pays

3. **Comparaison**: Analyse comparative entre COVID-19 et Mpox:
   - Tendances temporelles
   - Échelle logarithmique pour comparer les deux maladies
   - Filtres par pays

## Structure du projet

- `etl_script.py`: Script d'extraction, transformation et chargement des données
- `dashboard.py`: Interface utilisateur interactive
- `start_analysis.py`: Script principal qui orchestre l'ensemble du processus
- `requirements.txt`: Liste des dépendances Python
- `data/`: Dossier contenant les données brutes et transformées
- `visualizations/`: Dossier contenant les graphiques générés

## Remarques

Ce projet est à des fins éducatives et d'analyse. Les données sont régulièrement mises à jour par leurs sources respectives. 
