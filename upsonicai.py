import os
import openai
import json
from openai import OpenAI
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from pydantic import BaseModel
import requests


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

app = FastAPI(title="AI-Powered Price Tracker")

class Product(BaseModel):
    name: str
    price: float
    url: str

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

#sample product link checker for the URLs generated.
"""
def product_link_checker(url):
    #Checks if a product URL is valid by searching for specific error phrases in HTML content
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        html_content = response.text.lower()

        #these are common error phrases in e commerce platforms 
        error_phrases = [
            "dogsofamazon",            
            "we couldn't find this page",
            "aradığın içeriğe şu an ulaşılamıyor",
            "the page you're looking for can't be found",            
            "we looked everywhere",
            "page not found",
        ]
        
        for phrase in error_phrases:
            if phrase in html_content:
                print(phrase)
                return False
        
        if response.status_code != 200:
            return False
        
        return True
    
    except requests.exceptions.RequestException:
        return False
"""    

@app.get("/track_price")
async def track_price(product: str = Query(..., title="Product to Track")):
    """Tracks product prices using OpenAI to generate product information."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system", 
                    "content": """You are an e-commerce product search assistant. Always respond in strict JSON format with an array of products. If user writes generic product name such as Iphone, all three examples should be same iphone model such as Iphone 14, 64 GB.
                        CRITICAL INSTRUCTIONS:
                        - Always provide DIRECT product page links"""
                },
                {
                    "role": "user", 
                    "content": f"""Find 3 different product links for  this '{product}'. Check Amazon, Wallmart and trendyol. Get only product links, not search etc. 
                    Provide the following details for each product in JSON format
                    IMPORTANT(If user writes generic product name such as Iphone, all three examples should be same iphone model such as Iphone 14, 128 GB.)
                    Example.com url is sample. DON'T write example.com/iphone or something else. Check out websites like Amazon.com, wallmart.com, apple.com, ebay.com trendyol.com etc.
                    Sample links for Iphone (Amazon: https://www.amazon.com.tr/Apple-iPhone-14-128-GB/dp/B0BDHTNM23?th=1 , Wallmart: https://www.walmart.com/ip/Straight-Talk-Apple-iPhone-14-128GB-Purple-Prepaid-Smartphone-Locked-to-Straight-Talk/1450299768 , Trendyol: https://www.trendyol.com/apple/iphone-14-128-gb-mavi-p-355707135 )
            
                    Response should be in this exact JSON structure:
                    {{
                        "all_products": [
                            {{
                                "name": "Product Name",
                                "price": 49.99,
                                "url": "DIRECT Product Page URL"
                            }},
                            ...
                        ]
                    }}"""
                }
            ],
            max_tokens=300
        )

        result_text = response.choices[0].message.content
        result_data = json.loads(result_text)

        return {"all_products": result_data.get('all_products', [])}

    except Exception as e:
        return {"error": str(e)}
  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)