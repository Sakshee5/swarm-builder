from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'TwitterDiscussionSummarizer', 'swarm_structure': "['twitter_search_agent', ['twitter_search_agent', 'summary_analysis_agent'], ['summary_analysis_agent', 'twitter_search_agent']]"}

if __name__ == "__main__":
    run_demo_loop(twitter_search_agent, context_variables=context_variables, stream=True, debug=True)