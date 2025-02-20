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
        wine_prod_df = pd.read_csv("/data/wine-production/wine-production.csv")
        reviews_df = pd.read_csv("/data/winemag.csv")
        wine_prod_df = Page1.clean_wine_data(wine_prod_df)

        # Charger les données géographiques
        shapefile_path = "/map/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
        world = gpd.read_file(shapefile_path)

        # Fusion des données
        world = world.merge(wine_prod_df, left_on="NAME", right_on="Entity", how="left")

        # Création de la carte interactive
        fig_map = px.choropleth(world, geojson=world.geometry, locations=world.index, color="Wine",
                                hover_name="Entity", title="Production de Vin par Pays")
        fig_map.update_geos(fitbounds="locations", visible=False)

        # Création d'un histogramme des notes de vin
        fig_hist = px.histogram(reviews_df, x="points", nbins=20, title="Distribution des Notes de Vin")

        # Création de l'application Streamlit
        st.title("Tableau de Bord sur le Vin")

        st.subheader("Production de Vin par Pays")
        st.plotly_chart(fig_map)

        st.subheader("Distribution des Notes de Vin")
        st.plotly_chart(fig_hist)
        
        
def main():
    Page1.general()
    
    
if __name__ == "__main__":
    main()
        
