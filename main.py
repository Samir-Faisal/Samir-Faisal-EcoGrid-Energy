# asyncio → core Python library for asynchronous programming
import asyncio
# setup_logger → custom logging configuration
from logger import setup_logger
# EventBus → central event communication mechanism
from event_bus import EventBus
# MeterService → represents Metering bounded context
from meter_service import MeterService

# MarketplaceService → represents Marketplace bounded context
from marketplace_service import MarketplaceService

# SettlementService → represents Settlement bounded context
from settlement_service import SettlementService

async def main():
    # Initialise logging system (supports tracing and debugging across services)
    setup_logger()

    # Create shared event bus (enables loose coupling between services)
    event_bus = EventBus()

    # Instantiate services (each service = independent domain/bounded context)
    meter_service = MeterService(event_bus)
    marketplace_service = MarketplaceService(event_bus)
    settlement_service = SettlementService(event_bus)

    # Define event subscriptions (event-driven workflow wiring)

    # Marketplace reacts to energy availability events from Metering
    event_bus.subscribe("trade.offer.created", marketplace_service.handle_trade_offer)

    # Settlement reacts to completed trade matching events
    event_bus.subscribe("trade.matched", settlement_service.handle_trade_match)

    # Simulate smart meter input (system entry point)
    # Triggers full asynchronous pipeline:
    # Metering → Marketplace → Settlement
    await meter_service.ingest_reading(
        meter_id="MTR-001",
        household_id="H001",
        generated_kwh=8.5,
        consumed_kwh=5.0,
    )


if __name__ == "__main__":
    try:
        # If already running inside an event loop (e.g., notebook environment)
        loop = asyncio.get_running_loop()
        loop.create_task(main())
    except RuntimeError:
        # Standard execution → create new event loop
        asyncio.run(main())

