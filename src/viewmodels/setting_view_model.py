"""This module contains the SettingViewModel class, which represents the view model
for the term and conditions page activities.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from src.data.repository.common_operations_repository import CommonOperationRepository
from src.data.repository.setting_card_repository import SettingCardRepository
from src.data.repository.setting_repository import SettingRepository
from src.data.service.common_operation_service import CommonOperationService
from src.model.common_operation_model import CheckIndexerUrlRequestModel
from src.model.common_operation_model import CheckProxyEndpointRequestModel
from src.model.enums.enums_model import NativeAuthType
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
from src.model.setting_model import IsHideExhaustedAssetEnabled
from src.model.setting_model import IsNativeLoginIntoAppEnabled
from src.model.setting_model import IsShowHiddenAssetEnabled
from src.model.setting_model import NativeAuthenticationStatus
from src.model.setting_model import SettingPageLoadModel
from src.utils.constant import FEE_RATE
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import LN_INVOICE_EXPIRY_TIME
from src.utils.constant import LN_INVOICE_EXPIRY_TIME_UNIT
from src.utils.constant import MIN_CONFIRMATION
from src.utils.constant import SAVED_ANNOUNCE_ADDRESS
from src.utils.constant import SAVED_ANNOUNCE_ALIAS
from src.utils.constant import SAVED_BITCOIND_RPC_HOST
from src.utils.constant import SAVED_BITCOIND_RPC_PORT
from src.utils.constant import SAVED_INDEXER_URL
from src.utils.constant import SAVED_PROXY_ENDPOINT
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_KEYRING
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.error_message import ERROR_UNABLE_TO_SET_EXPIRY_TIME
from src.utils.error_message import ERROR_UNABLE_TO_SET_FEE
from src.utils.error_message import ERROR_UNABLE_TO_SET_INDEXER_URL
from src.utils.error_message import ERROR_UNABLE_TO_SET_MIN_CONFIRMATION
from src.utils.error_message import ERROR_UNABLE_TO_SET_PROXY_ENDPOINT
from src.utils.helpers import get_bitcoin_config
from src.utils.info_message import INFO_SET_ENDPOINT_SUCCESSFULLY
from src.utils.info_message import INFO_SET_EXPIRY_TIME_SUCCESSFULLY
from src.utils.info_message import INFO_SET_FEE_RATE_SUCCESSFULLY
from src.utils.info_message import INFO_SET_MIN_CONFIRMATION_SUCCESSFULLY
from src.utils.local_store import local_store
from src.utils.worker import ThreadManager
from src.views.components.toast import ToastManager


class SettingViewModel(QObject, ThreadManager):
    """This class represents the activities of the term and conditions page."""
    native_auth_enable_event = Signal(bool)
    native_auth_logging_event = Signal(bool)
    hide_asset_event = Signal(bool)
    exhausted_asset_event = Signal(bool)
    fee_rate_set_event = Signal(str)
    expiry_time_set_event = Signal(str, str)
    indexer_url_set_event = Signal(str)
    proxy_endpoint_set_event = Signal(str)
    bitcoind_rpc_host_set_event = Signal(str)
    bitcoind_rpc_port_set_event = Signal(int)
    announce_address_set_event = Signal(list[str])
    announce_alias_set_event = Signal(str)
    min_confirmation_set_event = Signal(int)
    on_page_load_event = Signal(SettingPageLoadModel)
    on_error_validation_keyring_event = Signal()
    on_success_validation_keyring_event = Signal()
    loading_status = Signal(bool)
    is_loading = Signal(bool)

    def __init__(self, page_navigation):
        super().__init__()
        self._page_navigation = page_navigation
        self.login_toggle: bool = False
        self.auth_toggle: bool = False
        self.indexer_url = None
        self.password = None
        self.key = None
        self.value = None

    def on_success_native_login(self, success: bool):
        """Callback function after native authentication successful"""
        if success:
            is_set: bool = SettingRepository.enable_logging_native_authentication(
                self.login_toggle,
            )
            if is_set is False:
                self.native_auth_logging_event.emit(not self.login_toggle)
                ToastManager.info(
                    description=ERROR_KEYRING,
                )
            else:
                self.native_auth_logging_event.emit(self.login_toggle)
        else:
            self.native_auth_logging_event.emit(not self.login_toggle)
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def on_success_native_auth(self, success: bool):
        """Callback function after native authentication successful"""
        if success:
            is_set: bool = SettingRepository.set_native_authentication_status(
                self.auth_toggle,
            )
            if is_set is False:
                self.native_auth_enable_event.emit(not self.auth_toggle)
                ToastManager.info(
                    description=ERROR_KEYRING,
                )
            else:
                self.native_auth_enable_event.emit(self.auth_toggle)
        else:
            self.native_auth_enable_event.emit(not self.auth_toggle)
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def on_error_native_login(self, error: Exception):
        """Callback function on error"""
        description = error.message if isinstance(
            error, CommonException,
        ) else ERROR_SOMETHING_WENT_WRONG
        ToastManager.error(description=description)
        self.native_auth_logging_event.emit(not self.login_toggle)

    def on_error_native_auth(self, error: Exception):
        """Callback function on error"""
        description = error.message if isinstance(
            error, CommonException,
        ) else ERROR_SOMETHING_WENT_WRONG
        ToastManager.error(description=description)
        self.native_auth_enable_event.emit(not self.auth_toggle)

    def enable_native_logging(self, is_checked: bool):
        """This method is used for accepting the terms and conditions."""
        self.login_toggle = is_checked
        self.run_in_thread(
            SettingRepository.native_authentication,
            {
                'args': [NativeAuthType.LOGGING_TO_APP],
                'callback': self.on_success_native_login,
                'error_callback': self.on_error_native_login,
            },
        )

    def enable_native_authentication(self, is_checked: bool):
        """This method is used for decline the terms and conditions."""
        self.auth_toggle = is_checked
        self.run_in_thread(
            SettingRepository.native_authentication,
            {
                'args': [NativeAuthType.MAJOR_OPERATION],
                'callback': self.on_success_native_auth,
                'error_callback': self.on_error_native_auth,
            },
        )

    def enable_exhausted_asset(self, is_checked: bool):
        """This method is used for decline the terms and conditions."""
        try:
            success: IsHideExhaustedAssetEnabled = SettingRepository.enable_exhausted_asset(
                is_checked,
            )
            if success.is_enabled:
                self.exhausted_asset_event.emit(is_checked)
            else:
                self.exhausted_asset_event.emit(not is_checked)
        except CommonException as error:
            self.exhausted_asset_event.emit(not is_checked)
            ToastManager.error(
                description=error.message,
            )
        except Exception:
            self.exhausted_asset_event.emit(not is_checked)
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def enable_hide_asset(self, is_checked: bool):
        """This method is used for decline the terms and conditions."""
        try:
            success: IsShowHiddenAssetEnabled = SettingRepository.enable_show_hidden_asset(
                is_checked,
            )
            if success.is_enabled:
                self.hide_asset_event.emit(is_checked)
            else:
                self.hide_asset_event.emit(not is_checked)
        except CommonException as exc:
            self.hide_asset_event.emit(not is_checked)
            ToastManager.error(
                description=exc.message,
            )
        except Exception:
            self.hide_asset_event.emit(not is_checked)
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def set_default_fee_rate(self, value: str):
        """Sets the default fee rate."""
        try:
            success: IsDefaultFeeRateSet = SettingCardRepository.set_default_fee_rate(
                value,
            )
            if success.is_enabled:
                ToastManager.success(
                    description=INFO_SET_FEE_RATE_SUCCESSFULLY,
                )
                self.fee_rate_set_event.emit(value)
                self.on_page_load()
            else:
                self.fee_rate_set_event.emit(str(FEE_RATE))
                ToastManager.error(
                    description=ERROR_UNABLE_TO_SET_FEE,
                )
        except CommonException as error:
            self.fee_rate_set_event.emit(str(FEE_RATE))
            ToastManager.error(
                description=error.message,
            )
        except Exception:
            self.fee_rate_set_event.emit(str(FEE_RATE))
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def set_default_expiry_time(self, time: int, unit: str):
        """
        Sets the default expiry time and unit for invoices.
        """
        try:
            success: IsDefaultExpiryTimeSet = SettingCardRepository.set_default_expiry_time(
                time, unit,
            )
            if success.is_enabled:
                ToastManager.success(
                    description=INFO_SET_EXPIRY_TIME_SUCCESSFULLY,
                )
                self.expiry_time_set_event.emit(time, unit)
                self.on_page_load()
            else:
                self.expiry_time_set_event.emit(
                    str(LN_INVOICE_EXPIRY_TIME), str(
                        LN_INVOICE_EXPIRY_TIME_UNIT,
                    ),
                )
                ToastManager.error(
                    description=ERROR_UNABLE_TO_SET_EXPIRY_TIME,
                )
        except CommonException as error:
            self.expiry_time_set_event.emit(
                str(LN_INVOICE_EXPIRY_TIME), str(LN_INVOICE_EXPIRY_TIME_UNIT),
            )
            ToastManager.error(
                description=error.message,
            )
        except Exception:
            self.expiry_time_set_event.emit(
                str(LN_INVOICE_EXPIRY_TIME), str(LN_INVOICE_EXPIRY_TIME_UNIT),
            )
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def on_page_load(self):
        'This method call on setting page load'
        try:
            status_of_native_auth_res: NativeAuthenticationStatus = (
                SettingRepository.get_native_authentication_status()
            )
            status_of_native_logging_auth_res: IsNativeLoginIntoAppEnabled = (
                SettingRepository.native_login_enabled()
            )
            status_of_hide_asset_res: IsShowHiddenAssetEnabled = (
                SettingRepository.is_show_hidden_assets_enabled()
            )
            status_of_exhausted_asset_res: IsHideExhaustedAssetEnabled = (
                SettingRepository.is_exhausted_asset_enabled()
            )
            value_of_default_fee_res: DefaultFeeRate = SettingCardRepository.get_default_fee_rate()
            value_of_default_expiry_time_res: DefaultExpiryTime = SettingCardRepository.get_default_expiry_time()
            value_of_default_indexer_url_res: DefaultIndexerUrl = SettingCardRepository.get_default_indexer_url()
            value_of_default_proxy_endpoint_res: DefaultProxyEndpoint = SettingCardRepository.get_default_proxy_endpoint()
            value_of_default_bitcoind_rpc_host_res: DefaultBitcoindHost = SettingCardRepository.get_default_bitcoind_host()
            value_of_default_bitcoind_rpc_port_res: DefaultBitcoindPort = SettingCardRepository.get_default_bitcoind_port()
            value_of_default_announce_address_res: DefaultAnnounceAddress = SettingCardRepository.get_default_announce_address()
            value_of_default_announce_alias_res: DefaultAnnounceAlias = SettingCardRepository.get_default_announce_alias()
            value_of_default_min_confirmation_res: DefaultMinConfirmation = SettingCardRepository.get_default_min_confirmation()
            self.on_page_load_event.emit(
                SettingPageLoadModel(
                    status_of_native_auth=status_of_native_auth_res,
                    status_of_native_logging_auth=status_of_native_logging_auth_res,
                    status_of_hide_asset=status_of_hide_asset_res,
                    status_of_exhausted_asset=status_of_exhausted_asset_res,
                    value_of_default_fee=value_of_default_fee_res,
                    value_of_default_expiry_time=value_of_default_expiry_time_res,
                    value_of_default_indexer_url=value_of_default_indexer_url_res,
                    value_of_default_proxy_endpoint=value_of_default_proxy_endpoint_res,
                    value_of_default_bitcoind_rpc_host=value_of_default_bitcoind_rpc_host_res,
                    value_of_default_bitcoind_rpc_port=value_of_default_bitcoind_rpc_port_res,
                    value_of_default_announce_address=value_of_default_announce_address_res,
                    value_of_default_announce_alias=value_of_default_announce_alias_res,
                    value_of_default_min_confirmation=value_of_default_min_confirmation_res,
                ),
            )
        except CommonException as exc:
            ToastManager.error(
                description=exc.message,
            )
            self._page_navigation.fungibles_asset_page()
        except Exception:
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )
            self._page_navigation.fungibles_asset_page()

    def on_success_of_keyring_validation(self):
        """This is a callback call on successfully unlock of node"""
        self.loading_status.emit(False)
        self.on_success_validation_keyring_event.emit()

    def on_error_of_keyring_enable_validation(self, error: Exception):
        """Callback function on error"""
        self.on_error_validation_keyring_event.emit()
        self.loading_status.emit(False)
        if isinstance(error, CommonException):
            ToastManager.error(
                description=error.message,
            )
        else:
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def enable_keyring(self, mnemonic: str, password: str):
        """Enable keyring status"""
        self.loading_status.emit(True)
        self.run_in_thread(
            CommonOperationService.keyring_toggle_enable_validation,
            {
                'args': [mnemonic, password],
                'callback': self.on_success_of_keyring_validation,
                'error_callback': self.on_error_of_keyring_enable_validation,
            },
        )

    def on_success_of_indexer_url_set(self, indexer_url):
        """Callback on successful setting of the indexer URL."""
        # Attempt to unlock the wallet using the new URL
        if self.unlock_the_wallet(SAVED_INDEXER_URL, indexer_url):
            success: IsDefaultEndpointSet = SettingCardRepository.set_default_endpoints(
                SAVED_INDEXER_URL,
                indexer_url,
            )
            if success.is_enabled:
                self.indexer_url_set_event.emit(indexer_url)

    def on_error_of_indexer_url_set(self):
        """Callback on error during setting of the indexer URL."""

        # Notify the user of the error
        ToastManager.error(
            description=ERROR_UNABLE_TO_SET_INDEXER_URL,
        )
        self._page_navigation.settings_page()
        try:
            self.unlock_the_wallet()
        except CommonException as exc:
            ToastManager.error(
                description=f"Unlock failed: {str(exc.message)}",
            )

    def check_indexer_url_endpoint(self, indexer_url: str, password: str):
        """
        Validates and sets the indexer URL in a background thread.
        Args:
            indexer_url (str): The new indexer URL to validate and set.
        """

        self.is_loading.emit(True)
        indexer_url = indexer_url.strip()
        self.password = password
        request_model = CheckIndexerUrlRequestModel(indexer_url=indexer_url)

        # Call the repository logic in a thread to avoid blocking the UI
        self.run_in_thread(
            SettingCardRepository.check_indexer_url,
            {
                'args': [request_model],
                'callback': lambda: self.on_success_of_indexer_url_set(indexer_url),
                'error_callback': self.on_error_of_indexer_url_set,
            },
        )

    def unlock_the_wallet(self, key=None, value=None):
        """
        Attempts to unlock the wallet, prioritizing the provided URL and falling back to the previous URL if necessary.
        Args:
            key (str): The key to access the stored URL.
            value (str): The new value (URL) to attempt unlocking with.
        """
        password = self.password
        stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()

        try:

            bitcoin_config = get_bitcoin_config(stored_network, password)
            if key and value is not None:
                bitcoin_config = bitcoin_config.copy(update={key: value})
            self.run_in_thread(
                CommonOperationRepository.unlock,
                {
                    'args': [bitcoin_config],
                    'callback': lambda: self._on_success_of_unlock(key, value),
                    'error_callback': self._on_error_of_unlock,
                },
            )
        except CommonException as e:
            self._on_error_of_unlock(e)

    def _on_success_of_unlock(self, key, value):
        """Callback for successful unlocking."""
        if key and value is not None:
            key_mapping = {
                SAVED_INDEXER_URL: 'indexer_endpoint',
                SAVED_PROXY_ENDPOINT: 'proxy_endpoint',
                SAVED_BITCOIND_RPC_HOST: 'bitcoind_rpc_host_endpoint',
                SAVED_BITCOIND_RPC_PORT: 'bitcoind_rpc_port_endpoint',
                SAVED_ANNOUNCE_ADDRESS: 'announce_address_endpoint',
                SAVED_ANNOUNCE_ALIAS: 'announce_alias_endpoint',
            }
            if isinstance(value, list):
                value = ', '.join(str(item) for item in value)

            local_store.set_value(key, value)
            key = QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, key_mapping.get(key), None,
            )
            ToastManager.success(
                description=INFO_SET_ENDPOINT_SUCCESSFULLY.format(key),
            )
        self.is_loading.emit(False)
        self.on_page_load()

    def _on_error_of_unlock(self, error: CommonException):
        """Callback for failed unlock."""
        try:
            if error.message == QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, 'wrong_password', None):

                ToastManager.error(
                    description=error.message,
                )
                self._page_navigation.enter_wallet_password_page()
                return

            ToastManager.error(
                description=f"Unlock failed: {str(error.message)}",
            )
            self.is_loading.emit(False)
            self.unlock_the_wallet()
        except CommonException as exc:
            ToastManager.error(
                description=f"Unlock failed: {str(exc.message)}",
            )
        self.is_loading.emit(False)

    def _on_success_of_proxy_endpoint_set(self, proxy_endpoint):
        """Callback on successful setting of the proxy endpoint."""
        if self.unlock_the_wallet(SAVED_PROXY_ENDPOINT, proxy_endpoint):
            success: IsDefaultEndpointSet = SettingCardRepository.set_default_endpoints(
                SAVED_PROXY_ENDPOINT,
                proxy_endpoint,
            )
            if success.is_enabled:
                self.proxy_endpoint_set_event.emit(proxy_endpoint)

    def _on_error_of_proxy_endpoint_set(self):
        """Callback on error during setting of the proxy endpoint."""
        try:
            ToastManager.error(
                description=ERROR_UNABLE_TO_SET_PROXY_ENDPOINT,
            )
            self._page_navigation.settings_page()
            self.unlock_the_wallet()
        except CommonException as error:
            ToastManager.error(
                description=f"Unlock failed: {str(error.message)}",
            )

    def check_proxy_endpoint(self, proxy_endpoint: str, password: str):
        """
        Validates and sets the proxy endpoint in a background thread.
        Args:
            proxy_endpoint (str): The new proxy endpoint to validate and set.
        """

        self.is_loading.emit(True)
        proxy_endpoint = proxy_endpoint.strip()
        self.password = password
        request_model = CheckProxyEndpointRequestModel(
            proxy_endpoint=proxy_endpoint,
        )

        self.run_in_thread(
            SettingCardRepository.check_proxy_endpoint,
            {
                'args': [request_model],
                'callback': lambda: self._on_success_of_proxy_endpoint_set(proxy_endpoint),
                'error_callback': self._on_error_of_proxy_endpoint_set,
            },
        )

    def set_bitcoind_host(self, bitcoind_host: str, password: str):
        """Sets the Default bitcoind host."""
        self.is_loading.emit(True)
        try:
            self.password = password
            if self._lock_wallet(SAVED_BITCOIND_RPC_HOST, bitcoind_host):
                success: IsDefaultEndpointSet = SettingCardRepository.set_default_endpoints(
                    SAVED_BITCOIND_RPC_HOST, bitcoind_host,
                )
                if success.is_enabled:
                    self.bitcoind_rpc_host_set_event.emit(bitcoind_host)
                    self.on_page_load()
        except CommonException as error:
            self.is_loading.emit(False)
            ToastManager.error(
                description=error.message,
            )

    def set_bitcoind_port(self, bitcoind_port: int, password: str):
        """Sets the Default bitcoind port."""
        self.is_loading.emit(True)
        try:
            self.password = password
            if self._lock_wallet(SAVED_BITCOIND_RPC_PORT, bitcoind_port):
                success: IsDefaultEndpointSet = SettingCardRepository.set_default_endpoints(
                    SAVED_BITCOIND_RPC_PORT, bitcoind_port,
                )
                if success.is_enabled:
                    self.bitcoind_rpc_port_set_event.emit(bitcoind_port)
                    self.on_page_load()
        except CommonException as error:
            self.is_loading.emit(False)
            ToastManager.error(
                description=error.message,
            )

    def set_announce_address(self, announce_address: str, password: str):
        """Sets the Default announce address."""
        self.is_loading.emit(True)

        try:
            self.password = password
            if self._lock_wallet(SAVED_ANNOUNCE_ADDRESS, [announce_address]):
                success: IsDefaultEndpointSet = SettingCardRepository.set_default_endpoints(
                    SAVED_ANNOUNCE_ADDRESS, announce_address,
                )
                if success.is_enabled:
                    self.announce_address_set_event.emit(announce_address)
                    self.on_page_load()
        except CommonException as error:
            self.is_loading.emit(False)
            ToastManager.error(
                description=error.message,
            )

    def set_announce_alias(self, announce_alias: str, password: str):
        """Sets the Default announce alias."""
        self.is_loading.emit(True)
        try:
            self.password = password
            if self._lock_wallet(SAVED_ANNOUNCE_ALIAS, announce_alias):
                success: IsDefaultEndpointSet = SettingCardRepository.set_default_endpoints(
                    SAVED_ANNOUNCE_ALIAS, announce_alias,
                )
                if success.is_enabled:
                    self.announce_alias_set_event.emit(announce_alias)
                    self.on_page_load()
        except CommonException as error:
            self.is_loading.emit(False)
            ToastManager.error(
                description=error.message,
            )

    def set_min_confirmation(self, min_confirmation: int):
        """Sets the default min confirmation."""
        try:
            success: IsDefaultMinConfirmationSet = SettingCardRepository.set_default_min_confirmation(
                min_confirmation,
            )
            if success.is_enabled:
                ToastManager.success(
                    description=INFO_SET_MIN_CONFIRMATION_SUCCESSFULLY,
                )
                self.min_confirmation_set_event.emit(min_confirmation)
                self.on_page_load()
            else:
                self.min_confirmation_set_event.emit(MIN_CONFIRMATION)
                ToastManager.error(
                    description=ERROR_UNABLE_TO_SET_MIN_CONFIRMATION,
                )
        except CommonException as error:
            self.min_confirmation_set_event.emit(MIN_CONFIRMATION)
            ToastManager.error(
                description=error.message,
            )
        except Exception:
            self.min_confirmation_set_event.emit(MIN_CONFIRMATION)
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def _lock_wallet(self, key, value):
        """Lock the wallet."""
        self.key = key
        self.value = value
        self.run_in_thread(
            CommonOperationRepository.lock, {
                'args': [],
                'callback': self._on_success_lock,
                'error_callback': self._on_error_lock,
            },
        )

    def _on_success_lock(self):
        """Handle success callback after lock the wallet."""
        self.unlock_the_wallet(self.key, self.value)

    def _on_error_lock(self, error: CommonException):
        """Handle error callback after lock the wallet."""
        self.is_loading.emit(False)
        ToastManager.error(
            description=error.message,
        )
