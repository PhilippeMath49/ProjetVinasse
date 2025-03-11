import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Exploration de CSV", layout="wide")

# Fonction pour charger les données avec mise en cache
@st.cache_data
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

    # Informations sur le dataset
    with st.expander("Informations sur le dataset"):
        st.write(f"**Nombre de lignes :** {df.shape[0]}")
        st.write(f"**Nombre de colonnes :** {df.shape[1]}")
        st.write(f"**Colonnes :** {df.columns.tolist()}")
        st.write("**Résumé statistique :**")
        st.write(df.describe())

# Fonction principale
def main():
    # Initialiser l'état d'affichage de la barre latérale
    if "show_sidebar" not in st.session_state:
        st.session_state.show_sidebar = False  # Par défaut, la barre latérale est masquée

    # Bouton pour afficher/masquer la barre latérale
    if st.button("🔧 Options Dataset"):
        st.session_state.show_sidebar = not st.session_state.show_sidebar

    # Dictionnaire des fichiers CSV
    csv_files = {
        "WineMag": "src/data/winemag.csv",
        "Wine Quality (Red)": "src/data/winequality-red.csv",
        "Temps d'ensoleillement": "src/data/temps-densoleillement-par-an-par-departement-feuille-1.csv",
        "LUCAS Soil 2018": "src/data/LUCAS-SOIL-2018.csv",
        "Wine Production": "src/data/wine-production.csv"
    }

    # Afficher la barre latérale uniquement si `show_sidebar` est True
    if st.session_state.show_sidebar:
        with st.sidebar:
            st.title("Sélectionnez un fichier CSV")
            option = st.radio(
                "Choisissez un dataset :",
                list(csv_files.keys()),
                key="selected_option"
            )

    else:
        # Utiliser la dernière sélection connue si la barre est masquée
        option = st.session_state.get("selected_option", "Wine Quality (Red)")

    # Chargement et affichage des données
    df = load_data(csv_files[option])
    if df is not None:
        st.title(f"Exploration du fichier : {option}")
        display_dataset_info(df)
    else:
        st.warning("Impossible de charger les données. Vérifiez le fichier.")

# Lancer l'application
if __name__ == "__main__":
    main()
