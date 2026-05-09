# logging → used for service-level logs (observability)
import logging

# TradeMatch → domain model for matched trades (event payload)
from models import TradeMatch

# Logger for Marketplace service
logger = logging.getLogger("MarketplaceService")


class MarketplaceService:
    def __init__(self, event_bus):
        # Event bus → async communication between services
        self.event_bus = event_bus

        # Sample buyers (prototype simplification)
        self.available_buyers = ["H002", "H003"]

    async def handle_trade_offer(self, offer):
        # Triggered by "trade.offer.created" event
        logger.info("Trade offer created by %s", offer.seller_id)

        # Simple matching → pick first buyer
        buyer_id = self.available_buyers[0]

        # Compute trade value
        total_price = offer.excess_kwh * offer.price_per_kwh

        # Create trade object
        trade = TradeMatch(
            buyer_id=buyer_id,
            seller_id=offer.seller_id,
            energy_kwh=offer.excess_kwh,
            total_price=total_price,
        )

        logger.info("Trade matched: %s -> %s", offer.seller_id, buyer_id)

        # Publish event to Settlement (with retry)
        await self.event_bus.publish_with_retry("trade.matched", trade)