
# coding: utf-8

# In[ ]:


### This notebook depends on you having a spotify developer account
### I started with this site https://developer.spotify.com/documentation/general/guides/authorization-guide/ 
### and then lots of stackoverflow posts to get it working

import shutil
import os
import random
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
import pandas as pd
# ^ some of these are unecessary and are leftover from other uses

#where to search for songs
market = [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", 
      "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", 
      "ID", "IE", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", 
      "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "SE", "SG", "SK", "SV", "TH", "TR", "TW", 
      "US", "UY", "VN" ]

CLIENT_ID = "{type your client ID here}"
CLIENT_SECRET = "{type your client secret ID here}"
username = 'your spotify user ID'
scope = 'user-top-read user-library-read playlist-modify-public playlist-modify-private playlist-read-private '
redirect_uri = '{type your redirect uri here}'

token = util.prompt_for_user_token(username=username,scope=scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)


# In[ ]:


### Top Albums according to Saved/Liked Songs

master_uri = []
for i in range(0, 3000, 50): #API allows you to get 50 songs at a time, so retrieve 50 multiple times
    try:
        results = sp.current_user_saved_tracks(50,i)
        for item in results['items']:
            master_uri.append(item['track']['album']['uri']) #append the album uri of track to the master list
    except:
        continue

# convert list of albums to a series and get top 5 most common appearances, print urls of top albums
s = pd.Series(master_uri)
s.groupby(s).size().sort_values(ascending=False)[:5]


# In[ ]:


### Top albums according to songs in playlists (maximum 50 playlists analysed)

albums = []
playlists = sp.user_playlists(username, limit=50, offset=0) #retrieve playlists

for item in playlists['items']:
    tracks = sp.user_playlist_tracks(username, item['uri']) #get track uri
    for item in tracks['items']:
        try:
            albums.append(sp.track(item['track']['uri'])['album']['uri']) #get album uri of that track and record
        except:
            continue
            
#convert list of albums to series, find 5 most common and print results
al = pd.Series(albums)
df = pd.DataFrame(al.groupby(al).size().sort_values(ascending=False)[:5])
for item in list(df.index):
    print(sp.album(item)['name'], '-', sp.album(item)['artists'][0]['name'])

