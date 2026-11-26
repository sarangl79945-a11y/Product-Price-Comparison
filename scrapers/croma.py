from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_headers, extract_price, clean_text, fetch_page
import urllib.parse

def search_croma(query):
    """Search products on Croma"""
    try:
        # Encode query for URL
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.croma.com/search/?q={encoded_query}"
        
        html = fetch_page(search_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # Croma product containers
        product_divs = soup.find_all('div', {'class': 'product-item'}) or soup.find_all('li', {'class': 'product-item'}) or soup.find_all('div', {'class': 'cp-product'})
        
        for div in product_divs[:10]:  # Limit to 10 results
            try:
                # Product name
                name_elem = div.find('h3', {'class': 'product-title'}) or div.find('a', {'class': 'product-title'}) or div.find('h2', {'class': 'product-title'})
                if not name_elem:
                    continue
                
                name = clean_text(name_elem.get_text())
                if not name:
                    continue
                
                # Product URL
                link_elem = name_elem.find('a') if name_elem.name != 'a' else name_elem
                url = ''
                if link_elem and link_elem.get('href'):
                    href = link_elem.get('href')
                    url = f"https://www.croma.com{href}" if href.startswith('/') else href
                
                # Price
                price_elem = div.find('span', {'class': 'amount'}) or div.find('span', {'class': 'price'}) or div.find('div', {'class': 'product-price'})
                price = 0
                if price_elem:
                    price = extract_price(price_elem.get_text())
                
                # Image
                img_elem = div.find('img', {'class': 'product-image'}) or div.find('img')
                image = ''
                if img_elem and (img_elem.get('src') or img_elem.get('data-src')):
                    image = img_elem.get('src') or img_elem.get('data-src')
                
                if name and price > 0:
                    products.append({
                        'name': name,
                        'model': name,  # Use name as model for now
                        'price': price,
                        'url': url,
                        'image': image,
                        'platform': 'croma'
                    })
            except Exception as e:
                continue
        
        return products
    except Exception as e:
        print(f"Error searching Croma: {e}")
        return []

