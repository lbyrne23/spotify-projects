import config
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
import pandas as pd
import sys
from tqdm import tqdm
import bs4
from bs4 import BeautifulSoup
import requests

#where to search for songs
market = [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", 
      "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", 
      "ID", "IE", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", 
      "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "SE", "SG", "SK", "SV", "TH", "TR", "TW", 
      "US", "UY", "VN" ]

# insert credentials here
CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET
username = config.username
scope = 'user-top-read user-library-read playlist-modify-public playlist-modify-private playlist-read-private'
redirect_uri = 'http://mysite.com/callback/'

token = util.prompt_for_user_token(username=username,scope=scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)

page = requests.get("http://everynoise.com/thesoundofeverything.html")
soup = BeautifulSoup(page.content, 'html.parser')
genre_playlists = {}
for song in soup.find_all('a', onclick="stopit()")[1:]:
    genre_playlists[song.get_text().lower()] = song['href']
	
def timeframe():
    ask_s = input("Choose a timeframe:\n1: Last 4 Weeks\n2: Last 6 Months\n3: All Time\n")
    ask = int(ask_s)
    if ask == 1:
        frame = "short_term"
    elif ask == 2:
        frame = "medium_term"
    elif ask == 3:
        frame = "long_term"
    else:
        timeframe()
        
    return frame

def most_popular_genre(frame, sp):
    top_songs = sp.current_user_top_tracks(limit=20, offset=0, time_range=frame)
    artists = [song['artists'][0]['uri'] for song in top_songs['items']]
    all_genres = [sp.artist(artist)['genres'] for artist in artists]
    flat_genres = [genre for sublist in all_genres for genre in sublist]
    top_genre = pd.Series(flat_genres).value_counts().index[0]
    print("\nTop Genre:", top_genre.title(), "\nSee Playlist:", genre_playlists[top_genre])
    popular_artists(genre_playlists[top_genre], sp)
    
def favorite_song_genre(frame, sp):
    top_songs = sp.current_user_top_tracks(limit=20, offset=0, time_range=frame)
    favorite_song_genre = sp.artist(top_songs['items'][0]['artists'][0]['uri'])['genres'][0]
    print("\nFavorite Song Genre:", favorite_song_genre.title(), "\nSee Playlist:", genre_playlists[favorite_song_genre])
    popular_artists(genre_playlists[favorite_song_genre], sp)
    
def popular_artists(uri, sp):
    print("\nSome Sample Artists from this Genre:")
    playlist = sp.playlist(uri)
    artists = [item['track']['artists'][0]['name'] for item in playlist['tracks']['items']]
    for name in list(pd.Series(artists).value_counts().index[:5]):
        print(name)
		
frame = timeframe()
most_popular_genre(frame, sp)
favorite_song_genre(frame, sp)