-- Modèle de base de données amélioré pour le projet OMS - Surveillance des pandémies

-- Table de dimension pour les dates
CREATE TABLE d_date (
    date_id INT PRIMARY KEY, -- Clé primaire 'surrogate' (ex: 20220501)
    full_date DATE NOT NULL, -- La date complète (YYYY-MM-DD)
    day INT, -- Numéro du jour (1-31)
    month INT, -- Numéro du mois (1-12)
    year INT,
    quarter INT, -- Trimestre (1-4)
    week_of_year INT, -- Semaine de l'année
    is_weekend BOOLEAN, -- Indique si c'est un weekend
    is_holiday BOOLEAN -- Indique si c'est un jour férié
);

-- Table de dimension pour les lieux
CREATE TABLE d_location (
    location_id INT PRIMARY KEY, -- Identifiant unique pour chaque lieu
    iso_code VARCHAR(10) NOT NULL, -- Code ISO ou identifiant (ex: OWID_AFR)
    location_name VARCHAR(100) NOT NULL, -- Nom du lieu (ex: Africa)
    continent VARCHAR(50), -- Continent
    region VARCHAR(100), -- Région
    population BIGINT, -- Population totale
    population_density DECIMAL(10,2), -- Densité de population
    median_age DECIMAL(5,2), -- Âge médian
    gdp_per_capita DECIMAL(15,2) -- PIB par habitant
);

-- Table de dimension pour les pandémies
CREATE TABLE d_pandemic (
    pandemic_id INT PRIMARY KEY, -- Identifiant unique de la pandémie
    pandemic_name VARCHAR(50) NOT NULL, -- Nom (COVID-19, MPOX, etc.)
    virus_scientific_name VARCHAR(100), -- Nom scientifique du virus
    start_date DATE, -- Date de début officielle
    end_date DATE, -- Date de fin (NULL si en cours)
    description TEXT, -- Description de la pandémie
    pathogen_type VARCHAR(50) -- Type de pathogène (virus, bactérie, etc.)
);

-- Table de dimension pour les sources de données
CREATE TABLE d_source (
    source_id INT PRIMARY KEY, -- Identifiant unique de la source de données
    source_name VARCHAR(100) NOT NULL, -- Nom de la source (OMS, etc.)
    data_format VARCHAR(10) NOT NULL, -- Format (CSV, JSON, etc.)
    url VARCHAR(255), -- URL de la source
    update_frequency VARCHAR(50), -- Fréquence de mise à jour
    last_updated TIMESTAMP -- Dernière mise à jour
);

-- Table de faits pour les données de pandémie
CREATE TABLE f_pandemic (
    pandemic_fact_id INT PRIMARY KEY, -- Clé primaire artificielle (auto-incr)
    
    location_id INT NOT NULL REFERENCES d_location(location_id),
    date_id INT NOT NULL REFERENCES d_date(date_id),
    pandemic_id INT NOT NULL REFERENCES d_pandemic(pandemic_id),
    source_id INT REFERENCES d_source(source_id), -- Peut être NULL
    
    -- Métriques de base
    total_cases DECIMAL(15,2),
    total_deaths DECIMAL(15,2),
    new_cases DECIMAL(15,2),
    new_deaths DECIMAL(15,2),
    
    -- Métriques lissées
    new_cases_smoothed DECIMAL(15,2),
    new_deaths_smoothed DECIMAL(15,2),
    
    -- Métriques par million
    new_cases_per_million DECIMAL(15,2),
    total_cases_per_million DECIMAL(15,2),
    new_cases_smoothed_per_million DECIMAL(15,2),
    new_deaths_per_million DECIMAL(15,2),
    total_deaths_per_million DECIMAL(15,2),
    new_deaths_smoothed_per_million DECIMAL(15,2),
    
    -- Métriques supplémentaires
    total_recovered DECIMAL(15,2),
    active_cases DECIMAL(15,2),
    serious_or_critical DECIMAL(15,2),
    total_tests DECIMAL(15,2),
    total_tests_per_1m_population DECIMAL(15,2),
    
    -- Métriques de vaccination (si disponibles)
    total_vaccinations DECIMAL(15,2),
    people_vaccinated DECIMAL(15,2),
    people_fully_vaccinated DECIMAL(15,2),
    total_boosters DECIMAL(15,2),
    
    -- Métadonnées
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table pour les variants
CREATE TABLE d_variant (
    variant_id INT PRIMARY KEY,
    pandemic_id INT REFERENCES d_pandemic(pandemic_id),
    variant_name VARCHAR(100) NOT NULL,
    first_detected_date DATE,
    first_detected_location_id INT REFERENCES d_location(location_id),
    description TEXT,
    transmissibility_factor DECIMAL(5,2), -- Facteur de transmissibilité par rapport à la souche originale
    severity_factor DECIMAL(5,2) -- Facteur de sévérité par rapport à la souche originale
);

-- Table pour les mesures sanitaires
CREATE TABLE f_health_measure (
    measure_id INT PRIMARY KEY,
    location_id INT REFERENCES d_location(location_id),
    pandemic_id INT REFERENCES d_pandemic(pandemic_id),
    date_id INT REFERENCES d_date(date_id),
    
    -- Types de mesures
    lockdown_level INT, -- Niveau de confinement (0-5)
    school_closing INT, -- Fermeture des écoles (0-3)
    workplace_closing INT, -- Fermeture des lieux de travail (0-3)
    cancel_public_events INT, -- Annulation d'événements publics (0-2)
    restrictions_on_gatherings INT, -- Restrictions sur les rassemblements (0-4)
    public_transport_closing INT, -- Fermeture des transports publics (0-2)
    stay_at_home_requirements INT, -- Obligation de rester à la maison (0-3)
    restrictions_on_internal_movement INT, -- Restrictions sur les déplacements internes (0-2)
    international_travel_controls INT, -- Contrôles des voyages internationaux (0-4)
    facial_coverings INT, -- Port du masque (0-4)
    
    -- Métadonnées
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Index pour optimiser les requêtes
CREATE INDEX idx_f_pandemic_location ON f_pandemic(location_id);
CREATE INDEX idx_f_pandemic_date ON f_pandemic(date_id);
CREATE INDEX idx_f_pandemic_pandemic ON f_pandemic(pandemic_id);
CREATE INDEX idx_f_health_measure_location ON f_health_measure(location_id);
CREATE INDEX idx_f_health_measure_date ON f_health_measure(date_id);
CREATE INDEX idx_f_health_measure_pandemic ON f_health_measure(pandemic_id);

-- Modèle de base de données normalisé pour le projet OMS - Surveillance des pandémies
-- Basé sur le modèle dbdiagram_normalized.txt

-- Table des pandémies
CREATE TABLE pandemic (
    pandemic_id INT AUTO_INCREMENT PRIMARY KEY,
    pandemic_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Nom de la pandémie (COVID-19, MPOX)'
);

-- Table des localisations
CREATE TABLE location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL COMMENT 'Nom du pays ou de la région',
    iso_code VARCHAR(10) COMMENT 'Code ISO du pays',
    continent VARCHAR(50) COMMENT 'Continent où se trouve le pays',
    population BIGINT COMMENT 'Population totale du pays'
);

-- Table des dates
CREATE TABLE date (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE COMMENT 'Date complète'
);

-- Table des statistiques de pandémie
CREATE TABLE pandemic_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    pandemic_id INT NOT NULL,
    location_id INT NOT NULL,
    date_id INT NOT NULL,
    
    -- Métriques essentielles
    total_cases DECIMAL(15,2) COMMENT 'Nombre total de cas',
    new_cases DECIMAL(15,2) COMMENT 'Nouveaux cas',
    total_deaths DECIMAL(15,2) COMMENT 'Nombre total de décès',
    new_deaths DECIMAL(15,2) COMMENT 'Nouveaux décès',
    total_recovered DECIMAL(15,2) COMMENT 'Nombre total de personnes guéries',
    active_cases DECIMAL(15,2) COMMENT 'Nombre de cas actifs',
    serious_or_critical DECIMAL(15,2) COMMENT 'Nombre de cas graves ou critiques',
    
    -- Métriques par million (utiles pour les comparaisons)
    cases_per_million DECIMAL(15,2) COMMENT 'Cas pour 1M d\'habitants',
    deaths_per_million DECIMAL(15,2) COMMENT 'Décès pour 1M d\'habitants',
    
    -- Métriques de tests
    total_tests DECIMAL(15,2) COMMENT 'Nombre total de tests effectués',
    tests_per_million DECIMAL(15,2) COMMENT 'Tests pour 1M d\'habitants',
    
    -- Contraintes de clés étrangères
    FOREIGN KEY (pandemic_id) REFERENCES pandemic(pandemic_id),
    FOREIGN KEY (location_id) REFERENCES location(location_id),
    FOREIGN KEY (date_id) REFERENCES date(date_id),
    
    -- Contrainte d'unicité
    UNIQUE KEY unique_pandemic_stats (pandemic_id, location_id, date_id)
);

-- Index pour optimiser les requêtes
CREATE INDEX idx_pandemic_stats_pandemic ON pandemic_stats(pandemic_id);
CREATE INDEX idx_pandemic_stats_location ON pandemic_stats(location_id);
CREATE INDEX idx_pandemic_stats_date ON pandemic_stats(date_id);

-- Procédure pour générer les dates (utile pour peupler la table date)
DELIMITER //
CREATE PROCEDURE generate_dates(start_date DATE, end_date DATE)
BEGIN
    DECLARE current_date DATE;
    SET current_date = start_date;
    
    WHILE current_date <= end_date DO
        INSERT IGNORE INTO date (date_id, full_date)
        VALUES (
            CAST(DATE_FORMAT(current_date, '%Y%m%d') AS UNSIGNED), -- Format YYYYMMDD
            current_date
        );
        SET current_date = DATE_ADD(current_date, INTERVAL 1 DAY);
    END WHILE;
END //
DELIMITER ;

CALL generate_dates('2019-01-01', '2023-12-31');

-- Exemple d'utilisation de la procédure pour générer les dates de 2019 à 2023
-- CALL generate_dates('2019-01-01', '2023-12-31');

/*
======================================================================================
EXPLICATION DE LA COMMANDE CALL generate_dates('2019-01-01', '2023-12-31')
======================================================================================

Cette commande appelle la procédure stockée 'generate_dates' avec deux paramètres :
1. '2019-01-01' : Date de début (1er janvier 2019)
2. '2023-12-31' : Date de fin (31 décembre 2023)

Fonctionnement détaillé :
-------------------------
1. La procédure va créer une boucle qui parcourt toutes les dates entre le 1er janvier 2019
   et le 31 décembre 2023 (soit 1826 jours).

2. Pour chaque date, elle insère une ligne dans la table 'date' avec :
   - date_id : un entier au format YYYYMMDD (ex: 20190101 pour le 1er janvier 2019)
   - full_date : la date complète au format SQL (ex: 2019-01-01)

3. La clause INSERT IGNORE permet d'éviter les erreurs si une date existe déjà dans la table.

4. Le format YYYYMMDD pour date_id est choisi car :
   - Il permet un tri chronologique naturel
   - Il est facilement lisible et compréhensible
   - Il peut être utilisé pour des calculs de périodes

Pourquoi cette période (2019-2023) ?
------------------------------------
- 2019 : Inclut la période juste avant le début de la pandémie de COVID-19
- 2023 : Couvre les données récentes, y compris la pandémie de MPOX

Cette plage de dates couvre donc l'ensemble des périodes pertinentes pour l'analyse
des deux pandémies principales de notre étude.

Utilisation dans le projet :
---------------------------
Cette table de dates servira de dimension temporelle dans notre modèle en étoile,
permettant des analyses chronologiques détaillées dans Power BI, comme :
- Évolution des cas au fil du temps
- Comparaisons mois par mois ou année par année
- Identification des pics épidémiques
- Analyse des tendances saisonnières
*/