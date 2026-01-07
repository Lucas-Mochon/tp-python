from database import get_connection

# Helper : convertir un tuple en dictionnaire
def _etudiant_to_dict(row):
    if not row:
        return None
    return {
        "id_etud": row[0],
        "nom": row[1],
        "prenom": row[2],
        "email": row[3],
        "date_inscription": row[4],
        "solde_amende": float(row[5])
    }

# CREATE
def create_etudiant(nom, prenom, email):
    if not (nom and prenom and email):
        print("Nom, prénom et email sont obligatoires.")
        return False

    conn = get_connection()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        query = """
        INSERT INTO Etudiant (nom, prenom, email)
        VALUES (%s, %s, %s)
        """
        cur.execute(query, (nom.strip(), prenom.strip(), email.strip().lower()))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur création étudiant : {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

# READ
def get_all_etudiants():
    conn = get_connection()
    if not conn:
        return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Etudiant ORDER BY id_etud")
        rows = cur.fetchall()
        return [_etudiant_to_dict(r) for r in rows]
    except Exception as e:
        print(f"Erreur récupération étudiants : {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_etudiant_by_id(id_etud):
    if not isinstance(id_etud, int):
        print("id_etud doit être un entier.")
        return None

    conn = get_connection()
    if not conn:
        return None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Etudiant WHERE id_etud=%s", (id_etud,))
        row = cur.fetchone()
        return _etudiant_to_dict(row)
    except Exception as e:
        print(f"Erreur récupération étudiant : {e}")
        return None
    finally:
        cur.close()
        conn.close()

# UPDATE
def update_etudiant(id_etud, nom=None, prenom=None, email=None, solde_amende=None):
    if not isinstance(id_etud, int):
        print("id_etud doit être un entier.")
        return False

    updates = []
    params = []
    if nom:
        updates.append("nom=%s")
        params.append(nom.strip())
    if prenom:
        updates.append("prenom=%s")
        params.append(prenom.strip())
    if email:
        updates.append("email=%s")
        params.append(email.strip().lower())
    if solde_amende is not None:
        try:
            solde_amende = float(solde_amende)
            if solde_amende < 0:
                print("Le solde de l'amende ne peut pas être négatif.")
                return False
            updates.append("solde_amende=%s")
            params.append(solde_amende)
        except ValueError:
            print("Le solde de l'amende doit être un nombre.")
            return False

    if not updates:
        print("Aucune donnée à mettre à jour.")
        return False

    conn = get_connection()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        query = f"UPDATE Etudiant SET {', '.join(updates)} WHERE id_etud=%s"
        params.append(id_etud)
        cur.execute(query, tuple(params))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur mise à jour étudiant : {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

# DELETE
def delete_etudiant(id_etud):
    if not isinstance(id_etud, int):
        print("id_etud doit être un entier.")
        return False

    conn = get_connection()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Etudiant WHERE id_etud=%s", (id_etud,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur suppression étudiant : {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
