from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'spotify_playlist_insights', 'swarm_structure': '[\n    "manager",                              # manager is the entry point for user communication\n    ["manager", "data_fetcher"],            # manager can transfer control to Data Fetcher\n    ["data_fetcher", "analyzer"],           # Data Fetcher can transfer control to Analyzer\n    ["analyzer", "formatter"],              # Analyzer can transfer control to Formatter\n    ["formatter", "manager"]                # Formatter can transfer back to manager\n]'}

if __name__ == "__main__":
    run_demo_loop(manager, context_variables=context_variables, stream=True, debug=True)