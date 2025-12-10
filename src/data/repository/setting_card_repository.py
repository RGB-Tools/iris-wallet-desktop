""""This module defines a repository class for managing settings card related to wallet initialization.
"""
from __future__ import annotations

from src.data.repository.setting_repository import SettingRepository
from src.model.common_operation_model import CheckIndexerUrlRequestModel
from src.model.common_operation_model import CheckIndexerUrlResponseModel
from src.model.common_operation_model import CheckProxyEndpointRequestModel
from src.model.enums.enums_model import NetworkEnumModel
from src.model.setting_model import DefaultAnnounceAddress
from src.model.setting_model import DefaultAnnounceAlias
from src.model.setting_model import DefaultBitcoindHost
from src.model.setting_model import DefaultBitcoindPort
from src.model.setting_model import DefaultExpiryTime
from src.model.setting_model import DefaultFeeRate
from src.model.setting_model import DefaultIndexerUrl
from src.model.setting_model import DefaultMinConfirmation
from src.model.setting_model import DefaultProxyEndpoint
from src.model.setting_model import IsDefaultEndpointSet
from src.model.setting_model import IsDefaultExpiryTimeSet
from src.model.setting_model import IsDefaultFeeRateSet
from src.model.setting_model import IsDefaultMinConfirmationSet
from src.utils.constant import ANNOUNCE_ADDRESS
from src.utils.constant import ANNOUNCE_ALIAS
from src.utils.constant import BITCOIND_RPC_HOST_MAINNET
from src.utils.constant import BITCOIND_RPC_HOST_REGTEST
from src.utils.constant import BITCOIND_RPC_HOST_TESTNET
from src.utils.constant import BITCOIND_RPC_HOST_TESTNET4
from src.utils.constant import BITCOIND_RPC_PORT_MAINNET
from src.utils.constant import BITCOIND_RPC_PORT_REGTEST
from src.utils.constant import BITCOIND_RPC_PORT_TESTNET
from src.utils.constant import BITCOIND_RPC_PORT_TESTNET4
from src.utils.constant import FEE_RATE
from src.utils.constant import INDEXER_URL_MAINNET
from src.utils.constant import INDEXER_URL_REGTEST
from src.utils.constant import INDEXER_URL_TESTNET
from src.utils.constant import INDEXER_URL_TESTNET4
from src.utils.constant import LN_INVOICE_EXPIRY_TIME
from src.utils.constant import LN_INVOICE_EXPIRY_TIME_UNIT
from src.utils.constant import MIN_CONFIRMATION
from src.utils.constant import PROXY_ENDPOINT_MAINNET
from src.utils.constant import PROXY_ENDPOINT_REGTEST
from src.utils.constant import PROXY_ENDPOINT_TESTNET
from src.utils.constant import PROXY_ENDPOINT_TESTNET4
from src.utils.constant import SAVED_ANNOUNCE_ADDRESS
from src.utils.constant import SAVED_ANNOUNCE_ALIAS
from src.utils.constant import SAVED_BITCOIND_RPC_HOST
from src.utils.constant import SAVED_BITCOIND_RPC_PORT
from src.utils.constant import SAVED_INDEXER_URL
from src.utils.constant import SAVED_PROXY_ENDPOINT
from src.utils.custom_context import repository_custom_context
from src.utils.decorators.lock_required import lock_required
from src.utils.endpoints import CHECK_INDEXER_URL_ENDPOINT
from src.utils.endpoints import CHECK_PROXY_ENDPOINT
from src.utils.handle_exception import handle_exceptions
from src.utils.local_store import local_store
from src.utils.request import Request


class SettingCardRepository:
    """
    Manages wallet settings such as fee rate, expiry time, indexer URL, and proxy endpoint.
    Provides methods to set and get these settings, and to validate indexer URLs and proxy endpoints.
    """
    @staticmethod
    def set_default_fee_rate(rate: str) -> IsDefaultFeeRateSet:
        """
        Sets the default fee rate.

        Args:
            rate (float | int): The fee rate to set.

        Returns:
            IsDefaultFeeRateSet: A model indicating whether the default fee rate is set.
        """
        try:
            local_store.set_value('defaultFeeRate', rate)
            # Verify the setting was applied
            if local_store.get_value('defaultFeeRate', value_type=int):
                return IsDefaultFeeRateSet(is_enabled=True)
            return IsDefaultFeeRateSet(is_enabled=False)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def get_default_fee_rate() -> DefaultFeeRate:
        """
        Gets the default fee rate.

        Returns:
            DefaultFeeRate: A model indicating the default fee rate.
        """
        try:
            fee_rate = local_store.get_value('defaultFeeRate')
            if fee_rate is None:
                fee_rate = FEE_RATE
            return DefaultFeeRate(fee_rate=fee_rate)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def set_default_expiry_time(time: int, unit: str) -> IsDefaultExpiryTimeSet:
        """
        Sets the default expiry time and unit.

        Args:
            time (int): The expiry time to set.
            unit (str): The expiry time unit to set

        Returns:
            ISDefaultExpiryTimeSet: A model indicating whether the default expiry time is set.
        """
        try:
            local_store.set_value('defaultExpiryTime', time)
            local_store.set_value('defaultExpiryTimeUnit', unit)

            # Verify the setting was applied
            if local_store.get_value('defaultExpiryTime', value_type=int) and local_store.get_value('defaultExpiryTimeUnit', value_type=str):
                return IsDefaultExpiryTimeSet(is_enabled=True)
            return IsDefaultExpiryTimeSet(is_enabled=False)

        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def get_default_expiry_time() -> DefaultExpiryTime:
        """
        Gets the default expiry time and its unit.

        Returns:
            DefaultExpiryTime: A model indicating the default expiry time and its unit.
        """
        try:
            time = local_store.get_value('defaultExpiryTime')
            unit = local_store.get_value('defaultExpiryTimeUnit')
            if time is None and unit is None:
                time = LN_INVOICE_EXPIRY_TIME
                unit = LN_INVOICE_EXPIRY_TIME_UNIT
            return DefaultExpiryTime(time=time, unit=unit)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    @lock_required
    def check_indexer_url(url: CheckIndexerUrlRequestModel) -> CheckIndexerUrlResponseModel:
        """
        Check the validity of the given indexer URL by sending a POST request to the check indexer URL endpoint.

        Args:
            url (CheckIndexerUrlRequestModel): The request model containing the URL to be checked.

        Returns:
            CheckIndexerUrlResponseModel: The response model containing the result of the URL check.

        Raises:
            HTTPError: If the request results in an HTTP error (4xx or 5xx).
        """
        with repository_custom_context():
            payload = url.dict()
            response = Request.post(CHECK_INDEXER_URL_ENDPOINT, payload)
            response.raise_for_status()
            data = response.json()
            return CheckIndexerUrlResponseModel(**data)

    @staticmethod
    def set_default_endpoints(key, value: str | int) -> IsDefaultEndpointSet:
        """
        Sets the default endpoint value.

        Args:
            key (str): The key to store the endpoint value.
            value (str | int): The value to be set for the specified key.

        Returns:
            IsDefaultEndpointSet: A model indicating whether the default endpoint
            value was successfully set.
        """
        try:
            local_store.set_value(key, value)

            # Verify the setting was applied
            stored_value = local_store.get_value(key)
            if stored_value == str(value) or stored_value == int(value):
                return IsDefaultEndpointSet(is_enabled=True)
            return IsDefaultEndpointSet(is_enabled=False)

        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def get_default_indexer_url() -> DefaultIndexerUrl:
        """
        Gets the default indexer url.

        Returns:
            DefaultIndexerUrl: A model indicating the default indexer url.
        """
        try:
            indexer_url = None
            stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()

            if stored_network == NetworkEnumModel.MAINNET:
                indexer_url = INDEXER_URL_MAINNET
            elif stored_network == NetworkEnumModel.TESTNET:
                indexer_url = INDEXER_URL_TESTNET
            elif stored_network == NetworkEnumModel.TESTNET4:
                indexer_url = INDEXER_URL_TESTNET4
            elif stored_network == NetworkEnumModel.REGTEST:
                indexer_url = INDEXER_URL_REGTEST
            url = local_store.get_value(SAVED_INDEXER_URL)
            if url is None:
                url = indexer_url
            return DefaultIndexerUrl(url=url)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    @lock_required
    def check_proxy_endpoint(endpoint: CheckProxyEndpointRequestModel):
        """
        Check the validity of the given indexer endpoint by sending a POST request to the check indexer URL endpoint.

        Args:
            url (CheckProxyEndpointRequestModel): The request model containing the URL to be checked.

        Raises:
            HTTPError: If the request results in an HTTP error (4xx or 5xx).
        """
        with repository_custom_context():
            payload = endpoint.dict()
            response = Request.post(CHECK_PROXY_ENDPOINT, payload)
            response.raise_for_status()
            return

    @staticmethod
    def get_default_proxy_endpoint() -> DefaultProxyEndpoint:
        """
        Gets the default proxy endpoint.

        Returns:
            DefaultProxyEndpoint: A model indicating the default proxy endpoint value.
        """
        try:
            proxy_endpoint = None
            stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()

            if stored_network == NetworkEnumModel.MAINNET:
                proxy_endpoint = PROXY_ENDPOINT_MAINNET
            elif stored_network == NetworkEnumModel.TESTNET:
                proxy_endpoint = PROXY_ENDPOINT_TESTNET
            elif stored_network == NetworkEnumModel.TESTNET4:
                proxy_endpoint = PROXY_ENDPOINT_TESTNET4
            elif stored_network == NetworkEnumModel.REGTEST:
                proxy_endpoint = PROXY_ENDPOINT_REGTEST
            endpoint = local_store.get_value(SAVED_PROXY_ENDPOINT)
            if endpoint is None:
                endpoint = proxy_endpoint
            return DefaultProxyEndpoint(endpoint=endpoint)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def get_default_bitcoind_host() -> DefaultBitcoindHost:
        """
        Gets the default bitcoind host value.

        Returns:
            DefaultBitcoindHost: A model indicating the default bitcoind host value.
        """
        try:
            bitcoind_host = None
            stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()

            if stored_network == NetworkEnumModel.MAINNET:
                bitcoind_host = BITCOIND_RPC_HOST_MAINNET
            elif stored_network == NetworkEnumModel.TESTNET:
                bitcoind_host = BITCOIND_RPC_HOST_TESTNET
            elif stored_network == NetworkEnumModel.TESTNET4:
                bitcoind_host = BITCOIND_RPC_HOST_TESTNET4
            elif stored_network == NetworkEnumModel.REGTEST:
                bitcoind_host = BITCOIND_RPC_HOST_REGTEST
            host = local_store.get_value(SAVED_BITCOIND_RPC_HOST)
            if host is None:
                host = bitcoind_host
            return DefaultBitcoindHost(host=host)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def get_default_bitcoind_port() -> DefaultBitcoindPort:
        """
        Gets the default bitcoind host value.

        Returns:
            DefaultBitcoindHost: A model indicating the default bitcoind host value.
        """
        try:
            bitcoind_port = None
            stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()

            if stored_network == NetworkEnumModel.MAINNET:
                bitcoind_port = BITCOIND_RPC_PORT_MAINNET
            elif stored_network == NetworkEnumModel.TESTNET:
                bitcoind_port = BITCOIND_RPC_PORT_TESTNET
            elif stored_network == NetworkEnumModel.TESTNET4:
                bitcoind_port = BITCOIND_RPC_PORT_TESTNET4
            elif stored_network == NetworkEnumModel.REGTEST:
                bitcoind_port = BITCOIND_RPC_PORT_REGTEST
            port = local_store.get_value(SAVED_BITCOIND_RPC_PORT)
            if port is None:
                port = bitcoind_port
            return DefaultBitcoindPort(port=port)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def get_default_announce_address() -> DefaultAnnounceAddress:
        """
        Gets the default announce address.

        Returns:
            DefaultAnnounceAddress: A model indicating the default announce address.
        """
        try:
            address = local_store.get_value(SAVED_ANNOUNCE_ADDRESS)
            if address is None:
                address = ANNOUNCE_ADDRESS
            return DefaultAnnounceAddress(address=address)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def get_default_announce_alias() -> DefaultAnnounceAlias:
        """
        Gets the default announce address.

        Returns:
            DefaultAnnounceAddress: A model indicating the default announce address.
        """
        try:
            alias = local_store.get_value(SAVED_ANNOUNCE_ALIAS)
            if alias is None:
                alias = ANNOUNCE_ALIAS
            return DefaultAnnounceAlias(alias=alias)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def set_default_min_confirmation(min_confirmation: int) -> IsDefaultMinConfirmationSet:
        """
        Sets the default min confirmation.

        Args:
            min_confirmation (int): The min confirmation to set.

        Returns:
            IsDefaultMinConfirmationSet: A model indicating whether the default min confirmation is set.
        """
        try:
            local_store.set_value('defaultMinConfirmation', min_confirmation)
            # Verify the setting was applied
            if local_store.get_value('defaultMinConfirmation', value_type=int):
                return IsDefaultMinConfirmationSet(is_enabled=True)
            return IsDefaultMinConfirmationSet(is_enabled=False)
        except Exception as exe:
            return handle_exceptions(exe)

    @staticmethod
    def get_default_min_confirmation() -> DefaultMinConfirmation:
        """
        Gets the default fee rate.

        Returns:
            DefaultFeeRate: A model indicating the default fee rate.
        """
        try:
            min_confirmation = local_store.get_value('defaultMinConfirmation')
            if min_confirmation is None:
                min_confirmation = MIN_CONFIRMATION
            return DefaultMinConfirmation(min_confirmation=min_confirmation)
        except Exception as exe:
            return handle_exceptions(exe)
