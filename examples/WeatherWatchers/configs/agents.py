# Agents configuration file



from configs.tools import *
from swarm import Agent

def manager_instructions():
    return """The manager agent is the primary interface for handling user requests. It does not require any tools, as its primary role is to receive city weather requests from the user and communicate these to the CityWeather agent. Once the CityWeather agent obtains the data, the manager delivers it back to the user. It can transfer tasks to the CityWeather agent when specific city weather information is requested."""



manager = Agent(
    name="manager",
    instructions=manager_instructions(),
    functions=[],
)




def city_weather_instructions():
    return """The CityWeather agent is responsible for fetching real-time weather data for any US city requested by the manager agent. It uses the WeatherAPI to access up-to-date information and can retrieve data such as temperature, humidity, wind speed, and more. Once it gathers the required data, it sends the results back to the manager agent."""



city_weather = Agent(
    name="city_weather",
    instructions=city_weather_instructions(),
    functions=[WeatherAPI],
)
