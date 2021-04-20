import os
import pandas as pd
from fastapi import FastAPI
cwd = os.getcwd() # dirname()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(cwd)))
CACHE_DIR = os.path.join(BASE_DIR, 'Data_Pipline/cache')

dataset = os.path.join(CACHE_DIR, 'ranking_movies_dataset_transform.csv')
app = FastAPI()

@app.get('/')
def read_root():
    return{"Hello": "World"}

@app.get('/movie_ranking')
def read_box_office_numbers():
    df = pd.read_csv(dataset)
    return df.to_dict("Rank")