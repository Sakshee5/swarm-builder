# Tools configuration file
from dotenv import load_dotenv
import os
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()


def get_latest_bitcoin_price():
    """
    Fetches the latest Bitcoin price using the CoinGecko API.

    Returns:
        float: Latest Bitcoin price in USD.
    """
    import requests
    try:
        api_url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data['bitcoin']['usd']
        else:
            raise ValueError("Failed to fetch data from CoinGecko API")
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_24_hour_price_change():
    """
    Fetches the 24-hour price change for Bitcoin using the CoinGecko API.

    Returns:
        float: 24-hour price change for Bitcoin in percentage.
    """
    import requests
    try:
        api_url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data['bitcoin']['usd_24h_change']
        else:
            raise ValueError("Failed to fetch data from CoinGecko API")
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_recent_bitcoin_news():
    """
    Fetches the most recent news articles related to Bitcoin using the NewsAPI.

    Returns:
        list: A list of dictionaries containing recent Bitcoin news headlines and summaries.
    """
    import requests
    try:
        api_key = os.getenv("NEWS_API_KEY")
        url = f'https://newsapi.org/v2/everything?q=bitcoin&apiKey={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json()["articles"]
            news_summary = [
                {
                    "title": article["title"],
                    "description": article.get("description", "No description available"),
                    "url": article["url"]
                }
                for article in articles
            ]
            return news_summary
        else:
            raise ValueError("Failed to fetch data from NewsAPI")
    except Exception as e:
        print(f"Error: {e}")
        return []

def delegate_to_price_agent():
    """
    Delegates the task to the Price Agent to fetch the latest Bitcoin price and 24-hour price change.

    Returns:
        dict: Dictionary containing the latest Bitcoin price and 24-hour price change.
    """
    price = get_latest_bitcoin_price()
    price_change_24h = get_24_hour_price_change()
    return {"latest_price": price, "price_change_24h": price_change_24h}

def delegate_to_news_agent(api_key):
    """
    Delegates the task to the News Agent to fetch recent Bitcoin news.

    Args:
        api_key (str): Your NewsAPI key to authenticate the API request.

    Returns:
        list: List of recent Bitcoin news summaries.
    """
    return fetch_recent_bitcoin_news()

def aggregate_information(price_data, news_data):
    """
    Aggregates the information from the Price and News agents into a comprehensive report.

    Args:
        price_data (dict): Dictionary containing Bitcoin's latest price and 24-hour price change.
        news_data (list): List containing recent Bitcoin news summaries.

    Returns:
        str: A summarized report of Bitcoin's price and news.
    """
 
    price_summary = price_data
    news_summary = "\n".join([article for article in news_data])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are summarizing price and news information for Bitcoin."},
            {"role": "user", "content": f"Price Information:\n{price_summary}\nNews Information:\n{news_summary}"}
        ]
    )
    return response.choices[0].message.content