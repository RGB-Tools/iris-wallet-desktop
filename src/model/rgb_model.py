# pylint: disable=too-few-public-methods
"""Module containing models related to RGB."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator

from src.model.enums.enums_model import AssignmentEnumModel
from src.model.enums.enums_model import FilterAssetEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.payments_model import BaseTimeStamps
from src.model.payments_model import Payment
from src.utils.constant import FEE_RATE_FOR_CREATE_UTXOS
from src.utils.constant import NO_OF_UTXO
from src.utils.constant import RGB_INVOICE_DURATION_SECONDS
from src.utils.constant import UTXO_SIZE_SAT
from src.utils.custom_exception import CommonException
# -------------------- Helper models -----------------------


class StatusModel(BaseModel):
    """Response status model."""

    status: bool


class AssignmentModel(BaseModel):
    """Assignment model"""
    type: AssignmentEnumModel
    value: int | None = None


class TransactionTxModel(BaseModel):
    """Mode for get single transaction method of asset detail page service"""
    tx_id: str | None = None
    idx: int | None = None

    # 'mode='before'' ensures the validator runs before others
    @model_validator(mode='before')
    def check_at_least_one(cls, values):  # pylint: disable=no-self-argument
        """
        Ensures that at least one of tx_id or idx is provided.
        """
        tx_id, idx = values.get('tx_id'), values.get('idx')
        if tx_id is None and idx is None:
            raise CommonException("Either 'tx_id' or 'idx' must be provided")

        if tx_id is not None and idx is not None:
            raise CommonException(
                "Both 'tx_id' and 'idx' cannot be accepted at the same time.",
            )

        return values


class Media(BaseModel):
    """Model for list asset"""
    file_path: str
    digest: str
    hex: str | None = None
    mime: str


class Balance(BaseModel):
    """Model for list asset"""
    settled: int
    future: int
    spendable: int


class Token(BaseModel):
    """Model for list asset"""
    index: int
    ticker: str | None = None
    name: str | None = None
    details: str | None = None
    embedded_media: bool
    media: Media
    attachments: dict[str, Media]
    reserves: bool


class AssetModel(BaseModel):
    """Model for asset """
    asset_id: str
    ticker: str | None = None
    name: str
    details: str | None
    precision: int
    issued_supply: int
    timestamp: int
    added_at: int
    balance: AssetBalanceResponseModel
    media: Media | None = None
    token: Token | None = None


class TransportEndpoint(BaseModel):
    """Model representing transport endpoints."""

    endpoint: str
    transport_type: str
    used: bool


class TransferAsset(BaseTimeStamps):
    """Model representing asset transfers."""

    idx: int
    status: str
    requested_assignment: AssignmentModel | None
    assignments: list[AssignmentModel | None] | None = []
    amount_status: str | None = None  # this for ui purpose
    kind: str
    transfer_Status: TransferStatusEnumModel | None = None
    txid: str | None = None
    recipient_id: str | None = None
    receive_utxo: str | None = None
    change_utxo: str | None = None
    expiration: int | None = None
    transport_endpoints: list[TransportEndpoint | None] | None = []

# -------------------- Request models -----------------------


class AssetIdModel(BaseModel):
    """Request model for asset balance."""

    asset_id: str


class CreateUtxosRequestModel(BaseModel):
    """Request model for creating UTXOs."""

    up_to: bool | None = False
    num: int = NO_OF_UTXO
    size: int = UTXO_SIZE_SAT
    fee_rate: int = FEE_RATE_FOR_CREATE_UTXOS
    skip_sync: bool = False


class DecodeRgbInvoiceRequestModel(BaseModel):
    """Request model for decoding RGB invoices."""

    invoice: str


class IssueAssetNiaRequestModel(BaseModel):
    """Request model for issuing assets nia."""

    amounts: list[int]
    ticker: str
    name: str
    precision: int = 0


class IssueAssetCfaRequestModelWithDigest(IssueAssetNiaRequestModel):
    """Request model for issuing assets."""
    file_digest: str


class IssueAssetCfaRequestModel(IssueAssetNiaRequestModel):
    """Request model for issuing assets."""
    file_path: str


class IssueAssetUdaRequestModel(IssueAssetCfaRequestModel):
    """Request model for issuing assets."""
    attachments_file_paths: list[list[str]]


class RefreshRequestModel(BaseModel):
    """Request model for refresh wallet"""
    skip_sync: bool = False


class RgbInvoiceRequestModel(BaseModel):
    """Request model for RGB invoices."""

    min_confirmations: int
    asset_id: str | None = None
    duration_seconds: int = RGB_INVOICE_DURATION_SECONDS
    witness: bool = False


class SendAssetRequestModel(BaseModel):
    """Request model for sending assets."""

    asset_id: str
    assignment: AssignmentModel
    recipient_id: str
    donation: bool | None = False
    fee_rate: int
    min_confirmations: int
    transport_endpoints: list[str]
    skip_sync: bool = False


class ListTransfersRequestModel(AssetIdModel):
    """Request model for listing asset transfers."""


class FilterAssetRequestModel(BaseModel):
    """Remove"""
    filter_asset_schemas: list[FilterAssetEnumModel] = Field(
        default_factory=lambda: [FilterAssetEnumModel.NIA],
    )


class GetAssetMediaModelRequestModel(BaseModel):
    """Response model for get asset medial api"""
    digest: str


class FailTransferRequestModel(BaseModel):
    """Response model for fail transfer"""
    batch_transfer_idx: int
    no_asset_only: bool = False
    skip_sync: bool = False

# -------------------- Response models -----------------------


class AssetBalanceResponseModel(Balance):
    """Response model for asset balance."""
    offchain_outbound: int
    offchain_inbound: int


class CreateUtxosResponseModel(StatusModel):
    """Response model for creating UTXOs."""


class DecodeRgbInvoiceResponseModel(BaseModel):
    """Response model for decoding RGB invoices."""

    recipient_id: str
    asset_schema: str | None = None
    asset_id: str | None = None
    assignment: AssignmentModel | None
    network: str
    expiration_timestamp: int
    transport_endpoints: list[str]


class GetAssetResponseModel(BaseModel):
    """Response model for list assets."""
    nia: list[AssetModel | None] | None = []
    uda: list[AssetModel | None] | None = []
    cfa: list[AssetModel | None] | None = []


class IssueAssetResponseModel(AssetModel):
    """Response model for issuing assets."""


class ListTransferAssetResponseModel(BaseModel):
    """Response model for listing asset transfers."""

    transfers: list[TransferAsset | None] | None = []


class ListTransferAssetWithBalanceResponseModel(ListTransferAssetResponseModel):
    """Response model for listing asset transfers with asset balance"""
    asset_balance: AssetBalanceResponseModel


class ListOffAndOnChainTransfer(BaseModel):
    """Response model for listing on-chain and off-chain asset transfers with respective details."""
    onchain_transfers: list[TransferAsset | None] | None = []
    off_chain_transfers: list[Payment | None] | None = []


class ListOnAndOffChainTransfersWithBalance(ListOffAndOnChainTransfer):
    """Response model for listing asset transfers with asset balance"""
    asset_balance: AssetBalanceResponseModel


class RefreshTransferResponseModel(StatusModel):
    """Response model for refreshing asset transfers."""


class RgbInvoiceDataResponseModel(BaseModel):
    """Response model for invoice data."""

    recipient_id: str
    invoice: str
    expiration_timestamp: datetime
    batch_transfer_idx: int


class SendAssetResponseModel(BaseModel):
    """Response model for sending assets."""

    txid: str


class GetAssetMediaModelResponseModel(BaseModel):
    """Response model for get asset media api"""
    bytes_hex: str


class PostAssetMediaModelResponseModel(BaseModel):
    """Response model for get asset media api"""
    digest: str


class RgbAssetPageLoadModel(BaseModel):
    """RGB asset detail page load model"""
    asset_id: str | None = None
    asset_name: str | None = None
    image_path: str | None = None
    asset_type: str


class FailTransferResponseModel(BaseModel):
    """Response model for fail transfer"""
    transfers_changed: bool
