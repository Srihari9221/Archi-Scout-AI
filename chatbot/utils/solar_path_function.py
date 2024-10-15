import pvlib # type: ignore
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import uuid
import os
from django.conf import settings


image_directory = os.path.join(settings.MEDIA_ROOT, 'solar_images')

if not os.path.exists(image_directory):
    os.makedirs(image_directory)

# Function to calculate and plot the solar path for a given date or range of dates and times
def plot_solar_path(start_datetime, end_datetime, latitude, longitude):
    
    location = pvlib.location.Location(latitude, longitude)

    # Generate a time range for the given date and time
    times = pd.date_range(start=start_datetime, end=end_datetime, freq='10min', tz=location.tz)
    
    # Calculate the solar positions for each time point
    solar_positions = location.get_solarposition(times)
    
    # Convert azimuth and zenith angles to radians for the polar plot
    azimuth_rad = np.radians(solar_positions['azimuth'])
    zenith = solar_positions['apparent_zenith']
    
    # Initialize a plot with polar projection
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    
    # Plot the sun path
    sc = ax.scatter(azimuth_rad, zenith, c=solar_positions['apparent_elevation'], cmap='plasma', s=10, label='Sun Path')
    
    # Annotate only the end time (sunset or specified end time)
    ax.text(azimuth_rad.iloc[-1], zenith.iloc[-1], times[-1].strftime('%I:%M %p'), fontsize=10, ha='center', weight='bold')
    
    # Customize the plot
    ax.set_theta_zero_location('N')  # Set 0° to North
    ax.set_theta_direction(-1)  # Clockwise direction
    ax.set_ylim(0, 90)  # Zenith angle range from 0° to 90°
    ax.set_yticks(np.arange(0, 91, 10))  # Zenith angle gridlines
    ax.set_rlabel_position(135)  # Position radial labels
    
    # Add a color bar to represent the solar elevation
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Solar Elevation (Degrees)')
    
    # Add a title
    plt.title(f'Solar Path from {start_datetime.strftime("%Y-%m-%d %I:%M %p")} to {end_datetime.strftime("%Y-%m-%d %I:%M %p")}', fontsize=14)
    
    # Generate a unique filename using UUID
    unique_id = uuid.uuid4()
    filename = f'solar_path_{unique_id}.png'
    image_path = os.path.join(image_directory, filename)
    image_return = f"media/solar_images/{filename}"
    # Save the plot as an image
    plt.savefig(image_path)
    plt.close()  # Close the plot to free up memory
    
    # Compute average values
    avg_elevation_value = solar_positions['apparent_elevation'].mean()
    avg_zenith_value = solar_positions['apparent_zenith'].mean()

    # Text summary of solar positions with technical details
    max_elevation_time = solar_positions['apparent_elevation'].idxmax()
    max_elevation_value = solar_positions['apparent_elevation'].max()
    max_zenith_value = solar_positions.loc[max_elevation_time, 'apparent_zenith']
    
    # Calculate sunrise and sunset times
    sunrise_time = times[solar_positions['apparent_elevation'] > 0].min()
    sunset_time = times[solar_positions['apparent_elevation'] > 0].max()

    # Calculate average solar noon time and azimuth
    average_solar_noon_time = times[solar_positions['apparent_elevation'] > 0].mean().to_pydatetime()
    average_solar_noon_azimuth = solar_positions['azimuth'].mean()

    solar_noon_zenith = solar_positions.loc[max_elevation_time, 'apparent_zenith']
    solar_noon_azimuth = solar_positions.loc[max_elevation_time, 'azimuth']

    # Store the detailed summary in a variable
    solar_path_summary = f"""
--- Solar Path Technical Summary ---
Date: Latitude {latitude:.4f}, Longitude {longitude:.4f}
Max Solar Noon: {max_elevation_time.strftime('%I:%M %p')} (Max Elevation: {max_elevation_value:.2f}°, Zenith: {max_zenith_value:.2f}°)
Max Solar Noon Azimuth: {solar_noon_azimuth:.2f}°
Average Solar Noon: {average_solar_noon_time.strftime('%I:%M %p')}
Average Solar Noon Azimuth: {average_solar_noon_azimuth:.2f}°
Max Zenith Angle: {max_zenith_value:.2f}°
Max Solar Elevation: {max_elevation_value:.2f}°
Average Solar Elevation: {avg_elevation_value:.2f}°
Average Zenith Angle: {avg_zenith_value:.2f}°
----------------------------
"""

    # Return the summary and image path
    return solar_path_summary, image_return

# Function to handle user inputs passed as a dictionary (JSON-like input)
def get_solar_input(latitude, longitude, param_dict):
    start_date_str = param_dict.get('start_date')
    start_time_str = param_dict.get('start_time')
    end_date_str = param_dict.get('end_date')
    end_time_str = param_dict.get('end_time')

    try:
        # Combine the date and time inputs
        start_datetime_str = f"{start_date_str} {start_time_str}"
        end_datetime_str = f"{end_date_str} {end_time_str}"

        # Convert user input into datetime objects
        start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %I:%M %p")
        end_datetime = datetime.strptime(end_datetime_str, "%Y-%m-%d %I:%M %p")

        # Call the function with the user-specified dates and times and get the summary
        summary, image_path = plot_solar_path(start_datetime, end_datetime, latitude, longitude)
        
        # Return the summary and image path
        return summary, image_path

    except ValueError:
        return "Invalid date or time format. Please ensure the date is in 'YYYY-MM-DD' format and time in 'HH:MM AM/PM' format."


