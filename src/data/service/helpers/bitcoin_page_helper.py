"""
This module provides helper functions to bitcoin page.
"""
from __future__ import annotations

from src.model.btc_model import Transaction
from src.model.enums.enums_model import TransactionStatusEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.enums.enums_model import TransferType
from src.utils.constant import NO_OF_UTXO
from src.utils.constant import UTXO_SIZE_SAT
from src.utils.custom_exception import ServiceOperationException


def calculate_transaction_amount(transaction: Transaction) -> str | None:
    """Calculate and return the 'amount' as a formatted string based on transaction type."""
    try:
        if transaction.transaction_type in ('User', 'RgbSend'):
            if transaction.sent > 0:
                # Transaction amount as negative because money was sent
                amount = transaction.sent - transaction.received
                return f'-{amount}'
            # Transaction amount as positive because money was received
            return f'+{transaction.received}'
        if transaction.transaction_type == TransferType.CREATEUTXOS.value:
            return f'-{(UTXO_SIZE_SAT * NO_OF_UTXO) + transaction.fee}'
        # Default case if none above, formatted as string for consistency
        return None
    except Exception as exc:
        error_message = str(exc) if str(exc) else 'Failed to get amount'
        raise ServiceOperationException(error_message) from exc


def get_transaction_status(
    transaction: Transaction,
) -> tuple[TransferStatusEnumModel | None, TransactionStatusEnumModel | None]:
    """This helper identifies the status of a transaction and returns
    a tuple of (transfer_status, transaction_status)."""
    try:
        if transaction.transaction_type in ('User', 'RgbSend'):
            if transaction.confirmation_time:
                # If there is a confirmation time, the transaction is confirmed
                if transaction.sent > 0:
                    return (
                        TransferStatusEnumModel.SENT,
                        TransactionStatusEnumModel.CONFIRMED,
                    )
                return (
                    TransferStatusEnumModel.RECEIVED,
                    TransactionStatusEnumModel.CONFIRMED,
                )
            # No confirmation time means the transaction is still pending
            return (
                TransferStatusEnumModel.ON_GOING_TRANSFER,
                TransactionStatusEnumModel.WAITING_CONFIRMATIONS,
            )

        if transaction.transaction_type == TransferType.CREATEUTXOS.value:
            if transaction.confirmation_time:
                return (
                    TransferStatusEnumModel.INTERNAL,
                    TransactionStatusEnumModel.CONFIRMED,
                )
            # CreateUtxos transactions are considered internal
            return (
                TransferStatusEnumModel.ON_GOING_TRANSFER,
                TransactionStatusEnumModel.WAITING_CONFIRMATIONS,
            )

        # If none of the conditions are met, return None or appropriate default values
        return (None, None)
    except Exception as exc:
        error_message = str(exc) if str(exc) else 'Failed to get status'
        raise ServiceOperationException(error_message) from exc
