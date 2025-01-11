import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def wine_prod_treatment(wineprod_df):
    wineprod_treated_df = wineprod_df.drop('Code', axis=1)
    return wineprod_treated_df