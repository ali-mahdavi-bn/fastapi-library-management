import redis
from fastapi import HTTPException, status, Request

redis_client = redis.Redis(host="redis", port=6379, db=0)


def rate_limit(limit: int, interval: int):
    def decorator(func):
        def wrapper(request: Request):
            ip_address = request.client.host

            key = f"rate_limit:{ip_address}:{request.url.path}"

            if redis_client.exists(key):
                current_count = int(redis_client.get(key))
                if current_count >= limit:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded. Try again later.",
                    )
                else:
                    redis_client.incr(key)
            else:
                redis_client.setex(key, interval, 1)

            return func(request)

        return wrapper

    return decorator
