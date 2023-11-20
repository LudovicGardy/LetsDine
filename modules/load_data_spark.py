import pandas as pd
import requests
import tempfile
from logger.logger import create_logs
from modules.cache_data_fun import create_cache_decorator
from logger.logger import loading_logger

from dotenv import dotenv_values

# Load environment variables
config = dotenv_values(".env")

# Initialize cache decorator for caching data
cache_decorator = create_cache_decorator(force_lru_cache=True)

@cache_decorator
def load_restaurants_from_parquet_spark(spark_session, parquet_file_path):
    """
    Load restaurant data from a Parquet file using Apache Spark.

    :param spark: Spark session object.
    :param parquet_file_path: Path to the Parquet file.
    :return: DataFrame containing restaurant data, or None in case of failure.
    """
    loading_logger.info("Loading data from Parquet using Spark.")

    try:
        # Read data from Parquet file
        restaurants_df = spark_session.read.parquet(parquet_file_path, header=True, inferSchema=True)

        # Drop missing values
        restaurants_df = restaurants_df.na.drop()

        # Ensure correct data types for latitude and longitude
        restaurants_df = restaurants_df.withColumn("latitude", restaurants_df["latitude"].cast("float")) \
                                       .withColumn("longitude", restaurants_df["longitude"].cast("float"))
        
        return restaurants_df
    except Exception as e:
        # Log exception and return None
        loading_logger.error(f"Error while loading the Parquet file: {e}")
        return None
