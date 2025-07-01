import requests
from bs4 import BeautifulSoup
import sys
from typing import Optional, Dict

# Function to scrape an article from a given URL
def fetch_article(url: str) -> Optional[Dict[str, str]]:

    " Fetch the raw HTML content of the article at the given URL. "
    "return the HTML content as a string if successful, None otherwise."

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'
        content = soup.get_text(separator='\n', strip=True)
        return { 
            'title': title,
            'content': content,
            'url': url
        }
    except requests.RequestException as e:
        print(f"Error fetching article from {url}: {e}", file=sys.stderr)
        return None
    

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_article.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    article = fetch_article(url)
    
    if article:
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Content:\n{article['content'][:500]}...")  # Print first 500 characters of content
    else:
        print("Failed to fetch the article.")
