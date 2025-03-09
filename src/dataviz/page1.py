import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import os
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go

# Charger les données
class Page1:
    


    # Nettoyage et traitement
    def clean_wine_data(df):
        df.dropna(subset=["Entity", "Wine"], inplace=True)
        df["Year"] = df["Year"].astype(int)
        return df.groupby("Entity")["Wine"].median().reset_index()
    
    def distrib_note():



        wine_prod_df = pd.read_csv("src/data/wine-production/wine-production.csv")
        reviews_df = pd.read_csv("src/data/winemag.csv")
        wine_prod_df = Page1.clean_wine_data(wine_prod_df)

        # # Charger les données géographiques
        

        # # Création d'un histogramme des notes de vin
        fig_hist = px.histogram(reviews_df, x="points", nbins=20, title="Distribution des Notes de Vin")

        # Création de l'application Streamlit
        st.title("Tableau de Bord sur le Vin")


        st.subheader("Distribution des Notes de Vin")
        st.plotly_chart(fig_hist)
        
        


    def distrib_meanscore():
        df = pd.read_csv("src/data/winemag.csv")
        mean = df["points"].mean()
        std = df["points"].std()

        # Générer les valeurs pour la courbe normale
        x = np.linspace(df["points"].min(), df["points"].max(), 100)
        normal_curve = norm.pdf(x, mean, std) * len(df["points"]) * (df["points"].max() - df["points"].min()) / 20  # Adapter à l'échelle de l'histogramme

        # Créer l'histogramme
        histogram = go.Histogram(x=df["points"], nbinsx=20, marker=dict(color='blue'), name="Données")

        # Courbe normale
        normal_line = go.Scatter(x=x, y=normal_curve, mode='lines', line=dict(color='red', width=2), name='Courbe normale')

        # Ligne de la moyenne
        mean_line = go.Scatter(x=[mean, mean], y=[0, max(normal_curve)], mode='lines', line=dict(color='green', dash='dash', width=2), name=f"Moyenne: {mean:.2f}")

        # Créer la boîte à moustaches
        boxplot = go.Box(x=df["points"], marker=dict(color='blue'), name="Boxplot", boxmean=True, boxpoints='all', jitter=0.3, pointpos=-1.8)
        histogram = go.Histogram(x=df["points"], nbinsx=20, marker=dict(color='blue', line=dict(width=1)), name="Données")

        # Création de la figure
        fig = go.Figure()
        fig.add_trace(histogram)
        fig.add_trace(normal_line)
        fig.add_trace(mean_line)
        fig.add_trace(boxplot)

        # Mettre en page la figure
        fig.update_layout(
            title="Distribution des scores des vins avec la moyenne",
            xaxis_title="Points",
            yaxis_title="Fréquence",
            barmode='overlay',
            template="plotly_white"
        )

        # Interface Streamlit
        st.title("Analyse des Scores des Vins")
        st.plotly_chart(fig)


    def general():
        Page1.distrib_note()
        Page1.distrib_meanscore()



    def load_data():
        csv_path = "src/data/wine-production/wine-production.csv"
        shapefile_path = "src/map/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
        
        if not os.path.exists(csv_path) or not os.path.exists(shapefile_path):
            st.error("Fichiers de données manquants ! Vérifiez votre déploiement.")
            return None, None
        
        wine_df = pd.read_csv(csv_path)
        wine_df['Year'] = wine_df['Year'].astype(int)
        wine_df['Entity'] = wine_df['Entity'].str.replace(r"\s\([A-Z]{3}\)", "", regex=True)
        
        world = gpd.read_file(shapefile_path)
        return wine_df, world

# Fonction principale
    def map():
        # Faire le traitement des données et affichage de la map ici avec streamlit
        pass
