from flask import Flask, request, jsonify
from flask_cors import CORS
import concurrent.futures
import sys
import os 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mock_data import get_mock_results
# Optional: Keep scrapers for fallback
try:
    from scrapers.flipkart import search_flipkart
    from scrapers.amazon import search_amazon
    from scrapers.reliance import search_reliance
    from scrapers.croma import search_croma
    SCRAPING_ENABLED = True
except:
    SCRAPING_ENABLED = False

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Enable/disable real scraping (set to False to use only mock data)
USE_REAL_SCRAPING = False

@app.route('/', methods=['GET'])
def index():
    """Root endpoint - provides API information"""
    return jsonify({
        'message': 'Product Price Comparison API',
        'endpoints': {
            'search': '/api/search?query=<product_name>',
            'health': '/api/health'
        },
        'instructions': 'Open the frontend/index.html file in your browser to use the web interface'
    })

@app.route('/api/search', methods=['GET'])
def search_products():
    """Search products across all e-commerce platforms"""
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    results = {
        'query': query,
        'products': []
    }
    
    # Use mock data as primary source
    mock_results = get_mock_results(query)
    
    # Optionally try real scraping if enabled
    scraped_results = []
    if USE_REAL_SCRAPING and SCRAPING_ENABLED:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                future_flipkart = executor.submit(search_flipkart, query)
                future_amazon = executor.submit(search_amazon, query)
                future_reliance = executor.submit(search_reliance, query)
                future_croma = executor.submit(search_croma, query)
                
                try:
                    flipkart_results = future_flipkart.result(timeout=10)
                except Exception as e:
                    flipkart_results = []
                
                try:
                    amazon_results = future_amazon.result(timeout=10)
                except Exception as e:
                    amazon_results = []
                
                try:
                    reliance_results = future_reliance.result(timeout=10)
                except Exception as e:
                    reliance_results = []
                
                try:
                    croma_results = future_croma.result(timeout=10)
                except Exception as e:
                    croma_results = []
            
            # Combine scraped results by product model
            product_map = {}
            
            for item in flipkart_results:
                model_key = item.get('model', item.get('name', '')).lower()
                if model_key not in product_map:
                    product_map[model_key] = {
                        'name': item.get('name', ''),
                        'model': item.get('model', item.get('name', '')),
                        'prices': {}
                    }
                product_map[model_key]['prices']['flipkart'] = {
                    'price': item.get('price', 0),
                    'url': item.get('url', ''),
                    'image': item.get('image', '')
                }
            
            for item in amazon_results:
                model_key = item.get('model', item.get('name', '')).lower()
                if model_key not in product_map:
                    product_map[model_key] = {
                        'name': item.get('name', ''),
                        'model': item.get('model', item.get('name', '')),
                        'prices': {}
                    }
                product_map[model_key]['prices']['amazon'] = {
                    'price': item.get('price', 0),
                    'url': item.get('url', ''),
                    'image': item.get('image', '')
                }
            
            for item in reliance_results:
                model_key = item.get('model', item.get('name', '')).lower()
                if model_key not in product_map:
                    product_map[model_key] = {
                        'name': item.get('name', ''),
                        'model': item.get('model', item.get('name', '')),
                        'prices': {}
                    }
                product_map[model_key]['prices']['reliance'] = {
                    'price': item.get('price', 0),
                    'url': item.get('url', ''),
                    'image': item.get('image', '')
                }
            
            for item in croma_results:
                model_key = item.get('model', item.get('name', '')).lower()
                if model_key not in product_map:
                    product_map[model_key] = {
                        'name': item.get('name', ''),
                        'model': item.get('model', item.get('name', '')),
                        'prices': {}
                    }
                product_map[model_key]['prices']['croma'] = {
                    'price': item.get('price', 0),
                    'url': item.get('url', ''),
                    'image': item.get('image', '')
                }
            
            scraped_results = list(product_map.values())
        except Exception as e:
            print(f"Scraping error: {e}")
            scraped_results = []
    
    # Combine mock and scraped results (prefer scraped if available, otherwise use mock)
    if scraped_results and len(scraped_results) > 0:
        results['products'] = scraped_results
    else:
        results['products'] = mock_results
    
    return jsonify(results)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

