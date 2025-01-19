# main.py
import pandas as pd  # Pour les manipulations de données
import numpy as np  # Pour les calculs numériques
import matplotlib.pyplot as plt  # Pour les graphiques
import seaborn as sns  # Pour les visualisations
from data import Data  


def Wine_Prod():
    wineprod_df = Data.data_extraction("data/wine-production/wine-production.csv")
    wineprod_treated_df = Data.wine_prod_treatment(wineprod_df)
    Data.wine_prod_prompt(wineprod_treated_df)

def main():
    Wine_Prod()



# Exécuter le script principal
if __name__ == "__main__":
    main()
