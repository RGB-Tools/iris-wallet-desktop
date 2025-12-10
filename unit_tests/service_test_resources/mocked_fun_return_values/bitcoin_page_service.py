"""This module contains the mocked function return values for the bitcoin page service."""
from __future__ import annotations

from unittest.mock import patch

from src.data.service.bitcoin_page_service import BitcoinPageService
from src.model.btc_model import BalanceResponseModel
from src.model.btc_model import BalanceStatus
from src.model.btc_model import ConfirmationTime
from src.model.btc_model import Transaction
from src.model.btc_model import TransactionListResponse
from src.model.btc_model import TransactionListWithBalanceResponse
from src.model.enums.enums_model import TransactionStatusEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel

# Mock data for testing
mocked_balance = BalanceResponseModel(
    vanilla=BalanceStatus(settled=500000, future=1000000, spendable=700000),
    colored=BalanceStatus(settled=0, future=0, spendable=0),
)

mocked_transaction_list = TransactionListResponse(
    transactions=[
        Transaction(
            transaction_type='User',
            txid='tx124unconfirmed',
            received=200000,
            sent=0,
            fee=1500,
            amount='+200000',
            transfer_status=TransferStatusEnumModel.ON_GOING_TRANSFER,
            transaction_status=TransactionStatusEnumModel.WAITING_CONFIRMATIONS,
            confirmation_normal_time=None,
            confirmation_date=None,
            confirmation_time=None,
        ),
        Transaction(
            transaction_type='User',
            txid='tx123confirmed',
            received=100000,
            sent=50000,
            fee=1000,
            amount='+50000',  # Adjusted the amount based on your service logic
            # Adjusted based on actual response
            transfer_status=TransferStatusEnumModel.RECEIVED,
            transaction_status=TransactionStatusEnumModel.CONFIRMED,
            # Adjusted based on actual confirmation time
            confirmation_normal_time='10:14:00',
            confirmation_date='2024-12-23',
            confirmation_time=ConfirmationTime(
                height=150, timestamp=1734929040,
            ),
        ),
    ],
)

# Mocked response you expect from the service
mocked_expected_response = TransactionListWithBalanceResponse(
    transactions=[
        Transaction(
            transaction_type='User',
            txid='tx124unconfirmed',
            received=200000,
            sent=0,
            fee=1500,
            amount='+200000',
            transfer_status=TransferStatusEnumModel.ON_GOING_TRANSFER,
            transaction_status=TransactionStatusEnumModel.WAITING_CONFIRMATIONS,
            confirmation_normal_time=None,
            confirmation_date=None,
            confirmation_time=None,
        ),
        Transaction(
            transaction_type='User',
            txid='tx123confirmed',
            received=100000,
            sent=50000,
            fee=1000,
            amount='+50000',  # Correct the amount here to match actual behavior
            transfer_status=TransferStatusEnumModel.RECEIVED,  # Ensure the correct status
            transaction_status=TransactionStatusEnumModel.CONFIRMED,
            confirmation_normal_time='10:14:00',  # Adjust the time here if needed
            confirmation_date='2024-12-23',
            confirmation_time=ConfirmationTime(
                height=150, timestamp=1734929040,
            ),
        ),
    ],
    balance=BalanceResponseModel(
        vanilla=BalanceStatus(
            settled=500000, future=1000000, spendable=700000,
        ),
        colored=BalanceStatus(settled=0, future=0, spendable=0),
    ),
)

# Test function


@patch('src.data.repository.btc_repository.BtcRepository.get_btc_balance')
@patch('src.data.repository.btc_repository.BtcRepository.list_transactions')
def test_get_btc_transaction(mock_list_transactions, mock_get_btc_balance):
    """This function tests the get_btc_transaction method of the BitcoinPageService class."""
    # Mocking the repository responses
    mock_get_btc_balance.return_value = mocked_balance
    mock_list_transactions.return_value = mocked_transaction_list

    # Calling the service method to get the transaction list
    response = BitcoinPageService.get_btc_transaction()

    # Assertions to verify the correctness of the response
    assert response == mocked_expected_response
