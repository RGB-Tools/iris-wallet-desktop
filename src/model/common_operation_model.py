# pylint:disable=too-few-public-methods
# Model classes are used to store data and don't require methods.
"""Module containing common operation models."""
from __future__ import annotations

from pydantic import BaseModel

from src.model.btc_model import OfflineAsset
from src.model.rgb_model import GetAssetResponseModel


# -------------------- Helper models -----------------------

class StatusModel(BaseModel):
    """Response status model."""

    status: bool


class SkipSyncModel(BaseModel):
    """Skip sync model"""
    skip_sync: bool = False

# -------------------- Request models -----------------------


class SignMessageRequestModel(BaseModel):
    """Sign message request model."""

    message: str


class SendOnionMessageRequestModel(BaseModel):
    """Send onion message request model."""

    node_ids: list[str]
    tlv_type: int
    data: str


class CheckIndexerUrlRequestModel(BaseModel):
    """Check Indexer Url request model."""

    indexer_url: str


class CheckProxyEndpointRequestModel(BaseModel):
    """Check Proxy Endpoint request model."""

    proxy_endpoint: str


class InitRequestModel(BaseModel):
    """Init request model."""

    password: str


class ChangePasswordRequestModel(BaseModel):
    """Change password request model."""

    old_password: str
    new_password: str


class BackupRequestModel(BaseModel):
    """Backup request model."""

    backup_path: str
    password: str


class UnlockRequestModel(InitRequestModel):
    """Unlock request model."""
    bitcoind_rpc_username: str
    bitcoind_rpc_password: str
    bitcoind_rpc_host: str
    bitcoind_rpc_port: int
    indexer_url: str
    proxy_endpoint: str
    announce_addresses: list[str]
    announce_alias: str


class RestoreRequestModel(BackupRequestModel):
    """Restore request model."""


# -------------------- Response models -----------------------

class InitResponseModel(BaseModel):
    """Init response model."""

    mnemonic: str


class BackupResponseModel(StatusModel):
    """Backup response model."""


class ChangePassWordResponseModel(StatusModel):
    """Change password response model."""


class LockResponseModel(StatusModel):
    """Lock response model."""


class NetworkInfoResponseModel(BaseModel):
    """Network information response model."""

    network: str
    height: int


class NodeInfoResponseModel(BaseModel):
    """Node information response model."""

    pubkey: str
    num_channels: int
    num_usable_channels: int
    local_balance_sat: int
    eventual_close_fees_sat: int
    pending_outbound_payments_sat: int
    num_peers: int
    account_xpub_vanilla: str
    account_xpub_colored: str
    max_media_upload_size_mb: int
    rgb_htlc_min_msat: int
    rgb_channel_capacity_min_sat: int
    channel_capacity_min_sat: int
    channel_capacity_max_sat: int
    channel_asset_min_amount: int
    channel_asset_max_amount: int
    network_nodes: int
    network_channels: int


class RestoreResponseModel(StatusModel):
    """Restore response model."""


class SendOnionMessageResponseModel(StatusModel):
    """Send onion message response model."""


class ShutDownResponseModel(StatusModel):
    """Shut down response model."""


class SignMessageResponseModel(BaseModel):
    """Sign message response model."""

    signed_message: str


class UnlockResponseModel(StatusModel):
    """Unlock response model."""


class MainPageDataResponseModel(GetAssetResponseModel):
    """To extend the get asset response model for vanilla asset"""
    vanilla: OfflineAsset


class CheckIndexerUrlResponseModel(BaseModel):
    """Check Indexer Url response model."""
    indexer_protocol: str
# -------------------- Component models -----------------------


class ConfigurableCardModel(BaseModel):
    ' A model representing a configurable card for the settings page.'
    title_label: str
    title_desc: str
    suggestion_label: str | None = None
    suggestion_desc: str | None = None
    placeholder_value: float | str


class AppPathsModel(BaseModel):
    """Model representing filesystem paths used by the application and node."""
    app_path: str
    node_data_path: str
    iriswallet_temp_folder_path: str
    cache_path: str
    app_logs_path: str
    node_logs_path: str
    ldk_logs_path: str
    pickle_file_path: str
    config_file_path: str
    backup_folder_path: str
    restore_folder_path: str
