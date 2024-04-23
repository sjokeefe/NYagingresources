# Disparities in NY State Older Adult Food Insecurity 
## Summary

This project examines the distribution of access to state-wide food assistance resources for low-income older adults living in NY state offered by NY State Office for the Aging (NYSOFA). 
Census-level population and spatial data is also analyzed, focusing on variables that most likely indicate economic and food insecurity amongst older adults.

## Input files 
The first input file is a csv from data.ny.gov, NY State's Open Data site. The csv file can be downloaded here: https://data.ny.gov/Human-Services/Congregate-Meals-Served-by-County-by-the-Office-fo/ytzm-8tkg/about_data

The following scripts also require API requests from data.ny.gov as well as the Census Bureau. For the Census API query, a unique Census key will be necessary. In [census.py](census.py), replace variable 'key_value' with a unique census key retrieved here: https://api.census.gov/data/key_signup.html

Spatial data is retrieved from the Census website. Tiger-line shape files for New York State counties can be downloaded here: 

## Scripts

1. [NYSOFA.py](NYSOFA.py)
Examines state-level spatial and administrative data regarding Area Agency on Aging Service Providers (local offices that support and administer aging services, including nutrition and meal services). 
The script exports a geopackage to be used later on in the analysis in QGIS. 

2. [census.py](census.py)
Looks at population data from the American Community Survey (ACS) and ACS Subject Tables related to poverty and food stamp/SNAP utilization by adults age 60 and older. 

3. [analysis.py](analysis.py)


## Results

