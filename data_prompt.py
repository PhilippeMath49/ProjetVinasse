import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def wine_prod_prompt(wineprod_treated_df):
    # 1. Histogramme de la production par pays
    fig1 = px.bar(wineprod_treated_df, x='Entity', y='Wine', color='Entity',
                  title='Production par Pays',
                  category_orders={'Pays': sorted(wineprod_treated_df['Entity'].unique())},  # Ordre des pays
                  labels={'Wine': 'Production Total', 'Entity': 'Country'})

    # 2. Courbe de la production par année et par pays
    fig2 = px.line(wineprod_treated_df, x='Year', y='Wine', color='Entity',
                   title='Production par Année par Pays',
                   markers=True, labels={'Wine': 'Production', 'Year': 'Année', 'Entity': 'Pays'})

    # Affichage des graphiques
    fig1.show()
    fig2.show()