import httpx
import json
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
BASE_URL = "http://localhost:8000"
PRODUCTS_ENDPOINT = f"{BASE_URL}/products/"

# Sample products to insert
def get_sample_products() -> List[Dict]:
    return [
        {
            "product_name": "Wireless Bluetooth Headphones",
            "permalink": "wireless-bluetooth-headphones",
            "regular_price": 1999.0,
            "stock_quantity": 50,
            "stock_status": "In Stock",
            "brand": "Sony",
            'image': 'https://example.com/wireless-bluetooth-headphones.jpg',
            "collection": "Audio",
            "description": "Premium wireless headphones with noise cancellation",
            "weight": 0.3,
            "shipping_charges": 50.0
        },
        {
            "product_name": "Smart LED TV",
            "permalink": "smart-led-tv",
            "regular_price": 49999.0,
            "stock_quantity": 10,
            "stock_status": "In Stock",
            "brand": "Samsung",
            "image": "https://example.com/smart-led-tv.jpg",
            "collection": "Electronics",
            "description": "4K Smart LED TV with built-in streaming apps",
            "weight": 15.0,
            "shipping_charges": 200.0,
            "length": 120.0,
            "height": 70.0,
            "width": 20.0
        },
        {
            "product_name": "Gaming Laptop",
            "permalink": "gaming-laptop",
            "regular_price": 89999.0,
            "stock_quantity": 8,
            "stock_status": "In Stock",
            "brand": "ASUS",
            "image": "https://example.com/gaming-laptop.jpg",
            "collection": "Computers",
            "description": "High-performance gaming laptop with RTX graphics",
            "weight": 2.5,
            "shipping_charges": 150.0
        }
    ]

def insert_products():
    """Insert sample products into the database."""
    # Get authentication token (replace with your actual token)
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuYXJlbmRyYTExNDcwQGdtYWlsLmNvbSIsImV4cCI6MTc0ODI1NTAyMiwidHlwZSI6ImFjY2VzcyJ9.1PXQk6AY1gk4wktUm3wnbmlGptH361JCTg2A5DCTZybGqJ_kB3faHWVg0T_u25-F2TSlvIQAAcV31Ezhr8q-DSfdnGNGLX2I-ATnLXndwBuj6D35NMkYCQaKcNt1-uj4eF7b0GbJyI42hDrdojpsjkTGrdmQmmBqIG-ya26VSNLBp9UTKyPPdwqJ7YxSpq6Ew2ccFMesah3VPJLIsMQpWFLD5Bg3spG9XQRcpEA19UwLjqLxPyFFfqocxlpb3o9DoRidZ2Rjvnnf3T3YCaOgtMXKHpiJnqNrrCAkWllewaKn_bX5-UVmsy-yWENDHzhF7lGubSq3jsiaZBdT4dQGLg"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Insert each product
    products = get_sample_products()
    successful_inserts = 0
    failed_inserts = 0

    print("\nStarting product insertion...")
    
    for product in products:
        try:
            response = httpx.post(
                PRODUCTS_ENDPOINT,
                headers=headers,
                json=product
            )
            
            if response.status_code == 201:
                print(f"✅ Successfully created product: {product['product_name']}")
                successful_inserts += 1
            else:
                print(f"❌ Failed to create product: {product['product_name']}")
                print(f"Error: {response.status_code} - {response.text}")
                failed_inserts += 1

        except Exception as e:
            print(f"❌ Error creating product: {product['product_name']}")
            print(f"Error: {str(e)}")
            failed_inserts += 1

    print("\nInsertion complete!")
    print(f"Successfully created: {successful_inserts} products")
    print(f"Failed: {failed_inserts} products")

if __name__ == "__main__":
    insert_products()
