import json
import requests
import pandas as pd

data = pd.read_csv('sample_inference_data.csv')
data = data.drop(columns=['Timestamp', 'Location', 'Future_weather_condition'])
url = "http://d88647e6-e0cc-4488-ac4d-340713502423.francecentral.azurecontainer.io/score"
headers = {'Content-Type': 'application/json'}

for i in range(len(data)):
    inference_data = {
        "Inputs": {
            "data": [
                {
                    "Temperature_C": float(data['Temperature_C'][i]),
                    "Humidity": float(data['Humidity'][i]),
                    "Wind_speed_kmph": float(data['Wind_speed_kmph'][i]),
                    "Wind_bearing_degrees": int(data['Wind_bearing_degrees'][i]),
                    "Visibility_km": float(data['Visibility_km'][i]),
                    "Pressure_millibars": float(data['Pressure_millibars'][i]),
                    "Current_weather_condition": int(data['Current_weather_condition'][i])
                }
            ]
        },
        "GlobalParameters": {
            "method": "predict"
        }
    }

    inference_data_json = json.dumps(inference_data)  
    r = requests.post(url, data=inference_data_json, headers=headers)
    print(f"{i} - {r.content}")
