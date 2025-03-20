"""This module contains the LnEndpointViewModel class, which represents the view model
for the LnEndpoint page activities.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from src.data.repository.common_operations_repository import CommonOperationRepository
from src.data.repository.setting_repository import SettingRepository
from src.model.common_operation_model import UnlockRequestModel
from src.model.common_operation_model import UnlockResponseModel
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import WalletType
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import LIGHTNING_URL_KEY
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.custom_exception import CommonException
from src.utils.helpers import get_bitcoin_config
from src.utils.keyring_storage import set_value
from src.utils.local_store import local_store
from src.utils.logging import logger
from src.utils.worker import ThreadManager
from src.views.components.toast import ToastManager


class LnEndpointViewModel(QObject, ThreadManager):
    """This class represents the activities of the LnEndpoint page."""
    loading_message = Signal(bool)
    stop_loading_message = Signal(bool)

    def __init__(self, page_navigation) -> None:
        """
        Initialize the LnEndpointViewModel with page navigation.

        Args:
            page_navigation: The page navigation object for navigating between pages.
        """
        super().__init__()
        self._page_navigation = page_navigation
        self.network: NetworkEnumModel = SettingRepository.get_wallet_network()

    def set_ln_endpoint(self, node_url: str, validation_label) -> None:
        """
        Set the Lightning Network endpoint URL if valid, and navigate to the wallet password page.

        Args:
            node_url (str): The Lightning Network node URL to set.
        """
        self.loading_message.emit(True)
        if self.validate_url(node_url, validation_label):
            local_store.set_value(LIGHTNING_URL_KEY, node_url)
            self.loading_message.emit(True)
            bitcoin_config: UnlockRequestModel = get_bitcoin_config(
                network=self.network, password='random@123',
            )
            # Calling unlock api to know whether node initialized in case of remote node connection

            self.run_in_thread(
                CommonOperationRepository.unlock,
                {
                    'args': [bitcoin_config],
                    'callback': self.on_success,
                    'error_callback': self.on_error,
                },
            )

    def on_success(self):
        """This method handle the store mnemonic on success unlock"""
        keyring_status: bool = SettingRepository.get_keyring_status()
        if keyring_status is False:
            set_value(WALLET_PASSWORD_KEY, 'random@123')
        self.stop_loading_message.emit(False)
        self._page_navigation.fungibles_asset_page()

    def on_error(self, error: Exception):
        """This method navigate the page on error"""
        if isinstance(error, CommonException):
            self.stop_loading_message.emit(False)
            if error.message == QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, 'not_initialized', None):
                self._page_navigation.set_wallet_password_page(
                    WalletType.REMOTE_TYPE_WALLET.value,
                )
            elif error.message == QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, 'wrong_password', None):
                self._page_navigation.enter_wallet_password_page()
            elif error.message == QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, 'already_unlocked', None):
                self.lock_wallet()
            elif error.message == QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, 'locked_node', None):
                self._page_navigation.enter_wallet_password_page()
            ToastManager.info(
                description=error.message,
            )
        logger.error(
            'Exception occurred: %s, Message: %s',
            type(error).__name__, str(error),
        )

    def validate_url(self, url: str, validation_label) -> bool:
        """
        Validate the provided URL.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        validation = url.startswith('http://') or url.startswith('https://')
        if validation:
            return True
        validation_label()
        raise ValueError('Invalid URL. Please enter a valid URL.')

    def lock_wallet(self):
        """Lock the wallet."""
        self.loading_message.emit(True)
        self.run_in_thread(
            CommonOperationRepository.lock, {
                'args': [],
                'callback': self.on_success_lock,
                'error_callback': self.on_error_lock,
            },
        )

    def on_success_lock(self, response: UnlockResponseModel):
        """Handle success callback after lock the wallet."""
        if response.status:
            self._page_navigation.enter_wallet_password_page()
        self.stop_loading_message.emit(False)

    def on_error_lock(self, error):
        """Handle error callback after lock the wallet."""
        self.stop_loading_message.emit(False)
        ToastManager.error(
            description=error.message,
        )
