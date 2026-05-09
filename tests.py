# Wallet → financial model under test
from models import Wallet


def test_wallet_debit():
    # Test successful debit
    wallet = Wallet("H001", 10.0)
    wallet.debit(2.5)
    
    # Balance should be reduced correctly
    assert wallet.balance == 7.5


def test_wallet_insufficient_balance():
    # Test debit failure when balance is insufficient
    wallet = Wallet("H001", 1.0)
    
    try:
        wallet.debit(2.0)
        assert False  # Should not reach here
    except ValueError:
        assert True  # Expected exception