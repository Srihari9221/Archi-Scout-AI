import requests
import folium
import numpy as np
import random
import geopy.distance
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from django.conf import settings

def get_historical_wind_data(lat, lon, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': start_date,
        'end_date': end_date,
        'hourly': 'windspeed_10m,winddirection_10m',
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['hourly']['windspeed_10m'], data['hourly']['winddirection_10m']
    else:
        print(f"Error: {response.status_code}")
        return None, None

def calculate_mean_direction(directions):
    directions_rad = np.radians(directions)
    mean_sin = np.mean(np.sin(directions_rad))
    mean_cos = np.mean(np.cos(directions_rad))
    mean_direction_rad = np.arctan2(mean_sin, mean_cos)
    mean_direction_deg = np.degrees(mean_direction_rad)
    if mean_direction_deg < 0:
        mean_direction_deg += 360
    return mean_direction_deg

def calculate_average_speed(speeds):
    return np.mean(speeds)

def generate_coordinates(lat, lon, radius_m, num_points):
    coordinates = []
    for _ in range(num_points):
        distance = random.uniform(0, radius_m)
        angle = random.uniform(0, 360)
        destination = geopy.distance.distance(meters=distance).destination((lat, lon), angle)
        coordinates.append((destination.latitude, destination.longitude))
    return coordinates

def get_historical_wind_data_for_coords(coords, start_date, end_date):
    all_data = {}
    cache = {}

    def cached_request(lat, lon):
        key = (round(lat, 2), round(lon, 2))  
        if key not in cache:
            cache[key] = get_historical_wind_data(lat, lon, start_date, end_date)
        return cache[key]
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_coord = {executor.submit(cached_request, lat, lon): (lat, lon) for lat, lon in coords}
        for future in as_completed(future_to_coord):
            lat_lon = future_to_coord[future]
            try:
                data = future.result()
                if data[0] and data[1]:
                    all_data[lat_lon] = data
            except Exception as e:
                print(f"Error fetching data for {lat_lon}: {e}")

    return all_data

def add_markers_to_map(map_obj, coords, wind_data, specified_lat, specified_lon,start_date,end_date):
    avg_wind_dir_spd = None  

    # Print the wind data for the specified coordinates if available
    if (specified_lat, specified_lon) in wind_data:
        windspeeds, winddirections = wind_data[(specified_lat, specified_lon)]
        if windspeeds and winddirections:
            mean_direction = calculate_mean_direction(winddirections)
            average_speed = calculate_average_speed(windspeeds)
            avg_wind_dir_spd = f" Start Date : {start_date} \n Wind Date : {end_date} \n Average Wind Speed: {average_speed:.2f} m/s \n Mean Wind Direction: {mean_direction:.2f}°\n"
    else:
        print("No data available for the specified latitude and longitude.")

    # Add all markers to the map
    for (lat, lon), (windspeeds, winddirections) in wind_data.items():
        if winddirections and windspeeds:
            mean_direction = calculate_mean_direction(winddirections)
            average_speed = calculate_average_speed(windspeeds)

            folium.Marker(
                location=[lat, lon],
                popup=f"Average Wind Speed: {average_speed:.2f} m/s<br>Mean Wind Direction: {mean_direction:.2f}°",
                icon=folium.DivIcon(
                    html=f"""
                    <div style="transform: rotate({mean_direction}deg);">
                        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L12 19" stroke="red" stroke-width="2"/>
                            <path d="M7 7L12 2L17 7" stroke="red" stroke-width="2"/>
                        </svg>
                    </div>
                    """
                )
            ).add_to(map_obj)
    
    return avg_wind_dir_spd

def generate_wind_map(lat, lon, date_dict, radius_m=1000, num_points=50):
    start_date = date_dict.get('start_date')
    end_date = date_dict.get('end_date')

    if not start_date or not end_date:
        print("Error: Start date and end date must be provided in 'date_dict'")
        return None
    
    # Generate coordinates
    coords = generate_coordinates(lat, lon, radius_m, num_points)
    
    # Include the specified lat/lon in the list to ensure it is always fetched
    coords.append((lat, lon))

    # Get historical wind data for each coordinate 
    wind_data = get_historical_wind_data_for_coords(coords, start_date, end_date)

    # Create a folium map 
    wind_map = folium.Map(location=[lat, lon], zoom_start=16)

    # Add markers to the map and get the wind data for the specified latitude and longitude
    avg_wind_dir_spd = add_markers_to_map(wind_map, coords, wind_data, lat, lon,start_date,end_date)

    
    save_dir = os.path.join(settings.BASE_DIR,'chatbot', 'templates')  
    os.makedirs(save_dir, exist_ok=True)
    
    # Save the map as an HTML file
    save_path = os.path.join(save_dir, 'wind_map.html')
    wind_map.save(save_path)

    return avg_wind_dir_spd, save_path  # Return the average wind speed and direction
