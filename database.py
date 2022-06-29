from collections import namedtuple
import sqlite3

sql_create_location_cache_table = """ CREATE TABLE IF NOT EXISTS location_cache (
                                    id integer PRIMARY KEY,
                                    name string NOT NULL,
                                    latitude real NOT NULL,
                                    longitude real NOT NULL,
                                    class string,
                                    type string,
                                    importance real
                                ); """

INSERT_LOCATION_SQL = ''' INSERT INTO location_cache(name, latitude, longitude, class, type, importance)
              VALUES('{name}',:lat,:lon, :class, :type, :importance) '''

SELECT_LOCATION_SQL = ''' SELECT * FROM location_cache
              WHERE NAME = ?'''

def create_location_cache_table(conn: sqlite3.Connection) -> None:
    c = conn.cursor()
    c.execute(sql_create_location_cache_table)

def insert_location(conn: sqlite3.Connection, name:str, location) -> int:
    c = conn.cursor()
    name = name.replace("'", "''")
    c.execute(INSERT_LOCATION_SQL.format(name=name), location)
    return c.lastrowid

def retrieve_location(conn: sqlite3.Connection, name: str) -> dict:
    c = conn.cursor()
    c.execute(SELECT_LOCATION_SQL, (name,))
    row = c.fetchone()
    if row is None:
        return None

    COLUMNS = ['id', 'name', 'lat', 'lon', 'class', 'type', 'importance']
    return {key: value for key, value in zip(COLUMNS, row)}
