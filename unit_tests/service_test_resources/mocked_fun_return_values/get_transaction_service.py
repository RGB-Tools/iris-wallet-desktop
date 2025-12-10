"""Mocked data for the bitcoin page service service test"""
from __future__ import annotations

from src.model.btc_model import BalanceResponseModel
from src.model.btc_model import BalanceStatus
from src.model.btc_model import ConfirmationTime
from src.model.btc_model import Transaction
from src.model.btc_model import TransactionListResponse
from src.model.btc_model import TransactionListWithBalanceResponse
from src.model.enums.enums_model import TransactionStatusEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel

mock_data_transaction_type_user_send = Transaction(
    transaction_type='User',
    txid='e28d416c3345e3558516830b7adfbc147f3f7563c9268e24f36d233048e6f9f2',
    received=99998405,
    sent=100000000,
    fee=595,
    confirmation_time=ConfirmationTime(height=105, timestamp=1717006775),
)
mock_data_transaction_type_user_receive = Transaction(
    transaction_type='User',
    txid='354ab4d3afbac320ea492086ad7590570455d625acd59aea799c58f83afc9f8f',
    received=100000000,
    sent=0,
    fee=2820,
    confirmation_time=ConfirmationTime(height=104, timestamp=1717006478),
)
mock_data_transaction_type_createutxo = Transaction(
    transaction_type='CreateUtxos',
    txid='673c88d7e435e6fe795bf30fd0363790a68c3a8dfd91f71b050170978c9413ea',
    received=199996291,
    sent=199998405,
    fee=2114,
    confirmation_time=ConfirmationTime(height=106, timestamp=1717006902),
)
mock_data_transaction_unconfirm_type_user_send = Transaction(
    transaction_type='User',
    txid='e28d416c3345e3558516830b7adfbc147f3f7563c9268e24f36d233048e6f9f2',
    received=99998405,
    sent=100000000,
    fee=595,
    confirmation_time=None,
)
mock_data_transaction_unconfirm_type_createutxos = Transaction(
    transaction_type='CreateUtxos',
    txid='673c88d7e435e6fe795bf30fd0363790a68c3a8dfd91f71b050170978c9413ea',
    received=199996291,
    sent=199998405,
    fee=2114,
    confirmation_time=None,
)
mock_data_transaction_unconfirm_type_user_receive = Transaction(
    transaction_type='User',
    txid='fb90ee1b9495be737595919f766b939c130dbc2f359b4e8ec21ead6358462a67',
    received=100000000,
    sent=0,
    fee=2820,
    confirmation_time=None,
)

mock_data_transaction_type_unknown = Transaction(
    transaction_type='unknow',
    txid='fb90ee1b9495be737595919f766b939c130dbc2f359b4e8ec21ead6358462a67',
    received=100000000,
    sent=0,
    fee=2820,
    confirmation_time=None,
)

mock_data_list_transaction_all = TransactionListResponse(
    transactions=[
        mock_data_transaction_type_user_send,
        mock_data_transaction_type_user_receive,
        mock_data_transaction_type_createutxo,
        mock_data_transaction_unconfirm_type_user_send,
        mock_data_transaction_unconfirm_type_createutxos,
        mock_data_transaction_unconfirm_type_user_receive,
    ],
)
mocked_data_balance = BalanceResponseModel(
    vanilla=BalanceStatus(
        settled=0, future=90332590, spendable=90332590,
    ), colored=BalanceStatus(settled=0, future=0, spendable=0),
)
mock_data_list_transaction_empty = TransactionListWithBalanceResponse(
    transactions=[], balance=mocked_data_balance,
)
mock_data_expected_list_transaction_all = TransactionListWithBalanceResponse(
    transactions=[
        Transaction(
            transaction_type='User',
            txid='e28d416c3345e3558516830b7adfbc147f3f7563c9268e24f36d233048e6f9f2',
            received=99998405,
            sent=100000000,
            fee=595,
            amount='-1595',
            transaction_status=TransactionStatusEnumModel.WAITING_CONFIRMATIONS,
            transfer_status=TransferStatusEnumModel.ON_GOING_TRANSFER,
            confirmation_normal_time=None,
            confirmation_date=None,
            confirmation_time=None,
        ),
        Transaction(
            transaction_type='CreateUtxos',
            txid='673c88d7e435e6fe795bf30fd0363790a68c3a8dfd91f71b050170978c9413ea',
            received=199996291,
            sent=199998405,
            fee=2114,
            amount='-130114',
            transfer_status=TransferStatusEnumModel.ON_GOING_TRANSFER,
            confirmation_normal_time=None,
            transaction_status=TransactionStatusEnumModel.WAITING_CONFIRMATIONS,
            confirmation_date=None,
            confirmation_time=None,
        ),
        Transaction(
            transaction_type='User',
            txid='fb90ee1b9495be737595919f766b939c130dbc2f359b4e8ec21ead6358462a67',
            received=100000000,
            sent=0,
            fee=2820,
            amount='+100000000',
            transaction_status=TransactionStatusEnumModel.WAITING_CONFIRMATIONS,
            transfer_status=TransferStatusEnumModel.ON_GOING_TRANSFER,
            confirmation_normal_time=None,
            confirmation_date=None,
            confirmation_time=None,
        ),
        Transaction(
            transaction_type='CreateUtxos',
            txid='673c88d7e435e6fe795bf30fd0363790a68c3a8dfd91f71b050170978c9413ea',
            received=199996291,
            sent=199998405,
            fee=2114,
            amount='-130114',
            transfer_status=TransferStatusEnumModel.INTERNAL,
            transaction_status=TransactionStatusEnumModel.CONFIRMED,
            confirmation_normal_time='23:51:42',
            confirmation_date='2024-05-29',
            confirmation_time=ConfirmationTime(
                height=106,
                timestamp=1717006902,
            ),
        ),
        Transaction(
            transaction_type='User',
            txid='e28d416c3345e3558516830b7adfbc147f3f7563c9268e24f36d233048e6f9f2',
            received=99998405,
            sent=100000000,
            fee=595,
            amount='-1595',
            transfer_status=TransferStatusEnumModel.SENT,
            transaction_status=TransactionStatusEnumModel.CONFIRMED,
            confirmation_normal_time='23:49:35',
            confirmation_date='2024-05-29',
            confirmation_time=ConfirmationTime(
                height=105,
                timestamp=1717006775,
            ),
        ),
        Transaction(
            transaction_type='User',
            txid='354ab4d3afbac320ea492086ad7590570455d625acd59aea799c58f83afc9f8f',
            received=100000000,
            sent=0,
            fee=2820,
            amount='+100000000',
            transfer_status=TransferStatusEnumModel.RECEIVED,
            transaction_status=TransactionStatusEnumModel.CONFIRMED,
            confirmation_normal_time='23:44:38',
            confirmation_date='2024-05-29',
            confirmation_time=ConfirmationTime(
                height=104,
                timestamp=1717006478,
            ),
        ),
    ],
    balance=BalanceResponseModel(
        vanilla=BalanceStatus(
            settled=0, future=90332590, spendable=90332590,
        ), colored=BalanceStatus(settled=0, future=0, spendable=0),
    ),
)
