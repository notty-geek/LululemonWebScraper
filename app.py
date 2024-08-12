import os
from fastapi import FastAPI, Depends

from middleware import logger_error_middleware
from products_app.services.product_service import ProductService
from mangum import Mangum
import redis

app = FastAPI()
app.middleware("http")(logger_error_middleware)

# Use environment variables for Redis connection
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
# Connect to the Redis instance
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

# Create a single instance of ProductService
product_service_instance = ProductService(redis_client)


def get_product_service():
    return product_service_instance


@app.get("/api/products")
def get_products(service: ProductService = Depends(get_product_service)):
    return service.fetch_all_products()


# Mangum handler for AWS Lambda
handler = Mangum(app)
