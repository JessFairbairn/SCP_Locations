import json
import sqlite3

from database import create_location_cache_table
from geography import get_coordinates

# with open('site_locations_dict.json', 'r') as list_file:
#         site_list = json.loads(list_file.read())
with open("site_locations_partial.json") as output_file:
    site_list = json.load(output_file)

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

# df.to_json("site_locations.json", default_handler=str, orient="records")
with open("site_locations.json", "w") as output_file:
    json.dump(site_list, output_file)
# map.save("map.html")
