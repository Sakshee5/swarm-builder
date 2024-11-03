from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'BitcoinInvestingSystem', 'swarm_structure': 'swarm_structure = [\n    "manager",           # Manager is the entry point for user interaction.\n    ["manager", "price"], # Manager can delegate to the Price Agent.\n    ["manager", "news"],  # Manager can delegate to the News Agent.\n    ["price", "manager"], # Price Agent reports back to the Manager.\n    ["news", "manager"]   # News Agent reports back to the Manager.\n]'}

if __name__ == "__main__":
    run_demo_loop(manager, context_variables=context_variables, stream=True, debug=True)