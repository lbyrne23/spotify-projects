import config
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2

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


def artist_genre(name, sp):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        if len(artist['genres']) > 0:
            print("\nGenres:")
            for item in artist['genres']:
                print(item)
        else:
            print("\nSpotify hasn't listed any genres for this artist :(")
    else:
        print("No Artist Found")
    

artist_name = input("Type Artist Name: ")
artist_genre(artist_name.lower(), sp)

