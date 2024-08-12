import json
import requests
from fastapi import HTTPException
from products_app.models import Product
from products_app.config import settings
from logger import logger


class ProductService:
    def __init__(self, redis_client):
        self.redis = redis_client

    def fetch_product_details(self, url: str) -> list[Product]:
        try:
            cached_data = self.redis.get(url)

            # Check if the URL response  is in the cache
            if cached_data:
                logger.info(f"Cache hit for URL: {url}")
                return json.loads(cached_data)
            else:
                logger.info(f"Cache miss for URL: {url}")

            response = requests.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")

            data = response.json()
            products_data = data.get('contents', [])[0].get('mainContent', [])[0].get('contents', [])[0].get('records',
                                                                                                             [])

            product_details = []
            for product in products_data:
                attributes = product.get('attributes', {})
                product_details.append(Product(
                    displayName=attributes.get('product.displayName', ['N/A'])[0],
                    price=attributes.get('product.price', ['N/A'])[0],
                    category=attributes.get('product.parentCategory.displayName', ['N/A'])[0],
                    images=attributes.get('product.sku.skuImages', []),
                    availableSizes=attributes.get('product.allAvailableSizes', []),
                    colors=attributes.get('colorGroup', []),
                    skuDetails=attributes.get('product.skuStyleOrder', []),
                    productURL=f"https://shop.lululemon.com{attributes.get('product.pdpURL', [''])[0]}"
                ).to_dict())

            self.redis.setex(url, settings.cache_ttl, json.dumps(product_details))

            return product_details
        except Exception as e:
            logger.error(f"An unexpected error occurred for URL: {url} with error: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred")

    def fetch_all_products(self) -> list[Product]:
        all_products = []
        for url in settings.product_urls:
            products = self.fetch_product_details(url)
            all_products.extend(products)
        return all_products
