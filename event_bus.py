import asyncio
from collections import defaultdict
from typing import Any, Awaitable, Callable


class EventBus:
    def __init__(self):
        # Dictionary to store event subscribers
        # Key = event type (e.g., "TradeMatched")
        # Value = list of async handler functions
        self.subscribers: dict[str, list[Callable[[Any], Awaitable[None]]]] = defaultdict(list)
        
        # Dead Letter Queue (DLQ)
        # Stores failed events after all retries are exhausted
        # Format: (event_type, payload, error_message)
        self.dead_letter_queue: list[tuple[str, Any, str]] = []

    def subscribe(self, event_type: str, handler: Callable[[Any], Awaitable[None]]) -> None:
        # Register a service (handler) to listen for a specific event type
        # Example: Settlement service subscribes to "TradeMatched"
        self.subscribers[event_type].append(handler)

    async def publish(self, event_type: str, payload: Any) -> None:
        # Get all handlers subscribed to this event
        handlers = self.subscribers.get(event_type, [])
        
        # Create async tasks for each handler (non-blocking execution)
        tasks = [handler(payload) for handler in handlers]
        
        if tasks:
            # Run all handlers concurrently (event-driven parallel processing)
            await asyncio.gather(*tasks)

    async def publish_with_retry(self, event_type: str, payload: Any, retries: int = 3) -> None:
        # Retry mechanism for fault tolerance (Design for Failure principle)
        for attempt in range(retries):
            try:
                # Try publishing the event
                await self.publish(event_type, payload)
                return  # Success → exit early
            
            except Exception as exc:
                # If last retry fails → send to Dead Letter Queue
                if attempt == retries - 1:
                    self.dead_letter_queue.append((event_type, payload, str(exc)))
                    raise  # Re-raise exception after logging
                
                # Exponential backoff (simple version)
                # Prevents system overload during repeated failures
                await asyncio.sleep(0.2 * (attempt + 1))