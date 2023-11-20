# Global configuration parameters
LATITUDE = 48.865
LONGITUDE = 2.380
RADIUS = 1000
USE_SPARK = False
BIG_DATA = False
VERBOSE = False

def default_parameters():
    """
    Defines default parameters for application configuration.

    :return: Dictionary containing default configuration parameters.
    """
    parameters_dict = {
        "use_spark": USE_SPARK,
        "big_data": BIG_DATA
    }

    return parameters_dict

def initial_configuration():
    """
    Sets up the initial configuration for the application.

    This function determines the default place and sets initial parameters like latitude, longitude, and radius.

    :return: Dictionary with initial configuration including the default place and coordinates.
    """
    default_place_index = 10

    popular_places_dict = get_popular_places_paris()
    place = list(popular_places_dict.keys())[default_place_index]

    init_dict = {
        "place": place,    
        "central_lat": 48.865,
        "central_lon": 2.380,
        "radius": 500
    }
    
    return init_dict

def get_popular_places_paris():
    """
    Provides a dictionary of popular places in Paris with their coordinates.

    This function is a temporary solution and the data should eventually be extended and stored in a database.

    :return: Dictionary where keys are names of popular places and values are tuples of (latitude, longitude).
    """
    popular_places_dict = {
        "Eiffel Tower": (48.8584, 2.2945),
        "Louvre": (48.8606, 2.3376),
        "Notre-Dame": (48.8529, 2.3508),
        "Sacré-Cœur": (48.8867, 2.3431),
        "Arc de Triomphe": (48.8738, 2.2950),
        "Musée d'Orsay": (48.8600, 2.3266),
        "Centre Pompidou": (48.8606, 2.3522),
        "Place de la Concorde": (48.8656, 2.3216),
        "Palais Garnier": (48.8718, 2.3317),
        "Panthéon": (48.8463, 2.3464),
        "Luxembourg Garden": (48.8462, 2.3372),
        "Rodin Museum": (48.8554, 2.3158),
        "Catacombs of Paris": (48.8338, 2.3324),
        "Opéra Bastille": (48.8520, 2.3695),
        "Parc des Princes": (48.8412, 2.2531),
        "La Défense": (48.8897, 2.2419),
        "La Sorbonne": (48.8491, 2.3434),
        "Latin Quarter": (48.8493, 2.3461),
        "Montmartre": (48.8867, 2.3431),
        "Place Vendôme": (48.8675, 2.3299),
    }

    return popular_places_dict
