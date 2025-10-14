import asyncio
import os
from dramatiq.brokers.redis import RedisBroker
import dramatiq
from dramatiq.middleware import AsyncIO, Retries, TimeLimit

redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
redis_broker = RedisBroker(url=redis_url)

if not any(isinstance(m, AsyncIO) for m in redis_broker.middleware):
    redis_broker.add_middleware(AsyncIO())
if not any(isinstance(m, Retries) for m in redis_broker.middleware):
    redis_broker.add_middleware(Retries(max_retries=3))
if not any(isinstance(m, TimeLimit) for m in redis_broker.middleware):
    redis_broker.add_middleware(TimeLimit(time_limit=30000))

dramatiq.set_broker(redis_broker)


class DramatiqBroker:
    def __init__(self):
        self.broker = redis_broker

    async def enqueue(self, function_name: str, *args, **kwargs):
        actor = self.broker.get_actor(function_name)
        if not actor:
            raise ValueError(f"No actor registered with name: {function_name}")

        message = actor.send(*args, **kwargs)
        return message.message_id

    def enqueue_sync(self, function_name: str, *args, **kwargs):
        async def _do_enqueue():
            return await self.enqueue(function_name, *args, **kwargs)

        return asyncio.run(_do_enqueue())


dramatiq_broker = DramatiqBroker()

arq_broker = dramatiq_broker
