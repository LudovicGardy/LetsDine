import pytest
import sys
import os

# Add the parent directory to the system path to import the main module
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(current_dir)[0])

from main import main

@pytest.mark.parametrize("latitude, longitude, radius, expected_count", [
    (48.8566, 2.3522, 1000, None),  # Example coordinates with a radius and an expected number of restaurants
])
def test_main(latitude, longitude, radius, expected_count):
    """
    Test the main function with given latitude, longitude, and radius.

    :param latitude: Latitude of the location to test.
    :param longitude: Longitude of the location to test.
    :param radius: Search radius around the location.
    :param expected_count: Expected number of restaurants within the radius. None if not checking count.
    """

    # Execute the main function and capture its output
    monitoring, nearby_restaurants = main(latitude, longitude, radius)

    # Check if the execution was successful
    assert monitoring is not None, "Failure of the main function"
    assert not nearby_restaurants.empty, "No restaurants found when some are expected"

    # Verify the number of returned restaurants
    if expected_count:
        assert len(nearby_restaurants) <= expected_count, "Too many restaurants found"

    # Check performance metrics
    assert monitoring['load_data_time'] < 1000, "Data loading takes too long (in ms)"
    assert monitoring['search_time'] < 500, "Search takes too long (in ms)"
