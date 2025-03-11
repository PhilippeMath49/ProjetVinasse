import pandas as pd
import plotly.graph_objects as go
import numpy as np
import holoviews as hv
from holoviews import opts

hv.extension('bokeh')

df_wine_export_ctc = pd.read_csv("data/wineexports/allwine_export_ctc_no_empty.csv")

countries = list(set(df_wine_export_ctc["reporterISO"].unique()) | set(df_wine_export_ctc["partnerISO"].unique()))

# Création d'une matrice d'adjacence
matrix = np.zeros((len(countries), len(countries)))

for _, row in df_wine_export_ctc.iterrows():
    i = countries.index(row["reporterISO"])
    j = countries.index(row["partnerISO"])
    matrix[i, j] = row["qtyUnitAbbr"]

# Création du Chord Diagram façon Sankey
fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=countries,
        pad=15,
        thickness=20,
    ),
    link=dict(
        source=[countries.index(exp) for exp in df_wine_export_ctc["reporterISO"]],
        target=[countries.index(imp) for imp in df_wine_export_ctc["partnerISO"]],
        value=df_wine_export_ctc["qtyUnitAbbr"]
    )
)])

fig.update_layout(title_text="Flux d'exportation pays à pays (Chord Diagram façon Sankey)")
fig.show()