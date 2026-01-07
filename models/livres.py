from database import get_session
from models.livre import Livre

def create_livre(isbn, titre, editeur, annee, stock):
    """Crée un nouveau livre"""
    if not (isbn and titre):
        print("ISBN et titre obligatoires.")
        return False

    try:
        annee = int(annee)
        stock = int(stock)
        if stock < 0:
            print("Stock invalide.")
            return False
    except ValueError:
        print("Année et stock doivent être des nombres.")
        return False

    session = get_session()
    try:
        livre = Livre(
            isbn=isbn.strip(),
            titre=titre.strip(),
            editeur=editeur.strip() if editeur else None,
            annee=annee,
            exemplaires_dispo=stock
        )
        session.add(livre)
        session.commit()
        return True
    except Exception as e:
        print(f"Erreur création livre : {e}")
        session.rollback()
        return False
    finally:
        session.close()

def get_all_livres():
    """Récupère tous les livres"""
    session = get_session()
    try:
        livres = session.query(Livre).order_by(Livre.titre).all()
        return [
            {
                "isbn": l.isbn,
                "titre": l.titre,
                "editeur": l.editeur,
                "annee": l.annee,
                "exemplaires_dispo": l.exemplaires_dispo
            }
            for l in livres
        ]
    except Exception as e:
        print(f"Erreur récupération livres : {e}")
        return []
    finally:
        session.close()

def get_livre_by_isbn(isbn):
    """Récupère un livre par son ISBN"""
    if not isbn:
        return None

    session = get_session()
    try:
        livre = session.query(Livre).filter(Livre.isbn == isbn).first()
        if not livre:
            return None
        return {
            "isbn": livre.isbn,
            "titre": livre.titre,
            "editeur": livre.editeur,
            "annee": livre.annee,
            "exemplaires_dispo": livre.exemplaires_dispo
        }
    except Exception as e:
        print(f"Erreur récupération livre : {e}")
        return None
    finally:
        session.close()

def update_livre(isbn, titre=None, editeur=None, annee=None, exemplaires_dispo=None):
    """Met à jour un livre"""
    if not isbn:
        print("ISBN obligatoire.")
        return False

    session = get_session()
    try:
        livre = session.query(Livre).filter(Livre.isbn == isbn).first()
        if not livre:
            print("Livre introuvable.")
            return False

        if titre:
            livre.titre = titre.strip()
        if editeur:
            livre.editeur = editeur.strip()
        if annee is not None:
            try:
                livre.annee = int(annee)
            except ValueError:
                print("Année invalide.")
                return False
        if exemplaires_dispo is not None:
            try:
                stock = int(exemplaires_dispo)
                if stock < 0:
                    print("Stock invalide.")
                    return False
                livre.exemplaires_dispo = stock
            except ValueError:
                print("Stock invalide.")
                return False

        session.commit()
        return True
    except Exception as e:
        print(f"Erreur mise à jour livre : {e}")
        session.rollback()
        return False
    finally:
        session.close()

def delete_livre(isbn):
    """Supprime un livre"""
    if not isbn:
        print("ISBN obligatoire.")
        return False

    session = get_session()
    try:
        livre = session.query(Livre).filter(Livre.isbn == isbn).first()
        if not livre:
            print("Livre introuvable.")
            return False
        session.delete(livre)
        session.commit()
        return True
    except Exception as e:
        print(f"Erreur suppression livre : {e}")
        session.rollback()
        return False
    finally:
        session.close()
