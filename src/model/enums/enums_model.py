"""
This module defines enumeration models for different models.
"""
from __future__ import annotations

from enum import Enum


class NetworkEnumModel(str, Enum):
    """Enum model for network"""
    REGTEST = 'regtest'
    MAINNET = 'mainnet'
    TESTNET = 'testnet'
    TESTNET4 = 'testnet4'
    SIGNET = 'signet'


class FilterAssetEnumModel(str, Enum):
    """Enum model for list asset"""
    NIA = 'Nia'
    UDA = 'Uda'
    CFA = 'Cfa'


class TransactionStatusEnumModel(str, Enum):
    """Enum model for transaction status"""
    WAITING_CONFIRMATIONS = 'WaitingConfirmations'
    WAITING_COUNTERPARTY = 'WaitingCounterparty'
    SETTLED = 'Settled'
    CONFIRMED = 'CONFIRMED'
    FAILED = 'Failed'


class TransferStatusEnumModel(str, Enum):
    """"Enum model for transfer status"""
    ON_GOING_TRANSFER = 'Ongoing transfer'
    SENT = 'SENT'
    RECEIVED = 'RECEIVED'
    INTERNAL = 'INTERNAL'
    SEND = 'send'
    RECEIVE = 'receive'
    SEND_BTC = 'send_btc'
    RECEIVE_BTC = 'receive_btc'


class AssetTransferStatusEnumModel(str, Enum):
    """Transder status for asset transaction"""
    ISSUANCE = 'Issuance'
    RECEIVE_BLIND = 'ReceiveBlind'
    RECEIVE_WITNESS = 'ReceiveWitness'
    SEND = 'Send'


class NativeAuthType(str, Enum):
    """Enum for authentication type for native"""
    LOGGING_TO_APP = 'LOGGING_TO_APP'
    # operation like issue nia or cfa  and transactions
    MAJOR_OPERATION = 'MAJOR_OPERATION'


class PaymentStatus(str, Enum):
    'Enum for payment status of ln transaction'
    PENDING = 'Pending'
    FAILED = 'Failed'
    SUCCESS = 'Succeeded'


class WalletType(str, Enum):
    """Enum for wallet type"""
    EMBEDDED_TYPE_WALLET = 'embedded'
    REMOTE_TYPE_WALLET = 'remote'


class AssetType(str, Enum):
    """Enum for asset type"""
    NIA = 'NIA'
    CFA = 'CFA'
    UDA = 'UDA'
    BITCOIN = 'BITCOIN'


class TransferType(str, Enum):
    """Enum for transfer type"""
    CREATEUTXOS = 'CreateUtxos'
    ISSUANCE = 'Issuance'
    OFF_CHAIN = 'Off chain'
    ON_CHAIN = 'On chain'
    LIGHTNING = 'Lightning'


class TokenSymbol(str, Enum):
    """Enum for token symbol"""
    BITCOIN = 'BTC'
    TESTNET_BITCOIN = 'tBTC'
    TESTNET4_BITCOIN = 'tBTC'
    REGTEST_BITCOIN = 'rBTC'
    SAT = 'SAT'


class UnitType(str, Enum):
    """Enum for expiry time unit"""
    MINUTES = 'minutes'
    HOURS = 'hours'
    DAYS = 'days'


class TransferOptionModel(str, Enum):
    """Enum for distinguish transfer type"""
    ON_CHAIN = 'on_chain'
    LIGHTNING = 'lightning'


class LoaderDisplayModel(str, Enum):
    """Enum for loader display modes."""
    FULL_SCREEN = 'full_screen'
    TOP_OF_SCREEN = 'top_of_screen'


class ToastPreset(Enum):
    """Enum for toast preset"""
    SUCCESS = 1
    WARNING = 2
    ERROR = 3
    INFORMATION = 4


class ChannelFetchingModel(str, Enum):
    """Enum for channel fetching"""
    FETCHING = 'fetching'
    FETCHED = 'fetched'
    FAILED = 'failed'


class AssignmentEnumModel(str, Enum):
    """Enum for assignment"""
    FUNGIBLE = 'Fungible'
    NON_FUNGIBLE = 'NonFungible'
    INFLATION_RIGHT = 'InflationRight'
    REPLACE_RIGHT = 'ReplaceRight'
    ANY = 'Any'
