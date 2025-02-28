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