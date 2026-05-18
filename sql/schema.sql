-- ══════════════════════════════════════════
-- MediSight — Healthcare DB Star Schema
-- ══════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS healthcare_db;
USE healthcare_db;

-- Dimension : Maladies
CREATE TABLE dim_disease (
  id           INT PRIMARY KEY,
  disease_type VARCHAR(50)
);

-- Dimension : Groupes d'âge
CREATE TABLE dim_age_group (
  id         INT PRIMARY KEY,
  group_name VARCHAR(30),
  min_age    INT,
  max_age    INT
);

-- Table de faits : Patients
CREATE TABLE fact_patients (
  patient_id   INT PRIMARY KEY AUTO_INCREMENT,
  age          INT,
  bmi          DOUBLE,
  glucose      DOUBLE,
  disease_id   INT,
  age_group_id INT,
  label        INT,
  FOREIGN KEY (disease_id)   REFERENCES dim_disease(id),
  FOREIGN KEY (age_group_id) REFERENCES dim_age_group(id)
);

-- Données de référence
INSERT INTO dim_disease VALUES
  (1, 'Diabetes'),
  (2, 'Heart Disease');

INSERT INTO dim_age_group VALUES
  (1, 'Jeune',  0,  30),
  (2, 'Adulte', 31, 50),
  (3, 'Senior', 51, 100);