from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

#spotify authorization
SPOTIFY_CLIENT_ID = "7e2ffd6bded9468da2dd022bb6c01c65"
SPOTIFY_CLIENT_SECRET = "e26027d5b340431e8d3155e5fe2f64b5"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="http://example.com",
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    show_dialog=True,
    cache_path="token.txt",
    username = "Antonio Margeretti"
))
user_id = sp.current_user()["id"]

date = input("What day would you like to travel back to? Format should be: YYYY-MM-DD:")
billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"

#scrape top 100 from billboard
billboard_response = requests.get(billboard_url)
billboard_soup = BeautifulSoup(billboard_response.text, "html.parser")

songs_soup = billboard_soup.findAll(name="h3")
songs_list =[]
i=1

for song in songs_soup:
    songs_list.append(song.getText().strip())
    if i > 100:
        break
    i+=1

songs_list = [song for song in songs_list if song != 'Songwriter(s):']
songs_list = [song for song in songs_list if song != 'Producer(s):']
songs_list = [song for song in songs_list if song != 'Imprint/Promotion Label:']


print(songs_list)

#spotify api to create playlist
uri_list = []
user_id = sp.current_user()["id"]
for song in songs_list:
    result = sp.search(q=f"track:{song}", type='track')
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        print(f"{song} does not exist in Spotify.")
#print(uri_list)

playlist_name = f"Top_100_{date}"
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list)
#sp.playlist_add_items(playlist_id=,items=uri_list)