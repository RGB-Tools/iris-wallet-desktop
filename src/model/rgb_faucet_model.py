# pylint:disable=too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""
This module defines Pydantic models related to faucet.
"""
from __future__ import annotations

from pydantic import BaseModel


# -------------------- Helper models -----------------------
class ListFaucetAssetBalance(BaseModel):
    """Represents the balance details for a faucet asset."""
    future: int
    settled: int
    spendable: int


class ListFaucetAssetDetail(BaseModel):
    """Represents the detailed information of a faucet asset."""
    balance: ListFaucetAssetBalance
    details: str | None = None
    name: str
    precision: int
    ticker: str


class RequestFaucetAsset(BaseModel):
    """Model for requesting a specific amount of a faucet asset."""
    amount: int
    asset_id: str
    details: str | None
    name: str
    precision: int
    ticker: str


class RequestDistribution(BaseModel):
    """Represents the distribution mode for an asset request."""
    mode: int


class BriefAssetInfo(BaseModel):
    """Represents brief information about an asset."""
    asset_name: str
    asset_id: str


class ListAvailableAsset(BaseModel):
    """Model for listing available assets in the faucet."""
    faucet_assets: list[BriefAssetInfo | None] | None = []


class Group(BaseModel):
    """Represents a group with distribution information."""
    distribution: RequestDistribution
    label: str
    requests_left: int

# -------------------- Request models of apis-----------------------


class RequestFaucetAssetModel(BaseModel):
    """Request model for a faucet asset, including wallet ID and invoice."""
    wallet_id: str
    invoice: str
    asset_group: str

# -------------------- Response models of apis-----------------------


class RequestAssetResponseModel(BaseModel):
    """Response model for an asset request, including asset and distribution details."""
    asset: RequestFaucetAsset
    distribution: RequestDistribution


class ListAssetResponseModel(BaseModel):
    """Response model listing all assets with their details."""
    assets: dict[str, ListFaucetAssetDetail]


class ConfigWalletResponse(BaseModel):
    """Represents the configuration response for a wallet, including asset groups."""
    groups: dict[str, Group]
    name: str
