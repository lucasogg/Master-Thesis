#---------------IPflowMap---------------------#
#/!\ PRE-REQUISITE :
# - registered & logged in by https://opencagedata.com/
# - a valid API key issued by https://opencagedata.com/, which is required to
#   retrieve latitude & longitude values based on "city" & "country" datas
#I. This script takes a processed ip_lookedup csv file as input
#II. It looks up the coordinate (latitude,longitude) for city/country,
#    thanks to opencage.geocoder API
#III. It finally plots IP adresses owners location & communication flows
#     (as lines) on a map
#-----------Lucas O., 2020-------------#
#OS, IDE, Python : Windows 10, Atom, 3.7.0

# -*- coding: utf-8 -*-

import sys,os
import csv,json,time
import pandas as pd
import numpy as np
import folium
from opencage.geocoder import OpenCageGeocode
from datetime import datetime

key = <API_KEY_FROM_OPENCAGEGEOCODE>
geocoder = OpenCageGeocode(key)
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
world_geo = f'{url}/world-countries.json'
source_coordinates = <COORDINATES_OF_IOT_DEVICE_LOCATION>

start_time = time.time()

print("[+] Start !")

print("[+] Import data")

file_path = <IPLOOKEDUP_CSV_FILES_PATH>
df = pd.read_csv(file_path, delimiter=';', encoding="utf-8")
cities = df[['City','Country','Description','CountryCode','Val']].drop_duplicates(subset = ['City','Country','Description'])
data = pd.DataFrame(data=cities, index=None, columns=['City','Country','Description','Val'])
list_lat = []
list_long = []
list_description = []
list_cities = []
providers_per_city = {}

print("[+] Generating dataframe... :")

for index,row in data.iterrows():
    city = row["City"]
    country = row["Country"]
    description = row["Description"]
    if city not in providers_per_city:
        providers_per_city[city] = description
    else:
        providers_per_city[city] += description
    city_country = (city,country)
    query = str(city)+','+str(country)
    results = geocoder.geocode(query)
    lat = results[0]['geometry']['lat']
    long = results[0]['geometry']['lng']
    list_lat.append(lat)
    list_long.append(long)
    list_description.append(description)
    list_cities.append(city)

data['Latitude'] = list_lat
data['Longitude'] = list_long

print("[+] Dataframe generated. Generating map...",flush = True)
source_adress = [46.5216603, 6.5733627]

m = folium.Map(location=[46.5216603, 6.5733627],
               zoom_start=2) #coordinates from the

print("[+] Map generated. Plotting markers and lines...",flush=True)
points = []
for i in range(len(list_lat)):
    points.append([list_lat[i], list_long[i]])
    points.append(source_adress)

print("[+] Markers list ready.",flush=True)
for index,lat in enumerate(list_lat):
    city = list_cities[index]
    long = list_long[index]
    providers = providers_per_city[city]
    marker_text = str(list_cities[index])+':\n'+str(providers)
    folium.Marker([lat,
                   long],
                  popup=(marker_text.format(index)),
                 icon=folium.Icon(color='blue',icon='server',prefix='fa')).add_to(m)

folium.PolyLine(points, color='blue', weight=1.6, opacity=0.5).add_to(m)

m.save('map.html')

end_time = time.time()
print("[+] Time required : --- %s seconds ---" % (end_time - start_time))
