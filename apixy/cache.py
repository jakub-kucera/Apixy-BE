"""Module for RedisJSON cache helper functions"""
import json
import logging
from functools import wraps
from typing import Any, Optional

import aioredis

logger = logging.getLogger(__name__)
REDIS: Optional[aioredis.Redis] = None


def redis_cache(coroutine_method: Any) -> Any:
    """
    A decorator to enforce DRY on caching for datasources.
    """

    @wraps(coroutine_method)
    async def wrapper(self: Any) -> Any:
        """
        Caching routines.
        """
        if REDIS is None:
            logger.error("Redis is not initialized")
            return await coroutine_method(self)

        if (
            self.cache_expire is not None
            and self.cache_expire >= 0
            and (cached := await REDIS.get(self.name))
        ):
            return json.loads(cached)

        data = await coroutine_method(self)

        if (
            self.cache_expire is not None
            and data is not None
            and self.cache_expire >= 0
        ):
            try:
                await REDIS.set(self.name, json.dumps(data), expire=self.cache_expire)
            except TypeError as error:
                logger.error("Cannot json.dumps() some data")
                logger.exception(error)

        return data

    return wrapper
