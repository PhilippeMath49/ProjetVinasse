import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import geopandas as gpd

class Data:
    
    def data_extraction(csv):
        """
        Charge un fichier CSV et retourne un DataFrame pandas.
        """
        try:
            wineprod_df = pd.read_csv(csv)
            return wineprod_df
        except FileNotFoundError:
            print(f"Erreur: Le fichier '{csv}' n'a pas été trouvé.")
            return None
        except pd.errors.EmptyDataError:
            print(f"Erreur: Le fichier '{csv}' est vide.")
            return None
        except pd.errors.ParserError:
            print(f"Erreur: Il y a un problème de parsing avec le fichier '{csv}'.")
            return None


    def get_average_ratings_by_country(winetaste_df):
        """
        Calcule la moyenne des notes des vins par pays.
        """
        # Regrouper les données par pays et calculer la moyenne des notes
        ratings_by_country = winetaste_df.groupby('country')['points'].mean().reset_index()

        return ratings_by_country


    def plot_map(ratings_by_country):
        """
        Affiche une carte du monde avec des couleurs basées sur les notes moyennes des vins par pays.
        """
        # Charger la carte du monde à l'aide de GeoPandas et geodatasets
        shapefile_path = "ne_110m_land/ne_110m_land.shp"
        world = gpd.read_file(shapefile_path)

        world.boundary.plot()
        plt.show()


    def wine_prod_prompt(wineprod_treated_df):
        
        """
        Affiche les graphiques de production de vin.
        """
        fig1 = px.bar(wineprod_treated_df, x='Entity', y='Wine', color='Entity',
                    title='Production par Pays',
                    category_orders={'Pays': sorted(wineprod_treated_df['Entity'].unique())},  # Ordre des pays
                    labels={'Wine': 'Production Total', 'Entity': 'Country'})

        # 2. Courbe de la production par année et par pays
        fig2 = px.line(wineprod_treated_df, x='Year', y='Wine', color='Entity',
                    title='Production par Année par Pays',
                    markers=True, labels={'Wine': 'Production', 'Year': 'Année', 'Entity': 'Pays'})

        # Affichage des graphiques
        fig1.show()
        fig2.show()


    def wine_prod_treatment(wineprod_df):
        wineprod_treated_df = wineprod_df.drop('Code', axis=1)
        return wineprod_treated_df


    def __init__(self, data):
        self.data = data
