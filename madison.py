# -*- coding: utf-8 -*-
"""
More in-depth analysis of food assistance resources and vulerable older adults in Madison County, NY 

"""

import geopandas as gpd
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 

#setting default DPI 
plt.rcParams['figure.dpi'] = 300
 
#reading in csv files and geopackages produced in earlier scripts
census = pd.read_csv('census.csv')
NYSOFA = gpd.read_file('AAAmeals.gpkg')

#highlighting Madison county's population of older adults
