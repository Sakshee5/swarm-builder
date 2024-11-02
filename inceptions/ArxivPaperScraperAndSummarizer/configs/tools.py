# Tools configuration file



import requests
import xml.etree.ElementTree as ET

def fetch_paper(topic):
    """
    Fetches a research paper from arXiv related to the specified topic.

    Args:
        topic (str): The topic to search for in the arXiv database.

    Returns:
        dict: A dictionary containing information about the paper such as title, summary, and authors.
    """
    base_url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': f'all:{topic}',
        'start': 0,
        'max_results': 1
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        # Parse the arXiv API XML response to get paper information
        return _parse_response(response.content)
    else:
        return {'error': 'Failed to fetch paper from arXiv'}


def _parse_response(xml_content):
    """
    Parses the XML response from arXiv to retrieve paper details.

    Args:
        xml_content (bytes): XML response content from arXiv.

    Returns:
        dict: A dictionary with paper details such as title, summary, and authors.
    """
    root = ET.fromstring(xml_content)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}

    paper_info = {}

    for entry in root.findall('atom:entry', namespace):
        title = entry.find('atom:title', namespace).text
        summary = entry.find('atom:summary', namespace).text
        authors = [author.find('atom:name', namespace).text for author in entry.findall('atom:author', namespace)]

        paper_info['title'] = title
        paper_info['summary'] = summary
        paper_info['authors'] = authors

    return paper_info


from transformers import pipeline

def generate_summary(paper_info):
    """
    Generates a brief summary of the given research paper.

    Args:
        paper_info (dict): A dictionary containing the paper's title, summary, and authors.

    Returns:
        str: A summarized version of the paper's content.
    """
    summarizer = pipeline('summarization')
    summary_text = summarizer(paper_info['summary'], max_length=130, min_length=30, do_sample=False)
    return summary_text[0]['summary_text']
