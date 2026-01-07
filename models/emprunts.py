from database import get_connection
from models.livres import get_livre_by_isbn, update_livre
from models.etudiants import get_etudiant_by_id

def create_emprunt(id_etud, isbn):
    etud = get_etudiant_by_id(id_etud)
    if not etud:
        print("Étudiant introuvable.")
        return False

    livre = get_livre_by_isbn(isbn)
    if not livre:
        print("Livre introuvable.")
        return False

    if livre["exemplaires_dispo"] <= 0:
        print("Aucun exemplaire disponible.")
        return False

    conn = get_connection()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Emprunt (id_etud, isbn) VALUES (%s, %s)",
            (id_etud, isbn)
        )
        update_livre(isbn, exemplaires_dispo=livre["exemplaires_dispo"] - 1)
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur création emprunt : {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

# READ
def get_all_emprunts():
    conn = get_connection()
    if not conn:
        return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Emprunt ORDER BY date_emprunt DESC")
        rows = cur.fetchall()
        result = []
        for r in rows:
            result.append({
                "id_emprunt": r[0],
                "id_etud": r[1],
                "isbn": r[2],
                "date_emprunt": r[3],
                "date_retour": r[4],
                "amende": float(r[5])
            })
        return result
    except Exception as e:
        print(f"Erreur récupération emprunts : {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_emprunts_by_etudiant(id_etud):
    if not isinstance(id_etud, int):
        print("id_etud doit être un entier.")
        return []

    conn = get_connection()
    if not conn:
        return []
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM Emprunt WHERE id_etud=%s ORDER BY date_emprunt DESC",
            (id_etud,)
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            result.append({
                "id_emprunt": r[0],
                "id_etud": r[1],
                "isbn": r[2],
                "date_emprunt": r[3],
                "date_retour": r[4],
                "amende": float(r[5])
            })
        return result
    except Exception as e:
        print(f"Erreur récupération emprunts : {e}")
        return []
    finally:
        cur.close()
        conn.close()


def retour_emprunt(id_emprunt):
    conn = get_connection()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        # Récupérer l'emprunt
        cur.execute("SELECT isbn, date_retour FROM Emprunt WHERE id_emprunt=%s", (id_emprunt,))
        emprunt_row = cur.fetchone()
        if not emprunt_row:
            print("Emprunt introuvable")
            return False

        isbn, date_retour = emprunt_row
        if date_retour is not None:
            print("Livre déjà retourné")
            return False

        cur.execute("UPDATE Emprunt SET date_retour=CURRENT_DATE WHERE id_emprunt=%s", (id_emprunt,))

        livre = get_livre_by_isbn(isbn)
        if livre:
            try:
                stock = int(livre["exemplaires_dispo"]) + 1
                update_livre(isbn, exemplaires_dispo=stock)
            except (TypeError, ValueError):
                print("Impossible de mettre à jour le stock du livre.")
                conn.rollback()
                return False

        conn.commit()
        return True
    except Exception as e:
        print("Erreur retour emprunt :", e)
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

# DELETE
def delete_emprunt(id_emprunt):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Emprunt WHERE id_emprunt=%s", (id_emprunt,))
        conn.commit()
        return True
    except Exception as e:
        print("Erreur:", e)
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
