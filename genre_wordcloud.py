import config
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
%matplotlib inline


#where to search for songs
market = [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", 
      "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", 
      "ID", "IE", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", 
      "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "SE", "SG", "SK", "SV", "TH", "TR", "TW", 
      "US", "UY", "VN" ]

# insert credentials here
CLIENT_ID = "type your client ID here"
CLIENT_SECRET = "type your client secret ID here"
username = "your spotify user ID"
scope = 'user-top-read user-library-read playlist-modify-public playlist-modify-private playlist-read-private'
redirect_uri = "type your redirect uri here"

token = util.prompt_for_user_token(username=username,scope=scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)

# replace the xxxx here with your spotify playlist URI (Go to playlist > share > copy Spotify URI)
tracks = sp.playlist_tracks("xxx", fields=None, limit=100)['items']

genres = []

for item in tracks:
    artist_genres = sp.artist(item['track']['artists'][0]['id'])['genres']
    for genre in artist_genres:
        genres.append(genre)

wordcloud = WordCloud(font_path='arial', width=1600, height=800).generate_from_frequencies(Counter(genres))
plt.figure(figsize=(20,10), facecolor='k')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()