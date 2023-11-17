import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# import credentials
with open("./credentials.json", "r") as f:
    creds = json.load(f)


def get_followed_artists():
    # Set up credentials
    client_id = creds['spotify_api']['CLIENT_ID']
    client_secret = creds['spotify_api']['CLIENT_SECRET']
    redirect_uri = creds['spotify_api']['REDIRECT']
    # username = creds['spotify_api']['USERNAME']

    # Set up the Spotify API authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope='user-follow-read'))

    # Get the user's followed artists
    followed_artists = sp.current_user_followed_artists()
    artists = followed_artists['artists']['items']

    return artists

def main():
    artists = get_followed_artists()
    # Print the followed artists
    print("Followed Artists:")
    for artist in artists:
        print(artist['name'])

if __name__ == "__main__":
  main()