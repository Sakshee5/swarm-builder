# Agents configuration file



from configs.tools import *
from swarm import Agent

def manager_instructions():
    return """The Manager Agent is responsible for initiating the system process by receiving user inputs. It delegates tasks to the Price Agent and News Agent to gather data on Bitcoin prices and recent news. Once the data is collected, it aggregates the information into a comprehensive report or summary that is fed back to the user. The Manager facilitates communication between the agents to ensure smooth operation."""


def transfer_to_price():
    return price


def transfer_to_news():
    return news


manager = Agent(
    name="manager",
    instructions=manager_instructions(),
    functions=[transfer_to_price, transfer_to_news, delegate_to_price_agent, delegate_to_news_agent, aggregate_information],
)




def price_instructions():
    return """The Price Agent fetches the latest Bitcoin price and computes the 24-hour price change from a reliable cryptocurrency API. After collecting the data, it formats the information and sends it back to the Manager for further processing. This agent ensures the price data is up-to-date and accurate."""


def transfer_to_manager():
    return manager


price = Agent(
    name="price",
    instructions=price_instructions(),
    functions=[transfer_to_manager, get_latest_bitcoin_price, get_24_hour_price_change],
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
