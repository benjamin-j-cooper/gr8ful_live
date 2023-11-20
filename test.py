import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import spacy
from datetime import datetime

def remove_extra_spaces(input_string):
    # Use regex to replace multiple consecutive spaces with a single space
    return re.sub(r'\s+', ' ', input_string)

def print_future_date_location(show_date_text,show_location_text):
    if show_date_text:
        try:
            # Convert the date string to a datetime object
            date_object = datetime.strptime(show_date_text, "%b %d %Y").date()

            # Get the current date
            current_date = datetime.now().date()

            # Check if the date is in the future
            if date_object > current_date:
                print(f"Date: {show_date_text}, Location: {show_location_text}")
        except Exception as e:
            return None
        
# Get the current date
current_date = datetime.now().date()

print("Current Date:", current_date)


# url = 'https://phish.com/tours/'
url = 'https://www.stringcheeseincident.com/tour/'
# url ='https://www.umphreys.com/tour/'
req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(req).read()
page_soup = BeautifulSoup(webpage, "html.parser")
title = page_soup.find("title")
print(title)

# containers = page_soup.findAll("p","promo")
# for container in containers:
#     print(container)

# upcoming_shows = page_soup.findAll("div", class_="purchase-entry clearfix p2")
# for show in upcoming_shows:
#     date = show.find("div",class_="date-block")
#     location = show.find("div",class_="purchase-show-location")
#     print(date.text.strip())
#     print(location.text.strip())

# Define regular expressions for class names and keywords
container_type_pattern = re.compile(r'\b(article|div|section)\b', re.IGNORECASE)
container_class_pattern = re.compile(r'\b(tour|show|shows|event)\b', re.IGNORECASE)
row_class_pattern = re.compile(r'\b(event|info|item|box)\b', re.IGNORECASE)
div_keyword_pattern = re.compile(r'\b(date|when|location|where|venue|city)\b', re.IGNORECASE)

# Extract containers with class names containing "tour," "show," or "event"
containers = page_soup.find_all(container_type_pattern, class_=container_class_pattern)
for container in containers:
    rows = container.find_all('div', class_=row_class_pattern)

    # for container in containers:
    #     date_divs = container.find_all('div', class_=div_keyword_pattern)
    #     date_text = [div.get_text() for div in date_divs]
    #     print(f"Container Class: {container['class']}")
    #     print(f"Date Text: {date_text}")
    #     print()

    # Iterate through containers sequentially and print date and location
    for row in rows:
        show_dates = row.find_all('div', class_=re.compile(r'\b(date|when)\b', re.IGNORECASE))
        show_locations = row.find_all('div', class_=re.compile(r'\b(location|where|venue|city)\b', re.IGNORECASE))

        # Iterate through each combination of date and location
        for show_date, show_location in zip(show_dates, show_locations):
            show_date_text = remove_extra_spaces(show_date.get_text().strip())
            show_location_text = remove_extra_spaces(show_location.get_text().strip())

            print_future_date_location(show_date_text,show_location_text)




# upcoming_shows = page_soup.findAll(re.compile("article|div|section"), class_= re.compile('tour|show|shows|event'))
# # print(upcoming_shows)

# def extract_show_info(text_content):
#     # Load spaCy English language model
#     nlp = spacy.load("en_core_web_sm")

#     # Process the text using spaCy
#     doc = nlp(text_content)

#     # Extract entities (date and location) using spaCy's named entity recognition
#     entities = []
#     for ent in doc.ents:
#         entities.append((ent.text, ent.label_))

#     return entities

# # Concatenate text content from all div elements in the ResultSet
# text_content = ' '.join([show.get_text() for show in upcoming_shows])

# # Extract show information
# show_info_entities = extract_show_info(text_content)

# # Print the extracted show information entities
# for entity, label in show_info_entities:
#     print(f"Entity: {entity}, Label: {label}")













# def extract_dates(text):
#     # Define a regular expression pattern to capture various date formats
#     # pattern = re.compile(r"\b(?:[A-Za-z]+(?:\s+|,|\s+-\s+|\s*\d{1,2},?\s*)\d{1,2}(?:,\s*\d{4})?|\d{1,2}\s+[A-Za-z]+\s+\d{4})\b", re.IGNORECASE)
#     pattern = re.compile(r"\d{1,2}.(\d{1,2}|[A-Z\s\S]+).\d{1,5}", re.IGNORECASE)

#     # Extract matches from the text
#     matches = pattern.findall(text)

#     return matches

# def extract_show_info(text_content):
#     # Load spaCy English language model
#     nlp = spacy.load("en_core_web_sm")

#     # Process the text using spaCy
#     doc = nlp(text_content)

#     # Extract entities (date and location) using spaCy's named entity recognition
#     entities = []
#     for ent in doc.ents:
#         entities.append((ent.text, ent.label_))

#     return entities

# def extract_dates_and_venues(text):
#     # Load spaCy English language model
#     nlp = spacy.load("en_core_web_sm")

#     # Define a regular expression pattern to capture date and venue
#     pattern = re.compile(r"\b(?:[A-Za-z]+(?:\s+|,|\s+-\s+|\s*\d{1,2},?\s*)\d{1,2}(?:,\s*\d{4})?|\d{1,2}\s+[A-Za-z]+\s+\d{4})\b(?:\s*(.*?)(?:\s*\n\s*\w.*?\n\s*\w.*?|$))?", re.IGNORECASE | re.DOTALL)

#     # Extract matches from the text
#     matches = pattern.findall(text)
#     print(matches)
#     # Process the matches and filter by spaCy entity recognition
#     result = []
#     for match in matches:
#         date = match[0]
#         venue_candidate = match[1].strip() if match[1] else None
#         print("date: ",date," location: ",venue_candidate)

#         # Check if the venue_candidate is recognized as ORG or GPE by spaCy
#         if venue_candidate:
#             doc = nlp(venue_candidate)
#             entities = [ent.label_ for ent in doc.ents]
#             if 'ORG' in entities or 'GPE' in entities or 'PERSON' in entities:
#                 result.append((date.strip(), venue_candidate))

#     return result

# webpage = urlopen(req).read()
# page_soup = BeautifulSoup(webpage, "html.parser")
# # Use findAll to get a ResultSet of div elements with the specified class
# upcoming_shows = page_soup.findAll("div", class_=re.compile('container'))

# # Concatenate text content from all div elements in the ResultSet
# text_content = ' '.join([show.get_text() for show in upcoming_shows])

# # print(text_content)




# # # Extract dates using the defined function
# # date_matches = extract_dates(text_content)

# # # Print the extracted dates
# # for date_match in date_matches:
# #     print(date_match)




# # # Extract show information
# # show_info_entities = extract_show_info(text_content)

# # # Print the extracted show information entities
# # for entity, label in show_info_entities:
# #     print(f"Entity: {entity}, Label: {label}")




# # Extract dates and venues using the defined function
# date_venue_matches = extract_dates_and_venues(text_content)

# # Print the extracted dates and venues
# for date, venue in date_venue_matches:
#     print(f"Date: {date}")
#     print(f"Venue: {venue}")
#     print()

