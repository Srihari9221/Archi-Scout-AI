import os
import requests
import matplotlib.pyplot as plt
from django.conf import settings 
import uuid  

# Function to fetch weather data from Open-Meteo API
def fetch_weather_data(lat, lon, start_date, end_date, metric):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': start_date,
        'end_date': end_date,
        'hourly': metric,
        'timezone': 'auto'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("hourly", {})
    else:
        print(f"Error fetching data from {start_date} to {end_date}")
        return {}

# Function to aggregate data over multiple years
def calculate_data_for_years(lat, lon, metric, start_year, end_year):
    data_by_year = {}
    
    for year in range(start_year, end_year + 1):
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        yearly_data = fetch_weather_data(lat, lon, start_date, end_date, metric)
        
        if yearly_data:
            data_points = yearly_data.get(metric, [])
            if data_points:
                if metric in ['temperature_2m', 'dew_point_2m', 'apparent_temperature', 'relative_humidity_2m', 
                              'cloud_cover', 'wind_speed_10m', 'pressure_msl', 'surface_pressure']:
                    data_by_year[year] = sum(data_points) / len(data_points)
                else:
                    data_by_year[year] = sum(data_points)
            else:
                data_by_year[year] = 0
    
    return data_by_year

# Function to aggregate data for each month of a specific year
def calculate_data_for_months(lat, lon, metric, year, start_month, end_month):
    data_by_month = {}
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    
    for month in range(start_month, end_month + 1):
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
        monthly_data = fetch_weather_data(lat, lon, start_date, end_date, metric)
        
        if monthly_data:
            data_points = monthly_data.get(metric, [])
            if data_points:
                if metric in ['temperature_2m', 'dew_point_2m', 'apparent_temperature', 'relative_humidity_2m', 
                              'cloud_cover', 'wind_speed_10m', 'pressure_msl', 'surface_pressure']:
                    data_by_month[months[month - 1]] = sum(data_points) / len(data_points)
                else:
                    data_by_month[months[month - 1]] = sum(data_points)
            else:
                data_by_month[months[month - 1]] = 0
    
    return data_by_month

# Function to visualize data for a single parameter and save the image with a unique ID
def visualize_data(data, label, is_year_based, representation_type, parameter_details):
    import matplotlib
    matplotlib.use('Agg') 

    keys = list(data.keys())
    values = list(data.values())
    
    unit = parameter_details.get('unit', '')
    description = parameter_details.get('description', label.replace("_", " ").capitalize())

    plt.figure(figsize=(10, 6))

    if representation_type == "bar chart":
        plt.bar(keys, values, width=0.4, label=f"{description} ({unit})", alpha=0.7)
        plt.title(f"{description} Data Visualization")
    elif representation_type == "line chart":
        plt.plot(keys, values, label=f"{description} ({unit})", marker='o')
        plt.title(f"{description} Data Visualization")
    elif representation_type == "pie chart":
        plt.pie(values, labels=keys, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
        plt.title(f"{description} Distribution")
    
    if representation_type != "pie chart":
        plt.legend()
        plt.xlabel('Year' if is_year_based else 'Month')
        plt.ylabel(f"{description} ({unit})")
        plt.xticks(rotation=45)
    
    # Save the plot with a unique ID
    save_path = os.path.join(settings.MEDIA_ROOT, 'climate_images')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    unique_id = str(uuid.uuid4())  # Generate a unique ID
    image_file_name = f"{label}_{unique_id}.png"
    image_file_path = os.path.join(save_path, image_file_name)
    plt.savefig(image_file_path)
    plt.close()
    
    # Return the relative URL to the image
    image_url = f'media/climate_images/{image_file_name}'
    return image_url

# Function to provide a summary in natural language
def summarize_data(data, parameter, is_year_based, parameter_details):
    unit = parameter_details.get('unit', 'units')
    description = parameter_details.get('description', parameter.replace("_", " ").capitalize())
    
    summary = f"Summary of {description} data:\n\n"
    
    if is_year_based:
        summary += "For each year, the data is as follows:\n"
    else:
        summary += "For each month, the data is as follows:\n"
    
    for time_period, value in data.items():
        summary += f"{time_period}: The average {description} was {value:.2f} {unit}.\n"
    
    return summary

# Function to handle user inputs passed as a dictionary 
def get_single_param_input(lat, lon, param_dict):
    parameter = param_dict.get('parameter')
    compare_span = param_dict.get('compare_span')
    
    parameter_definitions = {
        'temperature_2m': {'unit': '°C', 'description': 'Air temperature at 2 meters'},
        'relative_humidity_2m': {'unit': '%', 'description': 'Relative humidity at 2 meters'},
        'dew_point_2m': {'unit': '°C', 'description': 'Dew point temperature at 2 meters'},
        'apparent_temperature': {'unit': '°C', 'description': 'Apparent temperature'},
        'pressure_msl': {'unit': 'hPa', 'description': 'Atmospheric air pressure at sea level'},
        'surface_pressure': {'unit': 'hPa', 'description': 'Surface pressure'},
        'precipitation': {'unit': 'mm', 'description': 'Total precipitation'},
        'rain': {'unit': 'mm', 'description': 'Rainfall'},
        'snowfall': {'unit': 'cm', 'description': 'Snowfall'},
        'cloud_cover': {'unit': '%', 'description': 'Total cloud cover'},
        'shortwave_radiation': {'unit': 'W/m²', 'description': 'Shortwave solar radiation'},
        'wind_speed_10m': {'unit': 'km/h', 'description': 'Wind speed at 10 meters'},
        'et0_fao_evapotranspiration': {'unit': 'mm', 'description': 'Evapotranspiration'},
        'weather_code': {'unit': 'WMO code', 'description': 'Weather condition code'},
        'snow_depth': {'unit': 'meters', 'description': 'Snow depth on the ground'},
        'vapour_pressure_deficit': {'unit': 'kPa', 'description': 'Vapour pressure deficit'},
    }

    parameter_details = parameter_definitions.get(parameter, {'unit': 'units', 'description': parameter.replace("_", " ").capitalize()})
    
    if compare_span == "span":
        start_year = param_dict.get('start_year')
        end_year = param_dict.get('end_year')
        
        data = calculate_data_for_years(lat, lon, parameter, start_year, end_year)
        
        representation = param_dict.get('representation')
        
        if representation in ["bar chart", "line chart", "pie chart"]:
            image_url = visualize_data(data, parameter, is_year_based=True, representation_type=representation, parameter_details=parameter_details)
            summary = summarize_data(data, parameter, is_year_based=True, parameter_details=parameter_details)
            return summary, image_url
        else:
            print("Invalid representation type!")
    
    elif compare_span == "year":
        year = param_dict.get('year')
        start_month = param_dict.get('start_month', 1)
        end_month = param_dict.get('end_month', 12)
        
        data = calculate_data_for_months(lat, lon, parameter, year, start_month, end_month)
        
        representation = param_dict.get('representation')
        
        if representation in ["bar chart", "line chart", "pie chart"]:
            image_url = visualize_data(data, parameter, is_year_based=False, representation_type=representation, parameter_details=parameter_details)
            summary = summarize_data(data, parameter, is_year_based=False, parameter_details=parameter_details)
            return summary, image_url
        else:
            print("Invalid representation type!")
    
    else:
        print("Invalid comparison span!")


