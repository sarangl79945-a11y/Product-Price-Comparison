import random
import re

# Product-specific real-time links dataset
PRODUCT_LINKS = {
    'Apple iPhone 15 Pro Max': {
        'flipkart': 'https://www.flipkart.com/search?q=iphone+15+pro+max',
        'amazon': 'https://www.amazon.in/s?k=iphone+15+pro+max',
        'reliance': 'https://www.reliancedigital.in/search?q=iphone+15+pro+max',
        'croma': 'https://www.croma.com/search?q=iphone+15+pro+max'
    },
    'Apple iPhone 15 Pro': {
        'flipkart': 'https://www.flipkart.com/search?q=iphone+15+pro',
        'amazon': 'https://www.amazon.in/s?k=iphone+15+pro',
        'reliance': 'https://www.reliancedigital.in/search?q=iphone+15+pro',
        'croma': 'https://www.croma.com/search?q=iphone+15+pro'
    },
    'Apple iPhone 15': {
        'flipkart': 'https://www.flipkart.com/search?q=iphone+15',
        'amazon': 'https://www.amazon.in/s?k=iphone+15',
        'reliance': 'https://www.reliancedigital.in/search?q=iphone+15',
        'croma': 'https://www.croma.com/search?q=iphone+15'
    },
    'Apple iPhone 14 Pro': {
        'flipkart': 'https://www.flipkart.com/search?q=iphone+14+pro',
        'amazon': 'https://www.amazon.in/s?k=iphone+14+pro',
        'reliance': 'https://www.reliancedigital.in/search?q=iphone+14+pro',
        'croma': 'https://www.croma.com/search?q=iphone+14+pro'
    },
    'Apple iPhone 14': {
        'flipkart': 'https://www.flipkart.com/search?q=iphone+14',
        'amazon': 'https://www.amazon.in/s?k=iphone+14',
        'reliance': 'https://www.reliancedigital.in/search?q=iphone+14',
        'croma': 'https://www.croma.com/search?q=iphone+14'
    },
    'Apple iPhone 13': {
        'flipkart': 'https://www.flipkart.com/search?q=iphone+13',
        'amazon': 'https://www.amazon.in/s?k=iphone+13',
        'reliance': 'https://www.reliancedigital.in/search?q=iphone+13',
        'croma': 'https://www.croma.com/search?q=iphone+13'
    },
    'MacBook Pro 16-inch M3 Pro': {
        'flipkart': 'https://www.flipkart.com/search?q=macbook+pro+16+m3',
        'amazon': 'https://www.amazon.in/s?k=macbook+pro+16+m3',
        'reliance': 'https://www.reliancedigital.in/search?q=macbook+pro+16+m3',
        'croma': 'https://www.croma.com/search?q=macbook+pro+16+m3'
    },
    'MacBook Air M2': {
        'flipkart': 'https://www.flipkart.com/search?q=macbook+air+m2',
        'amazon': 'https://www.amazon.in/s?k=macbook+air+m2',
        'reliance': 'https://www.reliancedigital.in/search?q=macbook+air+m2',
        'croma': 'https://www.croma.com/search?q=macbook+air+m2'
    },
    'Dell XPS 15': {
        'flipkart': 'https://www.flipkart.com/search?q=dell+xps+15',
        'amazon': 'https://www.amazon.in/s?k=dell+xps+15',
        'reliance': 'https://www.reliancedigital.in/search?q=dell+xps+15',
        'croma': 'https://www.croma.com/search?q=dell+xps+15'
    },
    'HP Pavilion 15': {
        'flipkart': 'https://www.flipkart.com/search?q=hp+pavilion+15',
        'amazon': 'https://www.amazon.in/s?k=hp+pavilion+15',
        'reliance': 'https://www.reliancedigital.in/search?q=hp+pavilion+15',
        'croma': 'https://www.croma.com/search?q=hp+pavilion+15'
    },
    'Lenovo ThinkPad E14': {
        'flipkart': 'https://www.flipkart.com/search?q=lenovo+thinkpad+e14',
        'amazon': 'https://www.amazon.in/s?k=lenovo+thinkpad+e14',
        'reliance': 'https://www.reliancedigital.in/search?q=lenovo+thinkpad+e14',
        'croma': 'https://www.croma.com/search?q=lenovo+thinkpad+e14'
    },
    'ASUS VivoBook 15': {
        'flipkart': 'https://www.flipkart.com/search?q=asus+vivobook+15',
        'amazon': 'https://www.amazon.in/s?k=asus+vivobook+15',
        'reliance': 'https://www.reliancedigital.in/search?q=asus+vivobook+15',
        'croma': 'https://www.croma.com/search?q=asus+vivobook+15'
    },
    'Samsung 55-inch 4K Smart TV': {
        'flipkart': 'https://www.flipkart.com/search?q=samsung+55+inch+4k+smart+tv',
        'amazon': 'https://www.amazon.in/s?k=samsung+55+inch+4k+smart+tv',
        'reliance': 'https://www.reliancedigital.in/search?q=samsung+55+inch+4k+smart+tv',
        'croma': 'https://www.croma.com/search?q=samsung+55+inch+4k+smart+tv'
    },
    'LG 55-inch OLED TV': {
        'flipkart': 'https://www.flipkart.com/search?q=lg+55+inch+oled+tv',
        'amazon': 'https://www.amazon.in/s?k=lg+55+inch+oled+tv',
        'reliance': 'https://www.reliancedigital.in/search?q=lg+55+inch+oled+tv',
        'croma': 'https://www.croma.com/search?q=lg+55+inch+oled+tv'
    },
    'Sony Bravia 55-inch 4K': {
        'flipkart': 'https://www.flipkart.com/search?q=sony+bravia+55+inch+4k',
        'amazon': 'https://www.amazon.in/s?k=sony+bravia+55+inch+4k',
        'reliance': 'https://www.reliancedigital.in/search?q=sony+bravia+55+inch+4k',
        'croma': 'https://www.croma.com/search?q=sony+bravia+55+inch+4k'
    },
    'OnePlus 55-inch QLED TV': {
        'flipkart': 'https://www.flipkart.com/search?q=oneplus+55+inch+qled+tv',
        'amazon': 'https://www.amazon.in/s?k=oneplus+55+inch+qled+tv',
        'reliance': 'https://www.reliancedigital.in/search?q=oneplus+55+inch+qled+tv',
        'croma': 'https://www.croma.com/search?q=oneplus+55+inch+qled+tv'
    },
    'Sony WH-1000XM5': {
        'flipkart': 'https://www.flipkart.com/search?q=sony+wh1000xm5',
        'amazon': 'https://www.amazon.in/s?k=sony+wh1000xm5',
        'reliance': 'https://www.reliancedigital.in/search?q=sony+wh1000xm5',
        'croma': 'https://www.croma.com/search?q=sony+wh1000xm5'
    },
    'Apple AirPods Pro 2': {
        'flipkart': 'https://www.flipkart.com/search?q=airpods+pro+2',
        'amazon': 'https://www.amazon.in/s?k=airpods+pro+2',
        'reliance': 'https://www.reliancedigital.in/search?q=airpods+pro+2',
        'croma': 'https://www.croma.com/search?q=airpods+pro+2'
    },
    'Bose QuietComfort 45': {
        'flipkart': 'https://www.flipkart.com/search?q=bose+quietcomfort+45',
        'amazon': 'https://www.amazon.in/s?k=bose+quietcomfort+45',
        'reliance': 'https://www.reliancedigital.in/search?q=bose+quietcomfort+45',
        'croma': 'https://www.croma.com/search?q=bose+quietcomfort+45'
    },
    'Apple Watch Series 9': {
        'flipkart': 'https://www.flipkart.com/search?q=apple+watch+series+9',
        'amazon': 'https://www.amazon.in/s?k=apple+watch+series+9',
        'reliance': 'https://www.reliancedigital.in/search?q=apple+watch+series+9',
        'croma': 'https://www.croma.com/search?q=apple+watch+series+9'
    },
    'Samsung Galaxy Watch 6': {
        'flipkart': 'https://www.flipkart.com/search?q=samsung+galaxy+watch+6',
        'amazon': 'https://www.amazon.in/s?k=samsung+galaxy+watch+6',
        'reliance': 'https://www.reliancedigital.in/search?q=samsung+galaxy+watch+6',
        'croma': 'https://www.croma.com/search?q=samsung+galaxy+watch+6'
    },
    'Canon EOS R6 Mark II': {
        'flipkart': 'https://www.flipkart.com/search?q=canon+eos+r6+mark+ii',
        'amazon': 'https://www.amazon.in/s?k=canon+eos+r6+mark+ii',
        'reliance': 'https://www.reliancedigital.in/search?q=canon+eos+r6+mark+ii',
        'croma': 'https://www.croma.com/search?q=canon+eos+r6+mark+ii'
    },
    'Sony Alpha 7 IV': {
        'flipkart': 'https://www.flipkart.com/search?q=sony+alpha+7+iv',
        'amazon': 'https://www.amazon.in/s?k=sony+alpha+7+iv',
        'reliance': 'https://www.reliancedigital.in/search?q=sony+alpha+7+iv',
        'croma': 'https://www.croma.com/search?q=sony+alpha+7+iv'
    }
}

# Mock product database with realistic prices
MOCK_PRODUCTS = {
    'iphone': [
        {
            'name': 'Apple iPhone 15 Pro Max',
            'base_price': 134900,
            'variations': ['128GB', '256GB', '512GB', '1TB'],
            'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400'
        },
        {
            'name': 'Apple iPhone 15 Pro',
            'base_price': 134900,
            'variations': ['128GB', '256GB', '512GB'],
            'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400'
        },
        {
            'name': 'Apple iPhone 15',
            'base_price': 79900,
            'variations': ['128GB', '256GB', '512GB'],
            'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400'
        },
        {
            'name': 'Apple iPhone 14 Pro',
            'base_price': 124900,
            'variations': ['128GB', '256GB', '512GB'],
            'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400'
        },
        {
            'name': 'Apple iPhone 14',
            'base_price': 59900,
            'variations': ['128GB', '256GB'],
            'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400'
        },
        {
            'name': 'Apple iPhone 13',
            'base_price': 49900,
            'variations': ['128GB', '256GB'],
            'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400'
        },
    ],
    'laptop': [
        {
            'name': 'MacBook Pro 16-inch M3 Pro',
            'base_price': 249900,
            'variations': ['512GB SSD', '1TB SSD', '2TB SSD'],
            'image': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400'
        },
        {
            'name': 'MacBook Air M2',
            'base_price': 114900,
            'variations': ['256GB SSD', '512GB SSD'],
            'image': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400'
        },
        {
            'name': 'Dell XPS 15',
            'base_price': 149990,
            'variations': ['16GB RAM', '32GB RAM'],
            'image': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400'
        },
        {
            'name': 'HP Pavilion 15',
            'base_price': 54990,
            'variations': ['8GB RAM', '16GB RAM'],
            'image': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400'
        },
        {
            'name': 'Lenovo ThinkPad E14',
            'base_price': 69990,
            'variations': ['8GB RAM', '16GB RAM'],
            'image': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400'
        },
        {
            'name': 'ASUS VivoBook 15',
            'base_price': 44990,
            'variations': ['8GB RAM', '16GB RAM'],
            'image': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400'
        },
    ],
    'tv': [
        {
            'name': 'Samsung 55-inch 4K Smart TV',
            'base_price': 54990,
            'variations': ['55"', '65"', '75"'],
            'image': 'https://images.unsplash.com/photo-1593359677879-a4b92b19c8ab?w=400'
        },
        {
            'name': 'LG 55-inch OLED TV',
            'base_price': 129990,
            'variations': ['55"', '65"'],
            'image': 'https://images.unsplash.com/photo-1593359677879-a4b92b19c8ab?w=400'
        },
        {
            'name': 'Sony Bravia 55-inch 4K',
            'base_price': 79990,
            'variations': ['55"', '65"'],
            'image': 'https://images.unsplash.com/photo-1593359677879-a4b92b19c8ab?w=400'
        },
        {
            'name': 'OnePlus 55-inch QLED TV',
            'base_price': 49990,
            'variations': ['55"', '65"'],
            'image': 'https://images.unsplash.com/photo-1593359677879-a4b92b19c8ab?w=400'
        },
    ],
    'headphone': [
        {
            'name': 'Sony WH-1000XM5',
            'base_price': 29990,
            'variations': ['Black', 'Silver'],
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
        },
        {
            'name': 'Apple AirPods Pro 2',
            'base_price': 24900,
            'variations': ['White'],
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
        },
        {
            'name': 'Bose QuietComfort 45',
            'base_price': 27990,
            'variations': ['Black', 'White'],
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
        },
    ],
    'watch': [
        {
            'name': 'Apple Watch Series 9',
            'base_price': 41900,
            'variations': ['41mm', '45mm'],
            'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400'
        },
        {
            'name': 'Samsung Galaxy Watch 6',
            'base_price': 29999,
            'variations': ['40mm', '44mm'],
            'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400'
        },
    ],
    'camera': [
        {
            'name': 'Canon EOS R6 Mark II',
            'base_price': 219990,
            'variations': ['Body Only', 'With 24-105mm'],
            'image': 'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400'
        },
        {
            'name': 'Sony Alpha 7 IV',
            'base_price': 229990,
            'variations': ['Body Only', 'With 28-70mm'],
            'image': 'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400'
        },
    ],
}

def get_price_variation(base_price, platform):
    """Generate price variations for different platforms"""
    # Different platforms have different pricing strategies
    variations = {
        'flipkart': random.uniform(0.95, 1.05),  # -5% to +5%
        'amazon': random.uniform(0.97, 1.03),   # -3% to +3%
        'reliance': random.uniform(0.96, 1.04), # -4% to +4%
        'croma': random.uniform(0.98, 1.02),   # -2% to +2%
    }
    multiplier = variations.get(platform, 1.0)
    return int(base_price * multiplier)

def fuzzy_match(query, product_name):
    """Check if query matches product name (case-insensitive, partial match)"""
    query_lower = query.lower().strip()
    name_lower = product_name.lower()
    
    # Direct match
    if query_lower in name_lower or name_lower in query_lower:
        return True
    
    # Remove common words and check
    query_words = set(re.sub(r'[^\w\s]', '', query_lower).split())
    name_words = set(re.sub(r'[^\w\s]', '', name_lower).split())
    
    # Check if significant words match
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    query_words = query_words - common_words
    name_words = name_words - common_words
    
    if len(query_words) > 0 and len(query_words & name_words) > 0:
        return True
    
    return False

def search_mock_products(query):
    """Search mock products based on query"""
    query_lower = query.lower().strip()
    results = []
    
    # First, check if query matches a category directly
    for category, products in MOCK_PRODUCTS.items():
        if query_lower in category or category in query_lower:
            # Return all products in this category
            results.extend(products)
            break
    
    # If no category match, search individual products
    if not results:
        for category, products in MOCK_PRODUCTS.items():
            for product in products:
                if fuzzy_match(query, product['name']):
                    results.append(product)
    
    # If still no results, try broader search with keywords
    if not results:
        keywords = {
            'phone': 'iphone',
            'mobile': 'iphone',
            'smartphone': 'iphone',
            'notebook': 'laptop',
            'computer': 'laptop',
            'television': 'tv',
            'earphone': 'headphone',
            'earbuds': 'headphone',
        }
        
        for keyword, category in keywords.items():
            if keyword in query_lower:
                results.extend(MOCK_PRODUCTS[category][:5])  # Return first 5
                break
    
    # Remove duplicates and limit results
    seen = set()
    unique_results = []
    for product in results:
        product_id = product['name']
        if product_id not in seen:
            seen.add(product_id)
            unique_results.append(product)
    
    return unique_results[:10]

def generate_product_data(product, query):
    """Generate product data with prices from all platforms"""
    import urllib.parse
    
    platforms = ['flipkart', 'amazon', 'reliance', 'croma']
    prices = {}
    product_name = product['name']
    
    # Get product-specific links from dataset, or generate fallback URLs
    if product_name in PRODUCT_LINKS:
        # Use real-time product-specific links from dataset
        platform_urls = PRODUCT_LINKS[product_name]
    else:
        # Fallback: Generate URLs from product name
        clean_query = query.strip()
        query_encoded = urllib.parse.quote_plus(clean_query)
        
        platform_urls = {
            'flipkart': f'https://www.flipkart.com/search?q={query_encoded}',
            'amazon': f'https://www.amazon.in/s?k={query_encoded}',
            'reliance': f'https://www.reliancedigital.in/search?q={query_encoded}',
            'croma': f'https://www.croma.com/search?q={query_encoded}'
        }
    
    for platform in platforms:
        price = get_price_variation(product['base_price'], platform)
        # Use product-specific URL if available, otherwise use generated URL
        url = platform_urls.get(platform, f'https://www.{platform}.com/search?q={urllib.parse.quote_plus(query)}')
        
        prices[platform] = {
            'price': price,
            'url': url,
            'image': product.get('image', '')
        }
    
    return {
        'name': product['name'],
        'model': product['name'],
        'prices': prices
    }

def get_mock_results(query):
    """Get mock search results for a query"""
    products = search_mock_products(query)
    
    if not products:
        return []
    
    results = []
    for product in products:
        results.append(generate_product_data(product, query))
    
    return results
