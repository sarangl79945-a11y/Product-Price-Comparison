# Product Price Comparison Website

A web application that allows users to search for products and compare prices across multiple e-commerce platforms: Flipkart, Amazon, Reliance Digital, and Croma.

## Features

- **Product Search**: Search for any product across all platforms simultaneously
- **Price Comparison**: View prices side-by-side from all platforms
- **Daily Price Tracking**: Track price changes over time using localStorage
- **Interactive Graphs**: Visualize price trends with Chart.js
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
price-comparison/
├── frontend/
│   ├── index.html      # Main HTML file
│   ├── styles.css      # Styling
│   └── app.js          # Frontend logic
├── backend/
│   ├── app.py          # Flask server
│   ├── requirements.txt
│   ├── utils.py        # Helper functions
│   └── scrapers/
│       ├── flipkart.py
│       ├── amazon.py
│       ├── reliance.py
│       └── croma.py
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd price-comparison/backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the Flask server:
```bash
python app.py
```

The backend server will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd price-comparison/frontend
```

2. Open `index.html` in a web browser, or use a local server:
   - Python: `python -m http.server 8000`
   - Node.js: `npx http-server`
   - Or simply open the file directly in a browser

3. The frontend will connect to the backend API at `http://localhost:5000`

## Usage

1. Start the backend server (see Backend Setup above)
2. Open the frontend in a web browser
3. Enter a product name in the search box (e.g., "iPhone", "Laptop", "TV")
4. Click "Search" or press Enter
5. View the search results showing products from all platforms
6. Click on a product card to see detailed price comparison and graph
7. Prices are automatically saved to localStorage for daily tracking

## API Endpoints

- `GET /api/search?query=<product_name>` - Search products across all platforms
- `GET /api/health` - Health check endpoint

## Technical Notes

- **Web Scraping**: The scrapers use BeautifulSoup4 to parse HTML. Some sites may have anti-scraping measures.
- **CORS**: The backend has CORS enabled to allow frontend access.
- **Storage**: Price history is stored in browser localStorage (limited to ~5-10MB).
- **Chart Library**: Uses Chart.js (loaded via CDN) for price visualization.

## Limitations

- Web scraping may be blocked by some e-commerce sites
- Scraping may violate terms of service of some platforms
- For production use, consider using official APIs if available
- Rate limiting may be needed for frequent requests

## Troubleshooting

- **Backend not connecting**: Make sure the Flask server is running on port 5000
- **No results**: Some sites may block scraping. Check browser console for errors.
- **CORS errors**: Ensure flask-cors is installed and CORS is enabled in app.py


