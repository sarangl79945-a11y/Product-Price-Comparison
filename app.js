const API_BASE_URL = '/api';
const STORAGE_KEY = 'price_comparison_history';

let priceChart = null;
let currentProducts = [];

document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');

    if (searchBtn) {
        searchBtn.addEventListener('click', handleSearch);
    }

    if (searchInput) {
        searchInput.addEventListener('keypress', event => {
            if (event.key === 'Enter') {
                handleSearch();
            }
        });
    }
});

async function handleSearch() {
    const input = document.getElementById('searchInput');
    const query = input ? input.value.trim() : '';

    if (!query) {
        showError('Please enter a product name to search');
        return;
    }

    showLoading(true);
    hideError();
    hideResults();

    try {
        const response = await fetch(
            `${API_BASE_URL}/search?query=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Support both direct lists and object responses.
        if (Array.isArray(data)) {
            currentProducts = data;
        } else if (data && Array.isArray(data.products)) {
            currentProducts = data.products;
        } else if (data && Array.isArray(data.results)) {
            currentProducts = data.results;
        } else {
            currentProducts = [];
        }

        if (currentProducts.length === 0) {
            showError(
                'No products found. Try iphone, laptop, tv, headphone, watch, or camera.'
            );
            return;
        }

        displayProducts(currentProducts);
        saveToHistory(query, currentProducts);
        showResults();

    } catch (error) {
        console.error('Search error:', error);

        showError(
            `Unable to search products: ${error.message}. Check that the Flask backend is running.`
        );

    } finally {
        showLoading(false);
    }
}

function displayProducts(products) {
    const productList = document.getElementById('productList');

    if (!productList) return;

    productList.innerHTML = '';

    products.forEach((product, index) => {
        const card = document.createElement('div');

        card.className = 'product-card';
        card.dataset.index = index;

        const prices = product.prices || {};

        const imageUrl = Object.values(prices)
            .map(item => item && item.image)
            .find(Boolean) ||
            'https://via.placeholder.com/200?text=No+Image';

        const platforms = [
            'flipkart',
            'amazon',
            'reliance',
            'croma'
        ];

        const priceItems = platforms.map(platform => {
            const priceData = prices[platform];

            if (priceData && Number(priceData.price) > 0) {
                return `
                    <div class="price-item">
                        <span class="platform-name">${platform}</span>
                        <span class="platform-price">
                            ₹${formatPrice(priceData.price)}
                        </span>
                    </div>
                `;
            }

            return `
                <div class="price-item">
                    <span class="platform-name">${platform}</span>
                    <span class="no-price">Not available</span>
                </div>
            `;
        }).join('');

        const availablePrices = Object.entries(prices)
            .filter(([, item]) => item && Number(item.price) > 0)
            .map(([platform, item]) => ({
                platform,
                price: Number(item.price),
                url: item.url || '#'
            }));

        const bestPrice = availablePrices.length
            ? availablePrices.reduce((lowest, item) =>
                item.price < lowest.price ? item : lowest
            )
            : null;

        card.innerHTML = `
            <img
                src="${imageUrl}"
                alt="${escapeHTML(product.name || 'Product')}"
                onerror="this.src='https://via.placeholder.com/200?text=No+Image'"
            >

            <h4>${escapeHTML(product.name || 'Product')}</h4>

            <div class="product-prices">
                ${priceItems}
            </div>

            ${
                bestPrice
                    ? `
                        <a
                            href="${bestPrice.url}"
                            target="_blank"
                            rel="noopener noreferrer"
                            class="product-link"
                            onclick="event.stopPropagation()"
                        >
                            Best Price: ₹${formatPrice(bestPrice.price)}
                        </a>
                    `
                    : ''
            }
        `;

        card.addEventListener('click', () => {
            selectProduct(index);
        });

        productList.appendChild(card);
    });
}

function selectProduct(index) {
    document.querySelectorAll('.product-card').forEach(card => {
        card.classList.remove('selected');
    });

    const card = document.querySelector(`[data-index="${index}"]`);

    if (card) {
        card.classList.add('selected');
    }

    const product = currentProducts[index];

    if (product) {
        displayComparison(product);
        displayGraph(product);
    }
}

function displayComparison(product) {
    const section = document.getElementById('comparisonSection');
    const table = document.getElementById('comparisonTable');

    if (!section || !table) return;

    section.style.display = 'block';

    const platforms = [
        { key: 'flipkart', name: 'Flipkart' },
        { key: 'amazon', name: 'Amazon' },
        { key: 'reliance', name: 'Reliance Digital' },
        { key: 'croma', name: 'Croma' }
    ];

    let html = `
        <table>
            <thead>
                <tr>
                    <th>Platform</th>
                    <th>Price</th>
                    <th>Link</th>
                </tr>
            </thead>
            <tbody>
    `;

    platforms.forEach(platform => {
        const item = (product.prices || {})[platform.key];

        if (item && Number(item.price) > 0) {
            html += `
                <tr>
                    <td>${platform.name}</td>
                    <td class="price-cell">
                        ₹${formatPrice(item.price)}
                    </td>
                    <td>
                        <a
                            href="${item.url || '#'}"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            View Product
                        </a>
                    </td>
                </tr>
            `;
        } else {
            html += `
                <tr>
                    <td>${platform.name}</td>
                    <td class="price-cell na">Not Available</td>
                    <td>-</td>
                </tr>
            `;
        }
    });

    html += `
            </tbody>
        </table>
    `;

    table.innerHTML = html;
}

function displayGraph(product) {
    const graphSection = document.getElementById('graphSection');
    const chartCanvas = document.getElementById('priceChart');

    if (
        !graphSection ||
        !chartCanvas ||
        typeof Chart === 'undefined'
    ) {
        return;
    }

    graphSection.style.display = 'block';

    const history = getHistory();
    const productKey = product.model || product.name;
    const today = new Date().toISOString().split('T')[0];

    const platforms = [
        'flipkart',
        'amazon',
        'reliance',
        'croma'
    ];

    let dates = [today];

    if (history[productKey]) {
        dates = [
            ...Object.keys(history[productKey]).filter(date => date !== today),
            today
        ];
    }

    dates = [...new Set(dates)].sort().slice(-30);

    const datasets = platforms.map(platform => ({
        label: platform.charAt(0).toUpperCase() + platform.slice(1),

        data: dates.map(date => {
            if (date === today) {
                const item = (product.prices || {})[platform];

                return item && Number(item.price) > 0
                    ? Number(item.price)
                    : null;
            }

            return history[productKey]?.[date]?.[platform] || null;
        }),

        borderColor: getPlatformColor(platform),
        backgroundColor: getPlatformColor(platform, 0.1),
        tension: 0.1,
        fill: false
    }));

    if (priceChart) {
        priceChart.destroy();
    }

    priceChart = new Chart(chartCanvas, {
        type: 'line',

        data: {
            labels: dates,
            datasets: datasets
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                title: {
                    display: true,
                    text: `Price Trend: ${product.name}`
                },

                legend: {
                    display: true,
                    position: 'top'
                }
            },

            scales: {
                y: {
                    beginAtZero: false,

                    ticks: {
                        callback: value => '₹' + formatPrice(value)
                    }
                }
            }
        }
    });
}

function saveToHistory(query, products) {
    const history = getHistory();
    const today = new Date().toISOString().split('T')[0];

    products.forEach(product => {
        const key = product.model || product.name;

        if (!key) return;

        history[key] ||= {};
        history[key][today] ||= {};

        [
            'flipkart',
            'amazon',
            'reliance',
            'croma'
        ].forEach(platform => {
            const item = (product.prices || {})[platform];

            if (item && Number(item.price) > 0) {
                history[key][today][platform] = Number(item.price);
            }
        });
    });

    Object.keys(history).forEach(key => {
        const dates = Object.keys(history[key]).sort();

        dates
            .slice(0, Math.max(0, dates.length - 30))
            .forEach(date => {
                delete history[key][date];
            });
    });

    try {
        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(history)
        );
    } catch (error) {
        console.warn('Could not save price history:', error);
    }
}

function getHistory() {
    try {
        return JSON.parse(
            localStorage.getItem(STORAGE_KEY) || '{}'
        );
    } catch (error) {
        return {};
    }
}

function getPlatformColor(platform, alpha = 1) {
    const colors = {
        flipkart: `rgba(40, 116, 240, ${alpha})`,
        amazon: `rgba(255, 153, 0, ${alpha})`,
        reliance: `rgba(0, 102, 204, ${alpha})`,
        croma: `rgba(220, 38, 38, ${alpha})`
    };

    return colors[platform] ||
        `rgba(102, 126, 234, ${alpha})`;
}

function formatPrice(price) {
    const number = Number(price);

    if (!Number.isFinite(number)) {
        return '0';
    }

    return Math.round(number).toLocaleString('en-IN');
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, character => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    })[character]);
}

function showLoading(show) {
    const element = document.getElementById('loadingIndicator');

    if (element) {
        element.style.display = show ? 'block' : 'none';
    }
}

function hideError() {
    const element = document.getElementById('errorMessage');

    if (element) {
        element.style.display = 'none';
    }
}

function showError(message) {
    const element = document.getElementById('errorMessage');

    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    }
}

function showResults() {
    const element = document.getElementById('resultsSection');

    if (element) {
        element.style.display = 'block';
    }
}

function hideResults() {
    [
        'resultsSection',
        'comparisonSection',
        'graphSection'
    ].forEach(id => {
        const element = document.getElementById(id);

        if (element) {
            element.style.display = 'none';
        }
    });
}

// Side navigation
const sidenav = document.querySelector('.side-navbar');

function shownavbar() {
    if (sidenav) {
        sidenav.style.left = '0';
    }
}

function closenavbar() {
    if (sidenav) {
        sidenav.style.left = '-50%';
    }
}

// Animated background
const canvas = document.createElement('canvas');
const backgroundContext = canvas.getContext('2d');
const backgroundContainer = document.querySelector('.animated-background');

if (backgroundContainer) {
    backgroundContainer.appendChild(canvas);
}

let width = 0;
let height = 0;

const dots = [];
const numDots = 200;

function resizeCanvas() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;

    createDots();
}

function createDots() {
    dots.length = 0;

    for (let i = 0; i < numDots; i++) {
        dots.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 2 + 1,
            vx: Math.random() * 0.5 - 0.25,
            vy: Math.random() * 0.5 - 0.25,
            color: 'rgba(50, 150, 255, 0.8)'
        });
    }
}

function drawDots() {
    if (!backgroundContext) return;

    backgroundContext.clearRect(0, 0, width, height);

    for (let i = 0; i < dots.length; i++) {
        const first = dots[i];

        for (let j = i + 1; j < dots.length; j++) {
            const second = dots[j];

            const dx = first.x - second.x;
            const dy = first.y - second.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 100) {
                backgroundContext.beginPath();
                backgroundContext.moveTo(first.x, first.y);
                backgroundContext.lineTo(second.x, second.y);

                backgroundContext.strokeStyle =
                    `rgba(50, 150, 255, ${1 - distance / 100})`;

                backgroundContext.stroke();
            }
        }
    }

    dots.forEach(dot => {
        backgroundContext.beginPath();

        backgroundContext.arc(
            dot.x,
            dot.y,
            dot.radius,
            0,
            Math.PI * 2
        );

        backgroundContext.fillStyle = dot.color;
        backgroundContext.fill();
    });
}

function updateDots() {
    dots.forEach(dot => {
        dot.x += dot.vx;
        dot.y += dot.vy;

        if (dot.x > width) dot.x = 0;
        if (dot.x < 0) dot.x = width;
        if (dot.y > height) dot.y = 0;
        if (dot.y < 0) dot.y = height;
    });
}

function animate() {
    updateDots();
    drawDots();

    requestAnimationFrame(animate);
}

window.addEventListener('resize', resizeCanvas);

resizeCanvas();
animate();