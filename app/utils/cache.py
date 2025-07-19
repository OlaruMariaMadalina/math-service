import redis

from app.utils.config import settings


# Initialize Redis client connection
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


# Retrieve a cached value by key
def get_cached_result(key: str):
    return r.get(key)


# Store a value in cache with TTL (in seconds)
def set_cached_result(key: str, value: str, ttl: int = 3600):
    r.set(key, value, ex=ttl)
