"""Module containing BTC repository."""
from __future__ import annotations

from src.model.btc_model import AddressResponseModel
from src.model.btc_model import BalanceResponseModel
from src.model.btc_model import EstimateFeeRequestModel
from src.model.btc_model import EstimateFeeResponse
from src.model.btc_model import SendBtcRequestModel
from src.model.btc_model import SendBtcResponseModel
from src.model.btc_model import TransactionListResponse
from src.model.btc_model import UnspentsListResponseModel
from src.model.common_operation_model import SkipSyncModel
from src.utils.custom_context import repository_custom_context
from src.utils.decorators.unlock_required import unlock_required
from src.utils.endpoints import ADDRESS_ENDPOINT
from src.utils.endpoints import BTC_BALANCE_ENDPOINT
from src.utils.endpoints import ESTIMATE_FEE_ENDPOINT
from src.utils.endpoints import LIST_TRANSACTIONS_ENDPOINT
from src.utils.endpoints import LIST_UNSPENT_ENDPOINT
from src.utils.endpoints import SEND_BTC_ENDPOINT
from src.utils.helpers import process_response
from src.utils.request import Request


class BtcRepository:
    """Repository for handling Bitcoin-related operations."""

    @staticmethod
    @unlock_required
    def get_address() -> AddressResponseModel:
        """Get a Bitcoin address."""
        with repository_custom_context():
            response = Request.post(ADDRESS_ENDPOINT)
            data = process_response(response)
            return AddressResponseModel(**data)

    @staticmethod
    @unlock_required
    def get_btc_balance() -> BalanceResponseModel:
        """Get Bitcoin balance."""
        with repository_custom_context():
            payload = SkipSyncModel().dict()
            response = Request.post(BTC_BALANCE_ENDPOINT, payload)
            data = process_response(response)
            return BalanceResponseModel(**data)

    @staticmethod
    @unlock_required
    def list_transactions() -> TransactionListResponse:
        """List Bitcoin transactions."""
        with repository_custom_context():
            payload = SkipSyncModel().dict()
            response = Request.post(LIST_TRANSACTIONS_ENDPOINT, payload)
            data = process_response(response)
            return TransactionListResponse(**data)

    @staticmethod
    @unlock_required
    def list_unspents() -> UnspentsListResponseModel:
        """List unspent Bitcoin."""
        with repository_custom_context():
            payload = SkipSyncModel().dict()
            response = Request.post(LIST_UNSPENT_ENDPOINT, payload)
            data = process_response(response)
            return UnspentsListResponseModel(**data)

    @staticmethod
    @unlock_required
    def send_btc(send_btc_value: SendBtcRequestModel) -> SendBtcResponseModel:
        """Send Bitcoin."""
        payload = send_btc_value.dict()
        with repository_custom_context():
            response = Request.post(SEND_BTC_ENDPOINT, payload)
            data = process_response(response, invalidate_cache=True)
            return SendBtcResponseModel(**data)

    @staticmethod
    @unlock_required
    def estimate_fee(blocks: EstimateFeeRequestModel) -> EstimateFeeResponse:
        """Get Estimate Fee"""
        payload = blocks.dict()
        with repository_custom_context():
            response = Request.post(ESTIMATE_FEE_ENDPOINT, payload)
            data = process_response(response)
            return EstimateFeeResponse(**data)
