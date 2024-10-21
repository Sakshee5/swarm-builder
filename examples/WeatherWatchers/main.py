from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'WeatherWatchers', 'swarm_structure': "[['manager'], ['manager', 'city_weather'], ['city_weather', 'manager']]"}

if __name__ == "__main__":
    run_demo_loop(manager, context_variables=context_variables, stream=True, debug=True)