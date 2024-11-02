from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'ArXivPaperFetcher', 'swarm_structure': "['manager', ['manager', 'fetch_agent'], ['fetch_agent', 'summarize_agent'], ['summarize_agent', 'manager']]"}

if __name__ == "__main__":
    run_demo_loop(manager, context_variables=context_variables, stream=True, debug=True)