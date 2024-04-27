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
axes[0,0].set_xlabel('County', fontsize=7)

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

by_percent = census['percent'].sort_values( ascending=False)
print("Counties with the Highest Percentage of SNAP Households with a member age 60+")
print(by_percent.head(10))

by_below = census['% below pl 65+'].sort_values(ascending=False)
print("\nCounties with the Highest Percent of Older Adults (age 65+) living below the poverty line")
print(by_below.head(10))

#highlighting genesee county in a visual representation of percent of all households on SNAP with an older adult 
by_percent = by_percent.reset_index()
plt.figure(figsize=(10, 6))
bars = plt.bar(by_percent['NAME'], by_percent['percent'], color='skyblue')

highlighted_county = 'Genesee'
highlighted_index = by_percent[by_percent['NAME'] == highlighted_county].index[0]
bars[highlighted_index].set_color('orange')

# Adding labels and title
plt.xlabel('County')
plt.ylabel('Percent')
plt.title('Percent of Total SNAP Households with at Least One Member Age 60+')
# Rotate x-axis labels for better readability
plt.xticks(rotation=90)
plt.savefig('olderadultsonSNAP.png', bbox_inches='tight')
# Show plot
plt.show()


#comparing community sites to the population of older adults 
NYSOFA = NYSOFA.set_index('NAME')
both_data = pd.merge(census, NYSOFA, left_index=True, right_index=True)
ratio = both_data['Number of Community Sites']/both_data['Household with Food Stamp, 60+ member']
print("Ratio of Community Sites per county to number of households participating in SNAP with older adult member:")
print(ratio.sort_values())
ratio_total = both_data['Number of Community Sites']/ both_data['Total Population 60+']
print("Ratio of Number of Community sites per county to total population of older adults in each county:")
print(ratio_total.sort_values())

#population distribution 
census= census.reset_index()
plt.figure(figsize=(10,6))
plt.bar(census['NAME'], census['Total Population 60+'], color='skyblue')
plt.xlabel('County')
plt.ylabel('Population')
plt.title('Total Population Distribution by County, Age 60+')
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()
plt.savefig('population.png')


