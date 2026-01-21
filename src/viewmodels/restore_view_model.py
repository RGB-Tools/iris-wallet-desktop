"""This module contains the RestoreViewModel class, which represents the view model
for the restore page activities.
"""
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication

from src.data.repository.setting_repository import SettingRepository
from src.data.service.restore_service import RestoreService
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import ToastPreset
from src.utils.constant import MNEMONIC_KEY
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_GOOGLE_CONFIGURE_FAILED
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.error_message import ERROR_WHILE_RESTORE
from src.utils.gauth import authenticate
from src.utils.info_message import INFO_RESTORE_COMPLETED
from src.utils.info_message import INFO_WALLET_RESET
from src.utils.keyring_storage import set_value
from src.utils.local_store import local_store
from src.utils.logging import logger
from src.utils.reset_app import delete_app_data
from src.utils.worker import ThreadManager
from src.views.components.keyring_error_dialog import KeyringErrorDialog
from src.views.components.node_incompatibility import NodeIncompatibilityDialog


class RestoreViewModel(QObject, ThreadManager):
    """This class represents the activities of the restore page."""
    is_loading = Signal(bool)
    message = Signal(ToastPreset, str)

    def __init__(self, page_navigation):
        super().__init__()
        self._page_navigation = page_navigation
        self.mnemonic = None
        self.password = None
        self.sidebar = None

    def forward_to_fungibles_page(self):
        """Navigate to fungibles page"""
        self.sidebar = self._page_navigation.sidebar()
        if self.sidebar is not None:
            self.sidebar.my_fungibles.setChecked(True)
        self._page_navigation.enter_wallet_password_page()

    def on_success(self, response):
        """Callback after successful restore"""
        self.is_loading.emit(False)
        network: NetworkEnumModel = SettingRepository.get_wallet_network()

        if response:
            SettingRepository.set_wallet_initialized()
            SettingRepository.set_backup_configured(True)
            is_set_mnemonic: bool = set_value(
                MNEMONIC_KEY, self.mnemonic, network.value,
            )
            is_set_password: bool = set_value(
                WALLET_PASSWORD_KEY, self.password, network.value,
            )

            if is_set_password and is_set_mnemonic:
                self.message.emit(
                    ToastPreset.SUCCESS,
                    INFO_RESTORE_COMPLETED,
                )
                SettingRepository.set_keyring_status(status=False)
                self.forward_to_fungibles_page()
            else:
                keyring_warning_dialog = KeyringErrorDialog(
                    mnemonic=self.mnemonic,
                    password=self.password,
                    navigate_to=self.forward_to_fungibles_page,
                )
                keyring_warning_dialog.exec()
        else:
            self.message.emit(
                ToastPreset.ERROR,
                ERROR_WHILE_RESTORE,
            )

    def on_error(self, exc: Exception):
        """
        Callback after unsuccessful restore.

        Args:
            exc (Exception): The exception that was raised.
        """
        self.is_loading.emit(False)
        if isinstance(exc, CommonException) and getattr(exc, 'message', '') == 'RGB_LIB_INCOMPATIBLE':
            self.handle_rgb_lib_incompatibility()
        elif isinstance(exc, CommonException):
            self.message.emit(
                ToastPreset.ERROR,
                exc.message,
            )
        else:
            self.message.emit(
                ToastPreset.ERROR,
                ERROR_SOMETHING_WENT_WRONG,
            )

    def restore(self, mnemonic: str, password: str):
        """Method called by restore page to restore"""
        self.is_loading.emit(True)
        self.mnemonic = mnemonic
        self.password = password

        try:
            response = authenticate(QApplication.instance())
            if response is False:
                self.is_loading.emit(False)
                self.message.emit(
                    ToastPreset.ERROR,
                    ERROR_GOOGLE_CONFIGURE_FAILED,
                )
                return

            self.run_in_thread(
                RestoreService.restore,
                {
                    'args': [mnemonic, password],
                    'callback': self.on_success,
                    'error_callback': self.on_error,
                },
            )
        except Exception as exc:
            self.is_loading.emit(False)
            self.on_error(exc)

    def handle_rgb_lib_incompatibility(self):
        """Handles the case when the RGB lib version is incompatible."""
        rgb_lib_incompatible_dialog = NodeIncompatibilityDialog()
        rgb_lib_incompatible_dialog.show_node_incompatibility_dialog()
        clicked_button = rgb_lib_incompatible_dialog.node_incompatibility_dialog.clickedButton()

        if clicked_button == rgb_lib_incompatible_dialog.close_button:
            QApplication.instance().exit()

        elif clicked_button == rgb_lib_incompatible_dialog.delete_app_data_button:
            rgb_lib_incompatible_dialog.show_confirmation_dialog()
            confirm_button = rgb_lib_incompatible_dialog.confirmation_dialog.clickedButton()

            if confirm_button == rgb_lib_incompatible_dialog.confirm_delete_button:
                self.on_delete_app_data()
            elif confirm_button == rgb_lib_incompatible_dialog.cancel:
                self.handle_rgb_lib_incompatibility()

    def on_delete_app_data(self):
        """This function deletes the wallet data after user confirms when using an invalid rgb lib"""
        basepath = local_store.get_path()
        network_type = SettingRepository.get_wallet_network()
        delete_app_data(basepath, network=network_type.value)
        logger.info(INFO_WALLET_RESET)
