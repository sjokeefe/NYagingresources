# -*- coding: utf-8 -*-
"""
NYSOFA data visualizations 
Disparities in NY State Older Adult food insecurity 

"""
#creating some figures for visual reference 
import geopandas as gpd
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 

#setting default DPI 
plt.rcParams['figure.dpi'] = 300
 
#reading in csv files and geopackages produced in earlier scripts
census = pd.read_csv('census.csv')
NYSOFA = gpd.read_file('AAAmeals.gpkg')

