-- Table des étudiants
CREATE TABLE IF NOT EXISTS Etudiant (
    id_etud SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_inscription DATE DEFAULT CURRENT_DATE,
    solde_amende NUMERIC(5,2) DEFAULT 0 CHECK (solde_amende >= 0)
);

-- Table des livres
CREATE TABLE IF NOT EXISTS Livre (
    isbn CHAR(13) PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    editeur VARCHAR(100),
    annee INT CHECK (annee > 1900 AND annee < 2027),
    exemplaires_dispo INT DEFAULT 1 CHECK (exemplaires_dispo >= 0)
);

-- Table des emprunts
CREATE TABLE IF NOT EXISTS Emprunt (
    id_emprunt SERIAL PRIMARY KEY,
    id_etud INT NOT NULL,
    isbn CHAR(13) NOT NULL,
    date_emprunt DATE NOT NULL DEFAULT CURRENT_DATE,
    date_retour DATE,
    amende NUMERIC(5,2) DEFAULT 0,
    
    -- Contraintes de clé étrangère
    CONSTRAINT fk_etud FOREIGN KEY (id_etud)
        REFERENCES Etudiant(id_etud)
        ON DELETE RESTRICT,
    CONSTRAINT fk_livre FOREIGN KEY (isbn)
        REFERENCES Livre(isbn)
        ON DELETE RESTRICT
);
