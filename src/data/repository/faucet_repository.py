"""Module containing Apis call for faucet."""
from __future__ import annotations

import requests

from src.model.rgb_faucet_model import ConfigWalletResponse
from src.model.rgb_faucet_model import ListAssetResponseModel
from src.model.rgb_faucet_model import RequestAssetResponseModel
from src.model.rgb_faucet_model import RequestFaucetAssetModel
from src.utils.constant import API_KEY
from src.utils.constant import API_KEY_OPERATOR
from src.utils.custom_context import repository_custom_context
from src.utils.endpoints import LIST_FAUCET_ASSETS
from src.utils.endpoints import REQUEST_FAUCET_ASSET
from src.utils.endpoints import WALLET_CONFIG
from src.utils.helpers import process_response


class FaucetRepository:
    """Faucet Repository class"""

    @staticmethod
    def list_available_faucet_asset(faucet_url: str) -> ListAssetResponseModel:
        """List available asset of faucet"""
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': API_KEY_OPERATOR,
        }
        with repository_custom_context():
            response = requests.get(
                f'{faucet_url}{LIST_FAUCET_ASSETS}', headers=headers,
            )
            data = process_response(response, invalidate_cache=False)
            return ListAssetResponseModel(**data)

    @staticmethod
    def config_wallet(faucet_url: str, wallet_xpub: str) -> ConfigWalletResponse:
        """Configure the requested wallet in faucet"""
        headers = {'Content-Type': 'application/json', 'x-api-key': API_KEY}
        with repository_custom_context():
            response = requests.get(
                f'{faucet_url}{WALLET_CONFIG}/{wallet_xpub}', headers=headers,
            )
            data = process_response(response, invalidate_cache=False)
            return ConfigWalletResponse(**data)

    @staticmethod
    def request_asset(faucet_url: str, request_asset: RequestFaucetAssetModel) -> RequestAssetResponseModel:
        """Request asset from faucet"""
        headers = {'Content-Type': 'application/json', 'x-api-key': API_KEY}
        payload = request_asset.dict()
        with repository_custom_context():
            response = requests.post(
                f'{faucet_url}{REQUEST_FAUCET_ASSET}', headers=headers, json=payload,
            )
            data = process_response(response, invalidate_cache=True)
            return RequestAssetResponseModel(**data)
