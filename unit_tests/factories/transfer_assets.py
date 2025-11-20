"""Factory helpers for creating TransferAsset test data."""
from __future__ import annotations

from typing import Any

from src.model.rgb_model import TransferAsset


def make_transfer_asset(**overrides) -> TransferAsset:
    """Create a TransferAsset with common default optional fields, allowing overrides.
    """
    defaults: dict[str, Any] = {
        'txid': None,
        'recipient_id': None,
        'receive_utxo': None,
        'change_utxo': None,
        'expiration': None,
        'transport_endpoints': [],
    }
    defaults.update(overrides)
    return TransferAsset(**defaults)
