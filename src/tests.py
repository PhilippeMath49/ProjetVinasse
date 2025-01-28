import pandas as pd  # Pour les manipulations de données
import numpy as np  # Pour les calculs numériques
import matplotlib.pyplot as plt  # Pour les graphiques
import seaborn as sns  # Pour les visualisations
import geopandas as gpd  # Pour les cartes géographiques
from lib.data import Data


def Wine_Prod():
    # Extraction des données de production de vin depuis le fichier CSV
    wineprod_df = Data.data_extraction("data/wine-production/wine-production.csv")

    # Traitement des données (nettoyage, préparation)
    wineprod_treated_df = Data.wine_prod_treatment(wineprod_df)

    # Suppression des codes de pays entre parenthèses
    wineprod_treated_df['Entity'] = wineprod_treated_df['Entity'].str.replace(r"\s\([A-Z]{3}\)", "", regex=True)

    #date_specific = '2021'
    #filtered_df = wineprod_treated_df[wineprod_treated_df['Year'] == date_specific]
    #print(filtered_df.head())
    # Vérification des colonnes pour voir comment fusionner
    print("Colonnes de wineprod_treated_df : ", wineprod_treated_df.columns)

    # Charger la carte du monde (shapefile)
    shapefile_path = "map/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
    world = gpd.read_file(shapefile_path)
    # Vérification des colonnes du shapefile
    print("Colonnes de world : ", world.columns)

    # Assurez-vous que les noms de pays sont compatibles entre les deux DataFrames.
    # Vérifiez la colonne contenant les noms des pays dans 'world'.
    # Par exemple, cela pourrait être 'name' dans le shapefile et 'Entity' dans wineprod_treated_df.
    merged = world.set_index('SOVEREIGNT').join(wineprod_treated_df.set_index('Entity'), how='left')

    # Tracer la carte avec une couleur différente par pays en fonction de la production de vin
    fig, ax = plt.subplots(figsize=(15, 10))

    # Utilisation de la colonne 'Wine' pour colorier les pays
    merged.plot(ax=ax, column='Wine', cmap='coolwarm', legend=True,
                legend_kwds={'label': "Production de vin par pays", 'orientation': "horizontal"})

    # Assurer que l'aspect de la carte est égal
    ax.set_aspect('equal')

    # Afficher la carte
    plt.show()


def main():
    Wine_Prod()


# Exécuter le script principal
if __name__ == "__main__":
    main()
