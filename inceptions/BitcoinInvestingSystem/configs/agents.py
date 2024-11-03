# Agents configuration file



from configs.tools import *
from swarm import Agent

def manager_instructions():
    return """The Manager Agent is responsible for initiating the system process by receiving user inputs. It delegates tasks to the Price Agent to gather data on Bitcoin prices. Once all the data is collected by respective agents, it aggregates the information into a comprehensive report or summary that is fed back to the user using `aggregate_information`. The Manager facilitates communication between the agents to ensure smooth operation."""


def transfer_to_price():
    return price


def transfer_to_news():
    return news


manager = Agent(
    name="manager",
    instructions=manager_instructions(),
    functions=[transfer_to_price, aggregate_information],
)




def price_instructions():
    return """The Price Agent fetches the latest Bitcoin price using `get_latest_bitcoin_price` and computes the 24-hour price change using `get_24_hour_price_change` from a reliable cryptocurrency API. This agent ensures the price data is up-to-date and accurate.
    
After collecting the data, transfer to the news agent for it to collect the latest news about Bitcoin."""



price = Agent(
    name="price",
    instructions=price_instructions(),
    functions=[get_latest_bitcoin_price, get_24_hour_price_change, transfer_to_news],
)




def news_instructions():
    return """The News Agent is tasked with gathering the latest news on Bitcoin from a trusted news API. It processes headlines and relevant articles to provide a summary of the most recent developments in the Bitcoin ecosystem. This agent then sends the news summary back to the Manager."""


def transfer_to_manager():
    return manager


news = Agent(
    name="news",
    instructions=news_instructions(),
    functions=[transfer_to_manager, fetch_recent_bitcoin_news],
)
