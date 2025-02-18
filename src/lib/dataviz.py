import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
def load_data():
    file_path = "../data/winemag.csv"  # Modifier selon l'emplacement
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Titre de l'application
st.title("🍷 Analyse des Vins - Projet Vinasse")

# Affichage des données
toggle = st.checkbox("Afficher les données brutes")
if toggle:
    st.write(df.head())

# Statistiques générales
st.subheader("Statistiques générales")
st.write(df[['price', 'points']].describe())

# Visualisation : Distribution des prix
st.subheader("Distribution des prix")
fig, ax = plt.subplots()
sns.histplot(df['price'].dropna(), bins=30, kde=True, ax=ax)
st.pyplot(fig)

# Filtrage par pays
st.subheader("Filtrer les vins par pays")
country = st.selectbox("Sélectionnez un pays", df['country'].dropna().unique())
filtered_df = df[df['country'] == country]
st.write(filtered_df[['title', 'price', 'points']].head(10))

# Meilleures régions viticoles
st.subheader("Top 10 des meilleures régions viticoles")
top_regions = df.groupby('province')['points'].mean().sort_values(ascending=False).head(10)
st.bar_chart(top_regions)

st.markdown("---")
st.markdown("📌 *Application développée avec Streamlit* ")

