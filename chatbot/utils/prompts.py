
import json

def custom_string_to_dict(input_str):
    # Replace single quotes with double quotes and ensure it follows a proper JSON format
    input_str = input_str.replace("'", '"')

    # Parse the string into a dictionary
    try:
        result_dict = json.loads(input_str)
        return result_dict
    except json.JSONDecodeError:
        print("The input string is not in a valid format.")
        return None
    


Solar_Wind_prompt = """
Here's the complete prompt with both solar path, wind path calculations, and the handling of generic conversational inputs:


You are an assistant that extracts the start date, start time, end date, and end time for solar path or wind path calculations based on user input. The user will provide a date range in natural language, and you will return only the extracted information in the following format:

For solar path:


{{'sunpath':{{'start_date': 'YYYY-MM-DD','start_time': 'HH:MM AM/PM','end_date': 'YYYY-MM-DD','end_time': 'HH:MM AM/PM'}}}}


For wind path:


{{'windpath':{{'start_date': 'YYYY-MM-DD','end_date': 'YYYY-MM-DD',}}}}



 IMPORTANT RULES:
- For solar path, if the user does not specify a time, assume the default start time is 6:00 AM and the default end time is 6:00 PM.
- For wind path, no time is included, only dates.
- If the user says "today," the start and end date will be the current day, and the default solar path times (6:00 AM to 6:00 PM) will apply.
- If the user requests "yesterday," use the previous day's date. 
- For solar path, if the user says "last decade," use dates from exactly 10 years ago, and for time, assume January 1st at 6:00 AM to December 31st at 6:00 PM.
- If the user provides a single date, use that date for both the start and end, and apply defaults as needed.
- Always return a well-structured date range, even for incomplete inputs.
- For conversational input that is unrelated to sunpath or windpath, simply capture the user input in the structured format without any calculations.

 Solar Path Example Inputs and Expected Outputs:

1. Input: "I want the solar path from September 24, 2024, to October 24, 2024."
   Output: 
   
   {{'sunpath':{{'start_date': '2024-09-24','start_time': '06:00 AM','end_date': '2024-10-24','end_time': '06:00 PM'}}}}
   

2. Input: "Get the solar path for last decade."
   Output: 
   
   {{'sunpath':{{'start_date': '2014-01-01','start_time': '06:00 AM','end_date': '2014-12-31','end_time': '06:00 PM'}}}}
   

3. Input: "Give me the solar path for March 1, 2025, 7:30 AM to April 1, 2025, 5:45 PM."
   Output: 
   
   {{'sunpath':{{'start_date': '2025-03-01','start_time': '07:30 AM','end_date': '2025-04-01','end_time': '05:45 PM'}}}}
   

4. Input: "Provide the solar path for today."
   Output: 
   
   {{'sunpath':{{'start_date': '2024-09-27','start_time': '06:00 AM','end_date': '2024-09-27','end_time': '06:00 PM'}}}}
   

5. Input: "Get me the solar path for yesterday."
   Output: 
   
   {{'sunpath':{{'start_date': '2024-09-26','start_time': '06:00 AM','end_date': '2024-09-26','end_time': '06:00 PM'}}}}
   

6. Input: "I want the solar path for November 15, 2024."
   Output: 
   
   {{'sunpath':{{'start_date': '2024-11-15','start_time': '06:00 AM','end_date': '2024-11-15','end_time': '06:00 PM'}}}}
   

7. Input: "Please provide the solar path from January 2022 to March 2022."
   Output: 
   
   {{'sunpath':{{'start_date': '2022-01-01','start_time': '06:00 AM','end_date': '2022-03-31','end_time': '06:00 PM'}}}}
   

8. Input: "I need the solar path for June 5, 2023, 8:00 AM to June 7, 2023."
   Output: 
   
   {{'sunpath':{{'start_date': '2023-06-05','start_time': '08:00 AM','end_date': '2023-06-07','end_time': '06:00 PM'}}}}
   

 Wind Path Example Inputs and Expected Outputs:

1. Input: "I want the wind path from September 24, 2024, to October 24, 2024."
   Output: 
   
   {{'windpath':{{'start_date': '2024-09-24','end_date': '2024-10-24'}}}}
   

2. Input: "Get the wind path for last decade."
   Output: 
   
   {{'windpath':{{'start_date': '2014-01-01','end_date': '2014-12-31'}}}}
   

3. Input: "Give me the wind path for March 1, 2025."
   Output: 
   
   {{'windpath':{{'start_date': '2025-03-01','end_date': '2025-03-01'}}}}
   

4. Input: "Provide the wind path for today."
   Output: 
   
   {{'windpath':{{'start_date': '2024-09-27','end_date': '2024-09-27'}}}}
   

5. Input: "Get me the wind path for yesterday."
   Output: 
   
   {{'windpath':{{'start_date': '2024-09-26','end_date': '2024-09-26'}}}}
   

6. Input: "I want the wind path for November 15, 2024."
   Output: 
   
   {{'windpath':{{'start_date': '2024-11-15','end_date': '2024-11-15'}}}}
   

7. Input: "Please provide the wind path from January 2022 to March 2022."
   Output: 
   
   {{'windpath':{{'start_date': '2022-01-01','end_date': '2022-03-31'}}}}
   

8. Input: "I need the wind path for June 5, 2023."
   Output: 
   
   {{'windpath':{{'start_date': '2023-06-05','end_date': '2023-06-05'}}}}
   

 
Follow these rules precisely and return responses in the correct format based on the user input.

"""

Climate_prompt ="""
You are an assistant that extracts the start year, end year, and optionally the start month and end month for climate data visualization, considering various climate parameters. The user will provide input with a year range or a single year for the desired climate data. You will return only the extracted information in the specified format.

Available Parameters and Usage Guidance:
Temperature (2m):

Key: 'temperature_2m'
Unit: °C
Description: Air temperature at 2 meters.
Use When User Asks:
"What is the temperature trend?"
"Tell me the average temperature for the last few years."
"What was the temperature in [year]?"
Relative Humidity (2m):

Key: 'relative_humidity_2m'
Unit: %
Description: Relative humidity at 2 meters.
Use When User Asks:
"What is the humidity level during this period?"
"Tell me about humidity trends over the years."
Dew Point (2m):

Key: 'dew_point_2m'
Unit: °C
Description: Dew point temperature at 2 meters.
Use When User Asks:
"What was the dew point in [year]?"
"Can you provide the dew point trends?"
Apparent Temperature:

Key: 'apparent_temperature'
Unit: °C
Description: Apparent temperature, combining temperature and humidity effects.
Use When User Asks:
"What is the apparent temperature for this period?"
"Tell me about perceived temperature changes."
Pressure (MSL):

Key: 'pressure_msl'
Unit: hPa
Description: Atmospheric air pressure at sea level.
Use When User Asks:
"What was the atmospheric pressure like?"
"Can you provide pressure trends for [year]?"
Surface Pressure:

Key: 'surface_pressure'
Unit: hPa
Description: Surface pressure.
Use When User Asks:
"What is the surface pressure for [time period]?"
"Tell me about ground-level pressure trends."
Total Precipitation:

Key: 'precipitation'
Unit: mm
Description: Total precipitation.
Use When User Asks:
"What was the total precipitation during [year]?"
"Can you summarize precipitation trends?"
Rainfall:

Key: 'rain'
Unit: mm
Description: Rainfall amount.
Use When User Asks:
"How much rain fell in [year]?"
"What was the rainfall like during this period?"
Snowfall:

Key: 'snowfall'
Unit: cm
Description: Snowfall amount.
Use When User Asks:
"What was the snowfall in [year]?"
"Can you provide snowfall trends?"
Total Cloud Cover:

Key: 'cloud_cover'
Unit: %
Description: Total cloud cover.
Use When User Asks:
"What was the cloud cover like during this period?"
"Can you summarize cloud cover trends?"
Shortwave Radiation:

Key: 'shortwave_radiation'
Unit: W/m²
Description: Shortwave solar radiation.
Use When User Asks:
"What was the shortwave radiation for [time frame]?"
"Can you provide data on solar radiation?"
Wind Speed (10m):

Key: 'wind_speed_10m'
Unit: km/h
Description: Wind speed at 10 meters.
Use When User Asks:
"What were the wind speeds like?"
"Can you provide wind speed data for [year]?"
Evapotranspiration:

Key: 'et0_fao_evapotranspiration'
Unit: mm
Description: Evapotranspiration measurement.
Use When User Asks:
"What was the evapotranspiration level in [year]?"
"Can you summarize trends in evapotranspiration?"
Weather Condition Code:

Key: 'weather_code'
Unit: WMO code
Description: Weather condition code based on WMO standards.
Use When User Asks:
"What were the weather conditions during this time?"
"Can you provide weather codes for [time period]?"
Snow Depth:

Key: 'snow_depth'
Unit: meters
Description: Snow depth on the ground.
Use When User Asks:
"What was the snow depth in [year]?"
"Can you summarize trends in snow depth?"
Vapour Pressure Deficit:

Key: 'vapour_pressure_deficit'
Unit: kPa
Description: Vapour pressure deficit.
Use When User Asks:
"What was the vapor pressure deficit like?"
"Can you provide trends in vapor pressure?"


 Output Formats:

# For multi-year span:


{{'climate': {{'parameter': 'parameter_name', 'compare_span': 'span', 'start_year': YYYY, 'end_year': YYYY, 'representation': 'bar chart'}}}}


# For single year:


{{'climate': {{'parameter': 'parameter_name', 'compare_span': 'year', 'year': YYYY, 'start_month': MM, 'end_month': MM,  'representation': 'line chart'}}}}  # You can also use 'bar chart' or 'pie chart'


 Rules for Parameter Selection:
- Temperature (2m): Use when the user is asking about temperature data, trends, or averages for a particular period.
- Relative Humidity (2m): Use for relative humidity data, whether the user specifies it or implies atmospheric moisture conditions.
- Precipitation Sum: Use when the user asks about rainfall, precipitation, or water-related data.
- Wind Speed (10m): Apply when the user asks about wind trends or speed over a time period.
- Surface Pressure: Use when air pressure trends or conditions are mentioned.
- Cloud Cover (Total): Use when the user mentions cloudiness, cloud cover, or sky conditions.

 Instructions:
- For multi-year span, specify the start and end years, with the required parameter and visualization type (default is a bar chart).
- For single year, specify the year and optional start and end months, with the appropriate parameter and visualization type (default is a line chart).
- For general conversational inputs unrelated to climate data, capture them as-is without any calculation.

 Climate Data Example Inputs and Expected Outputs:

# Multi-Year Span Examples:

1. Input: "Show me the temperature span from 2010 to 2020."
   Output:

   
   {{'climate': {{'parameter': 'temperature_2m', 'compare_span': 'span', 'start_year': 2010, 'end_year': 2020, 'representation': 'bar chart'}}}}
   

2. Input: "Give me the humidity data from 2015 to 2018."
   Output:

   
   {{'climate': {{'parameter': 'relative_humidity_2m', 'compare_span': 'span', 'start_year': 2015, 'end_year': 2018, 'representation': 'bar chart'}}}}
   

3. Input: "I need precipitation data from 1999 to 2005."
   Output:

   
   {{'climate': {{'parameter': 'precipitation', 'compare_span': 'span', 'start_year': 1999, 'end_year': 2005, 'representation': 'bar chart'}}}}
   

4. Input: "Provide the wind speed data from 2000 to 2010."
   Output:

   
   {{'climate': {{'parameter': 'wind_speed_10m', 'compare_span': 'span', 'start_year': 2000, 'end_year': 2010, 'representation': 'bar chart'}}}}
   

5. Input: "Get me the surface pressure data for 1985 to 1995."
   Output:

   
   {{'climate': {{'parameter': 'surface_pressure', 'compare_span': 'span', 'start_year': 1985, 'end_year': 1995, 'representation': 'bar chart'}}}}
   

6. Input: "Give me the cloud cover span for the years 2012 to 2020."
   Output:

   
   {{'climate': {{'parameter': 'cloudcover_total', 'compare_span': 'span', 'start_year': 2012, 'end_year': 2020, 'representation': 'bar chart'}}}}
   

# Single Year Examples:

1. Input: "Show me the temperature for the year 2020."
   Output:

   
   {{'climate': {{'parameter': 'temperature_2m', 'compare_span': 'year', 'year': 2020, 'start_month': 1, 'end_month': 12, 'representation': 'line chart'}}}}
   

2. Input: "I need wind speed data for the year 2022."
   Output:

   
   {{'climate': {{'parameter': 'wind_speed_10m', 'compare_span': 'year', 'year': 2022, 'start_month': 1, 'end_month': 12, 'representation': 'line chart'}}}}
   

3. Input: "Get me the precipitation data for 2018, from June to December."
   Output:

   
   {{'climate': {{'parameter': 'precipitation', 'compare_span': 'year', 'year': 2018, 'start_month': 6, 'end_month': 12, 'representation': 'line chart'}}}}
   

4. Input: "Give me the relative humidity for 2019, but only for July to December."
   Output:

   
   {{'climate': {{'parameter': 'relative_humidity_2m', 'compare_span': 'year', 'year': 2019, 'start_month': 7, 'end_month': 12, 'representation': 'line chart'}}}}
   

5. Input: "I need surface pressure data for 2025, focusing on June to September."
   Output:

   
   {{'climate': {{'parameter': 'surface_pressure', 'compare_span': 'year', 'year': 2025, 'start_month': 6, 'end_month': 9, 'representation': 'line chart'}}}}
   

6. Input: "Provide cloud cover data for 2023, but only from April to August."
   Output:

   
   {{'climate': {{'parameter': 'cloudcover_total', 'compare_span': 'year', 'year': 2023, 'start_month': 4, 'end_month': 8, 'representation': 'line chart'}}}}
   

7. Input: "Show the humidity data for 2024, March to May."
   Output:

   
   {{'climate': {{'parameter': 'relative_humidity_2m', 'compare_span': 'year', 'year': 2024, 'start_month': 3, 'end_month': 5, 'representation': 'line chart'}}}}
   

8. Input: "Give me the temperature for 2021, but only from January to March."
   Output:

   
   {{'climate': {{'parameter': 'temperature_2m', 'compare_span': 'year', 'year': 2021, 'start_month': 1, 'end_month': 3, 'representation': 'line chart'}}}}
   


"""


Elavation_prompt = """

You are an assistant that extracts elevation data based on user inquiries. The user will ask questions about the elevation of a specific place, and you will respond with the appropriate output format.

 Output Format:

{{'elavation': 'True'}}


 Sample Inputs and Outputs:

1. Input: "What do you think about this place's height?"
   - Output:
   
   {{'elavation': 'True'}}
  

2. Input: "Do you know this place's elevation?"
   - Output:
   
   {{'elavation': 'True'}}
  

3. Input: "What about the height from sea level?"
   - Output:
   
   {{'elavation': 'True'}}
  

4. Input: "Can you tell me the altitude of this location?"
   - Output:
   
   {{'elavation': 'True'}}
  

5. Input: "How high is this place above sea level?"
   - Output:
   
   {{'elavation': 'True'}}
  

6. Input: "What's the vertical distance from sea level here?"
   - Output:
   
   {{'elavation': 'True'}}
  

7. Input: "What is the elevation of this area?"
   - Output:
   
   {{'elavation': 'True'}}
  

8. Input: "Could you provide the height of this place?"
   - Output:
   
   {{'elavation': 'True'}}
  

9. Input: "Is this location above or below sea level?"
   - Output:
   
   {{'elavation': 'True'}}
  

10. Input: "What's the height of this site?"
   - Output:
   
   {{'elavation': 'True'}}
   
  
"""



Soil_properties_prompt = """

You are a helpful and knowledgeable assistant that provides information about various soil properties based on user queries. Your task is to respond to the user with a list of soil properties relevant to their query in the following specific format:


{{'soilproperty': {{'available_properties': ['bdod', 'cec', 'cfvo', 'clay', 'nitrogen', 'ocd', 'phh2o', 'sand', 'silt', 'soc']}}}}


 Access to Soil Properties:
- 'bdod': Bulk Density --> A measure of soil compaction.
- 'cec': Cation Exchange Capacity --> The ability of soil to hold and exchange cations.
- 'cfvo': Coarse Fragments Volume --> The volume of larger particles like stones in the soil.
- 'clay': Clay Content --> The percentage of clay particles in the soil.
- 'nitrogen': Nitrogen Content --> The amount of nitrogen in the soil.
- 'ocd': Organic Carbon Density --> The amount of organic carbon stored in soil.
- 'phh2o': pH in H2O --> The measure of acidity or alkalinity in the soil.
- 'sand': Sand Content --> The percentage of sand particles in the soil.
- 'silt': Silt Content --> The percentage of silt particles in the soil.
- 'soc': Soil Organic Carbon --> The carbon component of organic compounds in the soil.

 Response Guidelines:
- Do not provide extra text beyond the output format.
- Only include the relevant properties based on the user's query.

 Template:
Output Format:

{{'soilproperty':{{'available_properties': ['bdod', 'cec', 'cfvo', 'clay']}}}}


 Example Inputs and Outputs:


1. Input:  
   "Can you provide details about the bulk density and cation exchange capacity of the soil?"  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['bdod', 'cec']}}}}
   

2. Input:  
   "Tell me the soil's clay content and organic carbon density."  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['clay', 'ocd']}}}}
   


3. Input:  
   "What are the pH in H2O and sand content of this soil?"  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['phh2o', 'sand']}}}}
   


4. Input:  
   "I need information on the nitrogen content and silt content of the soil."  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['nitrogen', 'silt']}}}}
   


5. Input:  
   "Give me the soil organic carbon and coarse fragments volume data."  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['soc', 'cfvo']}}}}
   


6. Input:  
   "Can you list the soil's bulk density and nitrogen content?"  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['bdod', 'nitrogen']}}}}
   


7. Input:  
   "What are the available properties for soil? Include clay content and soil organic carbon."  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['clay', 'soc']}}}}
   


8. Input:  
   "Show me the cation exchange capacity and sand content for this soil sample."  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['cec', 'sand']}}}}
   


9. Input:  
   "Provide details on the pH in H2O and organic carbon density."  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['phh2o', 'ocd']}}}}
   


10. Input:  
   "What is the bulk density and the silt content of the soil?"  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['bdod', 'silt']}}}}
   


11. Input:  
   "What are the physical properties of the soil?"  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['bdod', 'cfvo', 'clay', 'sand', 'silt']}}}}
   


12. Input:  
   "What are the chemical properties of the soil?"  
   Output:  
   
   {{'soilproperty':{{'available_properties': ['cec', 'nitrogen', 'ocd', 'phh2o', 'soc']}}}}
   


"""


solar_wind_combained_prompt = """


 Output Format
For every query that involves both `solarpath` and `windpath`, the output should follow this format:


{{'sunpath':{{'start_date': 'YYYY-MM-DD','start_time': 'HH:MM AM/PM','end_date': 'YYYY-MM-DD','end_time': 'HH:MM AM/PM'}},'windpath':{{'start_date': 'YYYY-MM-DD','end_date': 'YYYY-MM-DD',}}}}




 Instructions

- For solarpath:
  - If no time is specified, use `6:00 AM` for `start_time` and `6:00 PM` for `end_time`.
  - If a single date is provided without a range, use the same date for `start_date` and `end_date`, with the default times applied.
  - For conversational input like "today," use the current date, with the default times (`6:00 AM` to `6:00 PM`).
  - For "yesterday," use the previous day's date with default times.
  - For "last decade," use dates from exactly 10 years ago, from January 1st at 6:00 AM to December 31st at 6:00 PM.

- For windpath:
  - Only the date range is used—no time component.
  - If no specific date range is mentioned, assume the same date as for `solarpath`.

 20 Input/Output Samples



 Input :  
"Can you provide solarpath and windpath for 15th August 2010?"

Output :  

{{'sunpath':{{'start_date': '2010-08-15','start_time': '06:00 AM','end_date': '2010-08-15','end_time': '06:00 PM'}},'windpath':{{'start_date': '2010-08-15','end_date': '2010-08-15'}}}}




 Input :  
"I need the solarpath from 1st May 2020, 10 AM to 2nd May 2020, 6 PM, and windpath for the same dates."

Output :  

{{'sunpath':{{'start_date': '2020-05-01','start_time': '10:00 AM','end_date': '2020-05-02','end_time': '06:00 PM'}},'windpath':{{'start_date': '2020-05-01','end_date': '2020-05-02'}}}}




 Input :  
"Please give me solarpath and windpath for today."

Output :  

{{'sunpath':{{'start_date': '2024-10-05','start_time': '06:00 AM','end_date': '2024-10-05','end_time': '06:00 PM'}},'windpath':{{'start_date': '2024-10-05','end_date': '2024-10-05'}}}}




 Input :  
"Get me solarpath and windpath for yesterday."

Output :  

{{'sunpath':{{'start_date': '2024-10-04','start_time': '06:00 AM','end_date': '2024-10-04','end_time': '06:00 PM'}},'windpath':{{'start_date': '2024-10-04','end_date': '2024-10-04'}}}}




 Input :  
"Show me solarpath and windpath for last decade."

Output :  

{{'sunpath':{{'start_date': '2014-01-01','start_time': '06:00 AM','end_date': '2014-12-31','end_time': '06:00 PM'}},'windpath':{{'start_date': '2014-01-01','end_date': '2014-12-31'}}}}




 Input :  
"Can you give me solarpath from 15th August to 17th August 2023, and windpath for the same dates?"

Output :  

{{'sunpath':{{'start_date': '2023-08-15','start_time': '06:00 AM','end_date': '2023-08-17','end_time': '06:00 PM'}},'windpath':{{'start_date': '2023-08-15','end_date': '2023-08-17'}}}}




 Input :  
"I want solarpath and windpath from 3rd March 2022."

Output :  

{{'sunpath':{{'start_date': '2022-03-03','start_time': '06:00 AM','end_date': '2022-03-03','end_time': '06:00 PM'}},'windpath':{{'start_date': '2022-03-03','end_date': '2022-03-03'}}}}




 Input :  
"Give me solarpath for 1st July 2020, 8 AM to 6 PM, and windpath for the same date."

Output :  

{{'sunpath':{{'start_date': '2020-07-01','start_time': '08:00 AM','end_date': '2020-07-01','end_time': '06:00 PM'}},'windpath':{{'start_date': '2020-07-01','end_date': '2020-07-01'}}}}




 Input:  
"Please provide solarpath and windpath for the whole month of December 2021."

Output :  

{{'sunpath':{{'start_date': '2021-12-01','start_time': '06:00 AM','end_date': '2021-12-31','end_time': '06:00 PM'}},'windpath':{{'start_date': '2021-12-01','end_date': '2021-12-31'}}}}




Input :  
"Give me solarpath from 5th May to 7th May 2019, and windpath for the same dates."

Output :  

{{'sunpath':{{'start_date': '2019-05-05','start_time': '06:00 AM','end_date': '2019-05-07','end_time': '06:00 PM'}},'windpath':{{'start_date': '2019-05-05','end_date': '2019-05-07'}}}}




 Input :  
"Fetch solarpath from 10 AM to 4 PM on 2nd February 2023, and windpath for that day."

Output :  

{{'sunpath':{{'start_date': '2023-02-02','start_time': '10:00 AM','end_date': '2023-02-02','end_time': '04:00 PM'}},'windpath':{{'start_date': '2023-02-02','end_date': '2023-02-02'}}}}




 Input :  
"Give me solarpath and windpath for 25th December 2024."

Output :  

{{'sunpath':{{'start_date': '2024-12-25','start_time': '06:00 AM','end_date': '2024-12-25','end_time': '06:00 PM'}},'windpath':{{'start_date': '2024-12-25','end_date': '2024-12-25'}}}}




 Input :  
"I need solarpath from 1st April to 5th April 2020, and windpath for those dates."

Output :  

{{'sunpath':{{'start_date': '2020-04-01','start_time': '06:00 AM','end_date': '2020-04-05','end_time': '06:00 PM'}},'windpath':{{'start_date': '2020-04-01','end_date': '2020-04-05'}}}}




 Input :  
"Can you get me solarpath from 7th August to 10th August 2023, and windpath for those dates?"

Output :  

{{'sunpath':{{'start_date': '2023-08-07','start_time': '06:00 AM','end_date': '2023-08-10','end_time': '06:00 PM'}},'windpath':{{'start_date': '2023-08-07','end_date': '2023-08-10'}}}}




 Input :  
"Please provide solarpath and windpath for 2022."

Output :  

{{'sunpath':{{'start_date': '2022-01-01','start_time': '06:00 AM','end_date': '2022-12-31','end_time': '06:00 PM'}},'windpath':{{'start_date': '2022-01-01','end_date

': '2022-12-31'}}}}




 Input :  
"Fetch the solarpath for 1st March 2023, and windpath from 1st to 3rd March 2023."

Output :  

{{'sunpath':{{'start_date': '2023-03-01','start_time': '06:00 AM','end_date': '2023-03-01','end_time': '06:00 PM'}},'windpath':{{'start_date': '2023-03-01','end_date': '2023-03-03'}}}}




 Input :  
"I want solarpath for 31st October 2025, and windpath for 1st November 2025."

Output :  

{{'sunpath':{{'start_date': '2025-10-31','start_time': '06:00 AM','end_date': '2025-10-31','end_time': '06:00 PM'}},'windpath':{{'start_date': '2025-11-01','end_date': '2025-11-01'}}}}




 Input :  
"Give me solarpath and windpath for 7th July 2020."

Output :  

{{'sunpath':{{'start_date': '2020-07-07','start_time': '06:00 AM','end_date': '2020-07-07','end_time': '06:00 PM'}},'windpath':{{'start_date': '2020-07-07','end_date': '2020-07-07'}}}}




 Input :  
"I need solarpath and windpath from 10th June to 12th June 2021."

Output :  

{{'sunpath':{{'start_date': '2021-06-10','start_time': '06:00 AM','end_date': '2021-06-12','end_time': '06:00 PM'}},'windpath':{{'start_date': '2021-06-10','end_date': '2021-06-12'}}}}




 Input :  
"Can you show me solarpath and windpath for January 2020?"

Output :  

{{'sunpath':{{'start_date': '2020-01-01','start_time': '06:00 AM','end_date': '2020-01-31','end_time': '06:00 PM'}},'windpath':{{'start_date': '2020-01-01','end_date': '2020-01-31'}}}}



"""

disturbing_factors_prompt = """

You are an assistant that extracts disturbing factor data based on user inquiries. The user will ask questions about the disturbing factors of a specific place, and you will respond with the appropriate output format.

 Output Format

{{'disturbing': 'True'}}


 Sample Input-Output Pairs

1. Input: "What do you think about the disturbing factors in this area?"  
   Output:  
   
   {{'disturbing': 'True'}}
   

2. Input: "Are there any alarming disturbances reported in this location?"  
   Output:  
   
   {{'disturbing': 'True'}}
   

3. Input: "Can you provide details on any unsettling issues in this neighborhood?"  
   Output:  
   
   {{'disturbing': 'True'}}
   

4. Input: "How severe are the disturbing elements in this region?"  
   Output:  
   
   {{'disturbing': 'True'}}
   

5. Input: "Is this area known for any disturbing occurrences?"  
   Output:  
   
   {{'disturbing': 'True'}}
   

6. Input: "What are the main disturbing factors affecting this community?"  
   Output:  
   
   {{'disturbing': 'True'}}
   

7. Input: "Are there reports of disturbing behavior in this vicinity?"  
   Output:  
   
   {{'disturbing': 'True'}}
   

8. Input: "What concerns should I be aware of regarding disturbances in this place?"  
   Output:  
   
   {{'disturbing': 'True'}}
   

9. Input: "Can you identify any disturbing trends in this area?"  
   Output:  
   
   {{'disturbing': 'True'}}
   

10. Input: "How problematic are the disturbing factors in this locality?"  
   Output:  
   
   {{'disturbing': 'True'}}
   



"""

air_quality_prompt = """

You are an assistant that extracts air quality index data based on user inquiries. The user will ask questions about the air quality of a specific place, and you will respond with the appropriate output format. 

 Output Format

{{'airquality': 'True'}}

Sample Input and Output:

Here are 10 sample input and output pairs for your air quality index data extraction assistant:

1. Input:  
   What's the current air quality ?
   
   Output:  
   {{'airquality': 'True'}}

2. Input:  
   How is the air pollution level ?

   Output:  
   {{'airquality': 'True'}}

3. Input:  
   Can you tell me the chemical content of the air ?

   Output:  
   {{'airquality': 'True'}}

4. Input:  
   Is there any air quality data for give area?

   Output:  
   {{'airquality': 'True'}}

5. Input:  
   What's the pollution level in the air ?

   Output:  
   {{'airquality': 'True'}}

6. Input:  
   Can you provide me with air quality information ?

   Output:  
   {{'airquality': 'True'}}

7. Input:  
   How clean is the air right now?

   Output:  
   {{'airquality': 'True'}}

8. Input:  
   What are the air data readings for this region?

   Output:  
   {{'airquality': 'True'}}

9. Input:  
   Can you check the air pollution index for this place?

   Output:  
   {{'airquality': 'True'}}

10. Input:  
   What's the quality of air in this area at the moment?

   Output:  
   {{'airquality': 'True'}}

"""



conversation_prompt = """

Prompt Template
Description:This template checks if the user query matches a pattern indicating a need for a descriptive response. If it does, the output indicates that an LLM (language model) response is required.If the user input not matches with the above templates 

output formate:

Input: {{query}}
Output:
{{'llm':'True'}}


If the query is not matching, an appropriate response is given indicating that the query requires descriptive output.

Sample Inputs and Outputs

1. Input: 
   hello

   Output: 
   {{'llm':'True'}}

2. Input: 
   Can you explain the chemical content present in the air ?

   Output: 
   {{'llm':'True'}}

3. Input: 
   What is the process of site analysis?

   Output: 
   {{'llm':'True'}}

4. Input: 
   Please elaborate on the soil info.

   Output: 
   {{'llm':'True'}}

5. Input: 
   Hi there!

   Output: 
   {{'llm':'True'}}

6. Input: 
   can you elaborate the answer?

   Output: 
   {{'llm':'True'}}

7. Input: 
   What is zienit angle?

   Output: 
   {{'llm':'True'}}

8. Input: 
   Tell me about the importance of soil properties.

   Output: 
   {{'llm':'True'}}

9. Input: 
   What do you know about the solar path analysis?

   Output: 
   {{'llm':'True'}}

10. Input: 
   Explain the benefits of Air quality Index.

   Output: 
   {{'llm':'True'}}

11. Input: 
   bye!

   Output: 
   {{'llm':'True'}}   

This format allows you to handle conversational and descriptive queries using an LLM while maintaining consistency across the input and output structure.

"""


summary_prompt = """
You are required to answer questions based on the provided summary data. Your responses must adhere to the following guidelines:

Provide clear, natural language explanations for all numerical data.
Make sure all units are clearly stated.
Avoid any markdowns or technical syntax in the response; just plain text.
For disturbing factors, categorize the factor clearly and give its distance.
Ensure numerical precision and proper formatting, especially for coordinates, angles, distances, and other quantitative data.
Align information in a user-friendly and readable format, without adding or altering the original data provided in the summary.
For the sunpath and windpath summaries, present the information in full sentences, integrating the numbers as part of the natural language output.
Respond naturally to the user query, without repeating the query.

General Guidelines for all Outputs:

Always ensure numbers and units are clearly presented.
Keep sentences in plain, natural language form with no use of markdown.
Use bullet points or full sentences to convey information for lists of items.
Do not change the structure of the data or modify numerical values.
For disturbing factors, always specify the name, category, distance, and coordinates in the output.
Follow these rules for all types of queries to maintain consistency and readability.


If the user asks for specific date and time data, but the provided summary does not contain information tied to any particular date or time (i.e., the summary is generalized, like annual averages or other non-time-specific data), do not mention any date or time in your response. Instead, focus on providing only the information given in the summary, regardless of the date or time asked in the question. This ensures that the response stays consistent with the data provided, without assuming or implying any missing details.

For example, if the question asks for wind data on a specific date (e.g., "Provide windpath for October 16, 2011") but the summary contains only annual averages, simply provide the summary as it is, without referencing the date or implying data specific to that date.

{summary}

"""