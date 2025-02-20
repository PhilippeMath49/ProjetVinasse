# main.py
import pandas as pd  # Pour les manipulations de données
import numpy as np  # Pour les calculs numériques
import matplotlib.pyplot as plt  # Pour les graphiques
import seaborn as sns  # Pour les visualisations
import dataviz.page1 as page1  # Pour les visualisations




def main():
    # page1.Page1.general("./data/wine-production/wine-production.csv", "./data/winemag.csv")
    import os
    import streamlit as st

    st.write("Contenu du dossier data :", os.listdir("./data"))
    st.write("Contenu du dossier wine-production :", os.listdir("./data/wine-production"))

    
    



# Exécuter le script principal
if __name__ == "__main__":
    main()
