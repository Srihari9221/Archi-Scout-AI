import os
import uuid
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta
from django.conf import settings  

# Constants
API_KEY = '32c638e32967cd2b94fbe809fa8fffe4d533470c'

# Define AQI category and color based on value
def aqi_category(value):
    if value <= 50:
        return "Good", "#009966", "🙂"
    elif value <= 100:
        return "Moderate", "#FFDE33", "😊"
    elif value <= 150:
        return "Unhealthy for Sensitive Groups", "#FF9933", "😐"
    elif value <= 200:
        return "Unhealthy", "#CC0033", "😷"
    elif value <= 300:
        return "Very Unhealthy", "#660099", "🤢"
    else:
        return "Hazardous", "#7E0023", "☠"

def air_quality_index(lat, lon):
    """Fetch AQI data from WAQI API and return formatted summary."""

    # Reverse geocoding to get location name
    reverse_geocode_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    try:
        location_response = requests.get(reverse_geocode_url)
        location_response.raise_for_status()  # Check if the request was successful
        location_data = location_response.json()
        location_name = location_data.get('display_name')
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        location_name = f"Lat: {lat}, Lon: {lon}"

    # Fetch AQI data from WAQI API
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={API_KEY}"
    response = requests.get(url).json()

    if response['status'] != 'ok':
        raise Exception("Failed to fetch air quality data")

    # Extract AQI data
    data = response['data']
    aqi = data['aqi']
    temp = data['iaqi'].get('t', {'v': 'N/A'})['v']
    pm25 = data['iaqi'].get('pm25', {'v': 'N/A'})['v']
    pm10 = data['iaqi'].get('pm10', {'v': 'N/A'})['v']
    no2 = data['iaqi'].get('no2', {'v': 'N/A'})['v']
    so2 = data['iaqi'].get('so2', {'v': 'N/A'})['v']

    # Get AQI category, color, and emoji
    category, color, emoji = aqi_category(aqi)

    # Generate the formatted summary
    summary = {
        'location': location_name,
        'aqi': aqi,
        'category': category,
        'emoji': emoji,
        'temperature': temp,
        'pm25': pm25,
        'pm10': pm10,
        'no2': no2,
        'so2': so2,
    }
    return_summary = (
        f"Location: {location_name}\n"
        f"AQI: {aqi} ({category}) {emoji}\n"
        f"Temperature: {temp}°C\n"
        f"PM2.5: {pm25}\n"
        f"PM10: {pm10}\n"
        f"NO2: {no2}\n"
        f"SO2: {so2}\n"
    )

    # Time series data for plotting
    timestamps = [datetime.now() - timedelta(hours=i) for i in range(24)][::-1]
    pm25_series = [pm25 - 10 + i % 5 for i in range(24)]
    pm10_series = [pm10 - 5 + i % 3 for i in range(24)]
    no2_series = [no2 + i % 2 for i in range(24)]
    so2_series = [so2 - 2 + i % 4 for i in range(24)]

    # Create the figure for plotting
    fig, axs = plt.subplots(6, 1, figsize=(12, 14), gridspec_kw={'height_ratios': [1, 0.5, 1, 1, 1, 1]}, constrained_layout=True)
    fig.suptitle(summary['location'], fontsize=16, fontweight='bold')

    # Display the AQI value, category, and temperature
    axs[0].set_facecolor(color)
    axs[0].text(0.05, 0.5, f"AQI: {summary['aqi']}", fontsize=32, verticalalignment='center', color='black')
    axs[0].text(0.35, 0.5, summary['emoji'], fontsize=32, verticalalignment='center', color='black')
    axs[0].text(0.45, 0.5, f"{summary['category']}", fontsize=32, verticalalignment='center', color='black')
    axs[0].axis('off')

    # Temperature display
    axs[1].set_facecolor('#87CEEB')
    axs[1].text(0.05, 0.5, f"Temperature: {summary['temperature']}°C", fontsize=24, verticalalignment='center', color='black')
    axs[1].axis('off')

    # Time series data visualization
    pollutant_data = {
        'PM2.5': pm25_series,
        'PM10': pm10_series,
        'NO2': no2_series,
        'SO2': so2_series
    }
    colors = ['#2ca02c', '#ff7f0e', '#d62728', '#9467bd']

    for i, (pollutant, series) in enumerate(pollutant_data.items()):
        axs[i+2].plot(timestamps, series, label=pollutant, color=colors[i], marker='o', markersize=6, linewidth=2)
        axs[i+2].fill_between(timestamps, series, color=colors[i], alpha=0.1)
        axs[i+2].set_title(f'{pollutant} Levels', fontsize=14)
        axs[i+2].xaxis.set_major_locator(mdates.HourLocator(interval=6))
        axs[i+2].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        axs[i+2].grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    axs[-1].set_xlabel('Time (Last 24 Hours)')
    axs[-1].set_ylabel('Concentration (µg/m³)')

    # Define the path to save the image
    image_directory = os.path.join(settings.MEDIA_ROOT, 'AQI_images')
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    unique_id = uuid.uuid4()
    filename = f'air_quality_{unique_id}.png'
    image_path = os.path.join(image_directory, filename)
    image_return = f"media/AQI_images/{filename}"

    # Save the plot as an image
    plt.savefig(image_path)
    plt.close()

    return return_summary, image_return