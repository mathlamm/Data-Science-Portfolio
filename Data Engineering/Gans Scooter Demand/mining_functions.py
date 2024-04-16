import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
import pymysql
import sqlalchemy
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from keys import Openweather_API_key, Aerodata_API_key, Ninjas_API_key
from connection import connection_local, connection_cloud_local, connection_cloud_online


## Change connection, based on machine (local vs local cloud framework vs cloud)
connection = connection_cloud_local()


## Scrape Wikipedia for Information 
# Takes a list of City Names. 
# returns a dataframe with infos per city 
# Infos: Country & Coordinates
def city_scrape(cities_list_new):  # c should be a list of city names

    # create empty df for loop
    cities = pd.DataFrame(columns = ["city_name", "country", "longitude", "latitude"])

    # iterate through each city
    for city_name in cities_list_new:
        url = "https://en.wikipedia.org/wiki/"+city_name
        response = requests.get(url)
        city = BeautifulSoup(response.content, 'html.parser')

        country= city.find_all("th", string="Country")[0].find_next().get_text()
        lat = clean_coord(city.find(class_="latitude").get_text())
        long = clean_coord(city.find(class_="longitude").get_text())

        cities.loc[len(cities)] = [city_name,country,long,lat]

    return cities



# push new rows of cities table to sql
def push_cities(cities_df_new):

    # Pull existing cities list from sql table
    cities_sql_old = pd.read_sql("cities", con=connection)
    cities_list_old = cities_sql_old["city_name"].tolist()
    
    # new city list
    cities_list_new = cities_df_new["city_name"].tolist()

    # compare lists and keep only new cities in df
    cities_list_update = set(cities_list_old).symmetric_difference(set(cities_list_new))
    cities_df_update = cities_df_new.loc[cities_df_new["city_name"].isin(cities_list_update)]

    # push new cities
    cities_df_update.to_sql('cities',
                  if_exists='append',
                  con=connection,
                  index=False)

    return print("cities table successfully updated")



## API - City Population
# using Ninjas-API
def pop_scrape_api(city_df):

    popul = pd.DataFrame(columns = ["city_id", "population", "date_fetched"])
    
    for x, row in city_df.iterrows():
        name = row["city_name"].split(" ")[0]     # make sure that cities like "Halle (Saale) are found by the API"
        api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': Ninjas_API_key})
        if response.status_code == requests.codes.ok:
            population_json = response.json()
        else:
            print("Error:", response.status_code, response.text)
            break

        pop = population_json[0]["population"]
        date_fetched = datetime.today().strftime('%F %T')
        
        popul.loc[len(popul)] = [row["city_id"],pop,date_fetched]

    return popul



## update population table
def push_population(population_sql_new):

    # adapt datetype
    population_sql_new.date_fetched = pd.to_datetime(population_sql_new.date_fetched)

    # read old population list from sql
    population_sql_old = pd.read_sql("population", con=connection)

    # Merge both DataFrames on 'city_id' to find common and new records
    merged_df = population_sql_new.merge(population_sql_old, on='city_id', how='left', suffixes=('_new', '_old'))

    # Identify new city records that do not exist in the old data and update db
    new_cities = population_sql_new[~population_sql_new['city_id'].isin(population_sql_old['city_id'])]
    new_cities.to_sql('population', con=connection, if_exists='append', index=False)

    # Filter rows that need to be updated: newer by at least one year
    updates = merged_df[(merged_df['date_fetched_new'] > merged_df['date_fetched_old'] + pd.DateOffset(years=1) ) | merged_df['date_fetched_old'].isna()] 

    # Prepare the data for a bulk update
    update_data = updates[['population_id', 'city_id', 'population_new', 'date_fetched_new']].to_dict('records')

    # Update existing records
    with create_engine(connection).begin() as conn:    #  REMOVE 'create_engine' here for on-cloud version (just run connection.begin())
        for data in update_data:
            update_statement = text("""
                UPDATE population
                SET population = :population, date_fetched = :date_fetched
                WHERE city_id = :city_id
            """)
            conn.execute(update_statement, {'population': data['population_new'], 'date_fetched': data['date_fetched_new'], 'city_id': data['city_id']})

    # Close the connection
    conn.close()

    return("population data was updated\n")




## Weather Forecast
# based on openweathermap-API
def forecasting(cities_sql):
    weather_forecast_df = pd.DataFrame()

    # iterate through rows (cities) of cities table
    for x, row in cities_sql.iterrows():

        # request data, based on coordinates
        weather = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={row['latitude']}&lon={row['longitude']}&appid={Openweather_API_key}&units=metric", headers={'X-Api-Key': Openweather_API_key})
        weather_json = weather.json()

        # continue if request was successful. Otherwise break. 
        if weather_json["cod"] == "200":

            # iterate through 'weather' element and extract description for each prognosis (8 per day for 5 days = 40 entries)
            outlook = []
            for x in range(len(weather_json["list"])):
                _ = weather_json["list"][x]["weather"][0]["description"]
                outlook.append(_)
            
            # use 'pd.jason_normalize' to shape a dataframe including all information fronm 'list'. 
            weather_forecast = pd.json_normalize(weather_json["list"])

            # Add outlook, city_id and date_fetched.
            weather_forecast["outlook"] = outlook 
            weather_forecast["city_id"] = [row["city_id"]] * weather_forecast["weather"].count()  # repeat n times, where n matches the number of forecasts
            weather_forecast["date_fetched"] = [datetime.today().strftime('%F %T')] * weather_forecast["weather"].count()

            # some weather forecasts come without rain-prediction 
            if "rain.3h" not in weather_forecast.columns:
                weather_forecast["rain.3h"] = np.nan

            # keep only relevant weather information: Temperature, Perceived Temperature, Wind Speed, Rain during last 3 hours.
            weather_forecast = weather_forecast[["city_id","dt_txt","outlook", "main.temp","main.feels_like", "wind.speed", "rain.3h", "date_fetched"]]

            # insert "0" for missing values in rain.3h
            weather_forecast.loc[weather_forecast["rain.3h"].isnull(), "rain.3h"] = 0
            
            # Rename column names. Add dataframe to weather_forecast_df.
            weather_forecast.rename(columns={"dt_txt":"forecast_time", "main.feels_like": "feels_like","main.temp": "temp", "wind.speed": "wind_speed", "rain.3h":"rain_3h"}, inplace=True)
            weather_forecast_df = pd.concat([weather_forecast_df,weather_forecast],ignore_index=True)
        
        else: 
            print(f"The request was not successful. Errorcode {weather_json['cod']} on city {row['city_name']}")
            break

    # change data types
    weather_forecast_df["forecast_time"] = pd.to_datetime(weather_forecast_df["forecast_time"])
    weather_forecast_df["date_fetched"] = pd.to_datetime(weather_forecast_df["date_fetched"])

    return weather_forecast_df    





## Airport by Cities
# using aerodatabox-API
def icao_airport_codes(cities_df):

  icao_codes = []
  city_ids = []

  for index, row in cities_df.iterrows():
    latitude = row["latitude"]
    longitude = row["longitude"]
    
    # prepare and call the API
    url = "https://aerodatabox.p.rapidapi.com/airports/search/location"
    querystring = {"lat":latitude,"lon":longitude,"radiusKm":"60","limit":"10","withFlightInfoOnly":"true"}
    headers = {
      "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com",
      "X-RapidAPI-Key": Aerodata_API_key 
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        airport_json = response.json()
    else:
        return response.reason
    
    # get the data for each city
    for item in airport_json["items"]:
        icao_codes.append(item["icao"])
        city_ids.append(row["city_id"])  

  # after looping, turn data into dataframe
  return pd.DataFrame({"icao_code": icao_codes, "city_id":city_ids})


## update cities_airports
def push_cities_airports(cities_airports_df_new):
    # read existing table from sql
    cities_airports_df_old = pd.read_sql("cities_airports", con= connection)

    # only keep new values (cave: cant remove cities, only add new ones)
    cities_airports_df = cities_airports_df_new.loc[(cities_airports_df_old.city_id.count()):]

    # push to sql
    cities_airports_df.to_sql('cities_airports',
                  if_exists='append',
                  con=connection,
                  index=False)

    return print("cities_airports table updated\n")


## Airport info 
# using aerodatabox-API 
def airports(cities_airports_df):
    import requests

    # only use unique airport ICAOs
    cities_airports_df = cities_airports_df.drop_duplicates("icao_code")

    # create df
    airports_df = pd.DataFrame()

    for x, row in cities_airports_df.iterrows():
        # request airport data for each airport
        url = f"https://aerodatabox.p.rapidapi.com/airports/icao/{row['icao_code']}"
        querystring = {"withTime":"false","withRunways":"false"}
        headers = {"X-RapidAPI-Key": Aerodata_API_key, "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"}
        response = requests.get(url, headers=headers, params=querystring)

        # Check response. If positive, extract json format and normalize to df. Otherwise report error msg and line and break
        if response.status_code == 200:
            airports_json = response.json()
        else:
            print(f"**ERROR**\nAirport: {row['icao_code']}\nCode: {response.status_code}\nReason: {response.reason}")
        
        # normalize to df, select and rename columns
        airports_df_all = pd.json_normalize(airports_json)
        airport_df = airports_df_all.copy()[["icao", "iata", "fullName", "location.lat", "location.lon", "country.code"]]
        airport_df.rename(columns={"icao":"icao_code", "iata":"iata_code", "fullName": "full_name", "location.lat": "latitude", "location.lon":"longitude", "country.code":"country_code"}, inplace=True)

        # add to df
        airports_df = pd.concat([airports_df,airport_df],ignore_index=True)

    # return df
    return airports_df


## update airports table
def push_airports(airports_new):

    # read existing airports table
    airports_old = pd.read_sql("airports", con=connection)

    # only keep new airports
    airports_df = airports_new[~airports_new.icao_code.isin(airports_old.icao_code)]

    # push to sql
    airports_df.to_sql('airports',
                    if_exists='append',
                    con=connection,
                    index=False)

    return print("airports table was updated\n")




## Flight Arrivals per Airport
# based on cities_airports-data 
# using aerodatabox API

def arrrivals_by_airport(airports):   # 'airports' must be a dataframe containing a list of airport ICAOs

    # Define datetime of tommorow. The query need to be split in 2 x 12 hour windows (=max allowed time span query)
    tommorrow = (datetime.today()+timedelta(days=1)).strftime('%F')
    time_windows_start = [f"{tommorrow}T{x}" for x in ["00:00", "12:00"]]
    time_windows_end = [f"{tommorrow}T{x}" for x in ["11:59", "23:59"]]

    # create empty flights_df
    flights_df = pd.DataFrame()

    ## iterate through airports
    for x, row in airports.iterrows():

        ## iterate through the timewindows
        for timewindow in range(2):

            # request data, per timewindow and airport
            url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{row['icao_code']}/{time_windows_start[timewindow]}/{time_windows_end[timewindow]}"
            querystring = {"withLeg":"true","direction":"Arrival","withCancelled":"false","withCodeshared":"true","withCargo":"false","withPrivate":"false","withLocation":"false"}
            headers = {"X-RapidAPI-Key": Aerodata_API_key, "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"}

            response = requests.get(url, headers=headers, params=querystring)
            # Check response. If positive, extract json format and normalize to df. Otherwise report error msg and line and break
            if response.status_code == 200:
                flights_json = response.json()
                flights_df_timewindow_all = pd.json_normalize(flights_json["arrivals"])
            else:
                print(f"**ERROR**\nAirport: {row['icao_code']}\nCode: {response.status_code}\nReason: {response.reason}")
                break

            # Add city_id and airport_icao to df
            df_len = flights_df_timewindow_all["number"].count()
            flights_df_timewindow_all["arrival_airport_icao"] = [row["icao_code"]] * df_len
            flights_df_timewindow_all["date_fetched"] = [datetime.today().strftime('%F %T')] * df_len

            # Check if "arrival.revisedTime.local" exists. Some airports don't seem to report it. If it does not exist, create it, filled with NaNs
            if "arrival.revisedTime.local" not in flights_df_timewindow_all.columns:
                flights_df_timewindow_all["arrival.revisedTime.local"] = np.nan

            # choose relevant columns and rename. Then, concat to flights_df
            flights_df_timewindow = flights_df_timewindow_all[
                [   "arrival_airport_icao",
                    "departure.airport.icao",
                    "departure.airport.name",
                    "departure.scheduledTime.local",
                    "arrival.scheduledTime.local",
                    "arrival.revisedTime.local",
                    "aircraft.model",
                    "airline.name",
                    "date_fetched"
                ]]
            flights_df_timewindow.columns = [c.replace('.', '_') for c in flights_df_timewindow]
            flights_df = pd.concat([flights_df,flights_df_timewindow],ignore_index=True)


    # return flight_df

    # change datatypes. Cut of additional description within date cells, like "~Z" or "~+02:00".
    flights_df["date_fetched"] = pd.to_datetime(flights_df["date_fetched"])
    flights_df["departure_scheduledTime_local"] = pd.to_datetime(flights_df["departure_scheduledTime_local"].str[:16])
    flights_df["arrival_scheduledTime_local"] = pd.to_datetime(flights_df["arrival_scheduledTime_local"].str[:16])
    flights_df["arrival_revisedTime_local"] = pd.to_datetime(flights_df["arrival_revisedTime_local"].str[:16])

    return flights_df




## a function that changes the coordinate system
def clean_coord(coord):
    import re
    values = re.split(r"\D", coord, maxsplit=2)
    result = float(values[0])+float(values[1])/60
    if "″" in values[2]:
        result += float(values[2].split("″")[0])/3600
    if "S" in values[2] or "W" in values[2]:
        result *= -1
    return result
