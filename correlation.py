import requests
import datetime
from datetime import datetime, timedelta
import numpy
import creds
WIND_API_URL = "https://api.openweathermap.org/data/2.5/forecast"

# ChatGPT provided function to parse the correct values from the json.
def get_next_day_values(data):
    # Convert string keys to datetime objects
    parsed_data = {datetime.strptime(k, "%Y-%m-%d %H:%M:%S"): v for k, v in data.items()}
    
    # Find the earliest timestamp
    min_time = min(parsed_data.keys())
    
    # Get the next day's date
    next_day = (min_time + timedelta(days=1)).date()
    
    # Define target hours
    target_hours = ["06:00:00", "09:00:00", "12:00:00", "15:00:00"]
    
    # Extract values for the next day at specified times
    values = [parsed_data.get(datetime.strptime(f"{next_day} {hour}", "%Y-%m-%d %H:%M:%S"), None) for hour in target_hours]
    
    return values


def main():
    response = requests.get(WIND_API_URL, params={"lat": 60.1695, "lon": 24.9354, "appid": creds.api_key})
    
    if response.status_code == 200:
        data = response.json()
        wind_data = {entry['dt_txt']: entry['wind']['speed'] for entry in data['list']}
              
    else:
        print("Error fetching weather data.")
        return(response.status_code) 
    
    data2 = None
    response2 =requests.get("https://api.porssisahko.net/v1/latest-prices.json")
    if response2.status_code == 200:
        data2 = response2.json()

    wind_speed_list = get_next_day_values(wind_data)
    print("Compare the wind speeds and electricity prices on the next day at 6, 9, 12 and 15 o'clock and calculate the correlation.")
    print("Wind speeds:",wind_speed_list)
    electricity_price_list = []
    values = [16, 13, 10, 7]

    for value in values:
        electricity_price_list.append(data2["prices"][value]["price"])
    
    print("Electricity prices:",electricity_price_list)
    print("Pearson correlation coefficient:",numpy.corrcoef(wind_speed_list, electricity_price_list)[0,1])
    
if __name__ == '__main__':
    main()