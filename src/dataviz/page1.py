import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import os

# Charger les données
class Page1:
    


    # Nettoyage et traitement
    def clean_wine_data(df):
        df.dropna(subset=["Entity", "Wine"], inplace=True)
        df["Year"] = df["Year"].astype(int)
        return df.groupby("Entity")["Wine"].median().reset_index()
    
    def general():
        wine_prod_df = pd.read_csv("src/data/wine-production/wine-production.csv")
        reviews_df = pd.read_csv("src/data/winemag.csv")
        wine_prod_df = Page1.clean_wine_data(wine_prod_df)

        # Charger les données géographiques
        
        fig_map = Page1.map()

        # Création d'un histogramme des notes de vin
        fig_hist = px.histogram(reviews_df, x="points", nbins=20, title="Distribution des Notes de Vin")

        # Création de l'application Streamlit
        st.title("Tableau de Bord sur le Vin")

        st.subheader("Production de Vin par Pays")
        st.plotly_chart(fig_map)

        st.subheader("Distribution des Notes de Vin")
        st.plotly_chart(fig_hist)
        
        
        
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
        st.title("🌍 Visualisation de la production de vin")
        
        wine_df, world = Page1.load_data()
        if wine_df is None or world is None:
            return
        
        # Sélection de l'année
        selected_year = st.slider("Sélectionnez une année", min_value=int(wine_df['Year'].min()), max_value=int(wine_df['Year'].max()), value=2010)
        
        # Filtrer les données par année
        filtered_df = wine_df[wine_df['Year'] == selected_year]
        
        # Fusion avec les données géographiques
        merged = world.merge(filtered_df, left_on="NAME", right_on="Entity", how="left")
        
        # Création de la carte avec Plotly
        fig = px.choropleth(merged, geojson=merged.geometry, locations=merged.index,
                            color='Wine', title=f"Production de vin en {selected_year}",
                            hover_name="Entity", projection="natural earth")
        
        st.plotly_chart(fig)
def main():
    Page1.general()
    
    
if __name__ == "__main__":
    main()
        
