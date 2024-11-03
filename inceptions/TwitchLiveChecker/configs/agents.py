# Agents configuration file



from configs.tools import *
from swarm import Agent

def manager_instructions():
    return """The Manager agent is the entry point of the system. It receives requests from the user regarding the streamer's live status and delegates the task to the Live Status Checker agent. Based on the response from the Live Status Checker, it either informs the user that the streamer is live or initiates a transfer to the Humor Messenger for a funny message. It receives inputs from the user and makes decisions on which agent to engage next."""


def transfer_to_live_status_checker():
    return live_status_checker


manager = Agent(
    name="manager",
    instructions=manager_instructions(),
    functions=[transfer_to_live_status_checker],
)




def live_status_checker_instructions():
    return """The Live Status Checker agent uses the Twitch API to verify if the specified streamer is live. It receives the streamer's name from the Manager and uses check_twitch_live_status function to determine the streamer's status. If the streamer is live, it communicates back to the Manager agent. If not, it transitions to the Humor Messenger agent."""


def transfer_to_manager():
    return manager


def transfer_to_humor_messenger():
    return humor_messenger


live_status_checker = Agent(
    name="live_status_checker",
    instructions=live_status_checker_instructions(),
    functions=[transfer_to_manager, transfer_to_humor_messenger, check_twitch_live_status],
)




def humor_messenger_instructions():
    return """The Humor Messenger agent's role is to send a funny message to the user when the specified streamer is not live. It is activated by the Live Status Checker and utilizes the send_funny_message function to deliver an amusing message to brighten the user's day."""



humor_messenger = Agent(
    name="humor_messenger",
    instructions=humor_messenger_instructions(),
    functions=[send_funny_message],
)
