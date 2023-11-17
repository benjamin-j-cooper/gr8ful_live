import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

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

def find_band_website(band_name):
    search_url = f'https://www.google.com/search?q={band_name} official website'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        official_website = soup.find('cite').text
        return official_website
    except Exception as e:
        print(f"Error finding website for {band_name}: {e}")
        return None

def extract_upcoming_shows(website):
    try:
        response = requests.get(website)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Add your logic here to extract upcoming shows based on the structure of the band's website
        upcoming_shows = soup.find_all('div', class_='upcoming-show')
        return upcoming_shows
    except Exception as e:
        print(f"Error extracting upcoming shows: {e}")
        return None

def main():
    artists = get_followed_artists()
    # Print the followed artists
    print("Followed Artists:")
    for artist in artists:
        print(f"Finding website for {artist['name']}...")
        band_website = find_band_website(artist['name'])

        if band_website:
            print(f"Found website: {band_website}")
            upcoming_shows = extract_upcoming_shows(band_website)

            if upcoming_shows:
                print(f"Upcoming Shows for {artist['name']}:")
                for show in upcoming_shows:
                    print(show.text)
            else:
                print(f"No upcoming shows found for {artist['name']}")
        else:
            print(f"No official website found for {artist['name']}")
        
        print('\n' + '-' * 50 + '\n')
        

if __name__ == "__main__":
  main()