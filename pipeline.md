# 1.2 Rendre le script éxécutable
```bash
chmod +x /chemin/vers/le/script/search.py
```

## 1.2. Ajout d'un "shebang" (#!) tout en haut de search.py
```python
#!./env/bin/python
```

## Executer le script
Run from terminal

```bash
./search latitude=48.8319929 longitude=2.3245488 radius=100
./search latitude=48.865 longitude=2.380 radius=1000
./search latitude=48.865 longitude=2.380 radius=1000 use_spark=False big_data=False
```

## Streamlit
Run streamlit app

```bash
streamlit run search_GUI.py
```
## Run tests
```bash
cd APP
pytest tests/
```

## Push allowing workflows
```bash
git push https://username:token@github.com/username/repository.git
```

## Pandas vs Spark 15 000 000

### Pandas chargement
- 2 662 ms
- 2 756 ms

### Pandas exécution
- 66 207 ms
- 66 359 ms

### Spark chargement
- 4 871 ms
- 4 657 ms

### Spark exécution
- 314 ms
- 309 ms

## Pandas vs Spark 6 000

### Pandas chargement
- 19 ms
- 20 ms

### Pandas exécution
- 31 ms
- 29 ms

### Spark chargement
- 5 434 ms
- 4 674 ms

### Spark exécution
- 384 ms
- 305 ms


# Docker
docker build -t votre-application .
docker run -p 8501:8501 votre-application

# Git
brew install git-lfs
git lfs install
git lfs track "*.parquet"
git push origin main

```python
def get_user_parameters(self):

    # ID de votre Google Sheet
    sheet_id = "1uT4jj6syhrsQ19gBPezgnFEunH_JY_y7s4mwM6gUsWo"

    # ID de l'onglet du Google Sheet (0 pour la première feuille)
    gid = "0"

    # URL pour accéder aux données au format CSV
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    # Effectuer la requête HTTP pour obtenir les données
    response = requests.get(url) 

    # Assurer que la requête a réussi
    if response.status_code == 200:
        # Convertir les données CSV en DataFrame pandas
        data = pd.read_csv(url)
        print(data) 
    else:
        print("Erreur lors de l'accès au Google Sheet")

    # Accès à une cellule spécifique (ex: valeur en A1)
    cell_value = data.iloc[0, 0]
    self.use_spark = bool(cell_value)
    print("Use Spark:", cell_value)

    cell_value = data.iloc[0, 1]
    self.big_data = bool(cell_value)
    print("Big Data:", cell_value)
```