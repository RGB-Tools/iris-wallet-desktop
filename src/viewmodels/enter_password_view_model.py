"""This module contains the EnterWalletPasswordViewModel class, which represents the view model
for the set wallet password page.
"""
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLineEdit

from src.data.repository.setting_repository import SettingRepository
from src.data.service.common_operation_service import CommonOperationService
from src.model.common_operation_model import UnlockResponseModel
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import ToastPreset
from src.model.set_wallet_password_model import SetWalletPasswordModel
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.error_message import ERROR_NETWORK_MISMATCH
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.handle_exception import CommonException
from src.utils.keyring_storage import set_value
from src.utils.local_store import local_store
from src.utils.logging import logger
from src.utils.worker import ThreadManager
from src.views.components.message_box import MessageBox


class EnterWalletPasswordViewModel(QObject, ThreadManager):
    """This class represents the activities of the set wallet password page."""
    is_loading = Signal(bool)
    message = Signal(ToastPreset, str)

    def __init__(self, page_navigation) -> None:
        """Initialize the EnterWalletPasswordViewModel with the given page navigation."""
        super().__init__()
        set_wallet_password_model = SetWalletPasswordModel()
        self.password_shown_states = set_wallet_password_model.password_shown_states
        self.password_validation = None
        self._page_navigation = page_navigation
        self.password = ''
        self.sidebar = None

    def toggle_password_visibility(self, line_edit_value) -> bool:
        """Toggle the visibility of the password in the QLineEdit."""
        if line_edit_value not in self.password_shown_states:
            self.password_shown_states[line_edit_value] = True

        password_shown = self.password_shown_states[line_edit_value]

        if not password_shown:
            line_edit_value.setEchoMode(QLineEdit.Password)
            self.password_shown_states[line_edit_value] = True
        else:
            line_edit_value.setEchoMode(QLineEdit.Normal)
            self.password_shown_states[line_edit_value] = False

        return self.password_shown_states[line_edit_value]

    def forward_to_fungibles_page(self):
        """Navigate to fungibles asset page"""
        self.sidebar = self._page_navigation.sidebar()
        if self.sidebar is not None:
            self.sidebar.my_fungibles.setChecked(True)
        self._page_navigation.fungibles_asset_page()

    def on_success(self, response: UnlockResponseModel):
        """Handle success callback after unlocking."""
        try:
            self.is_loading.emit(False)
            if self.password and response.status:
                network: NetworkEnumModel = SettingRepository.get_wallet_network()
                keyring_status: bool = SettingRepository.get_keyring_status()

                if keyring_status is True or keyring_status == 'true':
                    self.forward_to_fungibles_page()
                else:
                    is_set = set_value(
                        WALLET_PASSWORD_KEY, self.password, network.value,
                    )

                    if is_set:
                        SettingRepository.set_keyring_status(False)
                        SettingRepository.set_wallet_initialized()
                        self.message.emit(
                            ToastPreset.SUCCESS,
                            'Wallet password set successfully',
                        )
                        self.forward_to_fungibles_page()
                    else:
                        SettingRepository.set_keyring_status(True)
                        SettingRepository.set_wallet_initialized()
                        self.message.emit(
                            ToastPreset.SUCCESS,
                            'Node unlock successfully with given password',
                        )
                        self.forward_to_fungibles_page()

            else:
                self.message.emit(
                    ToastPreset.ERROR,
                    f'Unable to get password {self.password}',
                )
        except CommonException as error:
            self.message.emit(
                ToastPreset.ERROR,
                error.message or ERROR_SOMETHING_WENT_WRONG,
            )
        except Exception as exc:
            logger.error(
                'Exception occurred: %s, Message: %s',
                type(exc).__name__, str(exc),
            )
            self.message.emit(
                ToastPreset.ERROR,
                ERROR_SOMETHING_WENT_WRONG,
            )

    def on_error(self, error: CommonException):
        """Handle error callback."""
        self.is_loading.emit(False)
        if error.message == ERROR_NETWORK_MISMATCH:
            local_store.clear_settings()
            MessageBox('critical', error.message)
            QApplication.instance().exit()
        self.message.emit(
            ToastPreset.ERROR,
            error.message or ERROR_SOMETHING_WENT_WRONG,
        )

    def set_wallet_password(self, enter_password_input: str):
        """Set the wallet password to the keychain and handle the unlocking process."""
        self.password = enter_password_input
        self.is_loading.emit(True)
        self.run_in_thread(
            CommonOperationService.enter_node_password, {
                'args': [str(self.password)],
                'callback': self.on_success,
                'error_callback': self.on_error,
            },
        )
