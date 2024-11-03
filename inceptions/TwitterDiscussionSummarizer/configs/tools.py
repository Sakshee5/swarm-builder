# Tools configuration file



import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
load_dotenv()

# Define the Twitter search function using Twitter API v2

def search_twitter(query, max_results=10):
    """
    Searches for tweets using the Twitter API v2.

    Args:
        bearer_token (str): The bearer token for authentication.
        query (str): The search query to use for finding tweets.
        max_results (int, optional): The maximum number of tweet results to return. Defaults to 10.

    Returns:
        dict: A dictionary containing the search results from Twitter.
    """
    url = "https://api.twitter.com/2/tweets/search/recent"
    bearer_token = os.getenv("TWITTER_KEY")
    headers = {
        'Authorization': f'Bearer {bearer_token}',
    }
    params = {
        'query': query,
        'max_results': max_results
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")  # Print the error for debugging
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")

    return response.json()


def collect_tweets(search_results):
    """
    Collect tweets from the search results.

    Args:
        search_results (dict): The search results obtained from the Twitter API.

    Returns:
        list: A list of tweet texts extracted from the search results.
    """
    tweets = [tweet['text'] for tweet in search_results.get('data', [])]
    return tweets

from collections import Counter

# Define a function to analyze the collected tweets
def analyze_tweets(tweets):
    """
    Analyzes the text of tweets to identify key themes and topics.

    Args:
        tweets (list): List of tweet texts.

    Returns:
        Counter: A counter object with the most common words/topics in the tweets as keys.
    """
    all_words = ' '.join(tweets).lower().split()
    word_count = Counter(all_words)
    common_words = word_count.most_common(10)
    return common_words



# Define a function to summarize discussions based on analyzed topics
def summarize_discussions(tweets, api_key):
    """
    Summarizes the discussions by generating a summary using OpenAI's GPT.

    Args:
        tweets (list): List of tweet texts.
        api_key (str): OpenAI API key for making requests to GPT.

    Returns:
        str: A summary of the main points and perspectives discovered in the tweets.
    """
    from dotenv import load_dotenv
    load_dotenv()
    import openai
    import os

    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()
    openai.api_key = api_key
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes key points and discussions from twitter feeds"},
            {"role": "user", "content": f"Analyze the following tweets and summarize the main points and discussions: {tweets}"}
        ]
    )
    result = response.choices[0].message.content
    return result