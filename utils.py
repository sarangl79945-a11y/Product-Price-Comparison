import requests
from bs4 import BeautifulSoup
import re

def get_headers():
    """Return headers to mimic a real browser"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def extract_price(price_text):
    """Extract numeric price from text"""
    if not price_text:
        return 0
    
    # Remove currency symbols and commas
    price_text = re.sub(r'[₹,Rs\.\s]', '', str(price_text))
    
    # Extract numbers
    numbers = re.findall(r'\d+', price_text)
    if numbers:
        try:
            return int(''.join(numbers))
        except ValueError:
            return 0
    return 0

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ''
    return ' '.join(text.split())

def fetch_page(url, headers=None):
    """Fetch a webpage with error handling"""
    if headers is None:
        headers = get_headers()
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


