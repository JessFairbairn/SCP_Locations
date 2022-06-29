import sqlite3
from typing import Tuple

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

from database import insert_location, retrieve_location

geolocator = Nominatim(user_agent="example app")

def get_coordinates(conn:sqlite3.Connection, location_name: str) -> Tuple[float, float]:
        geo_data = retrieve_location(conn, location_name)

        if geo_data is not None:
            return (geo_data["lat"], geo_data["lon"])

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
        return (geo_data["lat"], geo_data["lon"])
