# logging → service logs (observability)
import logging

# datetime → timestamp for readings
from datetime import datetime

# Domain models → event payloads
from models import MeterReading, TradeOffer

# Logger for Metering service
logger = logging.getLogger("MeterService")


class MeterService:
    def __init__(self, event_bus):
        # Event bus → async communication
        self.event_bus = event_bus

    async def ingest_reading(self, meter_id, household_id, generated_kwh, consumed_kwh):
        # Create meter reading event
        reading = MeterReading(
            meter_id=meter_id,
            household_id=household_id,
            generated_kwh=generated_kwh,
            consumed_kwh=consumed_kwh,
            timestamp=datetime.utcnow(),
        )

        logger.info("Meter reading received from %s", household_id)

        # Publish reading event
        await self.event_bus.publish("meter.reading.received", reading)

        # Calculate excess energy
        excess = generated_kwh - consumed_kwh

        if excess > 0:
            logger.info("Excess energy detected: %.2f kWh", excess)

            # Create trade offer (upstream → Marketplace)
            offer = TradeOffer(
                seller_id=household_id,
                excess_kwh=excess,
                price_per_kwh=0.30,
            )

            # Publish trade offer event
            await self.event_bus.publish("trade.offer.created", offer)