import streamlit as st
import dataviz.Intro as intro
import dataviz.page1 as page1

def accueil():
    
    
    tabs = ["Accueil", "Introduction"] 
    with tabs[0]:
        
        # Titre principal
        st.title("Bienvenue dans l'application de Visualisation de Données")

        # Un sous-titre pour expliquer brièvement l'objectif de l'application
        st.header("Analyse des Données des Vins Rouges")
        st.write(
            """
            Cette application permet d'explorer et d'analyser les données relatives aux caractéristiques des vins rouges.
            Vous pourrez visualiser différentes métriques et appliquer des modèles de régression pour prédire la qualité des vins.
            """
        )

        # Une section d'informations supplémentaires
        st.subheader("Objectif de l'Analyse")
        st.write(
            """
            Nous allons explorer comment certaines caractéristiques, telles que l'alcool, l'acidité volatile et les sulfates, influencent la qualité des vins.
            Des graphiques interactifs et des modèles de régression sont disponibles pour vous aider à mieux comprendre les relations entre ces variables.
            """
        )

        # Ajout d'un bouton pour accéder à la page suivante (exemple : page1)
        st.subheader("Explorez les Pages")
        st.write("Cliquez sur les boutons ci-dessous pour naviguer à travers l'application.")
        
        if st.button("Commencer l'Analyse"):
            # Cette fonction pourrait rediriger vers une autre page (exemple: page1)
            st.write("Introduction à l'Analyse des Données")
            page1.general()
            

        # Ajouter un peu de style personnalisé
        st.markdown("""
        <style>
        .stTitle {
            font-size: 32px;
            color: #1f77b4;
            text-align: center;
        }
        .stHeader {
            font-size: 24px;
            color: #4caf50;
        }
        .stSubHeader {
            font-size: 20px;
            color: #ff9800;
        }
        .stMarkdown {
            font-size: 16px;
        }
        </style>
        """, unsafe_allow_html=True)
    if tabs[1]:
        intro.main()

def main():
    accueil()

