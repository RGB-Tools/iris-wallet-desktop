"""This module contains the SplashViewModel class, which represents the view model
for splash page.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication

import src.flavour as bitcoin_network
from src.data.repository.common_operations_repository import CommonOperationRepository
from src.data.repository.setting_repository import SettingRepository
from src.model.common_operation_model import NodeInfoResponseModel
from src.model.common_operation_model import UnlockRequestModel
from src.model.enums.enums_model import NativeAuthType
from src.model.enums.enums_model import WalletType
from src.utils.constant import NODE_PUB_KEY
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_CONNECTION_FAILED_WITH_LN
from src.utils.error_message import ERROR_NATIVE_AUTHENTICATION
from src.utils.error_message import ERROR_REQUEST_TIMEOUT
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG_WHILE_UNLOCKING_LN_ON_SPLASH
from src.utils.helpers import get_bitcoin_config
from src.utils.keyring_storage import get_value
from src.utils.local_store import local_store
from src.utils.logging import logger
from src.utils.render_timer import RenderTimer
from src.utils.worker import ThreadManager
from src.viewmodels.wallet_and_transfer_selection_viewmodel import WalletTransferSelectionViewModel
from src.views.components.message_box import MessageBox
from src.views.components.toast import ToastManager


class SplashViewModel(QObject, ThreadManager):
    """This class represents splash page"""

    accept_button_clicked = Signal(str)  # Signal to update in the view
    decline_button_clicked = Signal(str)
    splash_screen_message = Signal(str)
    sync_chain_info_label = Signal(bool)

    def __init__(self, page_navigation):
        super().__init__()
        self._page_navigation = page_navigation
        self.wallet_transfer_selection_view_model: WalletTransferSelectionViewModel = None
        self.render_timer = RenderTimer(task_name='SplashScreenWidget')

    def on_success(self, response):
        """Callback after successful of native login authentication"""
        if response:
            self.handle_application_open()
        else:
            ToastManager.error(
                description=ERROR_NATIVE_AUTHENTICATION,
            )

    def on_error(self, error: Exception):
        """
        Callback after unsuccessful of native login authentication.

        Args:
            exc (Exception): The exception that was raised.
        """
        description = error.message if isinstance(
            error, CommonException,
        ) else ERROR_SOMETHING_WENT_WRONG
        ToastManager.error(description=description)
        QApplication.instance().exit()

    def is_login_authentication_enabled(self, view_model: WalletTransferSelectionViewModel):
        """Check login authentication enabled"""
        try:
            self.wallet_transfer_selection_view_model = view_model
            if SettingRepository.native_login_enabled().is_enabled:
                self.splash_screen_message.emit(
                    'Please authenticate the application..',
                )
            self.run_in_thread(
                SettingRepository.native_authentication,
                {
                    'args': [NativeAuthType.LOGGING_TO_APP],
                    'callback': self.on_success,
                    'error_callback': self.on_error,
                },
            )
        except CommonException as exc:
            ToastManager.error(
                description=exc.message,
            )
        except Exception:
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def on_success_of_unlock_api(self):
        """On success of unlock api it is forward the user to main page"""
        self.render_timer.stop()
        self._page_navigation.fungibles_asset_page()
        node_pub_key: NodeInfoResponseModel = CommonOperationRepository.node_info()
        if node_pub_key is not None:
            local_store.set_value(NODE_PUB_KEY, node_pub_key.pubkey)

    def on_error_of_unlock_api(self, error: Exception):
        """Handle error of unlock API."""
        error_message = error.message if isinstance(
            error, CommonException,
        ) else ERROR_SOMETHING_WENT_WRONG_WHILE_UNLOCKING_LN_ON_SPLASH

        if error_message == QCoreApplication.translate('iris_wallet_desktop', 'already_unlocked', None):
            # Node is already unlocked, treat it as a success
            self.on_success_of_unlock_api()
            return

        if error_message == QCoreApplication.translate('iris_wallet_desktop', 'not_initialized', None):
            self.render_timer.stop()
            self._page_navigation.term_and_condition_page()
            return

        if error_message in [ERROR_CONNECTION_FAILED_WITH_LN, ERROR_REQUEST_TIMEOUT]:
            MessageBox('critical', message_text=ERROR_CONNECTION_FAILED_WITH_LN)
            QApplication.instance().exit()

        # Log the error and display a toast message
        logger.error(
            'Error while unlocking node on splash page: %s, Message: %s',
            type(error).__name__, str(error),
        )
        ToastManager.error(
            description=error_message,
        )
        self._page_navigation.enter_wallet_password_page()

    def handle_application_open(self):
        """This method handle application start"""
        try:
            wallet_type: WalletType = SettingRepository.get_wallet_type()
            if WalletType.EMBEDDED_TYPE_WALLET.value == wallet_type.value:
                self.splash_screen_message.emit(
                    QCoreApplication.translate(
                        'iris_wallet_desktop', 'wait_node_to_start', None,
                    ),
                )
                self.wallet_transfer_selection_view_model.start_node_for_embedded_option()
            else:
                keyring_status = SettingRepository.get_keyring_status()
                if keyring_status is True:
                    self._page_navigation.enter_wallet_password_page()
                else:

                    self.splash_screen_message.emit(
                        QCoreApplication.translate(
                            'iris_wallet_desktop', 'wait_for_node_to_unlock', None,
                        ),
                    )
                    self.sync_chain_info_label.emit(True)
                    wallet_password = get_value(
                        WALLET_PASSWORD_KEY,
                        network=bitcoin_network.__network__,
                    )
                    bitcoin_config: UnlockRequestModel = get_bitcoin_config(
                        network=bitcoin_network.__network__, password=wallet_password,
                    )
                    self.run_in_thread(
                        CommonOperationRepository.unlock, {
                            'args': [bitcoin_config],
                            'callback': self.on_success_of_unlock_api,
                            'error_callback': self.on_error_of_unlock_api,
                        },
                    )
        except CommonException as error:
            logger.error(
                'Exception occurred at handle_application_open: %s, Message: %s',
                type(error).__name__, str(error),
            )
            ToastManager.error(
                description=error.message,
            )
        except Exception as error:
            logger.error(
                'Exception occurred at handle_application_open: %s, Message: %s',
                type(error).__name__, str(error),
            )
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )
