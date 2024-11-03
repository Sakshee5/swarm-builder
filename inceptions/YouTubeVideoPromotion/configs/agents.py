# Agents configuration file



from configs.tools import *
from swarm import Agent

def manager_instructions():
    return """The manager agent coordinates the workflow by communicating with the user and managing the task flow between the agents. It can transfer control to the 'youtube_data' agent once a YouTube video link is provided and instructs it to retrieve the video transcript using the YouTube API."""


def transfer_to_youtube_data():
    return youtube_data


manager = Agent(
    name="manager",
    instructions=manager_instructions(),
    functions=[transfer_to_youtube_data],
)




def youtube_data_instructions():
    return """This agent's role is to interact with the YouTube API to fetch the video transcript. Upon retrieving the transcript, it transfers the information to the 'content_creator' agent to generate the promotional content."""


def transfer_to_content_creator():
    return content_creator


youtube_data = Agent(
    name="youtube_data",
    instructions=youtube_data_instructions(),
    functions=[transfer_to_content_creator, fetch_video_transcript],
)




def content_creator_instructions():
    return """This agent takes the transcript from the 'youtube_data' agent, processes it to create a catchy one-sentence header and a concise, fun description. Once completed, it transfers the promotional content back to the 'manager' agent for user delivery."""


def transfer_to_manager():
    return manager


content_creator = Agent(
    name="content_creator",
    instructions=content_creator_instructions(),
    functions=[transfer_to_manager, generate_header, generate_summary],
)
