import os
import requests
import base64
from dotenv import load_dotenv
import os
load_dotenv()

def initialize_process(genre: str):
    """
    Initializes the process with the given genre.

    Args:
        genre (str): The music genre specified by the user.
    """
    print(f"Initializing the process for genre: {genre}...")
    return genre

def get_spotify_token(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')):
    """
    Gets the Spotify API access token using the Client Credentials flow.

    Args:
        client_id (str): Your Spotify app Client ID.
        client_secret (str): Your Spotify app Client Secret.

    Returns:
        str: Access token for Spotify API.
    """
    url = "https://accounts.spotify.com/api/token"
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, headers=headers, data={"grant_type": "client_credentials"})
    if response.status_code != 200:
        raise Exception(f"Error obtaining token: {response.json()}")

    token = response.json().get("access_token")
    return token

def fetch_spotify_data(genre):
    """
    Connects to the Spotify API to retrieve the top 20 songs for a given genre.

    Args:
        genre (str): The music genre for which to fetch song data.

    Returns:
        list: A list of dictionaries containing song data including popularity scores.
    """
    token = get_spotify_token()  # Get the token
    url = "https://api.spotify.com/v1/recommendations"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Making the API call
    params = {
        "seed_genres": genre,
        "limit": 20
    }
    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()
    
    if response.status_code != 200:
        raise Exception(f"Spotify API error: {response_data.get('error', {}).get('message', 'Unknown error')}")

    # Extract song information
    songs = response_data.get('tracks', [])
    
    # Get track IDs
    track_ids = [track['id'] for track in songs]
    return track_ids

def parse_song_data(songs: list[str]):
    """
    Parses and structures the fetched Spotify song data.

    Args:
        songs (list): A list of song IDs.

    Returns:
        list: A list of dictionaries containing structured song data.
    """
    track_data_list = []
    token = get_spotify_token()

    # Spotify API endpoint for getting details of several tracks
    tracks_url = "https://api.spotify.com/v1/tracks"
    
    if isinstance(songs, str):
        songs = songs.split(',')
    for song_id in songs:
        # Make a request to get detailed track information
        track_response = requests.get(f"{tracks_url}/{song_id}", headers={"Authorization": f"Bearer {token}"})
        if track_response.status_code != 200:
            print(f"Error fetching track data for ID {song_id}: {track_response.json().get('error', {}).get('message', 'Unknown error')}")
            continue

        track_info = track_response.json()

        # Structure desired information
        track_data = {
            'name': track_info.get('name'),
            'popularity': track_info.get('popularity'),
            'artists': [artist['name'] for artist in track_info.get('artists', [])]
        }

        track_data_list.append(track_data)

    return track_data_list



def analyze_data(parsed_data):
    # Convert the string representation of the list back to an actual list
    import ast
    try:
        songs = ast.literal_eval(parsed_data)
    except (ValueError, SyntaxError) as e:
        print("Error parsing data:", e)
        return

    # Proceed with analyzing the actual list of songs
    insights = {'popularity': []}

    for song in songs:
        insights['popularity'].append(song['popularity'])
    
    print("Insights:", insights)



def extract_insights(parsed_insights):
    # Convert the string representation of the dictionary back to an actual dictionary
    import ast
    try:
        insights = ast.literal_eval(parsed_insights)
    except (ValueError, SyntaxError) as e:
        print("Error parsing insights data:", e)
        return

    # Now that insights is a dictionary, you can access its keys
    if isinstance(insights, dict) and 'artists' in insights:
        for artist in insights['artists']:
            print("Artist:", artist)
    else:
        print("Insights data is not in the expected format or 'artists' key is missing.")




def identify_trends(insights):
    """
    Identifies notable trends in the song data based on popularity.

    Args:
        insights (dict): Insights containing data from analysis.

    Returns:
        dict: Updated insights including trends.
    """
    print("Identifying trends...")
    
    # Check if 'popularity' exists and is a list
    if isinstance(insights.get('popularity'), list) and insights['popularity']:
        average_popularity = sum(insights['popularity']) / len(insights['popularity'])
    else:
        average_popularity = 0

    insights['average_popularity'] = average_popularity
    insights['trends'] = []

    # Simple heuristic: if a song's popularity is above the average, it's a trend
    for popularity in insights.get('popularity', []):
        if isinstance(popularity, (int, float)) and popularity > average_popularity:
            insights['trends'].append(popularity)
    return insights

def format_summary(analysis_results):
    """
    Formats the analyzed insights into a readable text summary.

    Args:
        analysis_results (dict): Insights obtained from analysis.

    Returns:
        str: A formatted summary text.
    """
    print("Formatting insights into summary...")

    # Validate that expected keys exist and are of correct types
    popular_artists = analysis_results.get('popular_artists', [])
    average_popularity = analysis_results.get('average_popularity', 0)
    trends = analysis_results.get('trends', [])

    summary = """Music Genre Analysis:

Popular Artists:
{}.

Identified Trends:
Average Popularity: {}
Songs with Above Average Popularity: {}
""".format(
        ', '.join(popular_artists),
        average_popularity,
        ', '.join(map(str, trends))
    )
    return summary


def display_output(summary):
    """
    Displays the formatted summary in the terminal.

    Args:
        summary (str): The formatted summary text.
    """
    print("Displaying the formatted summary...")
    print(summary)
