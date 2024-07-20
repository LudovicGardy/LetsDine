import pytest
import sys
import os

# Adding the parent directory to the system path for module import
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(current_dir)[0])

from modules.GUI.home import App
from modules.config import get_popular_places_paris, initial_configuration, default_parameters

if __name__ == "__main__":
    init_dict = initial_configuration()
    param_dict = default_parameters()
    app = App(place=init_dict["place"],
              latitude=init_dict["central_lat"], 
              longitude=init_dict["central_lon"], 
              radius=init_dict["radius"],
              use_spark=False,
              big_data=False)

