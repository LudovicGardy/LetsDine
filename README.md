# Let's Dine - Prototype of a distance calculator

The prototype is available at https://letsdine.streamlit.com.

## Basic structure of the repository

- `LetsDine/`: Backend + Frontend.
    - `logger/`: Optional, notebooks for tests.
    - `logs/`: Process logs.
        - `errors_log.log`  
        - `execution_log.log`  
        - `loading_log.log`  
    - `modules/`: Modules code.
        - `cache_data.py`  
        - `config.py`  
        - `find_restaurants_spark.py`  
        - `find_restaurants.py`  
        - `load_data_spark.py`  
        - `load_data.py`  
    - `main.py`: Main script.
    - `search`: Executable script.
    - `search_GUI`: Web App Prototype.  
    - `test`: Unitary tests.
        - `test_find_restaurant.py`: evalute distance calculations. 
        - `test_load_data.py`: evalute data loading and data quality.
        - `test_main.py` : evalute main script.
        - `test_search_GUI.py`: evalute web app prototype.

To run the app locally, you can run the following instructions.

## 1. Set up the environment 

### 1.1. [Optional] Create a virtual environment with anaconda

In the terminal:
```bash
cd your_folderpath # that contains the files search, and main.py
conda create -n letsdine python=3.9
conda activate letsdine
```

### 1.2. Install librairies

In the terminal:
```bash
pip install -r requirements.txt
```

### 1.3 [Optional] Download a 15M lines example file
You can try the calculator using big data, with a table of 15,000,000 lines instead of 6,200+. 

If you want to use this feature, you need to download the data that are stored on a AWS S3 bucket by clicking [here](https://letsdine.s3.eu-west-3.amazonaws.com/restaurants_simulated_france.parquet).

Once downloaded, the file called `restaurants_simulated_france.parquet` should be placed in the `LetsDine/static/data/` folder. It will then be automatically detected when you call it later.

## 2. Run the distance calculator

You can choose between 3 execution modes. Use the one that suits you best :
- Run using the executable (2.1.)
- Run using the python script (2.2.)
- Run unsing streamlit (web UI, 2.3.)

### 2.1. OPTION 1: Run using the executable

In the terminal, exemple 1:
```bash
./search latitude=48.865 longitude=2.380 radius=1000
```

In the terminal, exemple 2:
```bash
./search latitude=48.865 longitude=2.380 radius=1000 use_spark=False big_data=False verbose=False
```

You must specify 3 mandatory values (see exemple 1):
- latitude: float, exemple: **48.865**
    geographic coordinate of the place of interest
- longitude: float, exemple: **2.380**
    geographic coordinate of the place of interest
- radius: float, exemple: **100**
    radius around the place of interest in which you want to find the restaurants

You can specify 3 optional values (see exemple 2):
- use_spark: bool, default is **False**
    use spark to process dataframes instead of pandas
- big_data: bool, default is **False**
    use a simulated dataset with 15 million simulated restaurants names and coordinates. if False, use the provided dataset (around 6000 restaurants)
- verbose: bool, default is **False**
    print infos, mainly for debugging

### 2.2. OPTION 2: Run using the python script

In the terminal:
```bash
python run main.py
```

[OPTIONAL] In the config file that you can find in `modules/config.py`, you can change the following parameters :
- LATITUDE: float, default is **48.865**
- LONGITUDE: float, default is **2.380**
- RADIUS: int, default is **1000**
- USE_SPARK: bool, default is **False** 
- BIG_DATA: False, default is **False**
- VERBOSE: False, default is **False**

### 2.3. OPTION 3: Run using streamlit (web UI)

In the terminal:
```bash
streamlit run search_GUI.py
```

The app will be available at:
-  Local URL: http://localhost:8501
- Network URL: http://192.168.1.5:8501

Streamlit has compatibility problems with Spark. To process data with Spark, you should use Option 1 or 2 above.

### 3. Run unitary tests

In the terminal:
```bash
pytest tests/
```

### 4. CI/CD

This solution implements a CI/CD pipeline where unit tests are executed and deployment is carried out upon each code push. In this prototype phase, failing unit tests do not halt the deployment process, allowing for flexible development, but this should be reconsidered for production stages to ensure application stability.