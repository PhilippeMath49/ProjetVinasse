# main.py
import pandas as pd  # Pour les manipulations de données
import numpy as np  # Pour les calculs numériques
import matplotlib.pyplot as plt  # Pour les graphiques
import seaborn as sns  # Pour les visualisations
from data_extraction import data_extraction  # Import de la fonction depuis data_extraction.py


def main():
    # Charge les données à partir du fichier CSV
    winetaste_df = data_extraction("winemag-data-130k-v2.csv")

    # Vérifie si les données ont été chargées avec succès
    if winetaste_df is not None:
        print(winetaste_df.head())  # Affiche les premières lignes du DataFrame
        # Vous pouvez ajouter des visualisations ou des analyses ici
    else:
        print("L'extraction des données a échoué.")


# Exécuter le script principal
if __name__ == "__main__":
    main()
