from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cache_ttl: int = 60 * 60
    product_urls: list[str] = [
        "https://shop.lululemon.com/c/womens-leggings/_/N-8r6?format=json",
        "https://shop.lululemon.com/c/accessories/_/N-1z0xcmkZ1z0xl44Z8ok?format=json"
    ]


settings = Settings()
