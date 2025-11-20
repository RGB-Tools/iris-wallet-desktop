# pylint:disable=too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""
Module containing models related to the transaction detail page.
"""
from __future__ import annotations

from pydantic import BaseModel

from src.model.enums.enums_model import PaymentStatus
from src.model.enums.enums_model import TransactionStatusEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.rgb_model import TransportEndpoint


class TransactionDetailPageModel(BaseModel):
    """
    This model is used extensively across the codebase to ensure a consistent structure
    for transaction-related data for transaction detail page. It serves as the standard format for passing transaction
    details into methods and for structuring responses from methods that deal with transaction
    information.
    """
    tx_id: str
    amount: str
    asset_id: str | None = None
    image_path: str | None = None
    asset_name: str | None = None
    confirmation_date: str | None = None
    confirmation_time: str | None = None
    updated_date: str | None = None
    updated_time: str | None = None
    transaction_status: TransactionStatusEnumModel | PaymentStatus | str
    transfer_status: TransferStatusEnumModel | None = None
    consignment_endpoints: list[TransportEndpoint | None] | None = []
    recipient_id: str | None = None
    receive_utxo: str | None = None
    change_utxo: str | None = None
    asset_type: str | None = None
    is_off_chain: bool = False
    inbound: bool | None = None
