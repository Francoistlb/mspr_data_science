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