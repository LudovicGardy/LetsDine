import sys
import os
import time
import logging

# Importing modules for data loading and processing
from modules.load_data import load_restaurants_from_geojson, load_restaurants_from_parquet
from modules.load_data_spark import load_restaurants_from_parquet_spark
from modules.find_restaurants import find_nearby_restaurants
from modules.find_restaurants_spark import find_nearby_restaurants_spark
from logger.logger import execution_logger

# Handling environment variables
from dotenv import dotenv_values
config = dotenv_values(".env")

# Setting up a logger for search operations
def main(latitude, longitude, radius, use_spark=False, big_data=False, verbose=False):
    """
    Main function to find nearby restaurants based on location and search radius.

    :param latitude: Latitude of the search location.
    :param longitude: Longitude of the search location.
    :param radius: Search radius in meters.
    :param use_spark: Flag to use Apache Spark for processing (default: False).
    :param big_data: Flag to handle big data sets (default: False).
    :param verbose: Flag for verbose output (default: False).
    :return: A dictionary with monitoring data and a DataFrame/Spark DataFrame of nearby restaurants.
    """
    # Verbose output if enabled
    if verbose:
        print(f"\nUse Spark: {use_spark}\nBig Data: {big_data}\nVerbose: {verbose}\n")

    # Data loading time measurement
    start_time = time.time()
    filepath = config['PARQUET_FILE_PATH_15M'] if big_data else config['PARQUET_FILE_PATH']
    if use_spark:
        spark_session, restaurants = load_restaurants_from_parquet_spark("", filepath)
    else:
        restaurants = load_restaurants_from_parquet(filepath)
    end_time = time.time()
    load_data_time = (end_time - start_time) * 1000  # Converting to milliseconds
    execution_logger.info(f"Data loading time: {round(load_data_time)} ms")

    # Finding nearby restaurants
    start_time = time.time()
    nearby_restaurants = find_nearby_restaurants_spark(restaurants, latitude, longitude, radius) if use_spark else find_nearby_restaurants(restaurants, latitude, longitude, radius)
    end_time = time.time()
    search_time = (end_time - start_time) * 1000  # Converting to milliseconds
    execution_logger.info(f"Search time: {round(search_time)} ms")

    # Displaying results
    if not use_spark:
        _display_results_pandas(nearby_restaurants, radius, load_data_time, search_time, verbose)
        n_restaurants = len(restaurants)
    else:
        _display_results_spark(nearby_restaurants, radius, load_data_time, search_time, verbose)
        n_restaurants = restaurants.count()

    monitoring = {
        'load_data_time': load_data_time,
        'search_time': search_time,
        'n_restaurants': n_restaurants
    }

    # Stop Spark session
    # if use_spark:
    #     spark_session.stop()

    return monitoring, nearby_restaurants

def _display_results_pandas(nearby_restaurants, radius, load_data_time, search_time, verbose):
    """
    Display results for non-Spark execution path.

    :param nearby_restaurants: DataFrame of nearby restaurants.
    :param radius: Search radius in meters.
    :param load_data_time: Time taken to load data in milliseconds.
    :param search_time: Time taken for the search in milliseconds.
    :param verbose: Flag for verbose output.
    """
    if not nearby_restaurants.empty:
        print(f"Restaurants found within a radius of {radius} meters:")
        if verbose:
            for index, row in nearby_restaurants.iterrows():
                print(f"{row['name']}, Distance: {row['distance']} meters")
        print(f"\nData loading time: {round(load_data_time)} ms\nSearch time: {round(search_time)} ms")
    else:
        print("No restaurants found within the specified radius.")

def _display_results_spark(nearby_restaurants, radius, load_data_time, search_time, verbose):
    """
    Display results for Spark execution path.

    :param nearby_restaurants: Spark DataFrame of nearby restaurants.
    :param radius: Search radius in meters.
    :param load_data_time: Time taken to load data in milliseconds.
    :param search_time: Time taken for the search in milliseconds.
    :param verbose: Flag for verbose output.
    """
    if nearby_restaurants.count() > 0:
        print(f"Restaurants found within a radius of {radius} meters:")
        if verbose:
            for row in nearby_restaurants.collect():
                print(f"{row['name']}, Distance: {row['distance']} meters")
        print(f"\nData loading time: {round(load_data_time)} ms\nSearch time: {round(search_time)} ms")
    else:
        print("No restaurants found within the specified radius.")

# Main script execution if this file is run directly
if __name__ == "__main__":
    try:
        from modules.config import LATITUDE, LONGITUDE, RADIUS, USE_SPARK, BIG_DATA, VERBOSE
        main(LATITUDE, LONGITUDE, RADIUS, USE_SPARK, BIG_DATA, VERBOSE)
    except Exception as e:
        execution_logger.error(f"Configuration module import error: {e}")
