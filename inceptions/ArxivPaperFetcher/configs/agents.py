# Agents configuration file



from configs.tools import *
from swarm import Agent

def manager_instructions():
    return """This agent acts as the primary interface with the user. It collects the topic of interest from the user and initiates the process of fetching and summarizing the paper by coordinating with the fetch_agent and summarize_agent."""



manager = Agent(
    name="manager",
    instructions=manager_instructions(),
    functions=[],
)




def fetch_agent_instructions():
    return """The fetch_agent uses the arXivAPI to fetch the latest paper related to the given topic. It then transfers the paper information to the summarize_agent for summarization."""



fetch_agent = Agent(
    name="fetch_agent",
    instructions=fetch_agent_instructions(),
    functions=[arXivAPI],
)




def summarize_agent_instructions():
    return """The summarize_agent takes the paper retrieved by the fetch_agent and uses the NLP_Summarizer tool to create a brief overview. The summary is then transferred back to the manager agent for user presentation."""



summarize_agent = Agent(
    name="summarize_agent",
    instructions=summarize_agent_instructions(),
    functions=[NLP_Summarizer],
)
