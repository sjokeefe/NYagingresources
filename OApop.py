# -*- coding: utf-8 -*-
"""
Siobhan O'Keefe
Spring 2024 

"""
#import modules 
import requests 
import pandas as pd


#API request for: "B22001_003E" "Estimate!!Total!!Household received Food Stamps/SNAP in the past 12 months!!At least one person in household 60 years or over","RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY PRESENCE OF PEOPLE 60 YEARS AND OVER FOR HOUSEHOLDS"
api = 'https://api.census.gov/data/2020/acs/acs5'
#indicating the type of geographic unit that should be returned 
for_clause = 'county:*'
#limiting selected geographic units to those that fall within larger geographic entity
#returning only counties in state 36  
in_clause = 'state:36'

#my census API key 
key_value = '4afc0d8a6d77ff2795a42ccb16deca415081c730'

#creating a new dictionary 
payload = {'get':'NAME, B22001_003E', 'for':for_clause, 'in':in_clause, 'key':key_value}

#building an https query string, sent to API endpoint and collecting the response 
response = requests.get(api, payload)
#checking to see if the https status code is successful, printing a message with what went wrong if not. 
if response.status_code != 200:
    print("Error:", response.status_code)
    print(response.text)
    #script will stop immediately if statement is reached
    assert False 

#parsing the JSON returned by the Census server and retunring a list of rows
row_list = response.json()

#setting column names to the first row of row_list
colnames = row_list[0]
#setting datarows to the remaining columns of row_list
datarows = row_list[1:]

#converting the data into a pandas dataframe 
SNAP = pd.DataFrame(columns=colnames, data=datarows)
#setting the index of attain to the "NAME" column
SNAP.set_index("NAME", inplace=True)


