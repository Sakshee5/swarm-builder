import requests
from bs4 import BeautifulSoup

# Google Custom Search API setup
API_KEY = "AIzaSyAFgqauNFcsyn5_BmfHzk3VpZ4mXOsHGQU"
SEARCH_ENGINE_ID = "04d381c3e293144a2"

def web_search(query, question):
    """
    Perform a Google Custom Search to find API documentation and scrape the first URL for relevant information.
    """

    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 1 
    }
    
    response = requests.get(search_url, params=params)
    search_results = response.json()

    first_url = search_results["items"][0]["link"]

    page_response = requests.get(first_url)
    soup = BeautifulSoup(page_response.content, 'html.parser')
    page_text = soup.get_text(separator=' ', strip=True)

    extracted_info = query_gpt_for_information(page_text, question)

    return extracted_info


def query_gpt_for_information(content, question):
    """
    Send the scraped content to GPT or another LLM to extract relevant information.

    Args:
    content (str): The full scraped content.
    question (str): The question to ask (e.g., "What is the base URL?").

    Returns:
    str: The relevant answer extracted by the LLM.
    """
    from dotenv import load_dotenv
    import os
    load_dotenv()
    import openai

    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Based on the following documentation, {question}\n\n{content}"
        }
    ]
)
    
    return response.choices[0].message.content


# Example usage:
query = "Stripe API documentation"
question = "What is the base URL?"
result = web_search(query, question)
print("Extracted Info:", result)
