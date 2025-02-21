"""This module contains the TermsViewModel class, which represents the view model
for the term and conditions page activities.
"""
from __future__ import annotations

import os

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication

import src.flavour as bitcoin_network
from src.data.repository.common_operations_repository import CommonOperationRepository
from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.model.setting_model import IsWalletInitialized
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.error_message import ERROR_UNABLE_TO_START_NODE
from src.utils.helpers import get_bitcoin_config
from src.utils.helpers import get_node_arg_config
from src.utils.info_message import INFO_LN_NODE_STOPPED
from src.utils.info_message import INFO_LN_SERVER_ALREADY_RUNNING
from src.utils.info_message import INFO_LN_SERVER_STARTED
from src.utils.keyring_storage import get_value
from src.utils.ln_node_manage import LnNodeServerManager
from src.utils.logging import logger
from src.utils.worker import ThreadManager
from src.views.components.message_box import MessageBox
from src.views.components.toast import ToastManager


class WalletTransferSelectionViewModel(QObject, ThreadManager):
    """This class represents the activities of embedded option and other"""
    ln_node_process_status = Signal(bool)
    prev_ln_node_stopping = Signal(bool, str)

    def __init__(self, page_navigation, splash_view_model):
        super().__init__()
        self._page_navigation = page_navigation
        self.splash_view_model = splash_view_model
        self.sidebar = None
        self.ln_node_manager = LnNodeServerManager.get_instance()
        self.ln_node_manager.process_started.connect(self.on_ln_node_start)
        self.ln_node_manager.process_terminated.connect(self.on_ln_node_stop)
        self.ln_node_manager.process_error.connect(self.on_ln_node_error)
        self.ln_node_manager.process_already_running.connect(
            self.on_ln_node_already_running,
        )
        self.is_node_data_exits: bool = False

    def on_ln_node_start(self):
        """Log and show toast on start"""
        try:
            logger.info('Ln node started')
            self.ln_node_process_status.emit(False)
            ToastManager.info(
                description=INFO_LN_SERVER_STARTED,
            )
            wallet: IsWalletInitialized = SettingRepository.is_wallet_initialized()
            password = get_value(
                WALLET_PASSWORD_KEY,
                network=bitcoin_network.__network__,
            )
            keyring_status = SettingRepository.get_keyring_status()
            stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()
            if self.is_node_data_exits and wallet.is_wallet_initialized:
                if keyring_status is True:
                    self._page_navigation.enter_wallet_password_page()
                else:
                    bitcoin_config = get_bitcoin_config(
                        stored_network, password,
                    )
                    self.sidebar = self._page_navigation.sidebar()
                    if self.sidebar is not None:
                        self.sidebar.my_fungibles.setChecked(True)
                        self.splash_view_model.splash_screen_message.emit(
                            QCoreApplication.translate(
                                'iris_wallet_desktop', 'wait_for_node_to_unlock', None,
                            ),
                        )
                        self.splash_view_model.sync_chain_info_label.emit(True)
                        self.run_in_thread(
                            CommonOperationRepository.unlock, {
                                'args': [bitcoin_config],
                                'callback': self.splash_view_model.on_success_of_unlock_api,
                                'error_callback': self.splash_view_model.on_error_of_unlock_api,
                            },
                        )
            else:
                self._page_navigation.welcome_page()
        except CommonException as exc:
            logger.error(
                'Exception occurred at on_ln_node_start: %s, Message: %s',
                type(exc).__name__, str(exc),
            )
            ToastManager.error(
                description=exc.message,
            )
        except Exception as exc:
            logger.error(
                'Exception occurred at on_ln_node_start: %s, Message: %s',
                type(exc).__name__, str(exc),
            )
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def on_error_of_unlock_node(self, error: Exception):
        """Call back function to handle error of unlock api"""
        error_message = error.message if isinstance(
            error, CommonException,
        ) else ERROR_SOMETHING_WENT_WRONG
        ToastManager.error(description=error_message)

    def on_ln_node_stop(self):
        """Log and show toast on ln stop"""
        logger.info('Ln node stop')
        self.ln_node_process_status.emit(False)
        ToastManager.info(
            description=INFO_LN_NODE_STOPPED,
        )

    def on_ln_node_error(self, code: int, error: str):
        """Log and show toast on ln error"""
        self.ln_node_process_status.emit(False)
        logger.error(
            'Exception occurred while stating ln node:Message: %s,Code:%s',
            str(error), str(code),
        )
        MessageBox('critical', message_text=ERROR_UNABLE_TO_START_NODE)
        QApplication.instance().exit()

    def on_ln_node_already_running(self):
        """Log and toast when node already running"""
        self.ln_node_process_status.emit(False)
        logger.info('Ln node already running')
        ToastManager.info(
            description=INFO_LN_SERVER_ALREADY_RUNNING,
        )

    def start_node_for_embedded_option(self):
        """This method is used to start node for embedded option"""
        try:
            self.ln_node_process_status.emit(True)
            stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()
            node_config = get_node_arg_config(stored_network)
            self.is_node_data_exits = os.path.exists(node_config[0])
            self.ln_node_manager.start_server(
                arguments=node_config,
            )
        except CommonException as exc:
            logger.error(
                'Exception occurred: %s, Message: %s',
                type(exc).__name__, str(exc),
            )
            ToastManager.error(
                description=exc.message,
            )
        except Exception as exc:
            logger.error(
                'Exception occurred: %s, Message: %s',
                type(exc).__name__, str(exc),
            )
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )
