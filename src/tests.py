import pandas as pd  # Pour les manipulations de données
import numpy as np  # Pour les calculs numériques
import matplotlib.pyplot as plt  # Pour les graphiques
import seaborn as sns  # Pour les visualisations
import geopandas as gpd  # Pour les cartes géographiques
from lib.data import Data
import plotly.express as px
import chardet



def modif():



    wineexport1_df = pd.read_csv('data/wineexports/TradeData_2_20_2025_10_30_9.csv', encoding='ISO-8859-1')
    wineexport2_df = pd.read_csv('data/wineexports/TradeData_2_20_2025_10_29_8.csv', encoding='ISO-8859-1')
    wineexport3_df = pd.read_csv('data/wineexports/TradeData_2_20_2025_10_17_32.csv', encoding='ISO-8859-1')
    #typeCode,freqCode,refPeriodId,refYear,refMonth,period,reporterCode,
    #|reporterISO|,reporterDesc,flowCode,|flowDesc|,partnerCode,partnerISO,
    #|partnerDesc|,partner2Code,partner2ISO,partner2Desc,classificationCode,
    #classificationSearchCode,isOriginalClassification,cmdCode,cmdDesc,
    # aggrLevel,isLeaf,customsCode,customsDesc,mosCode,motCode,motDesc,
    # |qtyUnitCode,qtyUnitAbbr,qty,isQtyEstimated|,altQtyUnitCode,altQtyUnitAbbr,
    # altQty,isAltQtyEstimated,netWgt,isNetWgtEstimated,grossWgt,isGrossWgtEstimated,
    # cifvalue,fobvalue,primaryValue,legacyEstimationFlag,isReported,isAggregate
    wineexport1_df = wineexport1_df.drop(['typeCode', 'freqCode', 'refPeriodId', 'refYear', 'period', 'reporterCode'], axis=1)
    print(wineexport1_df.head())



def main():
    modif()


# Exécuter le script principal
if __name__ == "__main__":
    main()
