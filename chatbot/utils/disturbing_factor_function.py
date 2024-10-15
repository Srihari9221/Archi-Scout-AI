import os
import requests
from fuzzywuzzy import fuzz
import spacy
from math import radians, sin, cos, sqrt, atan2
import joblib
import folium
import os
from django.conf import settings

# Load spaCy's English model for word embeddings
nlp = spacy.load('en_core_web_md')
model_path = os.path.join(settings.BASE_DIR, 'chatbot', 'models', 'logistic_regression_model.pkl')
le_path = os.path.join(settings.BASE_DIR, 'chatbot', 'models', 'label_encoder.pkl')
# Load the trained model and label encoder
model = joblib.load(model_path)
le = joblib.load(le_path)

def disturbing_factors(lat, lon):
    """
    Given the latitude and longitude, this function finds nearby places,
    checks for disturbing factors, and generates a map of disturbing places.
    
    Args:
    lat (float): Latitude of the user's location.
    lon (float): Longitude of the user's location.
    
    Returns:
    A formatted string of places with disturbing factors.
    """
    

    api_key = 'AIzaSyDJywdV0_cC5BOPajS994D5SNLDXwxKWDo'  
    radius = 5000  
    place_type = 'point_of_interest'
    disturbing_keywords = ["tasmac", "bar", "pub", "club", "wines", "factory", "industry", "manufacture", "pvt ltd"]
    
    user_location = (lat, lon)

    # Function to fetch nearby places using Google Places API
    def get_nearby_places(api_key, location, radius, place_type):
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'key': api_key,
            'location': f"{location[0]},{location[1]}",
            'radius': radius,
            'type': place_type
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {}
        except Exception as err:
            return {}

    # Function to find specific disturbing keywords using fuzzy matching and semantic similarity
    def find_disturbing_factors(place_name, keywords, fuzz_threshold=60, similarity_threshold=0.60):
        place_doc = nlp(place_name.lower())
        for keyword in keywords:
            if fuzz.token_set_ratio(keyword.lower(), place_name.lower()) >= fuzz_threshold:
                return keyword
            keyword_doc = nlp(keyword.lower())
            similarity = place_doc.similarity(keyword_doc)
            if similarity >= similarity_threshold:
                return keyword
        return None

    # Function to calculate distance using the Haversine formula
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371.0  # Radius of Earth in kilometers
        lat1, lon1, lat2, lon2 = radians(lat1), radians(lon1), radians(lat2), radians(lon2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c * 1000  # Convert km to meters

    # Function to analyze places for disturbing keywords and calculate distances
    def analyze_places(places, disturbing_keywords, user_location):
        results = []
        for place in places.get('results', []):
            place_name = place.get('name', '')
            place_location = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
            found_keyword = find_disturbing_factors(place_name, disturbing_keywords)

            if found_keyword:
                distance = calculate_distance(user_location[0], user_location[1], place_location[0], place_location[1])
                results.append({
                    'Name': place_name,
                    'Disturbing Factor': found_keyword,
                    'Distance': round(distance, 2),
                    'Coordinates': place_location
                })
        return results

    # Function to create and save a map
    def create_map(disturbing_places, user_location):
        map_center = disturbing_places[0]['Coordinates'] if disturbing_places else user_location
        map = folium.Map(location=map_center, zoom_start=13)

        for place in disturbing_places:
            folium.Marker(
                location=place['Coordinates'],
                popup=f"{place['Name']}<br>Disturbing Factor: {place['Disturbing Factor']}<br>Distance: {place['Distance']} m",
                icon=folium.Icon(color='red')
            ).add_to(map)

        folium.Marker(
            location=user_location,
            popup="Your Location",
            icon=folium.Icon(color='green')
        ).add_to(map)

        # Save the map in the specified directory
        save_dir = os.path.join('chatbot', 'templates')  
        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, 'disturbing_places_map.html')
        map.save(save_path)

    # Fetch nearby places
    places = get_nearby_places(api_key, user_location, radius, place_type)

    if places:
        disturbing_places = analyze_places(places, disturbing_keywords, user_location)

        if disturbing_places:
            # Encode 'Disturbing Factor' and make predictions
            for place in disturbing_places:
                place['Disturbing Factor Encoded'] = le.transform([place['Disturbing Factor']])[0]
                place['Prediction'] = model.predict([[place['Disturbing Factor Encoded'], place['Distance']]])[0]

            # Filter the places marked as disturbing
            disturbing_results = [p for p in disturbing_places if p['Prediction'] == 'Disturbing']

            # Create a formatted string summary
            summary = ""
            for place in disturbing_results:
                summary += (
                    f"Name: {place['Name']}\n"
                    f"Disturbing Factor: {place['Disturbing Factor']}\n"
                    f"Distance: {place['Distance']} meters\n"
                    f"Coordinates: {place['Coordinates']}\n\n"
                )

            # Create and save the map of disturbing places
            create_map(disturbing_results, user_location)

            return summary.strip()  
        else:
            return "No disturbing places found."
    else:
        return "Failed to retrieve places data."

