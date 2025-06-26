# 📊 Dashboard COVID-19 & Mpox - Version Finale

**Dashboard interactif moderne et robuste pour visualiser les données COVID-19 et Mpox**

## 🎯 Fonctionnalités

### 📈 Visuels disponibles
1. **Évolution des cas COVID-19** - Courbe temporelle
2. **Nombre de vaccinés par pays** - Barres horizontales  
3. **Cas totaux Mpox par pays** - Barres verticales
4. **Comparaison COVID vs Mpox par pays** - Barres groupées

### 🎚️ Filtres interactifs
- **📍 Filtre sur location (pays)** : Sélection multiple
- **📅 Filtre de période sur date** : Plage de dates

## 🚀 Installation rapide

### 1. Installer les dépendances
```bash
cd backend
pip install -r requirements_dashboard.txt
```

### 2. Lancer le dashboard
```bash
python launch_dashboard.py
```

### 3. Accéder au dashboard
Ouvrez votre navigateur : **http://localhost:8050**

## 📁 Structure du projet

```
backend/
├── scripts/
│   ├── dashboard_final.py      # Dashboard principal (version finale)
│   ├── etl_script.py          # Script ETL pour les données
│   ├── data/                  # Données transformées
│   │   ├── covid_processed.csv
│   │   └── mpox_processed.csv
│   └── dashboard_moderne.py   # Ancienne version (à ignorer)
├── launch_dashboard.py        # Script de lancement
├── requirements_dashboard.txt  # Dépendances
└── README_FINAL.md           # Ce fichier
```

## 🔧 Utilisation

### Lancement simple
```bash
# Depuis le dossier backend
python launch_dashboard.py
```

### Lancement manuel
```bash
cd scripts
python dashboard_final.py
```

## ✨ Avantages de cette version

### ✅ **Sans bugs**
- Gestion d'erreurs robuste
- Logging détaillé
- Vérification des données
- Callbacks sécurisés

### ✅ **Architecture propre**
- Code orienté objet
- Séparation des responsabilités
- Documentation complète
- Structure modulaire

### ✅ **Interface moderne**
- Design responsive
- Thème cohérent
- Interactions fluides
- Graphiques interactifs

### ✅ **Maintenance facile**
- Code commenté
- Variables configurables
- Extensible
- Tests intégrés

## 🛠️ Personnalisation

### Changer les couleurs
Modifiez la variable `colors` dans `dashboard_final.py` :
```python
self.colors = {
    'background': '#f8f9fa',
    'text': '#2c3e50',
    'primary': '#3498db',
    'secondary': '#e74c3c',
    'success': '#27ae60',
    'warning': '#f39c12'
}
```

### Ajouter un nouveau graphique
1. Ajoutez le composant dans `_setup_layout()`
2. Créez la méthode de génération
3. Ajoutez le callback

### Changer le port
Modifiez dans `dashboard_final.py` :
```python
dashboard.run(port=8051)  # Au lieu de 8050
```

## 🔍 Dépannage

### Problème : "Module not found"
```bash
pip install -r requirements_dashboard.txt
```

### Problème : "Données non disponibles"
```bash
cd scripts
python etl_script.py
```

### Problème : "Port déjà utilisé"
Changez le port dans `dashboard_final.py` ou arrêtez l'application qui utilise le port 8050.

### Problème : "Erreur de connexion"
- Vérifiez votre pare-feu
- Essayez `localhost:8050` au lieu de `127.0.0.1:8050`

## 📊 Sources de données

- **COVID-19** : Our World in Data (https://covid.ourworldindata.org/)
- **Mpox** : Kaggle Dataset (utkarshx27/mpox-monkeypox-data)

## 🎨 Fonctionnalités avancées

### Interactivité
- **Hover** : Survolez pour voir les détails
- **Zoom** : Molette de souris pour zoomer
- **Pan** : Cliquez et glissez pour naviguer
- **Reset** : Double-cliquez pour réinitialiser

### Filtres dynamiques
- **Pays** : Sélection multiple avec recherche
- **Dates** : Sélecteur de plage avec validation
- **Mise à jour automatique** : Les graphiques se mettent à jour instantanément

### Statistiques en temps réel
- **Cas totaux** : Nombre maximum de cas dans la période
- **Décès totaux** : Nombre maximum de décès
- **Vaccinés** : Nombre de personnes vaccinées

## 🔒 Sécurité

- Validation des entrées utilisateur
- Gestion des erreurs de données
- Protection contre les injections
- Logs de sécurité

## 📈 Performance

- Chargement optimisé des données
- Mise en cache des graphiques
- Rendu asynchrone
- Compression des assets

## 🤝 Contribution

1. Fork le repository
2. Créez une branche pour votre fonctionnalité
3. Testez vos modifications
4. Soumettez une pull request

## 📄 Licence

Ce projet utilise des données publiques et est open source.

---

## 🎉 **Votre dashboard est prêt !**

**Fichiers principaux à utiliser :**
- `dashboard_final.py` - Dashboard principal
- `launch_dashboard.py` - Script de lancement
- `requirements_dashboard.txt` - Dépendances

**Commande de lancement :**
```bash
python launch_dashboard.py
```

**Accès :** http://localhost:8050

---

*Dashboard créé avec ❤️ pour l'analyse de données COVID-19 et Mpox* 