# -*- coding: utf-8 -*-
"""
Advanced Policy Analysis Final Project 
Census Data Analysis 

"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns


plt.rcParams['figure.dpi'] = 300

import requests
import pandas as pd

# API endpoint
api = 'https://api.census.gov/data/2022/acs/acs1'

# Indicating the type of geographic unit that should be returned
for_clause = 'county:*'

# Limiting selected geographic units to those that fall within larger geographic entity
# Returning only counties in state 36 (New York)
in_clause = 'state:36'

# Your Census API key
key_value = '4afc0d8a6d77ff2795a42ccb16deca415081c730'

# Creating a new dictionary for parameters
#Estimate!!Total:!!Household received Food Stamps/SNAP in the past 12 months:!!At least one person in household 60 years or over	
payload = {'get': 'NAME,B22001_003E', 'for': for_clause, 'in': in_clause, 'key': key_value}

# Making the API request
response = requests.get(api, params=payload)

# Checking if the request was successful
if response.status_code != 200:
    print("Error:", response.status_code)
    print(response.text)
    # Script will stop immediately if statement is reached
    assert False

# Parsing the JSON returned by the Census server and returning a list of rows
row_list = response.json()

# Setting column names to the first row of row_list
colnames = row_list[0]

# Setting data rows to the remaining columns of row_list
datarows = row_list[1:]

# Converting the data into a pandas DataFrame
earnings = pd.DataFrame(columns=colnames, data=datarows)

# Displaying the DataFrame
print(earnings.head())

# API endpoint
apisubject = 'https://api.census.gov/data/2022/acs/acs1/subject'

# Creating a new dictionary for parameters
#Estimate!!Total:!!Household received Food Stamps/SNAP in the past 12 months:!!At least one person in household 60 years or over	
payload = {'get': 'NAME,S1702_C02_017E', 'for': for_clause, 'in': in_clause, 'key': key_value}

# Making the API request
response = requests.get(apisubject, params=payload)

# Checking if the request was successful
if response.status_code != 200:
    print("Error:", response.status_code)
    print(response.text)
    # Script will stop immediately if statement is reached
    assert False

# Parsing the JSON returned by the Census server and returning a list of rows
row_list = response.json()

# Setting column names to the first row of row_list
colnames = row_list[0]

# Setting data rows to the remaining columns of row_list
datarows = row_list[1:]

# Converting the data into a pandas DataFrame
subject = pd.DataFrame(columns=colnames, data=datarows)
