import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = os.getenv('REDIS_HOST', 'localhost')
    redis_port: int = int(os.getenv('REDIS_PORT', 6379))
    cache_ttl: int = int(os.getenv('CACHE_TTL', 300))
    product_urls: list[str] = [
        "https://shop.lululemon.com/c/womens-leggings/_/N-8r6?format=json1",
        "https://shop.lululemon.com/c/accessories/_/N-1z0xcmkZ1z0xl44Z8ok?format=json"
    ]


settings = Settings()
