# -*- coding: utf-8 -*-
"""
More in-depth analysis of food assistance resources and vulerable older adults in Madison County, NY 

"""

import geopandas as gpd
import pandas as pd

#reading the tigerline roads shape files 
yates_roads = gpd.read_file('tl_2023_36123_roads.zip')
yates = gpd.read_file('tl_2023_us_county.zip')
yates = yates[(yates['STATEFP']=='36')& (yates['COUNTYFP']=='123')]

#reading the historical SNAP data 
SNAP = pd.read_csv('historical-snap-retailer-locator-data-2023.12.31 (1).zip')

#dropping all retailers not located in Yates County 
SNAP = SNAP[SNAP['County'] == 'YATES']

#dropping all convenience stores 
SNAP = SNAP[SNAP['Store Type']!='Convenience Store']
SNAP = SNAP[SNAP['Store Type']!='Combination Grocery/Other']

#dropping all the stores with expired SNAP authorizations
SNAP = SNAP[SNAP['End Date'].astype(str).str.strip() == '']

#creating a geodataframe using the SNAP retailer data and the tigerline shape file 
gdf_points = gpd.GeoDataFrame(SNAP, geometry=gpd.points_from_xy(SNAP['Longitude'], SNAP['Latitude']), crs=yates_roads.crs)

#exporting to geopackages 
output = 'yates_stores_and_roads.gpkg'
gdf_points.to_file(output, layer='grocery', driver='GPKG')
yates_roads.to_file(output, layer='roads', driver='GPKG', append=True)
yates.to_file(output, layer='county',driver='GPKG', append=True)
