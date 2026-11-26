
import os
import sys
import concurrent.futures
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from mock_data import get_mock_results

# Optional scrapers
try:
    from scrapers.flipkart import search_flipkart
except Exception:
    search_flipkart = None

try:
    from scrapers.amazon import search_amazon
except Exception:
    search_amazon = None

try:
    from scrapers.reliance import search_reliance
except Exception:
    search_reliance = None

try:
    from scrapers.croma import search_croma
except Exception:
    search_croma = None


app = Flask(__name__)
CORS(app)

# Scraping is disabled by default for stable free hosting.
# Set USE_REAL_SCRAPING=true in Render environment variables
# if you want to enable the scrapers.
USE_REAL_SCRAPING = (
    os.getenv("USE_REAL_SCRAPING", "false").lower() == "true"
)


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/app.js")
def javascript():
    return send_from_directory(BASE_DIR, "app.js")


@app.route("/styles.css")
def stylesheet():
    return send_from_directory(BASE_DIR, "styles.css")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api")
def api_info():
    return jsonify({
        "message": "Product Price Comparison API",
        "endpoints": {
            "health": "/api/health",
            "search": "/api/search?query=<product_name>"
        }
    }), 200


def run_scraper(scraper, query):
    """Run one scraper safely."""
    if scraper is None:
        return []

    try:
        data = scraper(query)

        if data is None:
            return []

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            if isinstance(data.get("results"), list):
                return data["results"]
            return [data]

        return []

    except Exception as exc:
        app.logger.warning("A product scraper failed: %s", exc)
        return []


def get_scraped_results(query):
    """Run available scrapers concurrently."""
    scraper_functions = [
        search_amazon,
        search_flipkart,
        search_croma,
        search_reliance,
    ]

    scraper_functions = [
        scraper for scraper in scraper_functions
        if scraper is not None
    ]

    if not scraper_functions:
        return []

    combined_results = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=min(4, len(scraper_functions))
    ) as executor:

        futures = [
            executor.submit(run_scraper, scraper, query)
            for scraper in scraper_functions
        ]

        for future in concurrent.futures.as_completed(
            futures, timeout=45
        ):
            try:
                combined_results.extend(future.result())
            except Exception as exc:
                app.logger.warning(
                    "Scraper task failed: %s", exc
                )

    return combined_results


@app.route("/api/search", methods=["GET"])
def search_products():
    """Search products using mock data and optional scrapers."""

    query = (
        request.args.get("query")
        or request.args.get("q")
        or ""
    ).strip()

    if not query:
        return jsonify({
            "error": "Please provide a product name."
        }), 400

    try:
        # Use the project's mock data.
        mock_results = get_mock_results(query)

        # Stable default for Render free hosting.
        if not USE_REAL_SCRAPING:
            return jsonify(mock_results), 200

        # Optional real scraping.
        scraped_results = get_scraped_results(query)

        # Preserve the response format from mock_data.py.
        if isinstance(mock_results, dict):

            if isinstance(mock_results.get("results"), list):
                mock_results["results"].extend(
                    scraped_results
                )
                return jsonify(mock_results), 200

            return jsonify(mock_results), 200

        if isinstance(mock_results, list):
            return jsonify(
                mock_results + scraped_results
            ), 200

        return jsonify({
            "query": query,
            "results": scraped_results
        }), 200

    except Exception:
        app.logger.exception("Product search failed")

        return jsonify({
            "error": "Product search failed. Please try again."
        }), 500


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({
            "error": "API endpoint not found"
        }), 404

    return jsonify({
        "error": "Page not found"
    }), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
