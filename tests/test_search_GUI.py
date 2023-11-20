import pytest
import sys
import os

# Adding the parent directory to the system path for module import
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(current_dir)[0])

from search_GUI import App
from modules.config import get_popular_places_paris, initial_configuration

# Retrieving initial configuration
init_dict = initial_configuration()

def test_app_initialization():
    """
    Tests the initialization of the App class.

    This test checks whether an instance of the App class can be successfully created
    with the initial configuration parameters.
    """
    try:
        app = App(place=init_dict["place"], latitude=init_dict["central_lat"], 
                  longitude=init_dict["central_lon"], radius=init_dict["radius"])
        assert True, "App instance successfully created."
    except Exception as e:
        pytest.fail(f"Failed to create App instance: {e}")
