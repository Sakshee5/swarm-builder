# Tools configuration file
from dotenv import load_dotenv
import os
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()


import os
from googleapiclient.discovery import build

# You need to have the 'google-auth' library installed to use the YouTube API.
# You can install it by running: pip install google-auth google-auth-oauthlib google-auth-httplib2

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth

# Load environment variables
load_dotenv()

# Set the scope for YouTube API
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def authenticate_youtube():
    """Authenticate and return the YouTube API client."""
    creds = None
    # Check if token.json file exists for saved credentials
    if os.path.exists('token.json'):
        creds = google.auth.load_credentials_from_file('token.json', SCOPES)

    # If no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the YouTube API client
    youtube = build('youtube', 'v3', credentials=creds)
    return youtube

def fetch_video_transcript(video_id):
    """Fetches the transcript of a specified YouTube video using the YouTube API."""
    youtube = authenticate_youtube()

    # Retrieve the list of caption tracks
    caption_response = youtube.captions().list(part='id', videoId=video_id).execute()

    if 'items' not in caption_response or len(caption_response['items']) == 0:
        return "No captions found for this video."

    # Use the first available caption track
    caption_id = caption_response['items'][0]['id']

    # Download caption track
    captions = youtube.captions().download(id=caption_id, tfmt='vtt').execute()

    return captions.decode('utf-8')


import openai

# Make sure you have the OpenAI API installed and set up.
# You can install it by running: pip install openai

openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure this environment variable is set

def generate_header(transcript):
    """
    Generates a catchy one-sentence header from a YouTube video transcript.

    Parameters:
    transcript (str): The transcript of the YouTube video.

    Returns:
    str: A catchy one-sentence header.
    """
    response = client.chat.completions.create(
      engine="gpt-3.5-turbo",
      prompt=f"Create a catchy one-sentence headline for the following transcript: {transcript[:2000]}",
      max_tokens=10
    )

    return response.choices[0].message.content

import openai

openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure this environment variable is set

def generate_summary(transcript):
    """
    Generates a concise, fun description of a YouTube video from its transcript.

    Parameters:
    transcript (str): The transcript of the YouTube video.

    Returns:
    str: A concise and catchy description.
    """
    response = client.chat.completions.create(
      engine="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "You are a creative assistant."},
          {
              "role": "user",
              "content": f"Create a fun and catchy description for the following transcript: {transcript[:2000]}"
          }
      ],
      max_tokens=50
    )

    return response.choices[0].message.content