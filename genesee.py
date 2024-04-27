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

#genessee vs schoharie 

import matplotlib.pyplot as plt

# Extracting population data for Schoharie County and Genesee County
schoharie_population = census.loc[census['NAME'] == 'Schoharie County, New York', 'Total Population 60+'].values[0]
genesee_population = census.loc[census['NAME'] == 'Genesee County, New York', 'Total Population 60+'].values[0]

# Creating bar chart
counties = ['Schoharie', 'Genesee']
population = [schoharie_population, genesee_population]

plt.bar(counties, population, color=['blue', 'green'])
plt.xlabel('County')
plt.ylabel('Total Population 60+')
plt.title('Total Population 60+ in Schoharie County vs. Genesee County')

plt.tight_layout()
plt.savefig('comparison.png')
plt.show()


