"""This module contains the SetWalletPasswordViewModel class, which represents the view model
for the term and setwalletpassword page activities.
"""
from __future__ import annotations

import os
import random
import re
import string
from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLineEdit

from src.data.repository.setting_repository import SettingRepository
from src.data.service.common_operation_service import CommonOperationService
from src.model.common_operation_model import InitResponseModel
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import ToastPreset
from src.model.enums.enums_model import WalletType
from src.model.set_wallet_password_model import SetWalletPasswordModel
from src.utils.constant import MNEMONIC_KEY
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.error_message import ERROR_NETWORK_MISMATCH
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.gauth import TOKEN_PICKLE_PATH
from src.utils.handle_exception import CommonException
from src.utils.keyring_storage import set_value
from src.utils.local_store import local_store
from src.utils.logging import logger
from src.utils.worker import ThreadManager
from src.views.components.keyring_error_dialog import KeyringErrorDialog
from src.views.components.message_box import MessageBox


class SetWalletPasswordViewModel(QObject, ThreadManager):
    """This class represents the activities of the set wallet password page."""
    is_loading = Signal(bool)
    message = Signal(ToastPreset, str)

    def __init__(self, page_navigation) -> None:
        super().__init__()
        self.common_sidebar = None
        set_wallet_password_model = SetWalletPasswordModel()
        self.password_shown_states = set_wallet_password_model.password_shown_states
        self.password_validation = None
        self._page_navigation = page_navigation
        self.password: str = ''

    def toggle_password_visibility(self, line_edit) -> bool:
        """This method retrieves password visibility."""
        if line_edit not in self.password_shown_states:
            self.password_shown_states[line_edit] = True

        password_shown = self.password_shown_states[line_edit]

        if not password_shown:
            line_edit.setEchoMode(QLineEdit.Password)
            self.password_shown_states[line_edit] = True
        else:
            line_edit.setEchoMode(QLineEdit.Normal)
            self.password_shown_states[line_edit] = False

        return self.password_shown_states[line_edit]

    def set_wallet_password_in_thread(self, enter_password_input: QLineEdit, confirm_password_input: QLineEdit, validation: Any):
        """
        Executes the set_wallet_password method in a separate thread.

        This method starts a thread to execute the set_wallet_password function with the provided arguments.
        It emits a signal to indicate loading state and defines a callback for when the operation is successful.

        Args:
            proceed_wallet_password (Any): The wallet password procedure to be executed.
            enter_password_input (QLineEdit): Input field for entering the password.
            confirm_password_input (QLineEdit): Input field for confirming the password.
            validation (Any): Validation object to validate the password input.
        """
        password = enter_password_input.text()
        confirm_password = confirm_password_input.text()

        # Regular expression to check for special characters
        special_characters = re.compile(
            r'[`!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:"\\|,.<>\/?]',
        )
        if len(password) < 8 or len(confirm_password) < 8:
            validation('Minimum password length is 8 characters.')
            logger.error(
                'Password and confirm password must be at least 8 characters long.',
            )
            return

        if special_characters.search(password) or special_characters.search(confirm_password):
            validation('Password cannot contain special characters.')
            logger.error(
                'Password and confirm password cannot contain special characters.',
            )
            return
        if password == confirm_password:
            self.password = password
            self.is_loading.emit(True)
            self.run_in_thread(
                CommonOperationService.initialize_wallet,
                {
                    'args': [str(password)],
                    'callback': self.on_success,
                    'error_callback': self.on_error,
                },
            )
        else:
            validation('Passwords must be the same!')
            print('Passwords do not match')

    def forward_to_fungibles_page(self):
        """Navigate to fungibles page"""
        self.common_sidebar = self._page_navigation.sidebar()
        if self.common_sidebar is not None:
            self.common_sidebar.my_fungibles.setChecked(True)
        self._page_navigation.fungibles_asset_page()

    def on_success(self, response: InitResponseModel):
        """
        Handles the successful completion of the set wallet password process.

        This method emits a signal to update the loading state to False, indicating
        that the process has completed, and navigates to the main asset page.
        """
        try:
            if response.mnemonic:
                self.is_loading.emit(False)
                SettingRepository.set_wallet_initialized()
                network: NetworkEnumModel = SettingRepository.get_wallet_network()
                wallet_type: WalletType = SettingRepository.get_wallet_type()
                if wallet_type.value == WalletType.EMBEDDED_TYPE_WALLET.value:
                    set_value(MNEMONIC_KEY, response.mnemonic, network.value)
                    if os.path.exists(TOKEN_PICKLE_PATH):
                        SettingRepository.set_backup_configured(True)
                is_mnemonic_stored = set_value(
                    MNEMONIC_KEY, response.mnemonic, network.value,
                )
                is_password_stored = set_value(
                    WALLET_PASSWORD_KEY, self.password, network.value,
                )
                if is_password_stored and is_mnemonic_stored:
                    SettingRepository.set_keyring_status(status=False)
                    self.forward_to_fungibles_page()
                else:
                    keyring_warning_dialog = KeyringErrorDialog(
                        mnemonic=response.mnemonic,
                        password=self.password,
                        navigate_to=self.forward_to_fungibles_page,
                    )
                    keyring_warning_dialog.exec()
        except CommonException as error:
            self.message.emit(
                ToastPreset.ERROR,
                error.message or 'Something went wrong',
            )
        except Exception as error:
            logger.error(
                'Exception occurred: %s, Message: %s',
                type(error).__name__, str(error),
            )
            self.message.emit(
                ToastPreset.ERROR, ERROR_SOMETHING_WENT_WRONG,
            )

    def on_error(self, exc: CommonException):
        """
        Handles error scenarios for the set wallet password operation.

        This method is called when an exception occurs during the set wallet password process.

        Parameters:
        - exc (Exception): The exception that was raised during the wallet password setting process.

        """
        self.is_loading.emit(False)
        if exc.message == ERROR_NETWORK_MISMATCH:
            local_store.clear_settings()
            MessageBox('critical', exc.message)
            QApplication.instance().exit()
        self.message.emit(
            ToastPreset.ERROR,
            exc.message or 'Something went wrong',
        )

    def generate_password(self, length=8):
        """This method generates the wallet strong password."""
        try:
            # Validate length
            if length < 4:
                raise ValueError(
                    'Password length should be at least 4 to include all character types.',
                )

            # Character sets
            upper_case = string.ascii_uppercase
            lower_case = string.ascii_lowercase
            digits = string.digits

            # Ensure at least one character from each set is included
            password = [
                random.choice(upper_case),
                random.choice(lower_case),
                random.choice(digits),
            ]

            # Fill the rest of the password length with random choices from all character sets
            all_characters = upper_case + lower_case + digits
            password += random.choices(all_characters, k=length - 3)

            # Shuffle the list to prevent predictable patterns and convert to a string
            random.shuffle(password)
            return ''.join(password)

        except ValueError as _ve:
            return f'Error: {_ve}'
