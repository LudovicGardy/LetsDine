import pytest
import os
import sys
import pandas as pd
from dotenv import dotenv_values

# Load configuration from .env file
config = dotenv_values(".env")

# Add parent directory to system path to import modules
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(current_dir)[0])

from modules.load_data import load_restaurants_from_parquet

def test_load_restaurants_from_parquet():
    """
    Test to ensure that restaurants data is loaded correctly from a Parquet file.
    Verifies that the resulting DataFrame is not None and is indeed a DataFrame.
    """
    restaurants_df = load_restaurants_from_parquet(config['PARQUET_FILE_PATH'])

    assert restaurants_df is not None, "DataFrame should not be None"
    assert isinstance(restaurants_df, pd.DataFrame), "Result should be a DataFrame"

def test_data_quality():
    """
    Test to ensure data quality of the restaurants DataFrame.
    - Checks for the presence of key columns: 'name', 'latitude', 'longitude'.
    - Verifies that there are no null values in these key columns.
    - Asserts the correct data types for these columns.
    """
    restaurants_df = load_restaurants_from_parquet(config['PARQUET_FILE_PATH'])

    # Check if key columns are present
    assert all(column in restaurants_df.columns for column in ['name', 'latitude', 'longitude']), \
           "Key columns are missing"

    # Check for null values in key columns
    assert restaurants_df['name'].notnull().all(), "Column 'name' contains null values"
    assert restaurants_df['latitude'].notnull().all(), "Column 'latitude' contains null values"
    assert restaurants_df['longitude'].notnull().all(), "Column 'longitude' contains null values"
   

    assert pd.api.types.is_object_dtype(restaurants_df['name']), "Column 'name' should be of type string"
    assert pd.api.types.is_float_dtype(restaurants_df['latitude']), "Column 'longitude' should be of type float"
    assert pd.api.types.is_float_dtype(restaurants_df['longitude']), "Column 'longitude' should be of type float"