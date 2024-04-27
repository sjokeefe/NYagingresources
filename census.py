# -*- coding: utf-8 -*-
"""
Advanced Policy Analysis Final Project 
Census Data Analysis 

"""

import pandas as pd
import matplotlib.pyplot as plt
import requests
import pandas as pd

# API endpoint for 5-year estimates 2017-2021
api = 'https://api.census.gov/data/2021/acs/acs5'

# Indicating the type of geographic unit that should be returned
for_clause = 'county:*'

# Limiting selected geographic units to those that fall within larger geographic entity
# Returning only counties in state 36 (New York)
in_clause = 'state:36'

# Your Census API key
key_value = '4afc0d8a6d77ff2795a42ccb16deca415081c730'

# Creating a new dictionary for parameters
#Estimate!!Total:!!Household received Food Stamps/SNAP in the past 12 months:!!At least one person in household 60 years or over	
#Estimate!!Total!!Household received Food Stamps/SNAP in the past 12 months
payload = {'get': 'NAME,B22001_003E,B22001_002E', 'for': for_clause, 'in': in_clause, 'key': key_value}

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
foodstamp = pd.DataFrame(columns=colnames, data=datarows)
foodstamp = foodstamp.rename(columns={'B22001_003E': 'Household with Food Stamp, 60+ member', 'B22001_002E': 'Total Households on SNAP'})
foodstamp['Household with Food Stamp, 60+ member'] = foodstamp['Household with Food Stamp, 60+ member'].astype(float)
foodstamp = foodstamp.sort_values(by='Household with Food Stamp, 60+ member', ascending=False)

##########################################################################################
# API endpoint
apisubject = 'https://api.census.gov/data/2021/acs/acs5/subject'

# Creating a new dictionary for parameters
#All families!!Percent below poverty level!!Estimate!!Householder 65 years and 
#Total population age 60+ 
payload = {'get': 'NAME,S1702_C02_017E,S0101_C01_028E', 'for': for_clause, 'in': in_clause, 'key': key_value}

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
subject = subject.rename(columns={'S1702_C02_017E': '% below pl 65+', 'S0101_C01_028E': 'Total Population 60+'})
subject['% below pl 65+'] = subject['% below pl 65+'].astype(float)
subject['Total Population 60+'] = subject['Total Population 60+'].astype(float)
###################################################################


#merging the variables into one dataframe 
census = pd.merge(foodstamp, subject['% below pl 65+'], left_index=True, right_index=True)
census = pd.merge(census, subject['Total Population 60+'], left_index=True, right_index=True)
#dropping the state and county columns 
census = census.drop(columns=['state', 'county'])


#setting the index to the county name 
census.set_index('NAME', inplace=True)

#printing the head of the dataframe to see what it contains at the end of the data clean
print(census.head())

#exporting the result to a csv file for use in future script
census.to_csv('census.csv')
print("Dataframe exported to 'census.csv'")

