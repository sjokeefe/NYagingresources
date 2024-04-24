# Disparities in NY State Older Adult Food Insecurity 
## Summary

This project examines the distribution of access to state-wide food assistance resources for low-income older adults living in NY state offered by NY State Office for the Aging (NYSOFA). Data on New York State's Area Agencies on Aging  (local administrative offices) as well as multi-purpose senior centers where services including, but not limited to, congregate meals are provided to older adults. 
Census-level population and spatial data is also analyzed, focusing on variables that indicate economic and food insecurity amongst older adults, as well as SNAP/food stamp utilization.

## Input files 
The first input file is a csv from data.ny.gov, NY State's Open Data site. The csv file can be downloaded here: https://data.ny.gov/Human-Services/Congregate-Meals-Served-by-County-by-the-Office-fo/ytzm-8tkg/about_data
This file, marked as [NYSOFA_meals.csv holds](NYSOFA_Meals.csv) county-level data of congregate and home-delivered meals served to older adults in NY State since 1974. Congregate meals, served in community settings such as in multi-purpose senior centers, and home-delivered meals are targeted towards supporting low-income older adults. 

The following scripts also require API requests from data.ny.gov as well as the Census Bureau. For the Census API query, a unique Census key will be necessary. In [census.py](census.py), replace variable 'key_value' with a unique census key retrieved here: https://api.census.gov/data/key_signup.html
(No API key is needed for data.ny.gov)

Spatial data is retrieved from the Census website. Tiger-line shape files for New York State counties can be downloaded here: https://www.census.gov/cgi-bin/geo/shapefiles/index.php

## Scripts 
To view contents of the repository, run the following scripts in this order: 
1. [NYSOFA.py](NYSOFA.py)
Examines state-level spatial and administrative data regarding Area Agency on Aging Service Providers (local offices that support and administer aging services, including nutrition and meal services). 
The script exports geopackages to be used later on in the analysis in QGIS. 

2. [census.py](census.py)
Looks at population data from the American Community Survey (ACS) and ACS Subject Tables related to poverty and food stamp/SNAP utilization by adults age 60 and older. 
Creates visualizations using matplotlib and seaborn.  

3. [analysis.py](analysis.py)
Further analysis using outputs from both [NYSOFA.py](NYSOFA.py) and [census.py](census.py). 

## Results
Based on the analysis conducted in the scripts above, I noticed that Madison County, New York has Zero Multi-Purpose Senior Centers (places where older adults could obtain congregate meals or where home-delivered meals might be distributed from), but also had the 4th highest percentage of all SNAP participating households with an older adult member (age 65+), roughly 57.95%. 


