"""This module contains helper methods for faucet"""
from __future__ import annotations

import hashlib

from src.model.enums.enums_model import NetworkEnumModel
from src.utils.constant import rgbMainnetFaucetURLs
from src.utils.constant import rgbRegtestFaucetURLs
from src.utils.constant import rgbTestnet4FaucetURLs
from src.utils.constant import rgbTestnetFaucetURLs
from src.utils.custom_exception import ServiceOperationException
from src.utils.error_message import ERROR_FAILED_TO_GET_FAUCET_URL
from src.utils.error_message import ERROR_INVALID_NETWORK_TYPE


def get_faucet_url(network: NetworkEnumModel) -> str:
    """Return faucet url according to network"""
    try:
        if network.value == NetworkEnumModel.REGTEST.value:
            return rgbRegtestFaucetURLs[0]
        if network.value == NetworkEnumModel.TESTNET.value:
            return rgbTestnetFaucetURLs[0]
        if network.value == NetworkEnumModel.TESTNET4.value:
            return rgbTestnet4FaucetURLs[0]
        if network.value == NetworkEnumModel.MAINNET.value:
            return rgbMainnetFaucetURLs[0]
        raise ServiceOperationException(ERROR_INVALID_NETWORK_TYPE)
    except ServiceOperationException as exc:
        raise exc
    except Exception as exc:
        raise ServiceOperationException(
            ERROR_FAILED_TO_GET_FAUCET_URL,
        ) from exc


def generate_sha256_hash(input_string: str) -> str:
    """Generate SHA-256 hash of the input string."""
    # Create a new sha256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes of the input string
    sha256_hash.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the digest
    return sha256_hash.hexdigest()
