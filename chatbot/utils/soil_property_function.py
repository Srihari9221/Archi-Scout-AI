import os
import uuid
import httpx
from httpx import Client
import matplotlib.pyplot as plt
from django.conf import settings  


#list of depths
depths = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]



# Dictionary to map properties to their full names
property_names = {
    "bdod": "Bulk Density",
    "cec": "Cation Exchange Capacity",
    "cfvo": "Coarse Fragments Volume",
    "clay": "Clay Content",
    "nitrogen": "Nitrogen Content",
    "ocd": "Organic Carbon Density",
    "phh2o": "pH in H2O",
    "sand": "Sand Content",
    "silt": "Silt Content",
    "soc": "Soil Organic Carbon"
}

# Function to fetch data for a single property and return as a formatted string
def fetch_property_data(lat, lon, selected_property):
    attempts = 3
    depth_labels = []
    mean_values = []
    property_unit = ""
    property_data = ""  
    property_name = ""

    for attempt in range(attempts):
        with Client(timeout=60.0) as client:
            try:
                response = client.get(
                    url="https://api.openepi.io/soil/property",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "depths": depths,
                        "properties": [selected_property],
                        "values": ["mean"],
                    },
                )
                response.raise_for_status()
                json_data = response.json()

                for layer in json_data["properties"]["layers"]:
                    property_name = layer["name"]
                    property_unit = layer["unit_measure"]["mapped_units"]

                    for depth_info in layer["depths"]:
                        depth_label = depth_info["label"]
                        if "mean" in depth_info["values"]:
                            mean_value = depth_info["values"]["mean"]
                            depth_labels.append(depth_label)
                            mean_values.append(mean_value)
                            property_data += f"Property: {property_name}, Depth: {depth_label}, Mean Value: {mean_value} {property_unit} "

                return depth_labels, mean_values, property_unit, property_name, property_data.strip() 

            except httpx.TimeoutException:
                print(f"Attempt {attempt+1}/{attempts} for {selected_property} timed out.")
                if attempt + 1 == attempts:
                    return [], [], "", "", f"Failed to fetch data for {selected_property}."
            except Exception as e:
                return [], [], "", "", f"An error occurred: {str(e)}"

# Function to plot the data and save the image
def plot_property_data(depth_labels, mean_values, property_unit, property_name):
    if not depth_labels or not mean_values:
        return  # 
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(mean_values, depth_labels, marker='o', linestyle='-', color='dodgerblue', markersize=10, linewidth=2)
    plt.xlabel(f'Mean Value ({property_unit})', fontsize=14, fontweight='bold', color='darkslategray')
    plt.ylabel('Depth (cm)', fontsize=14, fontweight='bold', color='darkslategray')
    plt.title(f'{property_name} across Different Depths', fontsize=16, fontweight='bold', color='midnightblue')
    plt.gca().invert_yaxis()
    plt.grid(color='lightgray', linestyle='--', linewidth=0.7, alpha=0.5)
    plt.gca().set_facecolor('whitesmoke')
    plt.fill_betweenx(depth_labels, mean_values, color='lightblue', alpha=0.3)
    plt.xlim(min(mean_values) - 1, max(mean_values) + 1)

    # Adding data labels
    for i, value in enumerate(mean_values):
        plt.text(value, depth_labels[i], f'{value:.2f}', fontsize=10, ha='left', va='center', 
                 bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    plt.tight_layout()

    # Save the plot exactly in the specified path
    image_directory = os.path.join(settings.MEDIA_ROOT, 'soilproperty_images')
    os.makedirs(image_directory, exist_ok=True)  
    unique_id = uuid.uuid4()  
    filename = f'soilproperty_{unique_id}.png'
    image_path = os.path.join(image_directory, filename)  
    image_recovery_path = f"media/soilproperty_images/{filename}"  

    plt.savefig(image_path) 
    plt.close()  

    return image_recovery_path  


def process_all_properties(lat, lon, input_dict):
    soil_summary = []
    image_lst = []
    # Extract available properties from the input dictionary
    available_properties = input_dict.get('available_properties', [])

    for property_input in available_properties:
        # Fetch the data
        depth_labels, mean_values, property_unit, property_name, property_data = fetch_property_data(lat, lon, property_input)

        # Add the fetched data as a single string to the soil summary list
        soil_summary.append(property_data)

        image_recovery_path = plot_property_data(depth_labels, mean_values, property_unit, property_name)
        image_lst.append(image_recovery_path) 

    
    map_path_lst = ["NoData"] * len(soil_summary)  

    return soil_summary, image_lst, map_path_lst  


