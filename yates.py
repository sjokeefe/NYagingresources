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

SNAP = pd.read_csv('historical-snap-retailer-locator-data-2023.12.31 (1).zip')

#dropping all retailers not located in Yates County 
SNAP = SNAP[SNAP['County'] == 'YATES']

#dropping all convenience stores 
SNAP = SNAP[SNAP['Store Type']!='Convenience Store']
SNAP = SNAP[SNAP['Store Type']!='Combination Grocery/Other']
