from repository.etudiants import *
from repository.livres import *
from repository.emprunts import *

def menu():
    print("\n===== BIBLIOTHÈQUE =====")
    print("1. Ajouter un étudiant")
    print("2. Afficher tous les étudiants")
    print("3. Modifier un étudiant")
    print("4. Supprimer un étudiant")
    print("5. Ajouter un livre")
    print("6. Afficher tous les livres")
    print("7. Modifier un livre")
    print("8. Supprimer un livre")
    print("9. Enregistrer un emprunt")
    print("10. Retourner un livre")
    print("11. Afficher tous les emprunts")
    print("12. Afficher les emprunts d'un étudiant")
    print("13. Quitter")

def main():
    while True:
        menu()
        choix = input("Choix : ").strip()

        # ----------------- Étudiants -----------------
        if choix == "1":
            nom = input("Nom : ").strip()
            prenom = input("Prénom : ").strip()
            email = input("Email : ").strip()
            if create_etudiant(nom, prenom, email):
                print("Étudiant ajouté.")
            else:
                print("Échec ajout étudiant.")
        elif choix == "2":
            etudiants = get_all_etudiants()
            if etudiants:
                for e in etudiants:
                    print(f"{e['id_etud']}: {e['prenom']} {e['nom']} | {e['email']} | Inscrit le {e['date_inscription']} | Amende: {e['solde_amende']}")
            else:
                print("Aucun étudiant trouvé.")
        elif choix == "3":
            try:
                id_etud = int(input("ID de l'étudiant : "))
                etud = get_etudiant_by_id(id_etud)
                if not etud:
                    print("Étudiant introuvable.")
                    continue
                nom = input(f"Nouveau nom ({etud['nom']}) : ").strip() or None
                prenom = input(f"Nouveau prénom ({etud['prenom']}) : ").strip() or None
                email = input(f"Nouveau email ({etud['email']}) : ").strip() or None
                if update_etudiant(id_etud, nom, prenom, email):
                    print("Étudiant mis à jour.")
                else:
                    print("Échec mise à jour.")
            except ValueError:
                print("ID invalide.")
        elif choix == "4":
            try:
                id_etud = int(input("ID de l'étudiant à supprimer : "))
                if delete_etudiant(id_etud):
                    print("Étudiant supprimé.")
                else:
                    print("Échec suppression.")
            except ValueError:
                print("ID invalide.")

        # ----------------- Livres -----------------
        elif choix == "5":
            isbn = input("ISBN : ").strip()
            titre = input("Titre : ").strip()
            editeur = input("Éditeur : ").strip()
            try:
                annee = int(input("Année : "))
                stock = int(input("Exemplaires disponibles : "))
            except ValueError:
                print("Année et stock doivent être des nombres.")
                continue
            if create_livre(isbn, titre, editeur, annee, stock):
                print("Livre ajouté.")
            else:
                print("Échec ajout livre.")
        elif choix == "6":
            livres = get_all_livres()
            if livres:
                for l in livres:
                    print(f"{l['isbn']}: {l['titre']} | {l['editeur']} | {l['annee']} | Dispo: {l['exemplaires_dispo']}")
            else:
                print("Aucun livre trouvé.")
        elif choix == "7":
            isbn = input("ISBN du livre : ").strip()
            livre = get_livre_by_isbn(isbn)
            if not livre:
                print("Livre introuvable.")
                continue
            titre = input(f"Nouveau titre ({livre['titre']}) : ").strip() or None
            editeur = input(f"Nouveau éditeur ({livre['editeur']}) : ").strip() or None
            try:
                annee_input = input(f"Nouvelle année ({livre['annee']}) : ").strip()
                stock_input = input(f"Nouveau stock ({livre['exemplaires_dispo']}) : ").strip()
                annee = int(annee_input) if annee_input else None
                stock = int(stock_input) if stock_input else None
            except ValueError:
                print("Année et stock doivent être des nombres.")
                continue
            if update_livre(isbn, titre, editeur, annee, stock):
                print("Livre mis à jour.")
            else:
                print("Échec mise à jour.")
        elif choix == "8":
            isbn = input("ISBN du livre à supprimer : ").strip()
            if delete_livre(isbn):
                print("Livre supprimé.")
            else:
                print("Échec suppression.")

        # ----------------- Emprunts -----------------
        elif choix == "9":
            try:
                id_etud = int(input("ID étudiant : "))
            except ValueError:
                print("ID étudiant invalide.")
                continue
            isbn = input("ISBN du livre : ").strip()
            if create_emprunt(id_etud, isbn):
                print("Emprunt enregistré.")
            else:
                print("Échec enregistrement emprunt.")
        elif choix == "10":
            try:
                id_emprunt = int(input("ID de l'emprunt : "))
            except ValueError:
                print("ID emprunt invalide.")
                continue
            if retour_emprunt(id_emprunt):
                print("Livre retourné.")
            else:
                print("Échec retour livre.")
        elif choix == "11":
            emprunts = get_all_emprunts()
            if emprunts:
                for e in emprunts:
                    print(f"{e['id_emprunt']}: Étudiant {e['id_etud']} | Livre {e['isbn']} | Emprunt: {e['date_emprunt']} | Retour: {e['date_retour']} | Amende: {e['amende']}")
            else:
                print("Aucun emprunt trouvé.")
        elif choix == "12":
            try:
                id_etud = int(input("ID étudiant : "))
            except ValueError:
                print("ID invalide.")
                continue
            emprunts = get_emprunts_by_etudiant(id_etud)
            if emprunts:
                for e in emprunts:
                    print(f"{e['id_emprunt']}: Livre {e['isbn']} | Emprunt: {e['date_emprunt']} | Retour: {e['date_retour']} | Amende: {e['amende']}")
            else:
                print("Aucun emprunt pour cet étudiant.")
        elif choix == "13":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
