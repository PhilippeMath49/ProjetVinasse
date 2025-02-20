import pandas as pd  # Pour les manipulations de données
import numpy as np  # Pour les calculs numériques
import matplotlib.pyplot as plt  # Pour les graphiques
import seaborn as sns  # Pour les visualisations
import geopandas as gpd  # Pour les cartes géographiques
from lib.data import Data
import plotly.express as px
import pycountry_convert as pc
import pycountry

def normalize_country_name(country):
    """Essaie de normaliser un nom de pays donné en utilisant pycountry."""
    try:
        # Vérifie si le pays existe sous forme d'alpha-2 ou alpha-3
        country_obj = pycountry.countries.lookup(country)
        return country_obj.name  # Retourne le nom officiel du pays
    except LookupError:
        return country  # Si introuvable, renvoie le nom d'origine

def get_continent(country_name):
    """Renvoie le continent associé à un pays donné."""
    try:
        normalized_country = normalize_country_name(country_name)
        country_alpha2 = pc.country_name_to_country_alpha2(normalized_country)
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        continents = {
            "AF": "Afrique",
            "AS": "Asie",
            "EU": "Europe",
            "NA": "Amérique du Nord",
            "SA": "Amérique du Sud",
            "OC": "Océanie",
            "AN": "Antarctique"
        }
        return continents.get(continent_code, "Inconnu")
    except:
        return "Inconnu"

def modif():
    winemag_df = Data.data_extraction("data/winemag.csv")


    # Ajout de la colonne continent
    winemag_df['continent'] = winemag_df['country'].apply(get_continent)
    winemag_df.to_csv('data/winemagcontinent.csv', index=False)
    df_province = winemag_df.groupby(['continent', 'country', 'province'], as_index=False)['points'].mean()

    # Création du diagramme Sunburst
    fig = px.sunburst(
        df_province,
        path=['continent', 'country', 'province'],  # Hiérarchie : Continent → Pays → Province
        values='points',  # Utilisation des moyennes de notes comme valeurs
        color='points',  # Coloration selon la moyenne des notes
        color_continuous_scale='RdBu',  # Palette de couleurs
        title="Moyenne des notes de vin par Province, Pays et Continent"
    )

    # Affichage du graphique
    fig.show()


def main():
    modif()


# Exécuter le script principal
if __name__ == "__main__":
    main()
