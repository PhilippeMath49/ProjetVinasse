import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import os
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import gaussian_kde

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

    geo_columns = ["TH_LAT", "TH_LONG"]
    chem_columns = ["pH_CaCl2", "pH_H2O", "EC", "OC", "CaCO3", "P", "N", "K", "Ox_Al", "Ox_Fe"]
    required_columns = geo_columns + chem_columns
    
    # Vérification de la présence des colonnes requises
    if not all(col in df.columns for col in required_columns):
        st.error("Colonnes nécessaires (latitude, longitude, composés chimiques) manquantes.")
        return
    
    # Remplacer les valeurs non numériques
    df.replace({"< LOD>": None, "NA": None}, inplace=True)
    
    # Conversion des colonnes chimiques en numérique
    for col in chem_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Suppression des lignes avec des valeurs manquantes
    df = df.dropna(subset=required_columns)
    
    # Filtrage des données pour se concentrer sur l'Europe
    df_europe = df[(df["TH_LAT"] > 35) & (df["TH_LAT"] < 72) & (df["TH_LONG"] > -25) & (df["TH_LONG"] < 40)]
    
    # Réduction de la quantité de données via échantillonnage
    sample_size = 1000  # Limiter à 1000 points pour optimiser la performance
    if len(df_europe) > sample_size:
        df_europe = df_europe.sample(n=sample_size, random_state=42)
    
    # Détermination du composé chimique dominant pour chaque point
    df_europe["Dominant_Chemical"] = df_europe[chem_columns].idxmax(axis=1)
    
    # Création de la carte interactive
    fig = px.scatter_geo(
        df_europe,
        lat="TH_LAT", 
        lon="TH_LONG", 
        color="Dominant_Chemical", 
        hover_data=chem_columns + ["POINTID"],  # Afficher les valeurs des composés chimiques et l'ID au survol
        title="Carte des Composés Chimiques Dominants en Europe",
        template="plotly_dark"
    )
    
    # Configuration de l'affichage de la carte
    fig.update_geos(
        projection_type="mercator",
        center={"lat": 50, "lon": 10},  # Centrage sur l'Europe
        showcoastlines=True, coastlinecolor="Black",
        visible=True,
        projection_scale=5  # Zoom ajusté
    )

    # Affinage de l'affichage de la carte
    fig.update_layout(
        geo=dict(
            scope='europe',
            projection_scale=6,
            showland=True,
            landcolor="white",
            subunitcolor="grey",
            countrycolor="grey",
            coastlinecolor="Black"
        )
    )

    # Affichage de la carte dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

def load_and_display_sunshine_map():
    st.title("Carte de l'ensoleillement en France (jours/an)")
    
    # Charger les données
    df_soleil = pd.read_csv("src/data/temps-densoleillement-par-an-par-departement-feuille-1.csv")
    
    # Convertir les noms des départements en majuscules pour correspondance
    df_soleil["Departements"] = df_soleil["Departements"].str.upper()
    
    # Dictionnaire des codes INSEE par département
    codes_insee = {
        "AIN": "01", "AISNE": "02", "ALLIER": "03", "ALPES DE HAUTE PROVENCE": "04", "HAUTES-ALPES": "05",
        "ALPES-MARITIMES": "06", "ARDÈCHE": "07", "ARDENNES": "08", "ARIÈGE": "09", "AUBE": "10",
        "AUDE": "11", "AVEYRON": "12", "BOUCHES-DU-RHÔNE": "13", "CALVADOS": "14", "CANTAL": "15",
        "CHARENTE": "16", "CHARENTE-MARITIME": "17", "CHER": "18", "CORRÈZE": "19", "CÔTE-D’OR": "21",
        "CÔTES D'ARMOR": "22", "CREUSE": "23", "DORDOGNE": "24", "DOUBS": "25", "DRÔME": "26",
        "EURE": "27", "EURE-ET-LOIRE": "28", "FINISTÈRE": "29", "GARD": "30", "HAUTE-GARONNE": "31",
        "GERS": "32", "GIRONDE": "33", "HÉRAULT": "34", "ILLE-ET-VILAINE": "35", "INDRE": "36",
        "INDRE-ET-LOIRE": "37", "ISÈRE": "38", "JURA": "39", "LANDES": "40", "LOIR-ET-CHER": "41",
        "LOIRE": "42", "HAUTE-LOIRE": "43", "LOIRE-ATLANTIQUE": "44", "LOIRET": "45", "LOT": "46",
        "LOT-ET-GARONNE": "47", "LOZÈRE": "48", "MAINE-ET-LOIRE": "49", "MANCHE": "50", "MARNE": "51",
        "HAUTE-MARNE": "52", "MAYENNE": "53", "MEURTHE-ET-MOSELLE": "54", "MEUSE": "55", "MORBIHAN": "56",
        "MOSELLE": "57", "NIÈVRE": "58", "NORD": "59", "OISE": "60", "ORNE": "61", "PAS-DE-CALAIS": "62",
        "PUY-DE-DÔME": "63", "PYRÉNÉES-ATLANTIQUES": "64", "HAUTES-PYRÉNÉES": "65", "PYRÉNÉES-ORIENTALES": "66",
        "BAS-RHIN": "67", "HAUT-RHIN": "68", "RHÔNE": "69", "HAUTE-SAÔNE": "70", "SAÔNE-ET-LOIRE": "71",
        "SARTHE": "72", "SAVOIE": "73", "HAUTE-SAVOIE": "74", "PARIS": "75", "SEINE-MARITIME": "76",
        "SEINE-ET-MARNE": "77", "YVELINES": "78", "DEUX-SÈVRES": "79", "SOMME": "80", "TARN": "81",
        "TARN-ET-GARONNE": "82", "VAR": "83", "VAUCLUSE": "84", "VENDÉE": "85", "VIENNE": "86",
        "HAUTE-VIENNE": "87", "VOSGES": "88", "YONNE": "89", "TERRITOIRE-DE-BELFORT": "90",
        "ESSONNE": "91", "HAUTS-DE-SEINE": "92", "SEINE-SAINT-DENIS": "93", "VAL-DE-MARNE": "94",
        "VAL-D'OISE": "95"
    }
    
    # Ajouter les codes INSEE au DataFrame
    df_soleil["Code_INSEE"] = df_soleil["Departements"].map(codes_insee)
    
    # Vérifier si des valeurs sont manquantes
    if df_soleil["Code_INSEE"].isna().any():
        st.error("Certains départements ne correspondent pas à un code INSEE. Vérifiez les données.")
        return
    
    # Charger le fichier GeoJSON des départements français
    geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
    geojson_data = requests.get(geojson_url).json()
    
    # Convertir Code_INSEE en chaîne
    df_soleil["Code_INSEE"] = df_soleil["Code_INSEE"].astype(str)
    
    # Créer une carte choroplèthe
    fig = px.choropleth_mapbox(
        df_soleil,
        geojson=geojson_data,
        locations="Code_INSEE",  # Utilisation du code INSEE
        featureidkey="properties.code",  # Correspondance avec le GeoJSON
        color="ensoleillement (jours/an)",  # Vérifie le bon nom de colonne
        color_continuous_scale="YlOrRd",
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 46.603354, "lon": 1.888334},  # Centre de la France
        opacity=0.7
    )
    
    fig.update_layout(title="Carte de l'ensoleillement en France (jours/an)")
    
    # Afficher la carte dans Streamlit
    st.plotly_chart(fig, use_container_width=True)


def load_and_display_soil_sunlight_map():
    st.title("Cartes de l'Ensoleillement et des Sols en France")

    # Charger les données d'ensoleillement
    df_soleil = pd.read_csv("src/data/temps-densoleillement-par-an-par-departement-feuille-1.csv")
    df_soleil["Departements"] = df_soleil["Departements"].str.upper()

    # Dictionnaire des codes INSEE
    codes_insee = {
        "AIN": "01", "AISNE": "02", "ALLIER": "03", "ALPES DE HAUTE PROVENCE": "04", "HAUTES-ALPES": "05",
        "ALPES-MARITIMES": "06", "ARDÈCHE": "07", "ARDENNES": "08", "ARIÈGE": "09", "AUBE": "10",
        "AUDE": "11", "AVEYRON": "12", "BOUCHES-DU-RHÔNE": "13", "CALVADOS": "14", "CANTAL": "15",
        "CHARENTE": "16", "CHARENTE-MARITIME": "17", "CHER": "18", "CORRÈZE": "19", "CÔTE-D’OR": "21",
        "CÔTES D'ARMOR": "22", "CREUSE": "23", "DORDOGNE": "24", "DOUBS": "25", "DRÔME": "26",
        "EURE": "27", "EURE-ET-LOIRE": "28", "FINISTÈRE": "29", "GARD": "30", "HAUTE-GARONNE": "31",
        "GERS": "32", "GIRONDE": "33", "HÉRAULT": "34", "ILLE-ET-VILAINE": "35", "INDRE": "36",
        "INDRE-ET-LOIRE": "37", "ISÈRE": "38", "JURA": "39", "LANDES": "40", "LOIR-ET-CHER": "41",
        "LOIRE": "42", "HAUTE-LOIRE": "43", "LOIRE-ATLANTIQUE": "44", "LOIRET": "45", "LOT": "46",
        "LOT-ET-GARONNE": "47", "LOZÈRE": "48", "MAINE-ET-LOIRE": "49", "MANCHE": "50", "MARNE": "51",
        "HAUTE-MARNE": "52", "MAYENNE": "53", "MEURTHE-ET-MOSELLE": "54", "MEUSE": "55", "MORBIHAN": "56",
        "MOSELLE": "57", "NIÈVRE": "58", "NORD": "59", "OISE": "60", "ORNE": "61", "PAS-DE-CALAIS": "62",
        "PUY-DE-DÔME": "63", "PYRÉNÉES-ATLANTIQUES": "64", "HAUTES-PYRÉNÉES": "65", "PYRÉNÉES-ORIENTALES": "66",
        "BAS-RHIN": "67", "HAUT-RHIN": "68", "RHÔNE": "69", "HAUTE-SAÔNE": "70", "SAÔNE-ET-LOIRE": "71",
        "SARTHE": "72", "SAVOIE": "73", "HAUTE-SAVOIE": "74", "PARIS": "75", "SEINE-MARITIME": "76",
        "SEINE-ET-MARNE": "77", "YVELINES": "78", "DEUX-SÈVRES": "79", "SOMME": "80", "TARN": "81",
        "TARN-ET-GARONNE": "82", "VAR": "83", "VAUCLUSE": "84", "VENDÉE": "85", "VIENNE": "86",
        "HAUTE-VIENNE": "87", "VOSGES": "88", "YONNE": "89", "TERRITOIRE-DE-BELFORT": "90",
        "ESSONNE": "91", "HAUTS-DE-SEINE": "92", "SEINE-SAINT-DENIS": "93", "VAL-DE-MARNE": "94",
        "VAL-D'OISE": "95"
    }
    df_soleil["Code_INSEE"] = df_soleil["Departements"].map(codes_insee)

    # Charger les données de sol
    df_sol = pd.read_csv("src/data/LUCAS-SOIL-2018.csv")
    chem_columns = ["pH_CaCl2", "pH_H2O", "EC", "OC", "CaCO3", "P", "N", "K", "Ox_Al", "Ox_Fe"]

    # Assurez-vous que toutes les colonnes de chimie sont numériques
    df_sol[chem_columns] = df_sol[chem_columns].apply(pd.to_numeric, errors='coerce')

    # Supprimer les lignes où il manque des valeurs dans les colonnes pertinentes
    df_sol = df_sol.dropna(subset=["TH_LAT", "TH_LONG"] + chem_columns)

    # Remplir les valeurs NaN restantes (si nécessaire)
    df_sol[chem_columns] = df_sol[chem_columns].fillna(-float('inf'))  # Remplacer les NaN par -inf

    # Calculer la colonne Dominant_Chemical
    df_sol["Dominant_Chemical"] = df_sol[chem_columns].idxmax(axis=1)

    # Charger le fichier GeoJSON des départements
    geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
    geojson_data = requests.get(geojson_url).json()

    # Création de la carte d'ensoleillement
    fig_sunlight = px.choropleth_mapbox(
        df_soleil,
        geojson=geojson_data,
        locations="Code_INSEE",
        featureidkey="properties.code",
        color="ensoleillement (jours/an)",
        color_continuous_scale="YlOrRd",
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 46.603354, "lon": 1.888334},
        opacity=0.7
    )
    fig_sunlight.update_layout(title="Carte de l'ensoleillement en France (jours/an)")

    # Création de la carte des sols avec scatter_mapbox
    fig_soil = px.scatter_mapbox(
        df_sol,
        lat="TH_LAT",
        lon="TH_LONG",
        color="Dominant_Chemical",
        hover_data=chem_columns,
        title="Carte des Composés Chimiques Dominants en Europe",
        color_continuous_scale="viridis",
        mapbox_style="carto-positron",
        zoom=4,
        opacity=0.8
    )

    # Affichage des cartes dans Streamlit
    st.image("src/img/terre.gif",use_container_width =True, width=350)
    st.plotly_chart(fig_sunlight, use_container_width=True)
    st.image("src/img/ezgif.gif",use_container_width =True, width=350)
    st.plotly_chart(fig_soil, use_container_width=True)


def summary_model1():
    df_quality = pd.read_csv("src/data/winequality-red.csv")
    X = df_quality['alcohol']
    y = df_quality['quality']

    # Ajouter une constante pour l'intercept
    X = sm.add_constant(X)

    # Ajuster le modèle de régression
    model = sm.OLS(y, X).fit()

    # Obtenir le résumé du modèle
    summary_model1 = model.summary()

    # Afficher un cadre avec "Model 1" comme titre
    st.markdown("""
    <div style="border: 2px solid grey; padding: 10px; border-radius: 10px; background-color: #1d1f20;">
        <h3 style="text-align: center; font-size: 20px; font-weight: bold;">Model 1</h3>
        <pre style="white-space: pre-wrap; font-size: 14px; word-wrap: break-word;">
    """ + summary_model1.as_text() + """
        </pre>
    </div>
    """, unsafe_allow_html=True)

def summary_model2():
    df_quality = pd.read_csv("src/data/winequality-red.csv")
    
    # Sélection des variables
    X = df_quality[['alcohol', 'volatile acidity', 'sulphates', 'citric acid']]
    y = df_quality['quality']

    # Ajouter une constante pour l'intercept
    X = sm.add_constant(X)

    # Ajuster le modèle de régression
    model = sm.OLS(y, X).fit()

    # Obtenir le résumé du modèle
    model_summary = model.summary()

    # Afficher un cadre avec "Model 2" comme titre
    st.markdown("""
    <div style="border: 2px solid grey; padding: 10px; border-radius: 10px; background-color: #1d1f20;">
        <h3 style="text-align: center; font-size: 20px; font-weight: bold;">Model 2</h3>
        <pre style="white-space: pre-wrap; font-size: 14px; word-wrap: break-word;">
    """ + model_summary.as_text() + """
        </pre>
    </div>
    """, unsafe_allow_html=True)

def summary_model3():
    df_quality = pd.read_csv("src/data/winequality-red.csv")
    
    # Sélection des variables
    X = df_quality[['alcohol', 'volatile acidity', 'sulphates']]
    y = df_quality['quality']

    # Ajouter une constante pour l'intercept
    X = sm.add_constant(X)

    # Ajuster le modèle de régression
    model = sm.OLS(y, X).fit()

    # Obtenir le résumé du modèle
    model_summary = model.summary()

    # Afficher un cadre avec "Model 3" comme titre
    st.markdown("""
    <div style="border: 2px solid grey; padding: 10px; border-radius: 10px; background-color: #1d1f20;">
        <h3 style="text-align: center; font-size: 20px; font-weight: bold;">Model 3</h3>
        <pre style="white-space: pre-wrap; font-size: 14px; word-wrap: break-word;">
    """ + model_summary.as_text() + """
        </pre>
    </div>
    """, unsafe_allow_html=True)

def plot_residuals_model3():
    # Charger les données et ajuster le modèle
    df_quality = pd.read_csv("src/data/winequality-red.csv")
    X = df_quality[['alcohol', 'volatile acidity', 'sulphates']]
    y = df_quality['quality']
    
    # Ajouter une constante pour l'intercept
    X = sm.add_constant(X)
    
    # Ajuster le modèle de régression
    model = sm.OLS(y, X).fit()
    
    # Récupérer les résidus
    residuals = model.resid
    
    # Créer le graphique avec Matplotlib et Seaborn
    plt.figure(figsize=(8, 6))

    # Histogramme des résidus
    sns.histplot(residuals, bins=30, kde=True, color='blue')
    
    # Ajouter les labels et titre
    plt.xlabel("Résidus")
    plt.ylabel("Fréquence")
    plt.title("Distribution des résidus")
    
    # Affichage dans un cadre avec le titre "Model 1"
    st.markdown("""
    <div style="border: 2px solid grey; padding: 10px; border-radius: 10px; background-color: #1d1f20;">
        <h3 style="text-align: center; font-size: 20px; font-weight: bold;">Model 3</h3>
    </div>
    """, unsafe_allow_html=True)

    # Afficher le graphique dans Streamlit
    st.pyplot(plt)

def plot_qqplot_model3():
    # Charger les données et ajuster le modèle
    df_quality = pd.read_csv("src/data/winequality-red.csv")
    X = df_quality[['alcohol', 'volatile acidity', 'sulphates']]
    y = df_quality['quality']
    
    # Ajouter une constante pour l'intercept
    X = sm.add_constant(X)
    
    # Ajuster le modèle de régression
    model = sm.OLS(y, X).fit()
    
    # Récupérer les résidus
    residuals = model.resid
    
    # Créer le Q-Q plot des résidus
    plt.figure(figsize=(8, 6))
    sm.qqplot(residuals, line='s')
    
    # Ajouter le titre
    plt.title("Q-Q Plot des résidus")
    

    # Afficher le graphique dans Streamlit
    st.pyplot(plt)

# Appeler la fonction pour afficher le Q-Q plot

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


def alcool():
    data = {
    "Facteur": [
        "Nutriments du sol", "pH du sol", "Type de sol",
        "Durée et intensité du soleil", "Température", "Cycle jour/nuit"
    ],
    "Impact sur la production de sucre (et donc sur le taux d'alcool)": [
        "Un sol riche en éléments nutritifs (azote, potassium) favorise la croissance de la vigne, mais un excès peut réduire la concentration en sucre des raisins.",
        "Le pH du sol affecte la disponibilité des nutriments. Un pH mal équilibré (trop acide ou trop alcalin) peut limiter la croissance et la production de sucre des raisins.",
        "Les sols bien drainés (sableux) permettent une maturation plus lente des raisins, tandis que les sols plus lourds (argileux ou calcaires) peuvent augmenter la concentration en sucre.",
        "Un ensoleillement prolongé et intense favorise la photosynthèse, augmentant la production de sucre dans les raisins, ce qui peut augmenter le taux d'alcool du vin.",
        "Les températures plus élevées accélèrent la maturation des raisins et favorisent l'accumulation de sucre, ce qui donne un vin avec un taux d'alcool plus élevé.",
        "Un grand écart thermique entre le jour et la nuit peut favoriser l'accumulation de sucre tout en maintenant l'acidité des raisins, créant ainsi un équilibre propice à une bonne fermentation."
    ],
    "Tendance alcool": [
        "Augmentation", "Diminution", "Augmentation",
        "Augmentation", "Augmentation", "Augmentation"
    ]
}

    # Création du DataFrame

    # Fonction pour générer un mini graphe
    def plot_trend(tendance):
        fig, ax = plt.subplots(figsize=(1.5, 1.5))
        if tendance == "Augmentation":
            ax.barh([0], [1], color='green')
        else:
            ax.barh([0], [1], color='red')
        ax.set_xlim(0, 1)
        ax.set_yticks([])
        ax.set_xticks([])

        return fig

    # Affichage du titre
    st.title("Impact des Facteurs Environnementaux sur le Taux d'Alcool du Vin")
    df = pd.DataFrame(data)
    # Affichage du tableau avec graphiques
    for i in range(len(df)):
        col1, col2 = st.columns([4, 1])  # Définir deux colonnes (plus large à gauche)
        
        with col1:
            st.write(f"**{df['Facteur'][i]}**")
            st.write(df['Impact sur la production de sucre (et donc sur le taux d\'alcool)'][i])
        
        with col2:
            fig = plot_trend(df['Tendance alcool'][i])
            st.pyplot(fig)

def matrice_correlation():
    df_quality = pd.read_csv("src/data/winequality-red.csv")
    corr = df_quality.corr()

    # Création de la figure pour la carte thermique
    plt.figure(figsize=(10, 5))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', annot_kws={'size': 10})

    # Titre de la carte thermique
    plt.title('Matrice de corrélation entre les variables')

    # Affichage de la carte thermique dans Streamlit
    st.pyplot(plt)

def sun():
    st.subheader("📊 Visualisation Sunburst : Moyenne des Notes de Vin")

    # Chargement des données
    file_path = "src/data/winemagcontinent.csv"
    winemagcontinent_df = pd.read_csv(file_path)

    # Vérification si les données sont chargées correctement
    if winemagcontinent_df is not None:
        # Calcul de la moyenne des points par province
        df_province = winemagcontinent_df.groupby(['continent', 'country', 'province'], as_index=False)['points'].mean()

        # Création du diagramme Sunburst
        fig = px.sunburst(
            df_province,
            path=['continent', 'country', 'province'],  # Hiérarchie : Continent → Pays → Province
            values='points',  # Moyenne des notes comme valeurs
            color='points',  # Coloration selon la moyenne des notes
            color_continuous_scale='rdylgn',  # Palette de couleurs
            title="Moyenne des notes de vin par Province, Pays et Continent"
        )

        # Affichage du graphique
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Les données n'ont pas pu être chargées. Vérifiez le fichier CSV.")

def price_vs_score_plot():
    st.subheader("📊 Relation entre le prix et le score du vin")

    # Chargement des données
    file_path = "src/data/wine_data.csv"  # 🔧 Remplace par ton fichier réel
    df = pd.read_csv(file_path)

    if df is not None:
        # Vérifier que les colonnes nécessaires existent
        if "price" not in df.columns or "points" not in df.columns:
            st.error("Le fichier ne contient pas les colonnes 'price' et 'points'.")
            return

        # Supprimer les valeurs manquantes
        df = df.dropna(subset=["price", "points"])

        # Créer des tranches de prix
        price_bins = pd.cut(df["price"], bins=np.linspace(0, df["price"].quantile(0.95), 10), include_lowest=True)
        price_bin_centers = price_bins.cat.categories.mid  # Centres des tranches

        # Calculer les moyennes des scores par tranche de prix
        mean_scores = df.groupby(price_bins)["points"].mean()

        # Création du graphique
        fig, ax = plt.subplots(figsize=(10, 6))

        # Tracer uniquement les moyennes des scores par tranche de prix
        ax.plot(price_bin_centers, mean_scores, marker="o", color="orange", label="Moyenne des scores")

        # Ajouter une régression linéaire (courbe de tendance globale)
        sns.regplot(x=df["price"], y=df["points"], scatter=False, color="red", line_kws={"linewidth": 2, "alpha": 0.8}, label="Tendance globale", ax=ax)

        # Configurer les limites des axes
        ax.set_xlim(0, df["price"].quantile(0.95))  # Exclure les valeurs extrêmes
        ax.set_ylim(80, 100)

        # Ajouter un titre et des labels d'axes
        ax.set_title("Relation entre le prix et le score du vin", fontsize=14, fontweight="bold")
        ax.set_xlabel("Prix ($)")
        ax.set_ylabel("Points")

        # Ajouter une légende
        ax.legend()

        # Améliorer la mise en page
        plt.tight_layout()

        # Affichage du graphique dans Streamlit
        st.pyplot(fig)
    else:
        st.warning("Les données n'ont pas pu être chargées. Vérifiez le fichier.")


def general():
    # Interface principale avec onglets
    st.title("Tableau de Bord sur le Vin 🍷")
    tabs = st.tabs(["📊 Distribution des Notes et Analyse des Scores","📈 Variété et prix ","🍷 Caractéristique d'un bon vin"," ⛅Type de sol et Soleil"])

    with tabs[0]:
        distrib_note()
        distrib_meanscore()
        sun()
        price_vs_score_plot()

    with tabs[1]:
        top_countries_chart()
        top_varieties_chart()
        price_comparison_chart()
        

    with tabs[3]:
        
        # load_and_display_sunshine_map()
        load_and_display_soil_sunlight_map()
        alcool()

    with tabs[2] :
        # add the gif
        
        matrice_correlation()
        summary_model1()
        summary_model2()
        summary_model3()
        plot_residuals_model3()
        plot_qqplot_model3()


