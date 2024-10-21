

def WeatherAPI():
    """
    WeatherAPI is used to fetch real-time weather data for specified cities. It can access current weather conditions, forecasts, and historical data as needed.
    """
    import requests

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city_name):
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'imperial',  # for Fahrenheit
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Could not retrieve weather data'}

# Example Usage:
# weather_api = WeatherAPI(api_key='YOUR_API_KEY')
# weather_data = weather_api.get_weather('New York')
# print(weather_data)
