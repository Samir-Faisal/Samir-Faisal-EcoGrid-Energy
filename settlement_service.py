# logging → service logs (observability)
import logging

# Wallet, Transaction → financial domain models
from models import Wallet, Transaction

# Logger for Settlement service
logger = logging.getLogger("SettlementService")


class SettlementService:
    def __init__(self, event_bus):
        # Event bus → async communication
        self.event_bus = event_bus

        # Track processed trades (idempotency control)
        self.processed_transactions = set()

        # Simulated wallets (prototype data)
        self.wallets = {
            "H001": Wallet("H001", 5.00),
            "H002": Wallet("H002", 10.00),
            "H003": Wallet("H003", 8.00),
        }

    async def handle_trade_match(self, trade):
        # Create unique key for idempotency check
        trade_key = f"{trade.buyer_id}:{trade.seller_id}:{trade.total_price:.2f}"

        # Prevent duplicate processing (at-least-once delivery safety)
        if trade_key in self.processed_transactions:
            logger.warning("Duplicate trade ignored: %s", trade_key)
            return

        self.processed_transactions.add(trade_key)

        # Get buyer/seller wallets
        buyer_wallet = self.wallets[trade.buyer_id]
        seller_wallet = self.wallets[trade.seller_id]

        # Execute payment (debit → credit)
        buyer_wallet.debit(trade.total_price)
        seller_wallet.credit(trade.total_price)

        logger.info("Debited %s wallet by $%.2f", trade.buyer_id, trade.total_price)
        logger.info("Credited %s wallet by $%.2f", trade.seller_id, trade.total_price)

        # Create transaction record
        transaction = Transaction.new(
            buyer_id=trade.buyer_id,
            seller_id=trade.seller_id,
            amount=trade.total_price,
        )
        transaction.status = "SETTLED"

        logger.info("Payment settled successfully")

        # Publish settlement event (downstream notification)
        await self.event_bus.publish("payment.settled", transaction)