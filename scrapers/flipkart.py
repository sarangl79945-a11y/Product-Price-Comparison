from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_headers, extract_price, clean_text, fetch_page
import urllib.parse

def search_flipkart(query):
    """Search products on Flipkart"""
    try:
        # Encode query for URL
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.flipkart.com/search?q={encoded_query}"
        
        html = fetch_page(search_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # Flipkart product containers
        product_divs = soup.find_all('div', {'class': '_1AtVbE'}) or soup.find_all('div', {'class': '_2kHMtA'}) or soup.find_all('div', {'class': '_4ddWXP'})
        
        for div in product_divs[:10]:  # Limit to 10 results
            try:
                # Product name
                name_elem = div.find('a', {'class': '_1fQZEK'}) or div.find('a', {'class': 's1Q9rs'}) or div.find('div', {'class': '_4rR01T'})
                if not name_elem:
                    continue
                
                name = clean_text(name_elem.get_text())
                if not name:
                    continue
                
                # Product URL
                link_elem = div.find('a', {'class': '_1fQZEK'}) or div.find('a', {'class': 's1Q9rs'})
                url = ''
                if link_elem and link_elem.get('href'):
                    href = link_elem.get('href')
                    url = f"https://www.flipkart.com{href}" if href.startswith('/') else href
                
                # Price
                price_elem = div.find('div', {'class': '_30jeq3'}) or div.find('div', {'class': '_30jeq3 _1_WHN1'})
                price = 0
                if price_elem:
                    price = extract_price(price_elem.get_text())
                
                # Image
                img_elem = div.find('img', {'class': '_396cs4'}) or div.find('img')
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
                        'platform': 'flipkart'
                    })
            except Exception as e:
                continue
        
        return products
    except Exception as e:
        print(f"Error searching Flipkart: {e}")
        return []

