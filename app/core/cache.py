import json
import redis.asyncio as redis
from app.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_cache(key: str):
    value = await redis_client.get(key)
    if value:
        return json.loads(value)
    return None


async def set_cache(key: str, value, ttl: int = None):
    ttl = ttl or settings.CACHE_TTL_SECONDS
    await redis_client.set(key, json.dumps(value), ex=ttl)
