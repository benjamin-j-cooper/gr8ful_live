import json
import re
from datetime import datetime
from dateutil import parser
from datetime import timedelta
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    # #Get all urls associated with base URL, use that to choose tour page?
    # urls = []
    # for link in soup.find_all('a'):
    #     print(link.get('href'))
    try:
        # response = Request(url, headers=headers)
        # webpage = urlopen(response).read()
        # soup = BeautifulSoup(webpage, 'html.parser')
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        official_website = soup.find('cite').text
        return official_website
    except Exception as e:
        print(f"Error finding website for {band_name}: {e}")
        return None

def check_site_exists(website):
    try:
        tourwebsite = website + "/tour/"
        response = requests.get(tourwebsite)
        return tourwebsite
    except Exception as e:
        pass
    try:
        tourwebsite = website + "/tours/"
        response = requests.get(tourwebsite)
        return tourwebsite
    except Exception as e:
        print(f"error, no website found for {website} : {e}")
        return None

def get_web_content(url):
    try:
        #connect to site and scrape data
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup = BeautifulSoup(webpage, "html.parser")
        # title = page_soup.find("title")
        return page_soup
    except Exception as e:
        print(f"Unable to access {url}")
        return None

def selenium_scraper(url):
    try:
        # create driver instance
        driver = webdriver.Firefox()
        # Open the website
        driver.get(url)

        # Wait for the main page container to load completely (adjust the timeout as needed)
        main_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Get the HTML content of the main page container
        main_container_html = main_container.get_attribute("innerHTML")

        # Use BeautifulSoup to parse the HTML content
        page_soup = BeautifulSoup(main_container_html, 'html.parser')

        # print(f"successfully scraped html for {page_title}" )
    finally:
        # Close the browser window
        driver.quit()
    return page_soup

def remove_extra_spaces(input_string):
    # Use regex to replace multiple consecutive spaces with a single space
    return re.sub(r'\s+', ' ', input_string)

def print_future_date_location(show_date_text,show_location_text):
    if show_date_text:
        try:
            # Convert the date string to a datetime object
            # date_object = datetime.strptime(show_date_text, "%b %d %Y").date()
            # Get the current date
            current_date = datetime.now().date()
            # Check if the date is in the future
            if show_date_text > current_date:
                # print(f"Date: {show_date_text}, Location: {show_location_text}")
                return show_date_text, show_location_text
            else:
                return None, None
        except Exception as e:
            print(f"Error checking if {show_date_text} date was in future")
            return None
        
def normalize_date_parts(date_string):
    try:
        # Parse the date string using dateutil.parser
        parsed_date = parser.parse(date_string).date()

        # Extract normalized date parts
        # year = parsed_date.year
        # month = parsed_date.strftime("%b")  # abbreviated month name
        # day = parsed_date.day

        # Return the normalized date parts
        return parsed_date
    except:
        pass
    try:
        # Define the regular expression pattern
        pattern = re.compile(r'([A-Za-z]{3})(\d{2})(\d{4})')

        # Check if the pattern is found in the string
        if pattern.search(date_string):
            # Use re.sub to apply the pattern and add dashes
            result_string = re.sub(pattern, r'\1-\2-\3', date_string)
            parsed_date = parser.parse(result_string).date()
            return parsed_date

    except ValueError as e:
        print("error parsing date string ", date_string)
        return None
    
def expand_date_range(date_range):
    try:
        # Define the regular expression pattern to match date range components
        pattern = re.compile(r'([A-Za-z]{3})(\d{2})-(\d{2})(\d{4})')

        # Match the pattern in the input string
        match = pattern.match(date_range)

        if match:
            # Extract components from the match
            start_month, start_day, end_day, year = match.groups()

            # Parse start and end dates using datetime
            start_date = datetime.strptime(f"{start_month} {start_day} {year}", "%b %d %Y")
            end_date = datetime.strptime(f"{start_month} {end_day} {year}", "%b %d %Y")

            # Generate a list of sequential dates between start and end
            date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

            # Format the dates as strings
            formatted_dates = [date.strftime("%b %d %Y") for date in date_list]

            return formatted_dates
        else:
            # Split the input date range
            date_parts = date_range.split(" - ")

            # Parse start and end dates
            start_date = parser.parse(date_parts[0])
            end_date = parser.parse(date_parts[-1])

            # Generate a list of sequential dates between start and end
            date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

            # Format the dates as strings
            formatted_dates = [date.strftime("%b %d, %Y") for date in date_list]

            return formatted_dates
    except ValueError as e:
        print(f"Error parsing date range: {e}")
        return None       

def main():

    artists = get_followed_artists()

    for artist in artists:
        print(f"Finding website for {artist['name']}...")
        band_website = find_band_website(artist['name'])

        if band_website:
            url = check_site_exists(band_website)

            #Make empty dictionary for results:
            results_dict = {}

            page_soup = get_web_content(url) 

            # Define regular expressions for class names and keywords
            container_type_pattern = re.compile(r'\b(article|div|section)\b', re.IGNORECASE)
            container_class_pattern = re.compile(r'\b(upcoming|tour|tours|show|shows|event|events)\b', re.IGNORECASE)
            row_type_pattern = re.compile(r'\b(span|div)\b', re.IGNORECASE)
            row_class_pattern = re.compile(r'\b(event|info|item|box)\b', re.IGNORECASE)
            # div_keyword_pattern = re.compile(r'\b(date|when|location|where|venue|city)\b', re.IGNORECASE)

            # Extract containers with class names containing "tour," "show," or "event"
            containers = page_soup.find_all(container_type_pattern, class_=container_class_pattern)

            if not containers:
                page_soup = selenium_scraper(url)
                containers = page_soup.find_all(container_type_pattern, class_=container_class_pattern)

            for container in containers:
                rows = container.find_all(row_type_pattern, class_=row_class_pattern)

                # for container in containers:
                #     date_divs = container.find_all('div', class_=div_keyword_pattern)
                #     date_text = [div.get_text() for div in date_divs]
                #     print(f"Container Class: {container['class']}")
                #     print(f"Date Text: {date_text}")
                #     print()

                # Iterate through containers sequentially and print date and location
                for row in rows:
                    show_dates = row.find_all(row_type_pattern, class_=re.compile(r'\b(date|when)\b', re.IGNORECASE))
                    show_locations = row.find_all('div', class_=re.compile(r'\b(location|where|venue|city)\b', re.IGNORECASE))

                    # Iterate through each combination of date and location
                    for show_date, show_location in zip(show_dates, show_locations):
                        show_date_text = remove_extra_spaces(show_date.get_text().strip())
                        normalized_date_parts = normalize_date_parts(show_date_text)
                        if not normalized_date_parts:
                            normalized_date_parts = expand_date_range(show_date_text)
                            show_location_text = remove_extra_spaces(show_location.get_text().strip())
                            for date in normalized_date_parts:
                                expanded_show_date = parser.parse(date).date()
                                result_date, result_location = print_future_date_location(expanded_show_date,show_location_text)
                                if result_date and (result_date not in results_dict):
                                    # Add the values to the results dictionary
                                    results_dict[result_date] = result_location
                        else:
                            show_location_text = remove_extra_spaces(show_location.get_text().strip())
                            # print(f'date: {normalized_date_parts}, location: {show_location_text}')
                            result_date, result_location = print_future_date_location(normalized_date_parts,show_location_text)
                            if result_date and (result_date not in results_dict):
                                # Add the values to the results dictionary
                                results_dict[result_date] = result_location

            if results_dict:
                print(f"Upcoming Shows for {artist['name']}:")
                for expanded_show_date, show_location_text in results_dict.items():
                    print(f"Show Date: {expanded_show_date}, Show Location: {show_location_text}")
            else:
                print(f"No upcoming shows found for {artist['name']}")
        else:
            print(f"No official website found for {artist['name']}")

if __name__ == "__main__":
  main()