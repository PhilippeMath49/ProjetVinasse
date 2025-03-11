import pandas as pd
import plotly.express as px

# Charger le fichier fusionné
df_wine_export_world = pd.read_csv("data/wineexports/allwine_export_world_no_empty.csv")

# Choisir l'année à analyser
annee_cible = 2023  # Remplace par l'année souhaitée
df_filtered = df_wine_export_world[df_wine_export_world["refPeriodId"] == annee_cible]

# Regrouper les données par pays exportateur et sommer les quantités exportées
df_grouped = df_filtered.groupby("reporterISO", as_index=False)["qtyUnitAbbr"].sum()

# Sélectionner les 10 plus grands exportateurs
df_top10 = df_grouped.nlargest(10, "qtyUnitAbbr")

# Créer un histogramme (bar chart)
fig = px.bar(
    df_top10,
    x="reporterISO",
    y="qtyUnitAbbr",
    title=f"Top 10 des exportateurs de vin en {annee_cible}",
    labels={"reporterISO": "Pays exportateur", "qtyUnitAbbr": "Quantité exportée"},
    text_auto=True,  # Affiche les valeurs sur les barres
    color="qtyUnitAbbr",  # Ajoute une couleur basée sur la quantité exportée
    color_continuous_scale="Reds"  # Palette de couleurs
)

# Améliorer l'affichage
fig.update_layout(xaxis={'categoryorder':'total descending'})  # Trier les barres par ordre décroissant

# Afficher le graphique
fig.show()
