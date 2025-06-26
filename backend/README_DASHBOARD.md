# 📊 Dashboard COVID-19 & Mpox

Un dashboard interactif moderne pour visualiser et analyser les données COVID-19 et Mpox avec des filtres avancés.

## 🎯 Fonctionnalités

### 📈 Visuels disponibles

1. **Évolution des cas COVID-19** - Courbe temporelle
   - Source: `covid_processed.csv`
   - Type: Graphique en courbes avec échelle temporelle

2. **Nombre de vaccinés par pays** - Barres horizontales
   - Source: `covid_processed.csv`
   - Type: Graphique à barres horizontales avec tri par nombre de vaccinés

3. **Cas totaux Mpox par pays** - Barres verticales
   - Source: `mpox_processed.csv`
   - Type: Graphique à barres verticales avec tri par nombre de cas

4. **Comparaison COVID vs Mpox par pays** - Graphique combiné
   - Sources: `covid_processed.csv` + `mpox_processed.csv`
   - Type: Barres groupées pour comparaison directe

### 🎚️ Filtres disponibles

- **📍 Filtre sur location (pays)**: Sélection multiple de pays
- **📅 Filtre de période sur date**: Sélection de plage de dates

## 🚀 Installation et lancement

### Prérequis

- Python 3.7+
- Connexion internet (pour télécharger les données)

### Installation automatique

```bash
# Depuis le répertoire backend
python run_dashboard.py
```

Ce script va automatiquement :
1. ✅ Vérifier et installer les dépendances
2. 📊 Télécharger et préparer les données
3. 🚀 Lancer le dashboard

### Installation manuelle

Si vous préférez une installation manuelle :

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Préparer les données
cd scripts
python prepare_data.py

# 3. Lancer le dashboard
python dashboard_moderne.py
```

## 🌐 Accès au dashboard

Une fois lancé, le dashboard est accessible à l'adresse :
**http://localhost:8050**

## 📊 Utilisation

### Interface utilisateur

Le dashboard est organisé en sections :

1. **Header** - Titre principal avec icône
2. **Filtres** - Contrôles pour pays et période
3. **Graphiques** - 4 visuels principaux organisés en grille 2x2
4. **Statistiques** - Métriques globales en bas de page

### Navigation

- **Filtre pays** : Sélectionnez un ou plusieurs pays dans la liste déroulante
- **Filtre date** : Choisissez une plage de dates avec le sélecteur de dates
- **Interactivité** : Cliquez sur les graphiques pour plus de détails
- **Zoom** : Utilisez la molette de souris pour zoomer/dézoomer

### Fonctionnalités interactives

- **Hover** : Survolez les points/lignes pour voir les détails
- **Zoom** : Sélectionnez une zone pour zoomer
- **Pan** : Cliquez et glissez pour naviguer
- **Reset** : Double-cliquez pour réinitialiser la vue

## 📁 Structure des données

### COVID-19 (`covid_processed.csv`)
- `date` : Date de l'observation
- `location` : Nom du pays
- `total_cases` : Nombre total de cas
- `new_cases` : Nouveaux cas du jour
- `total_deaths` : Nombre total de décès
- `new_deaths` : Nouveaux décès du jour
- `people_vaccinated` : Nombre de personnes vaccinées
- `total_vaccinations` : Nombre total de vaccinations

### Mpox (`mpox_processed.csv`)
- `date` : Date de confirmation
- `location` : Nom du pays
- `total_cases` : Nombre total de cas
- `new_cases` : Nouveaux cas du jour
- `total_deaths` : Nombre total de décès
- `new_deaths` : Nouveaux décès du jour

## 🛠️ Développement

### Structure du code

```
backend/
├── scripts/
│   ├── dashboard_moderne.py    # Dashboard principal
│   ├── prepare_data.py         # Préparation des données
│   ├── etl_script.py          # Script ETL existant
│   └── dashboard.py           # Ancien dashboard
├── run_dashboard.py           # Script de lancement
└── README_DASHBOARD.md        # Ce fichier
```

### Personnalisation

Pour modifier le dashboard :

1. **Ajouter un nouveau graphique** : Modifiez `dashboard_moderne.py`
2. **Changer les couleurs** : Modifiez la variable `colors`
3. **Ajouter des filtres** : Ajoutez de nouveaux composants dans le layout
4. **Modifier les données** : Éditez `etl_script.py`

## 🔧 Dépannage

### Problèmes courants

**❌ "Module not found"**
```bash
pip install -r requirements.txt
```

**❌ "Port already in use"**
```bash
# Changer le port dans dashboard_moderne.py
app.run_server(debug=True, host='0.0.0.0', port=8051)
```

**❌ "Données non disponibles"**
```bash
# Régénérer les données
cd scripts
python prepare_data.py
```

**❌ "Erreur de téléchargement"**
- Vérifiez votre connexion internet
- Les données COVID-19 viennent d'Our World in Data
- Les données Mpox viennent de Kaggle

### Logs et débogage

Le dashboard affiche des messages informatifs :
- 🚀 Démarrage
- 📊 Chargement des données
- ✅ Succès
- ❌ Erreurs

## 📈 Améliorations futures

- [ ] Export des graphiques en PNG/PDF
- [ ] Notifications en temps réel
- [ ] Mode sombre/clair
- [ ] Graphiques supplémentaires (carte du monde, etc.)
- [ ] API REST pour les données
- [ ] Base de données pour les données historiques

## 🤝 Contribution

Pour contribuer au projet :

1. Fork le repository
2. Créez une branche pour votre fonctionnalité
3. Testez vos modifications
4. Soumettez une pull request

## 📄 Licence

Ce projet utilise des données publiques et est open source.

---

**🎉 Bonne utilisation du dashboard !** 