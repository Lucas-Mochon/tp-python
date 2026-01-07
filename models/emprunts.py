from database import get_session
from models.emprunt import Emprunt
from models.livre import Livre
from models.etudiant import Etudiant
from datetime import date

def create_emprunt(id_etud, isbn):
    """Crée un nouvel emprunt"""
    session = get_session()
    try:
        # Vérifier l'étudiant
        etudiant = session.query(Etudiant).filter(Etudiant.id_etud == id_etud).first()
        if not etudiant:
            print("Étudiant introuvable.")
            return False

        # Vérifier le livre
        livre = session.query(Livre).filter(Livre.isbn == isbn).first()
        if not livre:
            print("Livre introuvable.")
            return False

        # Vérifier la disponibilité
        if livre.exemplaires_dispo <= 0:
            print("Aucun exemplaire disponible.")
            return False

        # Créer l'emprunt
        emprunt = Emprunt(id_etud=id_etud, isbn=isbn)
        session.add(emprunt)

        # Décrémenter le stock
        livre.exemplaires_dispo -= 1

        session.commit()
        return True
    except Exception as e:
        print(f"Erreur création emprunt : {e}")
        session.rollback()
        return False
    finally:
        session.close()

def get_all_emprunts():
    """Récupère tous les emprunts"""
    session = get_session()
    try:
        emprunts = session.query(Emprunt).order_by(Emprunt.date_emprunt.desc()).all()
        return [
            {
                "id_emprunt": e.id_emprunt,
                "id_etud": e.id_etud,
                "isbn": e.isbn,
                "date_emprunt": e.date_emprunt,
                "date_retour": e.date_retour,
                "amende": float(e.amende)
            }
            for e in emprunts
        ]
    except Exception as e:
        print(f"Erreur récupération emprunts : {e}")
        return []
    finally:
        session.close()

def get_emprunts_by_etudiant(id_etud):
    """Récupère les emprunts d'un étudiant"""
    if not isinstance(id_etud, int):
        print("id_etud doit être un entier.")
        return []

    session = get_session()
    try:
        emprunts = session.query(Emprunt).filter(Emprunt.id_etud == id_etud).order_by(Emprunt.date_emprunt.desc()).all()
        return [
            {
                "id_emprunt": e.id_emprunt,
                "id_etud": e.id_etud,
                "isbn": e.isbn,
                "date_emprunt": e.date_emprunt,
                "date_retour": e.date_retour,
                "amende": float(e.amende)
            }
            for e in emprunts
        ]
    except Exception as e:
        print(f"Erreur récupération emprunts : {e}")
        return []
    finally:
        session.close()

def retour_emprunt(id_emprunt):
    """Enregistre le retour d'un livre"""
    session = get_session()
    try:
        emprunt = session.query(Emprunt).filter(Emprunt.id_emprunt == id_emprunt).first()
        if not emprunt:
            print("Emprunt introuvable.")
            return False

        if emprunt.date_retour is not None:
            print("Livre déjà retourné.")
            return False

        # Enregistrer la date de retour
        emprunt.date_retour = date.today()

        # Incrémenter le stock du livre
        livre = session.query(Livre).filter(Livre.isbn == emprunt.isbn).first()
        if livre:
            livre.exemplaires_dispo += 1

        session.commit()
        return True
    except Exception as e:
        print(f"Erreur retour emprunt : {e}")
        session.rollback()
        return False
    finally:
        session.close()

def delete_emprunt(id_emprunt):
    """Supprime un emprunt"""
    session = get_session()
    try:
        emprunt = session.query(Emprunt).filter(Emprunt.id_emprunt == id_emprunt).first()
        if not emprunt:
            print("Emprunt introuvable.")
            return False
        session.delete(emprunt)
        session.commit()
        return True
    except Exception as e:
        print(f"Erreur suppression emprunt : {e}")
        session.rollback()
        return False
    finally:
        session.close()
