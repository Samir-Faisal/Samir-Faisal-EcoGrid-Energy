# dataclass → simplifies data model definitions
from dataclasses import dataclass

# datetime → timestamp for events
from datetime import datetime

# uuid4 → generate unique transaction IDs
from uuid import uuid4


# MeterReading → telemetry event from smart meter
@dataclass
class MeterReading:
    meter_id: str
    household_id: str
    generated_kwh: float
    consumed_kwh: float
    timestamp: datetime


# TradeOffer → energy available for sale (Metering → Marketplace)
@dataclass
class TradeOffer:
    seller_id: str
    excess_kwh: float
    price_per_kwh: float


# TradeMatch → matched trade (Marketplace → Settlement)
@dataclass
class TradeMatch:
    buyer_id: str
    seller_id: str
    energy_kwh: float
    total_price: float


# Transaction → financial record for settlement
@dataclass
class Transaction:
    transaction_id: str
    buyer_id: str
    seller_id: str
    amount: float
    status: str = "PENDING"

    @staticmethod
    def new(buyer_id: str, seller_id: str, amount: float):
        # Create new transaction with unique ID
        return Transaction(
            transaction_id=str(uuid4()),
            buyer_id=buyer_id,
            seller_id=seller_id,
            amount=amount,
            status="PENDING"
        )


# Wallet → manages household balance
class Wallet:
    def __init__(self, household_id: str, balance: float = 0.0):
        self.household_id = household_id
        self.balance = balance

    def debit(self, amount: float):
        # Deduct amount (with balance check)
        if amount > self.balance:
            raise ValueError(f"Insufficient balance for {self.household_id}")
        self.balance -= amount

    def credit(self, amount: float):
        # Add amount to wallet
        self.balance += amount