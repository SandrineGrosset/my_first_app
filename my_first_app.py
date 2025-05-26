# Importation des bibliothèque
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate
import pandas as pd


# Données utilisateurs via fichier csv
df = pd.read_csv('utilisateur.csv')
lesDonneesDesComptes = {
                        'usernames':
                                    {
                                    row['username']:
                                                    {
                                                    'name': row['name'],
                                                    'password': row['password'],
                                                    'email': row['email'],
                                                    'failed_login_attemps': int(row['failed_login_attemps']),
                                                    'logged_in': row['logged_in'] == 'True',
                                                    'role': row['role']
                                                    }
                                    for _, row in df.iterrows()
                                    }
                        }

# authentification
authenticator = Authenticate(
                                lesDonneesDesComptes,  # Les données des comptes
                                "cookie name",         # Le nom du cookie, un str quelconque
                                "cookie key",          # La clé du cookie, un str quelconque
                                30,                    # Le nombre de jours avant que le cookie expire
                            )

authenticator.login()

# Initialisation de l'état de navigation
if "page" not in st.session_state:
    st.session_state["page"] = "special"  # Page spéciale affichée par défaut

# Authentification réussie
if st.session_state["authentication_status"]:

    with st.sidebar:
        # Récupérer l'identifiant de l'utilisateur connecté
        identifiant = st.session_state.get('username', '')
        if identifiant in lesDonneesDesComptes['usernames']:
            prénom = lesDonneesDesComptes['usernames'][identifiant]['name']
            st.write(f"Bienvenue {prénom} 👋")

        # Boutons de navigation
        if st.button("LogIn", type="secondary"):
            st.session_state["page"] = "login"
        if st.button("Accueil", type="secondary"):
            st.session_state["page"] = "accueil"
        if st.button("Album photo", type="secondary"):
            st.session_state["page"] = "album"


        # Déconnexion
        authenticator.logout("Déconnexion", "sidebar")

    # Affichage de la phrase spéciale uniquement si on n’a pas cliqué ailleurs
    if st.session_state["page"] == "login":
        st.title("Bienvenu! Tu as maintenant accès à la page du meilleur chien")

    # Page Accueil
    elif st.session_state["page"] == "accueil":
        st.title("Le Golden Retriever :dog:")
        st.image("https://i.pinimg.com/236x/52/b1/4c/52b14c4f01cbabcc53e8f6f24b5bf930.jpg")

    # Page Album
    elif st.session_state["page"] == "album":
        st.title("Les meilleures photos :laughing:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Baignade")
            st.image("https://cdn-s-www.dna.fr/images/1BEFD357-9A83-4485-91AE-023D08E60099/NW_raw/au-debut-elle-est-froide-mais-apres-elle-est-bonne-photo-dna-michel-koebel-1654527996.jpg")
        with col2:
            st.write("Jardinage")
            st.image("https://i.pinimg.com/736x/cd/5a/bf/cd5abf7a473f9062641818d0941f029b.jpg")
        with col3:
            st.write("Dodo")
            st.image("https://www.woopets.fr/assets/ckeditor/2017/jul/2372/originale/9.jpg")

# Authentification échouée
elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le mot de passe est incorrect")

# Champs vides
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplis')
