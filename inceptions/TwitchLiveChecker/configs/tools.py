# Tools configuration file



import requests
from dotenv import load_dotenv
import os
load_dotenv()

# Function to check if a Twitch streamer is currently live
# Requires setting up Twitch API client ID and secret

def check_twitch_live_status(streamer_name, client_id=os.getenv('TWITCH_CLIENT_ID'), client_secret=os.getenv('TWITCH_CLIENT_SECRET')):
    """
    Check if a specified Twitch streamer is currently live.

    Args:
    streamer_name (str): The name of the streamer to check.
    client_id (str): Twitch API client ID.
    client_secret (str): Twitch API client secret.

    Returns:
    bool: True if the streamer is live, False otherwise.
    """
    # API URL to get OAuth token
    token_url = 'https://id.twitch.tv/oauth2/token'
    
    # Get OAuth token
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }
    response = requests.post(token_url, params=params)
    access_token = response.json()['access_token']
    
    # Set up headers with OAuth token
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }

    # API URL to get stream status
    url = f'https://api.twitch.tv/helix/streams?user_login={streamer_name}'
    response = requests.get(url, headers=headers)
    data = response.json()['data']

    # If data list is empty, the streamer is not live
    return len(data) > 0

import random

# Function to send a funny message to lighten the mood

def send_funny_message():
    """
    Send a funny message to the user.

    Returns:
    str: A funny message from a predefined list.
    """
    messages = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why dont skeletons fight each other? They dont have the guts.",
        "I would avoid the sushi if I was you. Its a little fishy.",
        "What do you call fake spaghetti? An impasta!"
    ]
    return random.choice(messages)