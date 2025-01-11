import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def data_extraction(csv):
    """
    Charge un fichier CSV et retourne un DataFrame pandas.
    """
    try:
        wineprod_df = pd.read_csv(csv)
        return wineprod_df
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{csv}' n'a pas été trouvé.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Erreur: Le fichier '{csv}' est vide.")
        return None
    except pd.errors.ParserError:
        print(f"Erreur: Il y a un problème de parsing avec le fichier '{csv}'.")
        return None
