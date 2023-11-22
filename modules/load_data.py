import json
import pandas as pd
import sys

from modules.cache_data_fun import create_cache_decorator
from logger.logger import loading_logger

from dotenv import dotenv_values
config = dotenv_values(".env")

# Create a caching decorator to optimize data loading
cache_decorator = create_cache_decorator()

@cache_decorator
def load_restaurants_from_geojson(file_path, convert_to_parquet=False):
    """
    Load restaurant data from a GeoJSON file and optionally convert it to Parquet format.

    :param file_path: Path to the GeoJSON file.
    :param convert_to_parquet: Boolean flag to convert the data to Parquet format.
    :return: DataFrame containing restaurant data.
    """
    with open(file_path, 'r') as file:
        geojson_data = json.load(file)
        
        # Convert GeoJSON data to a DataFrame
        restaurants_df = pd.json_normalize(geojson_data["features"])
        original_count = len(restaurants_df)
        loading_logger.info(f"Total number of entries: {original_count}")

        # Filter out non-Point types and entries without coordinates or name
        restaurants_df = restaurants_df[
            (restaurants_df['geometry.type'] == 'Point') & 
            restaurants_df['geometry.coordinates'].apply(lambda x: x is not None and len(x) == 2) &
            restaurants_df['properties.name'].notna()
        ]

        filtered_count = len(restaurants_df)
        loading_logger.info(f"Number of entries after filtering: {filtered_count}")

        # Process coordinates
        restaurants_df[['longitude', 'latitude']] = pd.DataFrame(
            restaurants_df['geometry.coordinates'].tolist(), index=restaurants_df.index
        )
        
        # Remove duplicates
        restaurants_df = restaurants_df.drop_duplicates(subset=['properties.name', 'longitude', 'latitude'])
        duplicates_removed = original_count - filtered_count
        loading_logger.info(f"Number of duplicates removed: {duplicates_removed}")

        # Select and rename relevant columns
        restaurants_df = restaurants_df[
            ['properties.name', 'longitude', 'latitude']
        ].rename(columns={'properties.name': 'name'})

        if convert_to_parquet:
            restaurants_df.to_parquet(config['PARQUET_FILE_PATH'], index=False)

        return restaurants_df

@cache_decorator
def load_restaurants_from_parquet(parquet_file_path):
    """
    Load restaurant data from a Parquet file.

    :param parquet_file_path: Path to the Parquet file.
    :return: DataFrame containing restaurant data or None in case of failure.
    """
    try:
        loading_logger.info("Loading data from Parquet using Pandas.")
        restaurants_df = pd.read_parquet(parquet_file_path)
        return restaurants_df
    except Exception as e:
        loading_logger.error(f"Error while loading Parquet file: {e}")
        raise e
    
@cache_decorator
def load_restaurants_from_csv(csv_file_path):
    """
    Load restaurant data from a CSV file.

    :param csv_file_path: Path to the csv file.
    :return: DataFrame containing restaurant data or None in case of failure.
    """
    try:
        loading_logger.info("Loading data from CSV using Pandas.")
        restaurants_df = pd.read_csv(csv_file_path)
        return restaurants_df
    except Exception as e:
        loading_logger.error(f"Error while loading csv file: {e}")
        raise e