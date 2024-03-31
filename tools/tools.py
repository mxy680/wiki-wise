import requests
from bs4 import BeautifulSoup

def get_wiki_url(topic: str) -> str:
    """Get the wikipedia url for a given topic."""
    url = f"https://en.wikipedia.org/wiki/{topic}"
    response = requests.get(url)
    if response.status_code == 200:
        return url
    else:
        return 'No wikipedia page found. Try changing your capitalization'