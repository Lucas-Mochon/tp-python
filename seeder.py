from models.etudiants import create_etudiant, get_all_etudiants
from models.livres import create_livre, get_all_livres
from models.emprunts import create_emprunt
import random
import faker

fake = faker.Faker('fr_FR') # Pour générer des noms français 

# Générer 30 étudiants
def seed_etudiants(n=30):
    etudiants_crees = 0
    for _ in range(n):
        nom = fake.last_name()
        prenom = fake.first_name()
        email = fake.unique.email()
        if create_etudiant(nom, prenom, email):
            etudiants_crees += 1
    print(f"✅ {etudiants_crees} étudiants ajoutés.")


# Générer 50 livres
def seed_livres(n=50):
    livres_crees = 0
    for _ in range(n):
        isbn = str(random.randint(9780000000000, 9799999999999))
        titre = fake.sentence(nb_words=4).replace('.', '')
        editeur = fake.company()
        annee = random.randint(1990, 2025)
        stock = random.randint(1, 5)
        if create_livre(isbn, titre, editeur, annee, stock):
            livres_crees += 1
    print(f"✅ {livres_crees} livres ajoutés.")


# Générer 50 emprunts aléatoires
def seed_emprunts(n=50):
    etudiants = get_all_etudiants()
    livres = get_all_livres()
    
    emprunts_crees = 0
    attempts = 0

    while emprunts_crees < n and attempts < n * 5:
        etud = random.choice(etudiants)
        livre = random.choice(livres)
        id_etud = etud[0]
        isbn = livre[0]
        success = create_emprunt(id_etud, isbn)
        if success:
            emprunts_crees += 1
        attempts += 1

    print(f"✅ {emprunts_crees} emprunts créés.")


def run_seeder():
    print("⚡ Début du seed de la base de données")
    seed_etudiants()
    seed_livres()
    seed_emprunts()
    print("🎉 Base de données initialisée avec succès !")


if __name__ == "__main__":
    run_seeder()
