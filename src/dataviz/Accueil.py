import streamlit as st
import dataviz.Intro as intro
import dataviz.page1 as page1

def accueil():
    # Titre principal
    st.title("Bienvenue dans l'application de Visualisation de Données")

    # Onglets pour la navigation
    tab1, tab2 = st.tabs(["🏠 Accueil", "📊 Analyse des Vins"])

    with tab1:
        st.header("Analyse des Données des Vins Rouges")
        st.write("""
        Cette application permet d'explorer et d'analyser les données relatives aux caractéristiques des vins rouges.
        Vous pourrez visualiser différentes métriques et appliquer des modèles de régression pour prédire la qualité des vins.
        """)

        st.subheader("Objectif de l'Analyse")
        st.write("""
        Nous allons explorer comment certaines caractéristiques, telles que l'alcool, l'acidité volatile et les sulfates, influencent la qualité des vins.
        Des graphiques interactifs et des modèles de régression sont disponibles pour vous aider à mieux comprendre les relations entre ces variables.
        """)

    with tab2:
        st.header("Analyse des Données")
        st.write("Commencez l'analyse des vins rouges avec des visualisations interactives et des modèles prédictifs.")
        
        # Appel de la page d'analyse
        page1.general()

    # Onglet supplémentaire pour l'introduction (optionnel)
    tab_intro = st.expander("ℹ️ Introduction")
    with tab_intro:
        intro.main()


def main():
    accueil()

if __name__ == "__main__":
    main()
