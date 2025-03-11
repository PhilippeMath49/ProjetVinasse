import streamlit as st
import pandas as pd

# Configuration de la page (doit être appelée en premier dans le script)
st.set_page_config(page_title="Exploration de CSV", layout="wide")

# Fonction pour charger les données
@st.cache_data  # Mise en cache des données pour éviter de les recharger à chaque clic
def load_data(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return None

# Fonction pour afficher les informations du dataset
def display_dataset_info(df):
    st.write("### Aperçu des données :")
    st.dataframe(df)

    # Affichage des informations sur le dataset
    with st.expander("Informations sur le dataset"):
        st.write("**Nombre de lignes :**", df.shape[0])
        st.write("**Nombre de colonnes :**", df.shape[1])
        st.write("**Colonnes :**", df.columns.tolist())
        st.write("**Résumé statistique :**")
        st.write(df.describe())

# Fonction principale qui affiche tout
def main():
    # Sidebar pour sélectionner le dataset
    st.sidebar.title("Sélectionnez un fichier CSV")

    # Si une option est déjà sélectionnée dans le session_state, on l'utilise
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = "Wine Quality (Red)"  # Valeur par défaut

    option = st.sidebar.radio(
        "Choisissez un dataset :",
        [
            "WineMag",
            "Wine Quality (Red)",
            "Temps d'ensoleillement",
            "LUCAS Soil 2018",
            "Wine Production"
        ],
        index=["WineMag", "Wine Quality (Red)", "Temps d'ensoleillement", "LUCAS Soil 2018", "Wine Production"].index(st.session_state.selected_option)
    )

    # Sauvegarder la sélection dans session_state
    st.session_state.selected_option = option

    # Dictionnaire des fichiers CSV avec le chemin relatif src/data/
    csv_files = {
        "WineMag": "src/data/winemag.csv",
        "Wine Quality (Red)": "src/data/winequality-red.csv",
        "Temps d'ensoleillement": "src/data/temps-densoleillement-par-an-par-departement-feuille-1.csv",
        "LUCAS Soil 2018": "src/data/LUCAS-SOIL-2018.csv",
        "Wine Production": "src/data/wine-production.csv"
    }

    # Chargement des données et affichage
    df = None
    if option in csv_files:
        df = load_data(csv_files[option])
        if df is not None:
            st.title(f"Exploration du fichier : {option}")
            display_dataset_info(df)

    # Option pour afficher plus d'infos sur les datasets
    if df is None:
        st.warning("Sélectionnez un fichier pour afficher les données")

# Lancer l'application principale
if __name__ == "__main__":
    main()
