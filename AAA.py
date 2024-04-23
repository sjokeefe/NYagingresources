# -*- coding: utf-8 -*-
"""
NYS AAA spatial data 

"""

import requests
import pandas as pd 
import geopandas as gpd

#Open data NY api request for the directory multi-purpose senior centers  
url = "https://data.ny.gov/resource/t4ba-giyx.json"
response = requests.get(url)
# Check if request was successful (status code 200)
if response.status_code == 200:
        # Extracting JSON data
    data = response.json()

# Converting JSON data to DataFrame
cr = pd.DataFrame(data)

# Extracting latitude and longitude from 'georeference' column
cr = cr[cr['georeference'].apply(lambda x: isinstance(x, dict))]
cr['latitude'] = cr['georeference'].apply(lambda x: x['coordinates'][1])
cr['longitude'] = cr['georeference'].apply(lambda x: x['coordinates'][0])

# Converting relevant columns to appropriate data types
cr['latitude'] = cr['latitude'].astype(float)
cr['longitude'] = cr['longitude'].astype(float)

# Creating a GeoDataFrame from DataFrame
crgeo = gpd.GeoDataFrame(cr, crs='EPSG:4326', geometry=gpd.points_from_xy(cr.longitude, cr.latitude))
# Reprojecting the GeoDataFrame to UTM Zone 18N (EPSG:26918)
crgeo = crgeo.to_crs('EPSG:26918')

output_filename = "communityresources.gpkg"
crgeo.to_file(output_filename, driver="GPKG")

##### 
#Open data NY api request for the directory of AAA sites 
url2 = "https://data.ny.gov/resource/t8nk-j66w.json"
response2 = requests.get(url2)
# Check if request was successful (status code 200)
if response2.status_code == 200:
        # Extracting JSON data
    AAAdata = response2.json()

# Converting JSON data to DataFrame
AAA = pd.DataFrame(AAAdata)

# Extracting latitude and longitude from 'georeference' column
AAA = AAA[AAA['georeference'].apply(lambda x: isinstance(x, dict))]
AAA['latitude'] = AAA['georeference'].apply(lambda x: x['coordinates'][1])
AAA['longitude'] = AAA['georeference'].apply(lambda x: x['coordinates'][0])

# Converting relevant columns to appropriate data types
AAA['latitude'] = AAA['latitude'].astype(float)
AAA['longitude'] = AAA['longitude'].astype(float)

# Creating a GeoDataFrame from DataFrame
AAAgeo = gpd.GeoDataFrame(AAA, crs='EPSG:4326', geometry=gpd.points_from_xy(AAA.longitude, AAA.latitude))
# Reprojecting the GeoDataFrame to UTM Zone 18N (EPSG:26918)
AAAgeo = AAAgeo.to_crs('EPSG:26918')

output_filename2 = "AAAsites.gpkg"
AAAgeo.to_file(output_filename, driver="GPKG")


#reading in NYSOFA Meal data 
meals = pd.read_csv('NYSOFA_Meals.csv')
meals = meals.rename(columns = {'NYSOFA County Code': 'County Code', 'Meal Units Served': 'Total Meals Served'})
#deleting data from before 2018 for relevance 
meals = meals[meals['Year']>=2018]
meals['Home Delivered Meals Served'] = meals['Total Meals Served'].where(meals['Meal Type'] == 'Home Delivered Meals')
meals['Congregate Meals Served'] = meals['Total Meals Served'].where(meals['Meal Type'] == 'Congregate Meals')

#creating one row for each county for each year 
meals_aggregate = meals.groupby(['County Name', 'Year'], as_index=False).agg({
    'Total Meals Served': 'first',
    'Meal Type': '|'.join,
    'Home Delivered Meals Served': 'sum',
    'Congregate Meals Served': 'sum'
})
meals_aggregate.drop(["Total Meals Served", "Meal Type"], axis=1, inplace=True)


