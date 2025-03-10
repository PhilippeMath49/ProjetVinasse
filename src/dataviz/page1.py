import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import os
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go

def clean_wine_data(df):
    df.dropna(subset=["Entity", "Wine"], inplace=True)
    df["Year"] = df["Year"].astype(int)
    return df.groupby("Entity")["Wine"].median().reset_index()

def distrib_note():
    wine_prod_df = pd.read_csv("src/data/wine-production/wine-production.csv")
    reviews_df = pd.read_csv("src/data/winemag.csv")
    wine_prod_df = clean_wine_data(wine_prod_df)
    
    fig_hist = px.histogram(reviews_df, x="points", nbins=20, title="Distribution des Notes de Vin", color_discrete_sequence=['#636EFA'])
    
    st.subheader("Distribution des Notes de Vin")
    st.plotly_chart(fig_hist)

def distrib_meanscore():
    df = pd.read_csv("src/data/winemag.csv")
    mean = df["points"].mean()
    std = df["points"].std()
    
    x = np.linspace(df["points"].min(), df["points"].max(), 100)
    normal_curve = norm.pdf(x, mean, std) * len(df["points"]) * (df["points"].max() - df["points"].min()) / 20
    
    histogram = go.Histogram(x=df["points"], nbinsx=20, marker=dict(color='#636EFA'), name="Données")
    normal_line = go.Scatter(x=x, y=normal_curve, mode='lines', line=dict(color='red', width=2), name='Courbe normale')
    mean_line = go.Scatter(x=[mean, mean], y=[0, max(normal_curve)], mode='lines', line=dict(color='green', dash='dash', width=2), name=f"Moyenne: {mean:.2f}")
    
    fig = go.Figure([histogram, normal_line, mean_line])
    fig.update_layout(title="Distribution des scores des vins avec la moyenne",
                      xaxis_title="Points", yaxis_title="Fréquence",
                      barmode='overlay', template="plotly_white")
    
    st.subheader("Analyse des Scores des Vins")
    st.plotly_chart(fig)
    
    boxplot = px.box(df, x="points", title="Boîte à Moustaches des Scores de Vin", color_discrete_sequence=['#636EFA'])
    st.plotly_chart(boxplot)
    
    st.write(f"La moyenne des scores des vins est de {mean:.2f} avec un écart-type de {std:.2f}.")
    st.write("La distribution des scores des vins suit une distribution normale.")
    st.write("La majorité des vins ont des scores compris entre 85 et 90 points.")
    st.write("Il y a des vins exceptionnels avec des scores supérieurs à 90 points.")

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

def top_countries_chart():
    df = pd.read_csv("src/data/winemag.csv")
    top_countries = df["country"].value_counts().head(10)
    
    fig = px.bar(x=top_countries.index, y=top_countries.values,
                 title="Top 10 des pays avec le plus de variétés de vins",
                 labels={"x": "Pays", "y": "Nombre de vins"},
                 color=top_countries.index, color_discrete_sequence=px.colors.sequential.Viridis)
    
    fig.update_layout(xaxis_tickangle=-45)
    st.subheader("Top 10 des pays avec le plus de variétés de vins")
    st.plotly_chart(fig)

def top_varieties_chart():
    df = pd.read_csv("src/data/winemag.csv")
    top_varieties = df["variety"].value_counts().head(10)
    mean_prices = df.groupby("variety")["price"].mean().reindex(top_varieties.index)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=top_varieties.index, y=top_varieties.values, name="Nombre de vins",
                         marker_color=px.colors.sequential.Magma[4]))
    
    fig.add_trace(go.Scatter(x=top_varieties.index, y=mean_prices, name="Prix moyen",
                             mode='lines+markers', line=dict(color='blue', width=2)))
    
    fig.update_layout(title="Top 10 des variétés de cépages les plus populaires avec prix moyens",
                      xaxis_title="Variété",
                      yaxis_title="Nombre de vins",
                      yaxis2=dict(title="Prix moyen (en $)", overlaying='y', side='right', showgrid=False))
    
    st.subheader("Top 10 des variétés de cépages les plus populaires avec prix moyens")
    st.plotly_chart(fig)


def price_comparison_chart():
    df = pd.read_csv("src/data/winemag.csv")
    # Calcul du prix moyen par pays avec outliers
    avg_price_country = df.groupby("country")["price"].mean().sort_values(ascending=False).head(10)

    # Détection des outliers selon Tukey
    Q1 = df["price"].quantile(0.25)
    Q3 = df["price"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filtrer les prix sans les outliers
    df_no_outliers = df[(df["price"] >= lower_bound) & (df["price"] <= upper_bound)]

    # Calcul du prix moyen par pays sans outliers
    avg_price_country_no_outliers = (
        df_no_outliers.groupby("country")["price"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    # Création de la figure avec outliers
    fig_with_outliers = px.bar(
        x=avg_price_country.index,
        y=avg_price_country.values,
        labels={"x": "Pays", "y": "Prix moyen ($)"},
        title="Prix moyen des vins par pays (Top 10)",
        color=avg_price_country.index,
        color_continuous_scale="Viridis"
    )

    # Création de la figure sans outliers
    fig_no_outliers = px.bar(
        x=avg_price_country_no_outliers.index,
        y=avg_price_country_no_outliers.values,
        labels={"x": "Pays", "y": "Prix moyen ($)"},
        title="Prix moyen des vins par pays (Top 10) - Sans Outliers",
        color=avg_price_country_no_outliers.index,
        color_continuous_scale="Viridis"
    )

    st.subheader("Comparaison des prix moyens des vins par pays")

    # Utilisation de checkboxes pour afficher ou masquer les graphiques
    show_with_outliers = st.checkbox("Afficher les prix avec outliers", value=True)
    show_no_outliers = st.checkbox("Afficher les prix sans outliers", value=True)

    if show_with_outliers and show_no_outliers:
        # Afficher côte à côte si les deux graphiques sont activés
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_with_outliers, use_container_width=True)
        with col2:
            st.plotly_chart(fig_no_outliers, use_container_width=True)
    elif show_with_outliers:
        # Afficher seulement le graphique avec outliers en pleine largeur
        st.plotly_chart(fig_with_outliers, use_container_width=True)
    elif show_no_outliers:
        # Afficher seulement le graphique sans outliers en pleine largeur
        st.plotly_chart(fig_no_outliers, use_container_width=True)


def load_and_display_soil_map():
    # Charger le fichier CSV
    df = pd.read_csv("src/data/LUCAS-SOIL-2018.csv")  # Remplacez par le chemin réel du fichier CSV

    # Vérifier la présence des colonnes nécessaires
    if "TH_LAT" not in df.columns or "TH_LONG" not in df.columns or "LC0_Desc" not in df.columns:
        st.error("Colonnes nécessaires (latitude, longitude, type de sol) manquantes.")
        return
    
    # Nettoyer les données : supprimer les lignes où les latitudes ou longitudes sont manquantes
    df = df.dropna(subset=["TH_LAT", "TH_LONG", "LC0_Desc"])
    
    # Créer la carte Plotly
    fig = px.scatter_geo(df,
                         lat="TH_LAT", 
                         lon="TH_LONG", 
                         color="LC0_Desc", 
                         hover_name="POINTID",  # Afficher l'ID unique du point de l'enquête
                         color_continuous_scale="Viridis", 
                         title="Carte des Types de Sol",
                         labels={"LC0_Desc": "Type de Sol"},
                         template="plotly_dark")
    
    # Ajuster la projection de la carte
    fig.update_geos(projection_type="mercator", showcoastlines=True, coastlinecolor="Black")

    # Afficher la carte dans Streamlit
    st.plotly_chart(fig, use_container_width=True)


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



def general():
    # Interface principale avec onglets
    st.title("Tableau de Bord sur le Vin 🍷")
    tabs = st.tabs(["📊 Distribution des Notes et Analyse des Scores","📈 Variété et prix ","sol"])

    with tabs[0]:
        distrib_note()
        distrib_meanscore()

    with tabs[1]:
        top_countries_chart()
        top_varieties_chart()
        price_comparison_chart()
        
    with tabs[2]:
        load_and_display_soil_map()
