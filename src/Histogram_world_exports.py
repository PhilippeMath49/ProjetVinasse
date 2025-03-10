

import pandas as pd
import plotly.express as px

# Charger le fichier fusionné
df_wine_export_world = pd.read_csv("src/data/wineexports/allwine_export_world_no_empty.csv")

# Choisir l'année à analyser
annee_cible = 2023  # Remplace par l'année que tu veux
df_wine_export_world_filtered = df_wine_export_world[df_wine_export_world["refPeriodId"] == annee_cible]

# Regrouper les données par pays exportateur et sommer les quantités exportées
df_wine_export_world_grouped = df_wine_export_world_filtered.groupby("reporterISO", as_index=False)["qtyUnitAbbr"].sum()

# Créer un histogramme (bar chart)
fig = px.bar(
    df_wine_export_world_grouped,
    x="reporterISO",
    y="qtyUnitAbbr",
    title="Exportations par pays (vers le monde)",
    labels={"reporterISO": "Pays exportateur", "qtyUnitAbbr": "Quantité exportée"},
    text_auto=True  # Affiche les valeurs sur les barres
)

# Afficher le graphique
fig.show()