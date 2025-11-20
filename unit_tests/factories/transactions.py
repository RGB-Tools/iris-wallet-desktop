"""This module provides factory functions to create instances of Transaction."""
from __future__ import annotations

from src.model.btc_model import Transaction
from src.model.enums.enums_model import TransactionStatusEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel


def make_transaction(**overrides) -> Transaction:
    """Factory function to create a Transaction instance with optional overrides."""
    defaults = {
        'transfer_status': TransferStatusEnumModel.ON_GOING_TRANSFER,
        'transaction_status': TransactionStatusEnumModel.WAITING_CONFIRMATIONS,
        'confirmation_normal_time': None,
        'confirmation_date': None,
        'confirmation_time': None,
    }
    defaults.update(overrides)
    return Transaction(**defaults)
