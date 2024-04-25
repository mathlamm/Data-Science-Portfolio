![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-F7A600?style=for-the-badge&logo=openweathermap&logoColor=white)
![AeroDataBox](https://img.shields.io/badge/AeroDataBox-007D8A?style=for-the-badge&logo=airplane&logoColor=white)

# Data-Driven Scooter Distribution for Gans E-Scooter Sharing

## Project Set Up
Tasked with enhancing the operational strategy for Gans, an e-scooter-sharing startup, I developed a data pipeline to predict scooter movement across urban landscapes. 
This initiative supports the company's mission to ensure scooter availability precisely where and when they're needed, addressing the logistical challenges posed by city topographies, aiport availability, and varying weather conditions.

## Contributions & Tools
- **Data Acquisition:** Implemented web scraping with BeautifulSoup; utilized APIs for real-time data retrieval.
- **Data Parsing:** Navigated complex JSON structures to extract pertinent information.
- **Data Cleansing:** Applied Python's string operations, Pandas library, and regex for data sanitization.
- **Iterative Processing:** Wrote Python loops and comprehensions for data manipulation.
- **Function Structuring:** Modularized code with Python functions for better organization and reuse.
- **Database Management:** Set up and modeled a MySQL database, crafted table relationships, and defined schemas.
- **Cloud Services:** Configured a GCP SQL instance, established cloud-to-local connectivity, and automated data insertion via Python scripts.
- **Serverless Deployment:** Leveraged GCP Cloud Functions for scalable, on-demand code execution.
- **Task Scheduling:** Scheduled Cloud Functions for routine data updates, ensuring a consistent data flow.


## Files
- For a city selection, *01_Cities_Selection.ipynb* scrapes wikipedia information and inserts an sql table.
- Fot those cities, *02_Dynamic_Mining.ipynb* uses several APi to retrieve information about weather forecast, nearby airports and arriving flights, which is passed on to mysql tables.
- Functions are in *mining_functions.py*
- my sql structure is in *create_schema_cities.sql*

## Endpoint
The endpoint was a scheduled data mining function hosted on GCP. The results can be found in this [Medium Blog](https://medium.com/@nix-niemand/a-strong-alliance-mysql-and-python-195708ef880a) 


![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/80d3df58-a965-4358-bc68-669ec84356ac)
![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/9cbacaa5-8714-44bb-864e-46db01128a5b)

