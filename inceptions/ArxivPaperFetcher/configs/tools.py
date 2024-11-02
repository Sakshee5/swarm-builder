from transformers import pipeline
import requests
# Tools configuration file



def arXivAPI(topic: str):
    """
    Connects to the arXiv API to search for and retrieve the most recent papers on the specified topic.

    Args:
        topic (str): The topic to search for.

    Returns:
        dict: A dictionary containing information about the most recent paper.
    """
    import requests
    
    base_url = "http://export.arxiv.org/api/query"
    params = {
        'search_query': f'all:{topic}',
        'start': 0,
        'max_results': 1,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        # Parse the response to extract the necessary information for the recent paper
        # This is a placeholder for actual XML parsing
        return {'title': 'Sample Title', 'summary': 'Sample Summary', 'authors': ['Author1', 'Author2']}
    else:
        raise Exception("Failed to fetch data from arXiv API")

def NLP_Summarizer(text: str):
    """
    Uses a natural language processing library to generate a brief summary of the provided text.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: A brief summary of the text.
    """
    # Using transformers library's pipeline for summarization
    from transformers import pipeline
    
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
    return summary[0]['summary_text']