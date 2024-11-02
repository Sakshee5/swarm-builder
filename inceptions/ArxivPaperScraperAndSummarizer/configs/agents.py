# Agents configuration file



from configs.tools import *
from swarm import Agent

def manager_instructions():
    return """The Manager agent orchestrates the entire process. It begins the process by instructing the ArxivScraper agent to fetch a paper based on the specified topic. After the summarization is completed by the Summarize agent, it receives the summary and communicates the final output."""



manager = Agent(
    name="manager",
    instructions=manager_instructions(),
    functions=[],
)




def arxivscraper_instructions():
    return """The ArxivScraper agent queries arXiv's publicly available API to fetch a paper related to the given topic. The response is then forwarded to the Summarize agent for further processing."""



arxivscraper = Agent(
    name="arxivscraper",
    instructions=arxivscraper_instructions(),
    functions=[fetch_paper],
)




def summarize_instructions():
    return """The Summarize agent receives a research paper from the ArxivScraper agent, generates a brief overview using NLP tools, and sends the summary back to the Manager agent."""



summarize = Agent(
    name="summarize",
    instructions=summarize_instructions(),
    functions=[generate_summary],
)
