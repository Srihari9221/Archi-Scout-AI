import os
import requests
from django.conf import settings

def generate_elevation_map(lat, lon, filename='elevation_map.html'):
    directory = os.path.join(settings.BASE_DIR,'chatbot','templates')

    os.makedirs(directory, exist_ok=True)

    # Fetch elevation data from Google Elevation API
    api_key = "AIzaSyDJywdV0_cC5BOPajS994D5SNLDXwxKWDo" 
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            elevation = data['results'][0]['elevation']
            summary = f"The elevation of {lat}, {lon} from sea level: {elevation:.2f} meters"

            
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>3D Elevation Map with Graph</title>
    <style>
        #map {{
            height: 50%;
            width: 100%;
        }}
        #chart {{
            height: 50%;
            width: 100%;
        }}
        html, body {{
            height: 100%;
            margin: 0;
            padding: 0;
        }}
    </style>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
</head>
<body>
    <div id="map"></div>
    <div id="chart"></div>
    <script>
        function initMap() {{
            var location = {{lat: {lat}, lng: {lon}}};
            var map = new google.maps.Map(document.getElementById('map'), {{
                center: location,
                zoom: 14,
                mapTypeId: 'terrain'
            }});

            var marker = new google.maps.Marker({{
                position: location,
                map: map,
                title: 'Elevation: {elevation:.2f} meters',
                icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
            }});

            var infowindow = new google.maps.InfoWindow({{
                content: 'Elevation: {elevation:.2f} meters'
            }});
            infowindow.open(map, marker);
            drawChart({elevation});
        }}

        function drawChart(elevation) {{
            google.charts.load('current', {{'packages':['corechart']}}); 
            google.charts.setOnLoadCallback(function() {{
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Location');
                data.addColumn('number', 'Elevation');
                data.addRows([
                    ['Sea-Level', 0],
                    ['Mid', Math.round(elevation / 2)],
                    ['Location', elevation]
                ]);

                var options = {{
                    title: 'Elevation Profile',
                    hAxis: {{
                        title: 'Elevation (meters)',
                        textStyle: {{color: '#333'}},
                        gridlines: {{color: '#f3f3f3'}}
                    }},
                    vAxis: {{
                        title: 'Location',
                        textStyle: {{color: '#333'}},
                        gridlines: {{color: '#f3f3f3'}},
                        viewWindow: {{min: 0}},
                    }},
                    legend: 'none',
                    colors: ['#76A7FA'],
                    backgroundColor: '#e0f7fa',
                    chartArea: {{width: '80%', height: '70%'}},
                    bars: 'horizontal',
                    bar: {{ groupWidth: '75%' }},
                }};

                var chart = new google.visualization.BarChart(document.getElementById('chart'));
                chart.draw(data, options);
            }});
        }}
    </script>
    <script async defer
        src="https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap">
    </script>
</body>
</html>
"""
            # Save HTML content to a file in the specified directory
            filepath = os.path.join(directory, filename)
            with open(filepath, 'w') as file:
                file.write(html_content)
            return summary, filepath
        else:
            print(f"Error fetching elevation data: No results found.")
    else:
        print(f"Error fetching elevation data: {response.status_code}")

