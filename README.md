# Disparities in NY State Older Adult Food Insecurity 
## Summary

This project examines the distribution of access to state-wide food assistance resources for low-income older adults living in NY state offered by NY State Office for the Aging (NYSOFA). Data on New York State's Area Agencies on Aging  (local administrative offices) as well as multi-purpose senior centers where services including, but not limited to, congregate meals are provided to older adults. 
Census-level population and spatial data is also analyzed, focusing on variables that indicate economic and food insecurity amongst older adults, as well as SNAP/food stamp utilization.

## Input files 
The first input file required is a csv from data.ny.gov, NY State's Open Data site. The csv file can be downloaded here: https://data.ny.gov/Human-Services/Congregate-Meals-Served-by-County-by-the-Office-fo/ytzm-8tkg/about_data
This file, marked as [NYSOFA_meals.csv](NYSOFA_Meals.csv) contains county-level data of congregate and home-delivered meals served to older adults in NY State since 1974. Congregate meals, served in community settings such as in multi-purpose senior centers, and home-delivered meals are targeted towards supporting low-income older adults. 

The following scripts also require API requests from the United States Census Bureau. For the Census API query, a unique Census key will be necessary. In [census.py](census.py), replace variable 'key_value' with a unique census key retrieved here: https://api.census.gov/data/key_signup.html

Spatial data is retrieved from the Census website. Tiger-line shape files for New York State counties and roads can be downloaded here: https://www.census.gov/cgi-bin/geo/shapefiles/index.php
The shapefiles used in script [analysis.py](analysis.py) and [yates.py](yates.py) are: 
1. [tl_2023_us_county.zip](tl_2023_us_county.zip) - Counties and equivalent of NY State 
2. [tl_2023_36123_roads.zip](tl_2023_36123_roads.zip) (All roads in Yates County, NY)

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

4. [yates.py](yates.py) This script looks more closely at the food assistance resources available to older adult residents of Yates County, NY. A geopackage is exported for analysis in QGIS. 

2 QGIS projects are included with this repository using the outputs from the scripts above. Please load [NYSOFA.qgz](NYSOFA.qgz) and [yates.qgz](yates.qgz) to examine the origin of related .png files within the repository. 

## Results
Key Findings:

5 Counties serving the least number of congregate and home delivered meals (2021): 
Schuyler     35914
Tioga        31511
Sullivan     31463
[Yates](yates.py) 15617
St. Regis    10162

NY Counties with zero (0) multi-purpose community centers for older adult services:
Allegany
Delaware
Essex
Herkimer
Lewis
Livingston
Madison
Otsego
St. Lawrence
St. Regis
Wayne
[Yates](yates.py)


A closer look at Yates County, New York shows that the county has no multi-purpose senior centers where older adults can go to both receive meals and interact with others. In addition, [yates.qgz](yates.qgz) highlights the available grocery retailers in the county where SNAP benefits can be used. As the older adult population across the U.S. continues to age, similar analysis should be conducted across states to highlight counties where older adults could be better supported by congregate meal opportunities as well as proximity to SNAP retail grocery stores. 


