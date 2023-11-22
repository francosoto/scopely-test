import redis
from app import config


# Yield dependency
def get_cache():
    cache = Cache()
    session = cache._conn
    yield session
    session.close()
    # await session.wait_closed()


class Cache:
    def __init__(self):
        self._conn = redis.Redis(
            host=config.CACHE_HOST, port=6379, db=int(config.CACHE_DB)
        )

    async def get(self, key):
        return self._conn.get(key)

    async def set(self, key, value):
        return self._conn.set(key, value)
