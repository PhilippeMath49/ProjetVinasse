import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_extraction import data_extraction  # Assurez-vous que ce fichier est bien dans le même répertoire
import numpy as np
import geodatasets  # Importer geodatasets pour accéder aux données géographiques


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

