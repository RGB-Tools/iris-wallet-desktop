"""
This module provides helper functions to main asset page
"""
from __future__ import annotations

from src.data.repository.rgb_repository import RgbRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.model.rgb_model import AssetModel
from src.model.rgb_model import GetAssetMediaModelRequestModel
from src.model.rgb_model import GetAssetMediaModelResponseModel
from src.utils.custom_exception import ServiceOperationException


def get_offline_asset_ticker(network: NetworkEnumModel):
    """
    Returns the offline asset ticker based on the current network configuration.

    Returns:
        str: The asset ticker.

    Raises:
        ServiceOperationException: If the network configuration is invalid or fails.
    """
    try:
        if network.value == NetworkEnumModel.REGTEST.value:
            return 'r' + 'BTC'
        if network.value in (NetworkEnumModel.TESTNET.value, NetworkEnumModel.TESTNET4.value):
            return 't' + 'BTC'
        if network.value == NetworkEnumModel.MAINNET.value:
            return 'BTC'
        raise ServiceOperationException('INVALID_NETWORK_CONFIGURATION')
    except ServiceOperationException as exc:
        raise exc
    except Exception as exc:
        raise ServiceOperationException('FAILED_TO_GET_ASSET_TICKER') from exc


def get_asset_name(network: NetworkEnumModel):
    """
    Returns the asset name based on the current network configuration.

    Returns:
        str: The asset name.

    Raises:
        ServiceOperationException: If the network configuration is invalid or fails.
    """
    try:
        if network.value == NetworkEnumModel.REGTEST.value:
            return 'r' + 'Bitcoin'
        if network.value in (NetworkEnumModel.TESTNET.value, NetworkEnumModel.TESTNET4.value):
            return 't' + 'Bitcoin'
        if network.value == NetworkEnumModel.MAINNET.value:
            return 'Bitcoin'
        raise ServiceOperationException('INVALID_NETWORK_CONFIGURATION')
    except ServiceOperationException as exc:
        raise exc
    except Exception as exc:
        raise ServiceOperationException('FAILED_TO_GET_ASSET_NAME') from exc


def convert_digest_to_hex(asset: AssetModel) -> AssetModel:
    """Call getassetmedia api and convert into hex from digest"""
    try:
        if asset.media is None:
            return asset
        digest = asset.media.digest
        image_hex: GetAssetMediaModelResponseModel = RgbRepository.get_asset_media_hex(
            GetAssetMediaModelRequestModel(digest=digest),
        )
        asset.media.hex = image_hex.bytes_hex
        return asset
    except Exception as exc:
        raise exc
