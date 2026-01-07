from database import get_connection

# Helper : convertir un tuple en dict
def _livre_to_dict(row):
    if not row:
        return None
    return {
        "isbn": row[0],
        "titre": row[1],
        "editeur": row[2],
        "annee": row[3],
        "exemplaires_dispo": row[4]
    }

# CREATE
def create_livre(isbn, titre, editeur, annee, exemplaires_dispo):
    if not (isbn and titre):
        print("ISBN et titre obligatoires.")
        return False

    try:
        annee = int(annee)
        exemplaires_dispo = int(exemplaires_dispo)
        if exemplaires_dispo < 0:
            print("Stock invalide.")
            return False
    except ValueError:
        print("Année et stock doivent être des nombres.")
        return False

    conn = get_connection()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Livre (isbn, titre, editeur, annee, exemplaires_dispo) VALUES (%s, %s, %s, %s, %s)",
            (isbn.strip(), titre.strip(), editeur.strip() if editeur else None, annee, exemplaires_dispo)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur création livre : {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

# READ
def get_all_livres():
    conn = get_connection()
    if not conn:
        return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Livre ORDER BY titre")
        rows = cur.fetchall()
        return [_livre_to_dict(r) for r in rows]
    except Exception as e:
        print(f"Erreur récupération livres : {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_livre_by_isbn(isbn):
    if not isbn:
        return None
    conn = get_connection()
    if not conn:
        return None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Livre WHERE isbn=%s", (isbn,))
        row = cur.fetchone()
        return _livre_to_dict(row)
    except Exception as e:
        print(f"Erreur récupération livre : {e}")
        return None
    finally:
        cur.close()
        conn.close()

# UPDATE
def update_livre(isbn, titre=None, editeur=None, annee=None, exemplaires_dispo=None):
    if not isbn:
        print("ISBN obligatoire.")
        return False

    updates = []
    params = []
    if titre:
        updates.append("titre=%s")
        params.append(titre.strip())
    if editeur:
        updates.append("editeur=%s")
        params.append(editeur.strip())
    if annee is not None:
        try:
            annee = int(annee)
            updates.append("annee=%s")
            params.append(annee)
        except ValueError:
            print("Année invalide.")
            return False
    if exemplaires_dispo is not None:
        try:
            exemplaires_dispo = int(exemplaires_dispo)
            if exemplaires_dispo < 0:
                print("Stock invalide.")
                return False
            updates.append("exemplaires_dispo=%s")
            params.append(exemplaires_dispo)
        except ValueError:
            print("Stock invalide.")
            return False

    if not updates:
        print("Aucune modification fournie.")
        return False

    conn = get_connection()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        query = f"UPDATE Livre SET {', '.join(updates)} WHERE isbn=%s"
        params.append(isbn)
        cur.execute(query, tuple(params))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur mise à jour livre : {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

# DELETE
def delete_livre(isbn):
    if not isbn:
        print("ISBN obligatoire.")
        return False
    conn = get_connection()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Livre WHERE isbn=%s", (isbn,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur suppression livre : {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
