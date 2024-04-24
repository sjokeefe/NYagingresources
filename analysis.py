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

# Read the shapefile
shapefile_path = "tl_2023_us_county.zip"
gdf = gpd.read_file(shapefile_path)
# Filter to include only counties in New York State
ny_counties = gdf[gdf['STATEFP'] == '36']  # '36' is the FIPS code for New York State

#renaming the county column in census
census['NAME'] = census['NAME'].str.replace(' County, New York', '')
# Set the County column as the index
census.set_index('NAME', inplace=True)


# Creating a figure to show the data in four ways:
fig, axes = plt.subplots(2, 2, figsize=(12,10))

# A Bar plot of Household with Food Stamp Households with older adult member by County
census['Household with Food Stamp, 60+ member'].plot(kind='bar', ax=axes[0, 0])
axes[0, 0].set_title('Total Households Using SNAP/Food Stamps by County, with member age 60+')
axes[0, 0].set_ylabel('Households')
axes[0,0].set_xlabel('County')

#Scatter plot of % below poverty line 65+ vs Total Population 65+
sns.scatterplot(data=census, x='% below pl 65+', y='Total Population 60+', ax=axes[0, 1])
axes[0, 1].set_title('% Below poverty line 65+ vs Total Population 60+')

#Scatterplot of total population 60+ versus total households on SNAP with 60+ member
sns.scatterplot(data=census, x='Total Population 60+', y='Household with Food Stamp, 60+ member', ax=axes[1,0])
axes[1,0].set_title("Total Population 60+ versus Total Households on SNAP with Household Member age 60+")

# Horizontal bar plot of Total Population 65+
census['Total Population 60+'].plot(kind='barh', ax=axes[1, 1])
axes[1, 1].set_title('Total Population 60+')
axes[1, 1].set_xlabel('Population')

# Adjusting the layout
plt.tight_layout()
#saving the figure
fig.savefig('censusplots.png')

#seeing the proportion of total households on SNAP that have a member age 60+ 
census['percent']= census['Household with Food Stamp, 60+ member']/census['Total Households on SNAP']*100
#printing the ten counties with the highest proportion of older adult SNAP participants in the past 12 months 
census = census.sort_values(by='percent', ascending=False)
print("Counties with the highest percentages of total SNAP participating households containing a member age 60+: ")
print(census.head(10))

census = census.sort_values(by='% below pl 65+', ascending=False)
print("Counties with the highest percent of total population age 65+ living below the poverty level:")
print(census.head(10))

