import streamlit as st
import dataviz.page1 as page1

def accueil():
    # Titre de la page d'accueil
    st.title("Page d'Accueil")

    # Lien pour rediriger vers la page "page1.general"
    st.write("Bienvenue sur la page d'accueil de notre application Streamlit.")
    st.write("Cliquez sur le lien ci-dessous pour accéder à la page 'page1' :")

    # Lien vers la page "page1.general"
    if st.button("Accéder à la page1"):
        st.query_params(page="page1")
        page1.general()


def main():
    accueil()

