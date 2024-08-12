import redis
from config import settings
from utils.logger import logger


def get_redis_client():
    try:
        client = redis.StrictRedis(host=settings.redis_host, port=settings.redis_port, db=0)
        client.ping()  # Test the connection
        logger.info("Connected to Redis successfully.")
        return client
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Failed to connect to Redis at {settings.redis_host}:{settings.redis_port}. Error: {e}")
        return None  # Decide if you want to continue without Redis
