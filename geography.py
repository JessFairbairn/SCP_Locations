import sqlite3
from typing import Tuple

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

from database import insert_location, retrieve_location

geolocator = Nominatim(user_agent="example app")


BLACKLISTED_CLASSES = ["office", "shop", "amenity"]
def get_coordinates(conn:sqlite3.Connection, location_name: str) -> Tuple[float, float]:
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


    if geo_data["class"] in BLACKLISTED_CLASSES:
        return None
    return (geo_data["lat"], geo_data["lon"])
