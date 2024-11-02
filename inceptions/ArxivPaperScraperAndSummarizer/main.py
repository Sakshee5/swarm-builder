from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'ArxivPaperScraperAndSummarizer', 'swarm_structure': '[\n    manager,\n    [manager, arxivscraper],\n    [arxivscraper, summarize],\n    [summarize, manager]\n]'}

if __name__ == "__main__":
    run_demo_loop(manager, context_variables=context_variables, stream=True, debug=True)