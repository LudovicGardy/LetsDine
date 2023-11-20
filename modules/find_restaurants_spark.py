from pyspark.sql.functions import radians, cos, sin, atan2, sqrt, lit
from pyspark.sql.functions import round as pyspark_round
import sys

from logger.logger import execution_logger

def calculate_distance_spark(df, lat, lon):
    """
    Calculate the distance between each point in a DataFrame and a given latitude and longitude.

    This function uses the Haversine formula to calculate the distance on the Earth's surface.

    :param df: A PySpark DataFrame containing the columns 'latitude' and 'longitude'.
    :param lat: Latitude of the reference point.
    :param lon: Longitude of the reference point.
    :return: DataFrame with an additional column 'distance' representing the distance in meters.
    """
    # Earth's radius in meters
    R = 6371000

    # Convert coordinates to radians in the DataFrame
    lat_rad = radians(lit(lat))
    lon_rad = radians(lit(lon))
    df = df.withColumn("lat_rad", radians(df["latitude"])) \
           .withColumn("lon_rad", radians(df["longitude"]))

    # Calculate the distance
    df = df.withColumn("a", 
                       sin((df["lat_rad"] - lat_rad) / 2) ** 2 + 
                       cos(lat_rad) * cos(df["lat_rad"]) * 
                       sin((df["lon_rad"] - lon_rad) / 2) ** 2)
    df = df.withColumn("distance", 2 * atan2(sqrt(df["a"]), sqrt(1 - df["a"])) * R)

    return df

def find_nearby_restaurants_spark(df, lat, lon, radius=1000):
    """
    Find restaurants within a specified radius from a given latitude and longitude.

    This function first calculates the distance to each restaurant using the Haversine formula,
    then filters the restaurants based on the specified radius.

    :param df: A PySpark DataFrame containing restaurant data with 'latitude' and 'longitude' columns.
    :param lat: Latitude of the reference point.
    :param lon: Longitude of the reference point.
    :param radius: Radius within which to find restaurants, in meters. Default is 1000 meters.
    :return: DataFrame of restaurants within the specified radius.
    """
    try:
        df_with_distance = calculate_distance_spark(df, lat, lon)

        # Round the 'distance' column to 2 decimal places
        df_with_distance = df_with_distance.withColumn("distance", pyspark_round(df_with_distance["distance"], 2))

        nearby_restaurants = df_with_distance.filter(df_with_distance["distance"] <= radius)
        return nearby_restaurants
    except Exception as e:
        execution_logger.error(f"An error occurred: {e}")
        sys.exit(1)
