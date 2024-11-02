from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'arxiv_summary_tool', 'swarm_structure': '[\n    manager,\n    [manager, ArXivFetcher],\n    [ArXivFetcher, Summarizer],\n    [Summarizer, Reporter],\n    [Reporter, manager]\n]'}

if __name__ == "__main__":
    run_demo_loop(manager, context_variables=context_variables, stream=True, debug=True)