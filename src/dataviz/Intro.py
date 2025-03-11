import streamlit as st
import pandas as pd


def main():
    # Configuration de la page
    st.set_page_config(page_title="Exploration de CSV", layout="wide")

    # Fonction pour charger les données
    def load_data(file):
        return pd.read_csv(file)

    # Sidebar pour sélectionner le dataset
    st.sidebar.title("Sélectionnez un fichier CSV")
    option = st.sidebar.radio(
        "Choisissez un dataset :",
        [
            "WineMag",
            "Wine Quality (Red)",
            "Temps d'ensoleillement",
            "LUCAS Soil 2018",
            "Wine Production"
        ]
    )

    # Dictionnaire des fichiers CSV (remplacez par vos chemins réels)
    csv_files = {
        "WineMag": "winemag.csv",
        "Wine Quality (Red)": "winequality-red.csv",
        "Temps d'ensoleillement": "temps-densoleillement-par-an-par-departement-feuille-1.csv",
        "LUCAS Soil 2018": "LUCAS-SOIL-2018.csv",
        "Wine Production": "wine-production.csv"
    }

    # Chargement des données
    if option in csv_files:
        try:
            df = load_data(csv_files[option])
            st.title(f"Exploration du fichier : {option}")
            st.write("### Aperçu des données :")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")
    else:
        st.warning("Sélectionnez un fichier pour afficher les données")

    # Option pour afficher plus d'infos sur les datasets
    if 'df' in locals():
        with st.expander("Informations sur le dataset"):
            st.write("**Nombre de lignes :**", df.shape[0])
            st.write("**Nombre de colonnes :**", df.shape[1])
            st.write("**Colonnes :**", df.columns.tolist())
            st.write("**Résumé statistique :**")
            st.write(df.describe())



