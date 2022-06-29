import json
import sqlite3

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
# from geograpy import places
import folium
from folium.plugins import MarkerCluster

from database import create_location_cache_table, insert_location, retrieve_location
from geography import get_coordinates, retrieve_location

geolocator = Nominatim(user_agent="example app")

with open('site_locations_dict.json', 'r') as list_file:
        site_list = json.loads(list_file.read())

map = folium.Map(zoom_start=2)
marker_cluster = MarkerCluster().add_to(map)

with sqlite3.connect("data.db") as conn:
    create_location_cache_table(conn)

    for site_name, location_list in site_list.items():
        location = get_coordinates(conn, location_list[0])
        if location is None:
            continue
        folium.Marker(location=location,
                        popup = f"Site-{site_name}",
                        tooltip=location_list[0])\
            .add_to(marker_cluster)

map.save("map.html")
