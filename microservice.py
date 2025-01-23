from flask import Flask, jsonify, request
import requests
app = Flask(__name__)
api_key = "REDACTED" 
# Example endpoint
@app.route('/weather', methods=['GET'])
def get_weather():

    city = "Tampere" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return(f"The temperature in {city} is {temperature}°C")
    else:
        print("Error fetching weather data.")
        return(response.status_code) 

    #return jsonify({"message": "Tampere: {temperature}°C"})

if __name__ == '__main__':
    app.run(debug=True)