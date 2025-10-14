import os
import sys
import json
import logging
import asyncio

from google.pubsub_v1.services.subscriber.async_client import (
    SubscriberAsyncClient,
)
from google.cloud.pubsub_v1.subscriber.message import Message

from core_wms.app.tasks.registry import MAP
from core_wms.app.tasks.broker import dramatiq_broker

logger = logging.getLogger(__name__)


class WebhookSubscriber:
    """General base class for Webhook subscribers.

    Listens for webhook events from Pub/Sub and dispatches to Dramatiq tasks.
    Uses the async client for better performance.
    """

    def __init__(self):
        self.project_id = os.getenv("project_id")
        self.subscription_name = os.getenv("subscription_id")
        self.subscriber = SubscriberAsyncClient()
        self.subscription_path = self.subscriber.subscription_path(
            self.project_id, self.subscription_name
        )
        self.streaming_pull_future = None

    async def _process_message(self, message: Message) -> None:
        try:
            data = json.loads(message.data.decode("utf-8"))

            topic = data.get("topic")
            payload = data.get("payload", {})
            store_id = data.get("store_id")

            if not topic:
                logger.warning("Received message without topic")
                await message.ack()
                return

            handler_name = MAP.get(topic)

            if handler_name:
                logger.info(f"Processing webhook: {topic}")
                await dramatiq_broker.enqueue(handler_name, payload, store_id)
                logger.info(f"Successfully queued task for topic: {topic}")
                await message.ack()
            else:
                logger.warning(f"No handler registered for topic: {topic}")
                await message.ack()

        except Exception as e:
            logger.exception(f"Error processing message: {e}")
            await message.nack()

    async def start(self) -> None:
        logger.info(
            f"Starting async webhook subscriber on {self.subscription_path}"
        )

        try:
            streaming_pull = self.subscriber.streaming_pull(
                self.subscription_path
            )

            async with streaming_pull as stream:
                self.streaming_pull_future = stream
                async for response in stream:
                    for received_message in response.received_messages:
                        message = received_message.message

                        await self._process_message(message)

                        await self.subscriber.acknowledge(
                            self.subscription_path, [received_message.ack_id]
                        )
        except asyncio.CancelledError:
            await self.stop("Async task cancelled")
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            await self.stop("Error occurred")
            raise

    async def stop(self, reason: str = "Stopping") -> None:
        if self.streaming_pull_future:
            logger.info(f"{reason}, shutting down webhook subscriber...")
            self.streaming_pull_future.cancel()
            await self.subscriber.close()
            logger.info("Webhook subscriber stopped")


if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    subscriber = WebhookSubscriber()
    asyncio.run(subscriber.start())
