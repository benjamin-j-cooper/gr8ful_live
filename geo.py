from geopy.geocoders import Nominatim

#hardcode lat long for Duluth

def get_coordinates(location):
    geolocator = Nominatim(user_agent="your_app_name")  # Replace 'your_app_name' with a unique identifier
    try:
        location_info = geolocator.geocode(location)
        if location_info:
            return location_info.latitude, location_info.longitude
    except Exception as e:
        print(f"Error getting coordinates for {location}: {e}")
        return None
    
def calculate_distance(coord1, coord2):
    # This is a simple example, you may want to use a more accurate distance calculation method
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5

if __name__ == '__main__':
    city_name = input("Enter the city: ")

    # Get the coordinates of the specified city
    city_coordinates = get_coordinates(city_name)

    if not city_coordinates:
        print("Could not get coordinates for the specified city.")
    else:
        bands = ['band1', 'band2', 'band3']  # Add the list of bands here

        for band in bands:
            print(f"Finding website for {band}...")
            band_website = find_band_website(band)

            if band_website:
                print(f"Found website: {band_website}")
                upcoming_shows = extract_upcoming_shows(band_website, city_coordinates)

                if upcoming_shows:
                    print(f"Upcoming Shows for {band} within 200 miles of {city_name}:")
                    for show in upcoming_shows:
                        print(show)
                else:
                    print(f"No upcoming shows found for {band} within 200 miles of {city_name}")
            else:
                print(f"No official website found for {band}")

            print('\n' + '-' * 50 + '\n')