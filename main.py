# main.py
import pandas as pd  # Pour les manipulations de données
import numpy as np  # Pour les calculs numériques
import matplotlib.pyplot as plt  # Pour les graphiques
import seaborn as sns  # Pour les visualisations
from data_extraction import data_extraction  # Import de la fonction depuis data_extraction.py
from data_map import get_average_ratings_by_country, plot_map
from data_prompt import wine_prod_prompt
from data_treatment import wine_prod_treatment


def Wine_Prod():
    wineprod_df = data_extraction("data/wine-production/wine-production.csv")
    wineprod_treated_df = wine_prod_treatment(wineprod_df)
    wine_prod_prompt(wineprod_treated_df)

def main():
    Wine_Prod()



# Exécuter le script principal
if __name__ == "__main__":
    main()
