import os
from fastapi import FastAPI, Depends

from middleware import logger_error_middleware
from products_app.services.product_service import ProductService
from mangum import Mangum
from utils.redis_client import get_redis_client

app = FastAPI()
app.middleware("http")(logger_error_middleware)

# Initialize Redis client and ProductService
redis_client = get_redis_client()
# Create a single instance of ProductService
product_service_instance = ProductService(redis_client)


def get_product_service():
    return product_service_instance


@app.get("/api/products")
def get_products(service: ProductService = Depends(get_product_service)):
    return service.fetch_all_products()


# Mangum handler for AWS Lambda
handler = Mangum(app)
