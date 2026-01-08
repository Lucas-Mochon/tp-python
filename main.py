import streamlit as st
from repository.etudiants import *
from repository.livres import *
from repository.emprunts import *


st.set_page_config(
    page_title="Gestion Bibliothèque",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .section-header {
        color: #2c3e50;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    .success-box {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 class='main-header'>📚 Gestion de Bibliothèque</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Sélectionnez une section :",
        ["🏠 Accueil", 
         "👥 Étudiants", 
         "📖 Livres", 
         "📋 Emprunts",
         "📊 Statistiques"]
    )

# ==================== PAGE ACCUEIL ====================
if page == "🏠 Accueil":
    st.markdown("<h2 class='section-header'>Bienvenue</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Étudiants", len(get_all_etudiants() or []))
    
    with col2:
        st.metric("Total Livres", len(get_all_livres() or []))
    
    with col3:
        st.metric("Total Emprunts", len(get_all_emprunts() or []))
    
    st.info("""
    ### 📚 À propos de cette application
    
    Cette application gère :
    - **Étudiants** : Ajouter, modifier, supprimer des étudiants
    - **Livres** : Gérer le catalogue de la bibliothèque
    - **Emprunts** : Enregistrer et gérer les emprunts/retours
    - **Amendes** : Suivi automatique des amendes de retard
    """)

# ==================== PAGE ÉTUDIANTS ====================
elif page == "👥 Étudiants":
    st.markdown("<h2 class='section-header'>Gestion des Étudiants</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Ajouter", "Afficher", "Modifier", "Supprimer"])
    
    with tab1:
        st.subheader("➕ Ajouter un nouvel étudiant")
        with st.form("form_add_etudiant"):
            nom = st.text_input("Nom", placeholder="Dupont")
            prenom = st.text_input("Prénom", placeholder="Jean")
            email = st.text_input("Email", placeholder="jean.dupont@example.com")
            
            submitted = st.form_submit_button("Ajouter l'étudiant", use_container_width=True)
            
            if submitted:
                if nom and prenom and email:
                    if create_etudiant(nom, prenom, email):
                        st.markdown("<div class='success-box'>Étudiant ajouté avec succès !</div>", unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown("<div class='error-box'>Erreur lors de l'ajout de l'étudiant</div>", unsafe_allow_html=True)
                else:
                    st.warning("Veuillez remplir tous les champs")
    
    # TAB 2 : Afficher les étudiants
    with tab2:
        st.subheader("📋 Liste des étudiants")
        etudiants = get_all_etudiants()
        
        if etudiants:
            df_etudiants = st.dataframe(
                [
                    {
                        "ID": e['id_etud'],
                        "Prénom": e['prenom'],
                        "Nom": e['nom'],
                        "Email": e['email'],
                        "Date d'inscription": e['date_inscription'],
                        "Amende (€)": e['solde_amende']
                    }
                    for e in etudiants
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Aucun étudiant enregistré")
    
    # TAB 3 : Modifier un étudiant
    with tab3:
        st.subheader("✏️ Modifier un étudiant")
        etudiants = get_all_etudiants()
        
        if etudiants:
            etud_options = {f"{e['id_etud']} - {e['prenom']} {e['nom']}": e['id_etud'] for e in etudiants}
            selected = st.selectbox("Sélectionnez un étudiant", etud_options.keys())
            id_etud = etud_options[selected]
            
            etud = get_etudiant_by_id(id_etud)
            
            with st.form("form_update_etudiant"):
                nom = st.text_input("Nom", value=etud['nom'])
                prenom = st.text_input("Prénom", value=etud['prenom'])
                email = st.text_input("Email", value=etud['email'])
                
                submitted = st.form_submit_button("Mettre à jour", use_container_width=True)
                
                if submitted:
                    if update_etudiant(id_etud, nom, prenom, email):
                        st.markdown("<div class='success-box'>Étudiant mis à jour !</div>", unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown("<div class='error-box'>Erreur lors de la mise à jour</div>", unsafe_allow_html=True)
        else:
            st.info("Aucun étudiant à modifier")
    
    # TAB 4 : Supprimer un étudiant
    with tab4:
        st.subheader("🗑️ Supprimer un étudiant")
        etudiants = get_all_etudiants()
        
        if etudiants:
            etud_options = {f"{e['id_etud']} - {e['prenom']} {e['nom']}": e['id_etud'] for e in etudiants}
            selected = st.selectbox("Sélectionnez un étudiant à supprimer", etud_options.keys())
            id_etud = etud_options[selected]
            
            if st.button("Supprimer cet étudiant", type="secondary", use_container_width=True):
                if delete_etudiant(id_etud):
                    st.markdown("<div class='success-box'>Étudiant supprimé !</div>", unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown("<div class='error-box'>Erreur lors de la suppression</div>", unsafe_allow_html=True)
        else:
            st.info("Aucun étudiant à supprimer")

# ==================== PAGE LIVRES ====================
elif page == "📖 Livres":
    st.markdown("<h2 class='section-header'>Gestion des Livres</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Ajouter", "Afficher", "Modifier", "Supprimer"])
    
    # TAB 1 : Ajouter un livre
    with tab1:
        st.subheader("➕ Ajouter un nouveau livre")
        with st.form("form_add_livre"):
            isbn = st.text_input("ISBN", placeholder="978-2-07-036822-8")
            titre = st.text_input("Titre", placeholder="Le Seigneur des Anneaux")
            editeur = st.text_input("Éditeur", placeholder="Pocket")
            
            col1, col2 = st.columns(2)
            with col1:
                annee = st.number_input("Année de publication", min_value=1900, max_value=2100, value=2024)
            with col2:
                stock = st.number_input("Exemplaires disponibles", min_value=0, value=1)
            
            submitted = st.form_submit_button("Ajouter le livre", use_container_width=True)
            
            if submitted:
                if isbn and titre and editeur:
                    if create_livre(isbn, titre, editeur, int(annee), int(stock)):
                        st.markdown("<div class='success-box'>Livre ajouté avec succès !</div>", unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown("<div class='error-box'>Erreur lors de l'ajout du livre</div>", unsafe_allow_html=True)
                else:
                    st.warning("Veuillez remplir tous les champs")
    
    # TAB 2 : Afficher les livres
    with tab2:
        st.subheader("📚 Catalogue de livres")
        livres = get_all_livres()
        
        if livres:
            st.dataframe(
                [
                    {
                        "ISBN": l['isbn'],
                        "Titre": l['titre'],
                        "Éditeur": l['editeur'],
                        "Année": l['annee'],
                        "Disponibles": l['exemplaires_dispo']
                    }
                    for l in livres
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Aucun livre enregistré")
    
    # TAB 3 : Modifier un livre
    with tab3:
        st.subheader("✏️ Modifier un livre")
        livres = get_all_livres()
        
        if livres:
            livre_options = {f"{l['isbn']} - {l['titre']}": l['isbn'] for l in livres}
            selected = st.selectbox("Sélectionnez un livre", livre_options.keys())
            isbn = livre_options[selected]
            
            livre = get_livre_by_isbn(isbn)
            
            with st.form("form_update_livre"):
                titre = st.text_input("Titre", value=livre['titre'])
                editeur = st.text_input("Éditeur", value=livre['editeur'])
                
                col1, col2 = st.columns(2)
                with col1:
                    annee = st.number_input("Année", min_value=1900, max_value=2100, value=livre['annee'])
                with col2:
                    stock = st.number_input("Stock", min_value=0, value=livre['exemplaires_dispo'])
                
                submitted = st.form_submit_button("Mettre à jour", use_container_width=True)
                
                if submitted:
                    if update_livre(isbn, titre, editeur, int(annee), int(stock)):
                        st.markdown("<div class='success-box'>Livre mis à jour !</div>", unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown("<div class='error-box'>Erreur lors de la mise à jour</div>", unsafe_allow_html=True)
        else:
            st.info("Aucun livre à modifier")
    
    # TAB 4 : Supprimer un livre
    with tab4:
        st.subheader("🗑️ Supprimer un livre")
        livres = get_all_livres()
        
        if livres:
            livre_options = {f"{l['isbn']} - {l['titre']}": l['isbn'] for l in livres}
            selected = st.selectbox("Sélectionnez un livre à supprimer", livre_options.keys())
            isbn = livre_options[selected]
            
            if st.button("Supprimer ce livre", type="secondary", use_container_width=True):
                if delete_livre(isbn):
                    st.markdown("<div class='success-box'>Livre supprimé !</div>", unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown("<div class='error-box'>Erreur lors de la suppression</div>", unsafe_allow_html=True)
        else:
            st.info("Aucun livre à supprimer")

# ==================== PAGE EMPRUNTS ====================
elif page == "📋 Emprunts":
    st.markdown("<h2 class='section-header'>Gestion des Emprunts</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Enregistrer", "Retourner", "Tous les emprunts", "Par étudiant"])
    
    # TAB 1 : Enregistrer un emprunt
    with tab1:
        st.subheader("➕ Enregistrer un nouvel emprunt")
        etudiants = get_all_etudiants()
        livres = get_all_livres()
        
        if etudiants and livres:
            with st.form("form_add_emprunt"):
                etud_options = {f"{e['id_etud']} - {e['prenom']} {e['nom']}": e['id_etud'] for e in etudiants}
                selected_etud = st.selectbox("Sélectionnez un étudiant", etud_options.keys())
                id_etud = etud_options[selected_etud]
                
                livre_options = {f"{l['isbn']} - {l['titre']}": l['isbn'] for l in livres}
                selected_livre = st.selectbox("Sélectionnez un livre", livre_options.keys())
                isbn = livre_options[selected_livre]
                
                submitted = st.form_submit_button("Enregistrer l'emprunt", use_container_width=True)
                
                if submitted:
                    if create_emprunt(id_etud, isbn):
                        st.markdown("<div class='success-box'>Emprunt enregistré !</div>", unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown("<div class='error-box'>Erreur lors de l'enregistrement</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Veuillez d'abord ajouter des étudiants et des livres")
    
    # TAB 2 : Retourner un livre
    with tab2:
        st.subheader("📚 Retourner un livre")
        emprunts = get_all_emprunts()
        
        if emprunts:
            emprunts_actifs = [e for e in emprunts if e['date_retour'] is None]
            
            if emprunts_actifs:
                emprunt_options = {
                    f"{e['id_emprunt']} - Étudiant {e['id_etud']} - Livre {e['isbn']}": e['id_emprunt'] 
                    for e in emprunts_actifs
                }
                selected = st.selectbox("Sélectionnez un emprunt", emprunt_options.keys())
                id_emprunt = emprunt_options[selected]
                
                if st.button("Retourner ce livre", type="secondary", use_container_width=True):
                    if retour_emprunt(id_emprunt):
                        st.markdown("<div class='success-box'>Livre retourné !</div>", unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown("<div class='error-box'>Erreur lors du retour</div>", unsafe_allow_html=True)
            else:
                st.info("Aucun emprunt actif")
        else:
            st.info("Aucun emprunt enregistré")
    
    # TAB 3 : Tous les emprunts
    with tab3:
        st.subheader("📋 Tous les emprunts")
        emprunts = get_all_emprunts()
        
        if emprunts:
            st.dataframe(
                [
                    {
                        "ID": e['id_emprunt'],
                        "Étudiant": e['id_etud'],
                        "Livre": e['isbn'],
                        "Date d'emprunt": e['date_emprunt'],
                        "Date de retour": e['date_retour'] or "En cours",
                        "Amende (€)": e['amende']
                    }
                    for e in emprunts
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Aucun emprunt enregistré")
    
    # TAB 4 : Emprunts par étudiant
    with tab4:
        st.subheader("👤 Emprunts par étudiant")
        etudiants = get_all_etudiants()
        
        if etudiants:
            etud_options = {f"{e['id_etud']} - {e['prenom']} {e['nom']}": e['id_etud'] for e in etudiants}
            selected = st.selectbox("Sélectionnez un étudiant", etud_options.keys())
            id_etud = etud_options[selected]
            
            emprunts = get_emprunts_by_etudiant(id_etud)
            
            if emprunts:
                st.dataframe(
                    [
                        {
                            "ID": e['id_emprunt'],
                            "Livre": e['isbn'],
                            "Date d'emprunt": e['date_emprunt'],
                            "Date de retour": e['date_retour'] or "En cours",
                            "Amende (€)": e['amende']
                        }
                        for e in emprunts
                    ],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Cet étudiant n'a aucun emprunt")
        else:
            st.info("Aucun étudiant enregistré")

# ==================== PAGE STATISTIQUES ====================
elif page == "📊 Statistiques":
    st.markdown("<h2 class='section-header'>Statistiques</h2>", unsafe_allow_html=True)
    
    etudiants = get_all_etudiants() or []
    livres = get_all_livres() or []
    emprunts = get_all_emprunts() or []
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Livres", len(livres))
    
    with col2:
        st.metric("Total Étudiants", len(etudiants))
    
    with col3:
        emprunts_actifs = len([e for e in emprunts if e['date_retour'] is None])
        st.metric("Emprunts Actifs", emprunts_actifs)
    
    with col4:
        total_amendes = sum([e['solde_amende'] for e in etudiants])
        st.metric("Amendes Totales (€)", f"{total_amendes:.2f}")
    
    # Graphiques
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Stock de livres")
        if livres:
            stock_data = {l['titre'][:20]: l['exemplaires_dispo'] for l in livres}
            st.bar_chart(stock_data)
    
    with col2:
        st.subheader("💰 Amendes par étudiant")
        if etudiants:
            amendes_data = {f"{e['prenom']} {e['nom'][:10]}": e['solde_amende'] for e in etudiants if e['solde_amende'] > 0}
            if amendes_data:
                st.bar_chart(amendes_data)
            else:
                st.info("Aucune amende à afficher")
    
    # Tableau détaillé
    st.divider()
    st.subheader("Détails des amendes")
    
    etudiants_amendes = [e for e in etudiants if e['solde_amende'] > 0]
    
    if etudiants_amendes:
        st.dataframe(
            [
                {
                    "ID": e['id_etud'],
                    "Prénom": e['prenom'],
                    "Nom": e['nom'],
                    "Email": e['email'],
                    "Amende (€)": e['solde_amende']
                }
                for e in etudiants_amendes
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("Aucune amende en attente !")
