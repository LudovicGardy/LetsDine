import pandas as pd
import streamlit as st
import streamlit_folium
import folium
from folium.plugins import MarkerCluster, MiniMap

from main import main
from modules.config import (
    get_popular_places_paris,
    initial_configuration,
    default_parameters,
)

# Retrieving popular places in Paris
POPULAR_PLACES = get_popular_places_paris()

# Streamlit page configuration
st.set_page_config(
    page_title="Let's Dine!",
    page_icon="images/logo-DALLE.png",
    layout="centered",
    initial_sidebar_state="expanded",
)


class App:
    def __init__(
        self,
        place: str,
        latitude: float,
        longitude: float,
        radius: int,
        use_spark: bool,
        big_data: bool,
        verbose: bool = False,
    ):
        """
        Initialize the application with given parameters.

        :param place: Default place name.
        :param latitude: Default latitude for the location.
        :param longitude: Default longitude for the location.
        :param radius: Default search radius.
        :param use_spark: Flag to use Apache Spark for data processing.
        :param big_data: Flag to indicate handling of big data.
        """
        print("Initializing the app...")

        # Initialization of instance variables
        self.use_spark = use_spark
        self.big_data = big_data
        self.place = place
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.verbose = verbose
        self.popular_places_dict = get_popular_places_paris()

        # Setting up the sidebar
        with st.sidebar:
            self.setup_sidebar()
            self.initialize_ui()

        # Fetching nearby restaurants
        self.get_nearby_restaurants()

    def setup_sidebar(self):
        """
        Set up the sidebar for the application.
        """
        logo_path = "images/logo-DALLE.png"
        desired_width = 60

        # Creating columns for layout
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(logo_path, width=desired_width)
        with col2:
            st.write("# Let's Dine")

        # Sidebar welcome message
        st.caption("""Welcome to Let's Dine! A prototype to find a restaurant near you or a popular place.\n
                   \nTo use the application, simply choose a location. 
                   \nIf you are curious, you can also use latitude and longitude.
                   \n Logo: DALL.E
                   """)

        st.divider()

    def initialize_ui(self):
        """
        Initialize the user interface elements.
        """
        # ComboBox to select a popular place
        default_index = list(self.popular_places_dict.keys()).index(self.place)
        self.selected_place = st.selectbox(
            "Select a popular place in Paris",
            options=list(self.popular_places_dict.keys()),
            index=default_index,
        )

        # Update coordinates based on selected place
        self.latitude, self.longitude = self.popular_places_dict[self.selected_place]

        # User data input widgets
        col1, col2 = st.columns([1, 1])

        with col1:
            self.central_lat = st.number_input(
                "Latitude", value=self.latitude, format="%.6f"
            )
        with col2:
            self.central_lon = st.number_input(
                "Longitude", value=self.longitude, format="%.6f"
            )

        self.radius = st.number_input("Radius (in meters)", value=self.radius, step=100)

        self.use_spark = st.sidebar.checkbox(
            "Use Apache Spark for processing", value=self.use_spark
        )

    def get_nearby_restaurants(self):
        """
        Fetch nearby restaurants based on user input and display results.
        """
        monitoring, nearby_restaurants = main(
            latitude=self.central_lat,
            longitude=self.central_lon,
            radius=self.radius,
            use_spark=self.use_spark,
            big_data=self.big_data,
            verbose=self.verbose,
        )

        # Displaying monitoring information
        st.write("### Monitoring")
        st.write("The monitoring section exists for development purposes only.")

        col1, col2, col3 = st.columns([1, 0.5, 0.5])

        with col1:
            st.info(f"Number of restaurants: {monitoring['n_restaurants']}")

        with col2:
            if self.use_spark:
                st.error("Pandas: False")
            else:
                st.success("Pandas: True")

        with col3:
            if self.use_spark:
                st.success("Spark: True")
            else:
                st.error("Spark: False")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.info(f"Data loading time: {round(monitoring['load_data_time'])} ms")
        with col2:
            st.info(f"Search time: {round(monitoring['search_time'])} ms")

        st.divider()

        # Checking if the DataFrame is empty
        if self.use_spark:
            # Displaying restaurants if any are found
            st.write(
                f"### Restaurants found within a radius of :green[{self.radius}] meters around :green[{self.selected_place}]"
            )
            st.write(f"Your position is marked in :red[red], enjoy your meal!")
            self.plot_map_spark(nearby_restaurants)
            st.divider()
            st.write(
                f"### List of :green[{nearby_restaurants.count()}] restaurants found on the map"
            )
            self.plot_table_spark(nearby_restaurants)
        elif not self.use_spark:
            if not nearby_restaurants.empty:
                st.write(
                    f"### Restaurants found within a radius of :green[{self.radius}] meters around :green[{self.selected_place}]"
                )
                st.write(f"Your position is marked in :red[red], enjoy your meal!")
                self.plot_map(nearby_restaurants)
                st.divider()
                st.write(
                    f"### List of :green[{len(nearby_restaurants)}] restaurants found on the map"
                )
                self.plot_table(nearby_restaurants)
            else:
                st.write("No restaurants found within the specified radius.")

    def plot_map(self, nearby_restaurants: pd.DataFrame):
        """
        Plot a map with markers for nearby restaurants using Folium.

        :param nearby_restaurants: DataFrame containing restaurant data.
        """
        # Custom map style
        tileset = "CartoDB positron"

        # Initializing the map
        map = folium.Map(
            location=[self.central_lat, self.central_lon], tiles=tileset, zoom_start=12
        )

        # Marker for the reference point
        folium.Marker(
            [self.central_lat, self.central_lon],
            popup="<b>You are here</b>",
            icon=folium.Icon(color="red"),
        ).add_to(map)

        # Cluster for markers
        marker_cluster = MarkerCluster().add_to(map)

        # Adding markers for each restaurant
        for index, row in nearby_restaurants.iterrows():
            folium.Marker(
                [row["latitude"], row["longitude"]],
                popup=f"<b>{row['name']}</b><br>Distance: {row['distance']} m",
                icon=folium.Icon(color="green", icon="cutlery", prefix="fa"),
            ).add_to(marker_cluster)

        # Adding a MiniMap
        minimap = MiniMap(tileset=tileset)
        map.add_child(minimap)

        # Displaying the map in Streamlit
        streamlit_folium.st_folium(map, width=700, height=500)

    def plot_map_spark(self, nearby_restaurants: pd.DataFrame):
        """
        Plot a map with markers for nearby restaurants, specifically for Spark dataframes.

        :param nearby_restaurants: Spark DataFrame containing restaurant data.
        """
        tileset = "CartoDB positron"
        map = folium.Map(
            location=[self.central_lat, self.central_lon], tiles=tileset, zoom_start=12
        )

        folium.Marker(
            [self.central_lat, self.central_lon],
            popup="<b>You are here</b>",
            icon=folium.Icon(color="red"),
        ).add_to(map)

        marker_cluster = MarkerCluster().add_to(map)

        # Collect necessary data
        rows = nearby_restaurants.select(
            "latitude", "longitude", "name", "distance"
        ).collect()

        for row in rows:
            folium.Marker(
                [row["latitude"], row["longitude"]],
                popup=f"<b>{row['name']}</b><br>Distance: {row['distance']} m",
                icon=folium.Icon(color="green", icon="cutlery", prefix="fa"),
            ).add_to(marker_cluster)

        minimap = MiniMap(tileset=tileset)
        map.add_child(minimap)

        streamlit_folium.st_folium(map, width=700, height=500)

    def plot_table(self, nearby_restaurants: pd.DataFrame):
        """
        Display a sorted table of nearby restaurants.

        :param nearby_restaurants: DataFrame containing restaurant data.
        """
        # Sorting the DataFrame by distance in ascending order
        sorted_nearby_restaurants = nearby_restaurants.sort_values(by="distance")

        # Defining the height for the DataFrame
        height = 400 if len(sorted_nearby_restaurants) > 10 else None

        # Displaying the sorted DataFrame with style and defined height
        st.dataframe(
            sorted_nearby_restaurants[["name", "distance", "latitude", "longitude"]],
            height=height,
            use_container_width=True,
        )

    def plot_table_spark(self, nearby_restaurants: pd.DataFrame):
        # Sort the DataFrame by distance in ascending order
        sorted_nearby_restaurants = nearby_restaurants.orderBy("distance")

        # Collect necessary data
        sorted_nearby_restaurants = sorted_nearby_restaurants.select(
            "name", "distance", "latitude", "longitude"
        ).toPandas()

        # Defining the height for the DataFrame
        height = 400 if len(sorted_nearby_restaurants) > 10 else None

        # Displaying the sorted DataFrame with style and defined height
        st.dataframe(sorted_nearby_restaurants, height=height, use_container_width=True)


# Exécution du script principal si ce fichier est exécuté directement
if __name__ == "__main__":
    init_dict = initial_configuration()
    param_dict = default_parameters()
    app = App(
        place=init_dict["place"],
        latitude=init_dict["central_lat"],
        longitude=init_dict["central_lon"],
        radius=init_dict["radius"],
        use_spark=False,
        big_data=False,
    )
