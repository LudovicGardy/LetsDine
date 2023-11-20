import math

from logger.logger import create_logs

# Logger
error_logger = create_logs('errors_log', 'error')

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two points on the Earth's surface.

    Args:
    lat1, lon1: Latitude and longitude of the first point in degrees.
    lat2, lon2: Latitude and longitude of the second point in degrees.

    Returns:
    float: Distance in meters.
    """
    # Radius of the Earth in meters
    R = 6371000  

    # Convert coordinates from degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Calculate the distance
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def find_nearby_restaurants(df, central_lat, central_lon, radius):
    """
    Find restaurants within a specified radius from a central latitude and longitude.

    This function calculates the distance to each restaurant using the Haversine formula,
    then filters the restaurants based on the specified radius.

    Args:
    df: DataFrame containing restaurant data with 'latitude' and 'longitude' columns.
    central_lat, central_lon: Latitude and longitude of the central point in degrees.
    radius: Radius within which to find restaurants, in meters.

    Returns:
    DataFrame: Restaurants within the specified radius with an additional 'distance' column.
    """
    # Calculate distance for each restaurant
    df['distance'] = df.apply(lambda row: haversine_distance(central_lat, central_lon, row['latitude'], row['longitude']), axis=1)

    # Filter restaurants within the specified radius
    nearby_restaurants = df[df['distance'] <= radius].copy()
    
    # Round the distance to two decimal places
    nearby_restaurants['distance'] = nearby_restaurants['distance'].round(2)

    return nearby_restaurants
