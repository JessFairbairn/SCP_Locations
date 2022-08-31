import json
import sqlite3

import pandas as pd

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
# from geograpy import places
import folium
from folium.plugins import MarkerCluster

from database import create_location_cache_table, insert_location, retrieve_location
from geography import get_coordinates, retrieve_location

geolocator = Nominatim(user_agent="example app")

# with open('site_locations_dict.json', 'r') as list_file:
#         site_list = json.loads(list_file.read())
with open("site_locations_partial.json") as output_file:
    site_list = json.load(output_file)

map = folium.Map(zoom_start=3, )
marker_cluster = MarkerCluster().add_to(map)

with sqlite3.connect("data.db") as conn:
    create_location_cache_table(conn)

    for row in site_list:
        location = get_coordinates(conn, row["location name"])
        if location is None:
            continue
        row["lat"] = location[0]
        row["long"] = location[1]
        site_long_name = row["site long name"]
        source_sentence = row["sentence"]

        popup = folium.Popup(
            f"""{site_long_name}<br/><i>{source_sentence}</i>
            <br>from <a href="https://www.scp-wiki.net/{row["page name"]}">{row["page name"]}</a> """,
            max_width=500
        )
        folium.Marker(location=location,
                        popup = popup,
                        tooltip=row["location name"])\
            .add_to(marker_cluster)

# df.to_json("site_locations.json", default_handler=str, orient="records")
with open("site_locations.json", "w") as output_file:
    json.dump(site_list, output_file)
map.save("map.html")
