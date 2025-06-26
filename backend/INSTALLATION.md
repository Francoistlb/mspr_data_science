# 🚀 Guide d'installation du Dashboard

## Installation rapide (3 étapes)

### 1. Récupérer le projet
```bash
git clone [URL_DU_REPO]
cd mspr_data_science
```

### 2. Installer les dépendances
```bash
pip install -r backend/requirements_dashboard.txt
```

### 3. Lancer le dashboard
```bash
cd backend
python launch_dashboard.py
```

### 4. Ouvrir le navigateur
Aller à : **http://localhost:8050**

---

## 🎯 Méthodes de lancement

### Méthode 1 : Script automatique (recommandée)
```bash
cd backend
python launch_dashboard.py
```

### Méthode 2 : Double-clic (Windows)
Double-cliquez sur : `backend/lancer_dashboard.bat`

### Méthode 3 : Lancement direct
```bash
cd backend/scripts
python dashboard_final.py
```

---

## 🔧 Dépannage

### Problème : "Module not found"
```bash
pip install -r backend/requirements_dashboard.txt
```

### Problème : "Port déjà utilisé"
Changez le port dans `dashboard_final.py` ligne 411 :
```python
self.app.run(debug=debug, host='localhost', port=8051)
```

### Problème : "Données non disponibles"
```bash
cd backend/scripts
python etl_script.py
```

---

## 📊 Fonctionnalités

- **4 graphiques interactifs** : COVID, Vaccinés, Mpox, Comparaison
- **Filtres** : Pays et période
- **Interface moderne** avec Dash et Plotly
- **Données en temps réel**

---

## 🎉 C'est tout !

Votre dashboard est maintenant accessible sur **http://localhost:8050** 