# pylint:disable=too-few-public-methods
# Model classes are used to store data and don't require methods.
"""
Bitcoin Model Module
====================

This module defines Pydantic models related to Bitcoin transactions and addresses.
"""
from __future__ import annotations

from pydantic import BaseModel

from src.model.enums.enums_model import TransactionStatusEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.rgb_model import AssignmentModel

# -------------------- Helper models -----------------------


class ConfirmationTime(BaseModel):
    """Model part of transaction list api response model"""
    height: int
    timestamp: int


class Transaction(BaseModel):
    """Model part of transaction list api response model"""
    transaction_type: str
    txid: str
    received: int
    sent: int
    fee: int
    amount: str | None = None
    transfer_status: TransferStatusEnumModel | None = None
    transaction_status: TransactionStatusEnumModel | None = None
    confirmation_normal_time: str | None = None
    confirmation_date: str | None = None
    confirmation_time: ConfirmationTime | None = None


class Utxo(BaseModel):
    """Model part of list unspents api response model"""
    outpoint: str
    btc_amount: int
    colorable: bool


class RgbAllocation(BaseModel):
    """Model part of list unspents api response model"""
    asset_id: str | None = None
    assignment: AssignmentModel
    settled: bool


class Unspent(BaseModel):
    """Model part of list unspents api response model"""
    utxo: Utxo
    rgb_allocations: list[RgbAllocation | None]


class BalanceStatus(BaseModel):
    """Model representing the status of a Bitcoin balance."""

    settled: int
    future: int
    spendable: int


class OfflineAsset(BaseModel):
    """Model for offline asset"""
    asset_id: str | None = None
    ticker: str
    balance: BalanceStatus
    name: str


# -------------------- Request Models -----------------------

class EstimateFeeRequestModel(BaseModel):
    """Model for estimated fee"""
    blocks: int


class SendBtcRequestModel(BaseModel):
    """Model representing a request to send Bitcoin."""

    amount: int
    address: str
    fee_rate: int
    skip_sync: bool = False

# -------------------- Response Models -----------------------


class TransactionListResponse(BaseModel):
    """Model representing response of list transaction api"""
    transactions: list[Transaction | None]


class TransactionListWithBalanceResponse(TransactionListResponse):
    """Model representing response of list transaction api"""
    balance: BalanceResponseModel


class UnspentsListResponseModel(BaseModel):
    """Model representing response of list unspents api"""
    unspents: list[Unspent | None]


class SendBtcResponseModel(BaseModel):
    """Model representing response of sendbtc api"""
    txid: str


class BalanceResponseModel(BaseModel):
    """Model representing a response containing Bitcoin balance information."""

    vanilla: BalanceStatus
    colored: BalanceStatus


class AddressResponseModel(BaseModel):
    """Model representing a response containing a Bitcoin address."""

    address: str


class EstimateFeeResponse(BaseModel):
    """Model representing a response containing the estimated fee_rate"""
    fee_rate: float
