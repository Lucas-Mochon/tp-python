from database import get_session
from models.etudiant import Etudiant

def create_etudiant(nom, prenom, email):
    """Crée un nouvel étudiant"""
    if not (nom and prenom and email):
        print("Nom, prénom et email sont obligatoires.")
        return False

    session = get_session()
    try:
        etudiant = Etudiant(
            nom=nom.strip(),
            prenom=prenom.strip(),
            email=email.strip().lower()
        )
        session.add(etudiant)
        session.commit()
        return True
    except Exception as e:
        print(f"Erreur création étudiant : {e}")
        session.rollback()
        return False
    finally:
        session.close()

def get_all_etudiants():
    """Récupère tous les étudiants"""
    session = get_session()
    try:
        etudiants = session.query(Etudiant).order_by(Etudiant.id_etud).all()
        return [
            {
                "id_etud": e.id_etud,
                "nom": e.nom,
                "prenom": e.prenom,
                "email": e.email,
                "date_inscription": e.date_inscription,
                "solde_amende": float(e.solde_amende)
            }
            for e in etudiants
        ]
    except Exception as e:
        print(f"Erreur récupération étudiants : {e}")
        return []
    finally:
        session.close()

def get_etudiant_by_id(id_etud):
    """Récupère un étudiant par son ID"""
    if not isinstance(id_etud, int):
        print("id_etud doit être un entier.")
        return None

    session = get_session()
    try:
        etudiant = session.query(Etudiant).filter(Etudiant.id_etud == id_etud).first()
        if not etudiant:
            return None
        return {
            "id_etud": etudiant.id_etud,
            "nom": etudiant.nom,
            "prenom": etudiant.prenom,
            "email": etudiant.email,
            "date_inscription": etudiant.date_inscription,
            "solde_amende": float(etudiant.solde_amende)
        }
    except Exception as e:
        print(f"Erreur récupération étudiant : {e}")
        return None
    finally:
        session.close()

def update_etudiant(id_etud, nom=None, prenom=None, email=None, solde_amende=None):
    """Met à jour un étudiant"""
    if not isinstance(id_etud, int):
        print("id_etud doit être un entier.")
        return False

    session = get_session()
    try:
        etudiant = session.query(Etudiant).filter(Etudiant.id_etud == id_etud).first()
        if not etudiant:
            print("Étudiant introuvable.")
            return False

        if nom:
            etudiant.nom = nom.strip()
        if prenom:
            etudiant.prenom = prenom.strip()
        if email:
            etudiant.email = email.strip().lower()
        if solde_amende is not None:
            try:
                solde = float(solde_amende)
                if solde < 0:
                    print("Le solde de l'amende ne peut pas être négatif.")
                    return False
                etudiant.solde_amende = solde
            except ValueError:
                print("Le solde doit être un nombre.")
                return False

        session.commit()
        return True
    except Exception as e:
        print(f"Erreur mise à jour étudiant : {e}")
        session.rollback()
        return False
    finally:
        session.close()

def delete_etudiant(id_etud):
    """Supprime un étudiant"""
    if not isinstance(id_etud, int):
        print("id_etud doit être un entier.")
        return False

    session = get_session()
    try:
        etudiant = session.query(Etudiant).filter(Etudiant.id_etud == id_etud).first()
        if not etudiant:
            print("Étudiant introuvable.")
            return False
        session.delete(etudiant)
        session.commit()
        return True
    except Exception as e:
        print(f"Erreur suppression étudiant : {e}")
        session.rollback()
        return False
    finally:
        session.close()
