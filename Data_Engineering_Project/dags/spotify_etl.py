from sqlite3.dbapi2 import Cursor, Timestamp
import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
from datetime import datetime as dt
import datetime
import sqlite3
import spotipy
from spotipy.client import Spotify

tdy = datetime.datetime.now()


def check_valid_data(df: pd.DataFrame) -> bool:
    #check if dataframe is empty
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    currentMonth = tdy.month
    if df.empty:
        print("No tracks downloaded")
        return False
    #primary key check 
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    #check for missing values
    if df.isnull().values.any():
        raise Exception("Null valued found")
    for i in df['timestamp'].dt.month:
        if i == currentMonth:
            raise Exception("one or more songs are not from the previous month")


# job scheduling
def run_spotify_etl():

    def perform_auth():
        SPOTIPY_CLIENT_ID=''
        SPOTIPY_CLIENT_SECRET=''
        SPOTIPY_REDIRECT_URI=''

        scope='user-read-recently-played'

        oauth_object = spotipy.SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=scope)

        token_dict = oauth_object.get_access_token()

        now = datetime.datetime.now()
        access_token = token_dict["access_token"]
        expires_in = token_dict["expires_in"] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        access_token = access_token
        access_token_expires = expires

        return access_token, access_token_expires

    def get_access_token():
        token, expires = perform_auth()
        now = datetime.datetime.now()
        if expires < now:
            perform_auth()
            return get_access_token()
        elif token == None:
            perform_auth()
            return get_access_token() 
        return token
    
    def get_resource_header():
        access_token = get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
    
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=get_access_token())
    }
    

    db_location = "sqlite:///my_played_tracks.sqlite"
    

    
    tdy_unix_timestamp = int(tdy.timestamp()) * 1000
    
    response = requests.get("https://api.spotify.com/v1/me/player/recently-played?before={time}".format(time=tdy_unix_timestamp), headers=headers)
    
    data = response.json()

    
    song_names = []
    artist_names =[]
    played_at = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name" : song_names,
        "artist_name" : artist_names,
        "played_at" : played_at,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name","played_at", "timestamp"])


    print(song_df)

    #check data 
    if check_valid_data(song_df):
        print("Data validated")

    #Load

    engine = sqlalchemy.create_engine(db_location)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    Cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    Cursor.execute(sql_query)

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists")

    conn.close()
    print("Close database connection")

run_spotify_etl()
