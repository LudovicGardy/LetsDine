import pytest
import sys
import os

# Add the parent directory to the system path for module imports
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(current_dir)[0])

from modules.load_data import load_restaurants_from_parquet
from modules.find_restaurants import haversine_distance, find_nearby_restaurants 

from dotenv import dotenv_values
config = dotenv_values(".env")

def test_haversine_distance():
    """
    Test the Haversine distance function between two geographic locations.

    This test uses coordinates of Paris and Lyon as an example and checks 
    if the calculated distance is within the expected range, allowing for some rounding.
    """
    # Coordinates of Paris and Lyon
    distance = haversine_distance(48.8566, 2.3522, 45.7640, 4.8357)
    # Expected distance is approximately 392km
    assert 391000 <= distance <= 393000  # Tolerance for rounding

@pytest.fixture
def restaurants_df():
    """
    Pytest fixture to load restaurants data from a Parquet file.

    The path to the Parquet file is obtained from the .env configuration.
    """
    # Load data from Parquet file specified in .env configuration
    return load_restaurants_from_parquet(config['PARQUET_FILE_PATH'])

def test_find_nearby_restaurants(restaurants_df):
    """
    Test finding nearby restaurants within various radii.

    This test checks the functionality of find_nearby_restaurants function
    with small, medium, and large radii, as well as with a zero radius.
    """
    # Coordinates of Paris as the central point
    central_lat, central_lon = 48.8566, 2.3522

    # Test with a small radius (100 meters)
    small_radius = 100
    small_radius_result = find_nearby_restaurants(restaurants_df, central_lat, central_lon, small_radius)
    assert all(small_radius_result['distance'] <= small_radius), "All restaurants should be within 100m"

    # Test with a medium radius (1 kilometer)
    medium_radius = 1000
    medium_radius_result = find_nearby_restaurants(restaurants_df, central_lat, central_lon, medium_radius)
    assert all(medium_radius_result['distance'] <= medium_radius), "All restaurants should be within 1km"

    # Test with a large radius (10 kilometers)
    large_radius = 10000
    large_radius_result = find_nearby_restaurants(restaurants_df, central_lat, central_lon, large_radius)
    assert all(large_radius_result['distance'] <= large_radius), "All restaurants should be within 10km"

    # Test with a zero radius (expecting no restaurants found)
    zero_radius = 0
    zero_radius_result = find_nearby_restaurants(restaurants_df, central_lat, central_lon, zero_radius)
    assert len(zero_radius_result) == 0, "No restaurants should be found with a zero radius"
