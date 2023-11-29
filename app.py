from flask import Flask, render_template, request
import json
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        wind_speed = float(request.form['wind_speed'])
        wind_bearing = int(request.form['wind_bearing'])
        visibility = float(request.form['visibility'])
        pressure = float(request.form['pressure'])
        current_weather = int(request.form['current_weather'])

        # Prepare data for inference
        inference_data = {
            "Inputs": {
                "data": [
                    {
                        "Temperature_C": temperature,
                        "Humidity": humidity,
                        "Wind_speed_kmph": wind_speed,
                        "Wind_bearing_degrees": wind_bearing,
                        "Visibility_km": visibility,
                        "Pressure_millibars": pressure,
                        "Current_weather_condition": current_weather
                    }
                ]
            },
            "GlobalParameters": {
                "method": "predict"
            }
        }

        # Convert data to JSON
        inference_data_json = json.dumps(inference_data)

        # Make a request to the Azure ML service
        url = "http://d88647e6-e0cc-4488-ac4d-340713502423.francecentral.azurecontainer.io/score"
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=inference_data_json, headers=headers)
        result = r.content.decode('utf-8')

        return render_template('index.html', result=result)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

