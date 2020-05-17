import config
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
import pandas as pd
import sys
from tqdm import tqdm

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

ask = input("How many albums do you want listed?: ")
amount = int(ask)

def print_top_albums(songlist, amount):
    series = pd.Series(songlist)
    top = series.groupby(series).size().sort_values(ascending=False)[:amount]
    
    for item in list(top.index):
        print(sp.album(item)['name'], '-', sp.album(item)['artists'][0]['name'])
     
### Top albums according to Saved Songs
     
saved_song_albums = []

print("\nAnalyzing Saved Songs..")
for i in tqdm(range(0, 3000, 50)): #API allows you to get 50 songs at a time, so retrieve 50 multiple times
    try:
        results = sp.current_user_saved_tracks(50,i)
        for item in results['items']:
            saved_song_albums.append(item['track']['album']['uri']) #append the album uri of track to the master list
    except:
        continue

print("\nTop albums according to saved songs: \n")
print_top_albums(saved_song_albums, amount)


### Top albums according to songs in playlists (maximum 50 playlists analysed)

playlist_albums = []
playlists = sp.user_playlists(username) #retrieve playlists

print("\nAnalyzing Playlists..")
for item in tqdm(playlists['items']):
    if item['collaborative'] == False and item['owner']['id'] == username:
        tracks = sp.user_playlist_tracks(username, item['uri']) #get track uri
        for item in tracks['items']:
            try:
                playlist_albums.append(sp.track(item['track']['uri'])['album']['uri']) #get album uri of that track and record
            except:
                continue

print("\nTop albums according to playlists: \n")            
print_top_albums(playlist_albums, amount)



