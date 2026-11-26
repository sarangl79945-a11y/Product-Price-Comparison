from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_headers, extract_price, clean_text, fetch_page
import urllib.parse

def search_amazon(query):
    """Search products on Amazon"""
    try:
        # Encode query for URL
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.amazon.in/s?k={encoded_query}"
        
        html = fetch_page(search_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # Amazon product containers
        product_divs = soup.find_all('div', {'data-component-type': 's-search-result'}) or soup.find_all('div', {'class': 's-result-item'})
        
        for div in product_divs[:10]:  # Limit to 10 results
            try:
                # Product name
                name_elem = div.find('h2', {'class': 'a-size-mini'}) or div.find('h2', {'class': 'a-size-base-plus'}) or div.find('span', {'class': 'a-size-medium'})
                if not name_elem:
                    continue
                
                name = clean_text(name_elem.get_text())
                if not name:
                    continue
                
                # Product URL
                link_elem = name_elem.find('a') or div.find('a', {'class': 'a-link-normal'})
                url = ''
                if link_elem and link_elem.get('href'):
                    href = link_elem.get('href')
                    url = f"https://www.amazon.in{href}" if href.startswith('/') else href
                
                # Price
                price_elem = div.find('span', {'class': 'a-price-whole'}) or div.find('span', {'class': 'a-offscreen'})
                price = 0
                if price_elem:
                    price_text = price_elem.get_text()
                    price = extract_price(price_text)
                
                # Image
                img_elem = div.find('img', {'class': 's-image'}) or div.find('img')
                image = ''
                if img_elem and img_elem.get('src'):
                    image = img_elem.get('src')
                
                if name and price > 0:
                    products.append({
                        'name': name,
                        'model': name,  # Use name as model for now
                        'price': price,
                        'url': url,
                        'image': image,
                        'platform': 'amazon'
                    })
            except Exception as e:
                continue
        
        return products
    except Exception as e:
        print(f"Error searching Amazon: {e}")
        return []

