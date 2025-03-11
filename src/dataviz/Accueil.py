import streamlit as st

# Titre de la page d'accueil
st.title("Page d'Accueil")

# Lien pour rediriger vers la page "page1.general"
st.write("Bienvenue sur la page d'accueil de notre application Streamlit.")
st.write("Cliquez sur le lien ci-dessous pour accéder à la page 'page1.general' :")

# Lien vers la page "page1.general"
st.markdown("[Accéder à la page1.general](./page1_general)")
