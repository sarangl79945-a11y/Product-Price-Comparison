from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import concurrent.futures
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from mock_data import get_mock_results

# Optional scrapers. The app continues to work with mock data if imports fail.
try:
    from scrapers.flipkart import search_flipkart
    from scrapers.amazon import search_amazon
    from scrapers.reliance import search_reliance
    from scrapers.croma import search_croma
    SCRAPING_ENABLED = True
except Exception as exc:
    print(f"Scrapers unavailable; using mock data only: {exc}")
    SCRAPING_ENABLED = False

app = Flask(__name__)
CORS(app)

# Keep False for reliable demo/deployment with sample data.
# Enable only after confirming scrapers work reliably on your hosting provider.
USE_REAL_SCRAPING = False


@app.route("/", methods=["GET"])
def index():
    """Serve the website homepage."""
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/app.js", methods=["GET"])
def javascript_file():
    """Serve the frontend JavaScript."""
    return send_from_directory(BASE_DIR, "app.js")


@app.route("/styles.css", methods=["GET"])
def css_file():
    """Serve the frontend stylesheet."""
    return send_from_directory(BASE_DIR, "styles.css")


@app.route("/api/search", methods=["GET"])
def search_products():
    """Search products and return mock data, or scraper data if enabled."""
    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    results = {
        "query": query,
        "products": []
    }

    mock_results = get_mock_results(query)
    scraped_results = []

    if USE_REAL_SCRAPING and SCRAPING_ENABLED:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = {
                    "flipkart": executor.submit(search_flipkart, query),
                    "amazon": executor.submit(search_amazon, query),
                    "reliance": executor.submit(search_reliance, query),
                    "croma": executor.submit(search_croma, query),
                }

                platform_results = {}
                for platform, future in futures.items():
                    try:
                        platform_results[platform] = future.result(timeout=10) or []
                    except Exception as exc:
                        print(f"{platform} scraper failed: {exc}")
                        platform_results[platform] = []

            product_map = {}

            for platform, items in platform_results.items():
                for item in items:
                    model = item.get("model") or item.get("name") or ""
                    model_key = model.lower().strip()

                    if not model_key:
                        continue

                    if model_key not in product_map:
                        product_map[model_key] = {
                            "name": item.get("name") or model,
                            "model": model,
                            "prices": {}
                        }

                    product_map[model_key]["prices"][platform] = {
                        "price": item.get("price", 0),
                        "url": item.get("url", ""),
                        "image": item.get("image", "")
                    }

            scraped_results = list(product_map.values())

        except Exception as exc:
            print(f"Scraping error: {exc}")
            scraped_results = []

    results["products"] = (
        scraped_results if scraped_results else mock_results
    )

    return jsonify(results)


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # Local development only. Render starts the app with Gunicorn.
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )