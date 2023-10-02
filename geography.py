import sqlite3
from operator import itemgetter
from typing import List, Optional, Tuple

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

from database import insert_location, retrieve_location

geolocator = Nominatim(user_agent="example app")


BLACKLISTED_CLASSES = ["office", "shop", "amenity"]

def _data_lookup(conn: sqlite3.Connection, location_name: str) -> Optional[Tuple[float, float]]:
    if location_name.startswith("the "):
        location_name = location_name[4:]

    geo_data = retrieve_location(conn, location_name)


    if geo_data is None:

        try:
            response = geolocator.geocode(location_name)
            if response is None:
                print(f"Couldn't locate {location_name}")
                return None
        except GeopyError as ex:
            print(ex)
            return None

        geo_data = response.raw
        # geo_data = places.PlaceContext([location_list[0]])
        # geo_data = locator.Locator().locateLocation(location_list[0])


        insert_location(conn, location_name, geo_data)
    return geo_data

def get_coordinates(conn: sqlite3.Connection, location_name: str) -> Tuple[float, float]:
    geo_data = _data_lookup(conn, location_name)

    if geo_data is None or geo_data["class"] in BLACKLISTED_CLASSES:
        return None
    return (geo_data["lat"], geo_data["lon"])

def get_importance(conn: sqlite3.Connection, location_name: str) -> float:
    geo_data = _data_lookup(conn, location_name)
    
    if geo_data is None:
        return 0

    if geo_data["class"] in BLACKLISTED_CLASSES:
        return 0
    return geo_data["importance"]

def pick_location(locations: List[str]):
    location_importance = {}
    with sqlite3.connect("data.db") as conn:
        for location_str in locations:
            location_importance[location_str] = get_importance(conn, location_str)
    return max(location_importance.items(), key=itemgetter(1))[0]