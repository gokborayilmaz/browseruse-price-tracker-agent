import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from upsonic import Agent, Task, ObjectResponse
from upsonic.client.tools import BrowserUse  # Importing BrowserUse

# Load environment variables
load_dotenv()

app = FastAPI(title="AI-Powered Price Tracker")

# Initialize the AI agent
price_tracker_agent = Agent("Price Tracker Agent", model="azure/gpt-4o", reflection=True)

# Define response format for individual products
class Product(ObjectResponse):
    name: str
    price: float
    url: str

# Define response format for the product list
class ProductList(ObjectResponse):
    products: list[Product]

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Price Tracker</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 flex justify-center items-center h-screen">
        <div class="bg-white p-8 rounded-lg shadow-lg w-96">
            <h1 class="text-2xl font-bold text-center mb-4">🔍 Price Tracker</h1>
            <input id="product" type="text" placeholder="Enter product name" class="w-full p-2 border rounded mb-4">
            <button onclick="trackPrice()" class="bg-blue-500 text-white px-4 py-2 rounded w-full">Track Price</button>
            <div id="result" class="mt-4 text-sm text-gray-800 bg-gray-50 p-4 rounded overflow-y-auto h-64"></div>
        </div>
        <script>
            async function trackPrice() {
                const product = document.getElementById("product").value;
                if (!product) {
                    alert("Please enter a product name.");
                    return;
                }
                const response = await fetch(`/track_price?product=${encodeURIComponent(product)}`);
                const data = await response.json();
                if (data.error) {
                    document.getElementById("result").innerHTML = `<p class='text-red-500'>Error: ${data.error}</p>`;
                } else {
                    const productsHTML = data.all_products.map(p => {
                        return `<div class='mb-2'>
                            <p><strong>Name:</strong> ${p.name}</p>
                            <p><strong>Price:</strong> $${p.price.toFixed(2)}</p>
                            <p><a href="${p.url}" class="text-blue-500 underline" target="_blank">View Product</a></p>
                            <hr class='my-2'>
                        </div>`;
                    }).join('');
                    document.getElementById("result").innerHTML = `<div>${productsHTML}</div>`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/track_price")
async def track_price(product: str = Query(..., title="Product to Track")):
    """Tracks product prices on multiple e-commerce websites and displays them in the app."""
    try:
        # Task to track product prices using BrowserUse
        track_task = Task(
            f"Search for the product '{product}' on Amazon, eBay, and AliExpress. Retrieve product names, prices, and links.",
            tools=[BrowserUse],
            response_format=ProductList
        )
        price_tracker_agent.do(track_task)
        response = track_task.response

        if not response:
            return {"error": "Failed to track prices."}

        # Return all products in a clean format
        return {
            "all_products": [{"name": p.name, "price": p.price, "url": p.url} for p in response.products]
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)