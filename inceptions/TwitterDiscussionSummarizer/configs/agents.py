# Agents configuration file



from configs.tools import *
from swarm import Agent

def twitter_search_agent_instructions():
    return """The Twitter Search Agent is responsible for querying Twitter using the Twitter API. It searches for recent posts based on a specified topic or question provided by the user. The agent collects tweets that match the search criteria and prepares them for analysis. It interacts with the Summary Analysis Agent by transferring the collected tweets for further processing."""


def transfer_to_summary_analysis_agent():
    return summary_analysis_agent


twitter_search_agent = Agent(
    name="twitter_search_agent",
    instructions=twitter_search_agent_instructions(),
    functions=[transfer_to_summary_analysis_agent, search_twitter, collect_tweets],
)




def summary_analysis_agent_instructions():
    return """The Summary Analysis Agent receives tweets from the Twitter Search Agent. It analyzes the text in the tweets to identify key themes and popular opinions. This agent then generates a summary of the discussions, focusing on the main points and varying perspectives shared by the community. The summarized information is presented back to the user, with the possibility of requesting further searches or clarifications from the Twitter Search Agent if necessary."""


def transfer_to_twitter_search_agent():
    return twitter_search_agent


summary_analysis_agent = Agent(
    name="summary_analysis_agent",
    instructions=summary_analysis_agent_instructions(),
    functions=[transfer_to_twitter_search_agent, analyze_tweets, summarize_discussions],
)
