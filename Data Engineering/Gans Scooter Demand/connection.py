import pandas
import pymysql
import sqlalchemy
from keys import db_pw, db_user

def connection_cloud_local():
    schema = "cities"
    host = "34.78.126.24" # Change this to your instance's IP
    user = db_user
    password = db_pw # Your database password goes here
    port = 3306
    connection_string =  f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    return connection_string


def connection_cloud_online():
    connection_name = "studious-depth-419209:europe-west1:wbs"
    schema_name = "cities"

    driver_name = 'mysql+pymysql'
    query_string = {"unix_socket": f"/cloudsql/{connection_name}"}

    db = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername = driver_name,
            username = db_user,
            password = db_pw,
            database = schema_name,
            query = query_string
        )
    )
    return db


def connection_local():
    schema = "cities"
    host = "127.0.0.1"
    user = db_user
    password = db_pw
    port = 3306
    connection = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'

    return connection


