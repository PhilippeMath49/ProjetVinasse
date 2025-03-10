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
                      yaxis2=dict(title="Prix moyen (en $)", overlaying='y', side='right'))
    
    st.subheader("Top 10 des variétés de cépages les plus populaires avec prix moyens")
    st.plotly_chart(fig)
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
                      yaxis2=dict(title="Prix moyen (en $)", overlaying='y', side='right'))
    
    st.subheader("Top 10 des variétés de cépages les plus populaires avec prix moyens")
    st.plotly_chart(fig)

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
    tabs = st.tabs(["📊 Distribution des Notes et Analyse des Scores","📈 Variété et prix "])

    with tabs[0]:
        distrib_note()
        distrib_meanscore()

    with tabs[1]:
        top_countries_chart()
        top_varieties_chart()
