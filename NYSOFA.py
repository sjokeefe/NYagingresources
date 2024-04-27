# -*- coding: utf-8 -*-
"""
NYS County-Level Data 

"""
import requests
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.dpi'] = 300


#reading in data on meals served by county
meals = pd.read_csv('NYSOFA_Meals.csv')
# Converting JSON data to DataFrame
meals = pd.DataFrame(meals)

meals = meals.rename(columns = {'NYSOFA County Code': 'County Code', 'Meal Units Served': 'Total Meals Served'})

#looking at meals served over time in Madison county 
quicklook = meals[meals['County Name']=='Madison']
fig, ax1 = plt.subplots()
sns.barplot(data=quicklook,x='Year',y='Total Meals Served',
            hue='Meal Type',palette='deep',ax=ax1)
plt.xticks(rotation=45, ha='right', fontsize=6)
plt.tight_layout()
plt.show()
ax1.set_title("NYSOFA Meals Served (Madison County, Since 1974)")
ax1.set_xlabel("Year")
ax1.set_ylabel("Meals Served")
fig.tight_layout()
fig.savefig('madisonmeals.png')

#looking at meals served over time in onondaga county 
quicklook = meals[meals['County Name']=='Onondaga']
fig, ax1 = plt.subplots()
sns.barplot(data=quicklook,x='Year',y='Total Meals Served',
            hue='Meal Type',palette='deep',ax=ax1)
plt.xticks(rotation=45, ha='right', fontsize=6)
plt.tight_layout()
plt.show()
ax1.set_title("NYSOFA Meals Served (Onondaga County, Since 1974)")
ax1.set_xlabel("Year")
ax1.set_ylabel("Meals Served")
fig.tight_layout()
fig.savefig('onondagameals.png')


#parcing out certain years 
meals = meals[meals['Year']==2021]
meals['Home Delivered Meals Served'] = meals['Total Meals Served'].where(meals['Meal Type'] == 'Home Delivered Meals')
meals['Congregate Meals Served'] = meals['Total Meals Served'].where(meals['Meal Type'] == 'Congregate Meals')

#creating one row for each county for each year 
meals_aggregate = meals.groupby(['County Name', 'Year'], as_index=False).agg({
    'Total Meals Served': 'first',
    'Meal Type': '|'.join,
    'Home Delivered Meals Served': 'sum',
    'Congregate Meals Served': 'sum'
})
#dropping unneeded columns and setting the index 
meals_aggregate.drop(["Total Meals Served", "Meal Type", "Year"], axis=1, inplace=True)
meals_aggregate.set_index("County Name", inplace=True)

#adding a totals column 
meals_aggregate['Total Meals Served'] = meals_aggregate['Home Delivered Meals Served'] + meals_aggregate['Congregate Meals Served']
#sorting by total meals served 
meals_sorted = meals_aggregate.sort_values(by='Total Meals Served', ascending=False)

#printing informative messages about congregate meals and home delivered meals served by county
top_5 = meals_sorted.head(5)
print("\nTop 5 Counties Ranks by Total Number of Congregate and Home Delivered Meals Meals Served (2021):")
print(top_5['Total Meals Served'])
bottom_5 = meals_sorted.tail(5)
print("\n5 Counties serving the least number of congregate and home delivered meals (2021):", bottom_5['Total Meals Served'])




#Open data NY api request for the directory multi-purpose senior centers, which provide services including but not limited to congregate meals   
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

#setting the index
cr.set_index("county_name", inplace=True)

# Creating a GeoDataFrame from DataFrame
crgeo = gpd.GeoDataFrame(cr, crs='EPSG:4326', geometry=gpd.points_from_xy(cr.longitude, cr.latitude))

# Reprojecting the GeoDataFrame to UTM Zone 18N (EPSG:26918)
crgeo = crgeo.to_crs('EPSG:26918')

output_filename = "communityresources.gpkg"
crgeo.to_file(output_filename, driver="GPKG")

#counting the number of locations in each county
cr_by_county = crgeo.groupby('county_name').size()
#renaming the column produced 
cr_by_county = cr_by_county.rename("Number of Community Sites")


#using geopandas to read the US county shapefile
geodata = gpd.read_file('tl_2023_us_county.zip')
#filtering geodata down to NY counties 
geodata = geodata.query('STATEFP == "36"')


#merging onto the Census data
#setting the index for merging 
geodata.rename(columns={'NAME':'county_name'}, inplace=True)
geodata.set_index('county_name',inplace=True)
geodata = geodata.merge(cr_by_county, on='county_name',how='left', indicator=True)
#value counts for "_merge" 
print(geodata['_merge'].value_counts() )
geodata.drop(columns='_merge',inplace=True)

#filling in nan values with zero for QGIS purposes
geodata['Number of Community Sites'].fillna(0, inplace=True)

#writing the dataframe to a .gpkg file with layer set to 'earnings'
geodata.to_file("cr.gpkg",layer="resources")




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

#setting the index
AAA.set_index("county_name", inplace=True)
# Creating a GeoDataFrame from DataFrame
AAAgeo = gpd.GeoDataFrame(AAA, crs='EPSG:4326', geometry=gpd.points_from_xy(AAA.longitude, AAA.latitude))

# Reprojecting the GeoDataFrame to UTM Zone 18N (EPSG:26918)
AAAgeo = AAAgeo.to_crs('EPSG:26918')

#merging the number of multipurpose senior centers onto the AAA site data 
AAA_by_county = pd.merge(AAAgeo, cr_by_county, how='left', left_index=True, right_index=True)

#filling in Nan values as zero 
AAA_by_county["Number of Community Sites"] = AAA_by_county['Number of Community Sites'].fillna(0)
#printing the number of counties with no multi-purpose senior centers 
no_sites = AAA_by_county[AAA_by_county['Number of Community Sites']== 0].index
print("\nNY Counties with zero (0) multi-purpose community centers for older adult services:")
for county_name in no_sites:
    print(county_name)

#2 multi-purpose senior centers 
two = AAA_by_county[AAA_by_county['Number of Community Sites']==2].index
print("\nNY Counties with 2 multi-purpose community centers for older adult services:")
for county_name in two:
    print(county_name)    

#1 multi-purpose senior center 
one = AAA_by_county[AAA_by_county['Number of Community Sites']==1].index
print("\nNY Counties with 1 multi-purpose community center for older adult services:")
for county_name in one:
    print(county_name)
    
#merging the meals data onto the AAA data 
AAA_by_county = pd.merge(AAA_by_county, meals_aggregate, how='left', left_index=True, right_index=True)
#dropping unneeded columns
AAA_by_county = AAA_by_county.drop(columns=['nysofa_county_code', 'service_provider'])
#resetting the index
AAA_by_county.reset_index(drop=False, inplace=True)
#renaming the county column 
AAA_by_county.rename(columns={'county_name': 'NAME'}, inplace=True)

#trimming the dataframe/dropping columns not needed for further analysis 
trimmed = ['resource_type','street_address', 'city','state','zip','phone' ]
for column in trimmed:
    del AAA_by_county[column]

#coverting to a geoPackage 
output_filename2 = "AAAmeals.gpkg"
AAA_by_county.to_file(output_filename2, driver="GPKG")









