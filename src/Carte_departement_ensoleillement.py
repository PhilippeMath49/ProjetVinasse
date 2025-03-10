import pandas as pd
import plotly.express as px
import json
import requests

# Charger les données
df_soleil = pd.read_csv("data/temps-densoleillement-par-an-par-departement-feuille-1.csv")

# Vérifier le nom exact des colonnes
print(df_soleil.columns)

# Convertir les noms des départements en majuscules pour correspondance
df_soleil["Departements"] = df_soleil["Departements"].str.upper()

# Dictionnaire des codes INSEE par département
codes_insee = {
    "AIN": "01", "AISNE": "02", "ALLIER": "03", "ALPES DE HAUTE PROVENCE": "04", "HAUTES-ALPES": "05",
    "ALPES-MARITIMES": "06", "ARDÈCHE": "07", "ARDENNES": "08", "ARIÈGE": "09", "AUBE": "10",
    "AUDE": "11", "AVEYRON": "12", "BOUCHES-DU-RHÔNE": "13", "CALVADOS": "14", "CANTAL": "15",
    "CHARENTE": "16", "CHARENTE-MARITIME": "17", "CHER": "18", "CORRÈZE": "19", "CÔTE-D’OR": "21",
    "CÔTES D'ARMOR": "22", "CREUSE": "23", "DORDOGNE": "24", "DOUBS": "25", "DRÔME": "26",
    "EURE": "27", "EURE-ET-LOIRE": "28", "FINISTÈRE": "29", "GARD": "30", "HAUTE-GARONNE": "31",
    "GERS": "32", "GIRONDE": "33", "HÉRAULT": "34", "ILLE-ET-VILAINE": "35", "INDRE": "36",
    "INDRE-ET-LOIRE": "37", "ISÈRE": "38", "JURA": "39", "LANDES": "40", "LOIR-ET-CHER": "41",
    "LOIRE": "42", "HAUTE-LOIRE": "43", "LOIRE-ATLANTIQUE": "44", "LOIRET": "45", "LOT": "46",
    "LOT-ET-GARONNE": "47", "LOZÈRE": "48", "MAINE-ET-LOIRE": "49", "MANCHE": "50", "MARNE": "51",
    "HAUTE-MARNE": "52", "MAYENNE": "53", "MEURTHE-ET-MOSELLE": "54", "MEUSE": "55", "MORBIHAN": "56",
    "MOSELLE": "57", "NIÈVRE": "58", "NORD": "59", "OISE": "60", "ORNE": "61", "PAS-DE-CALAIS": "62",
    "PUY-DE-DÔME": "63", "PYRÉNÉES-ATLANTIQUES": "64", "HAUTES-PYRÉNÉES": "65", "PYRÉNÉES-ORIENTALES": "66",
    "BAS-RHIN": "67", "HAUT-RHIN": "68", "RHÔNE": "69", "HAUTE-SAÔNE": "70", "SAÔNE-ET-LOIRE": "71",
    "SARTHE": "72", "SAVOIE": "73", "HAUTE-SAVOIE": "74", "PARIS": "75", "SEINE-MARITIME": "76",
    "SEINE-ET-MARNE": "77", "YVELINES": "78", "DEUX-SÈVRES": "79", "SOMME": "80", "TARN": "81",
    "TARN-ET-GARONNE": "82", "VAR": "83", "VAUCLUSE": "84", "VENDÉE": "85", "VIENNE": "86",
    "HAUTE-VIENNE": "87", "VOSGES": "88", "YONNE": "89", "TERRITOIRE-DE-BELFORT": "90",
    "ESSONNE": "91", "HAUTS-DE-SEINE": "92", "SEINE-SAINT-DENIS": "93", "VAL-DE-MARNE": "94",
    "VAL-D'OISE": "95"
}

# Ajouter les codes INSEE au DataFrame
df_soleil["Code_INSEE"] = df_soleil["Departements"].map(codes_insee)

print(df_soleil["Departements"])
# Vérifier si des valeurs sont manquantes
print(df_soleil[df_soleil["Code_INSEE"].isna()])

# Vérifier que la colonne ensoleillement est correcte
print(df_soleil.columns)

# Charger le fichier GeoJSON des départements français
geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
geojson_data = requests.get(geojson_url).json()

# Vérifier les propriétés du GeoJSON
print(geojson_data["features"][0]["properties"])

# Convertir Code_INSEE en chaîne
df_soleil["Code_INSEE"] = df_soleil["Code_INSEE"].astype(str)

# Créer une carte choroplèthe
fig = px.choropleth_mapbox(
    df_soleil,
    geojson=geojson_data,
    locations="Code_INSEE",  # Utilisation du code INSEE
    featureidkey="properties.code",  # Correspondance avec le GeoJSON
    color="ensoleillement (jours/an)",  # Vérifie le bon nom de colonne
    color_continuous_scale="YlOrRd",
    mapbox_style="carto-positron",
    zoom=5,
    center={"lat": 46.603354, "lon": 1.888334},  # Centre de la France
    opacity=0.7
)

fig.update_layout(title="Carte de l'ensoleillement en France (jours/an)")
fig.show()
