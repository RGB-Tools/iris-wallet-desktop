"""This module contains the IssueNIAViewModel class, which represents the view model
for the issue RG20 page activities.
"""
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from src.data.repository.rgb_repository import RgbRepository
from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NativeAuthType
from src.model.rgb_model import IssueAssetNiaRequestModel
from src.model.rgb_model import IssueAssetResponseModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.worker import ThreadManager
from src.views.components.toast import ToastManager


class IssueNIAViewModel(QObject, ThreadManager):
    """This class represents the activities of the issue NIA page."""

    issue_button_clicked = Signal(bool)
    close_button_clicked = Signal(bool)
    is_issued = Signal(str)
    token_amount = None
    asset_name = None
    short_identifier = None

    def __init__(self, page_navigation: Any) -> None:
        super().__init__()
        self._page_navigation = page_navigation

    def on_success_native_auth_nia(self, success: bool):
        """Callback function after native authentication successful"""
        try:
            if not success:
                raise CommonException('Authentication failed')
            if self.token_amount is None or self.asset_name is None or self.short_identifier is None:
                raise CommonException('Few fields missing')
            asset = IssueAssetNiaRequestModel(
                amounts=[int(self.token_amount)],
                name=self.asset_name,
                ticker=self.short_identifier,
            )
            self.run_in_thread(
                RgbRepository.issue_asset_nia,

                {
                    'args': [asset],
                    'callback': self.on_success,
                    'error_callback': self.on_error,
                },
            )
        except CommonException as error:
            ToastManager.error(
                description=error.message,
            )
        except Exception:
            self.issue_button_clicked.emit(False)
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def on_error_native_auth_nia(self, error: Exception):
        """Callback function on error"""
        self.issue_button_clicked.emit(False)
        description = error.message if isinstance(
            error, CommonException,
        ) else ERROR_SOMETHING_WENT_WRONG
        ToastManager.error(description=description)

    def on_issue_click(self, short_identifier: str, asset_name: str, amount: str):
        """"
        Executes the set_wallet_password method in a separate thread.
        This method starts a thread to execute the issue_nia function with the provided arguments.
        It emits a signal to indicate loading state and defines a callback for when the operation is successful.
        """
        self.issue_button_clicked.emit(True)
        self.token_amount = amount
        self.short_identifier = short_identifier
        self.asset_name = asset_name
        self.run_in_thread(
            SettingRepository.native_authentication,
            {
                'args': [NativeAuthType.MAJOR_OPERATION],
                'callback': self.on_success_native_auth_nia,
                'error_callback': self.on_error_native_auth_nia,
            },
        )

    def on_success(self, response: IssueAssetResponseModel) -> None:
        """This method is used  handle onsuccess for the NIA issue page."""
        self.issue_button_clicked.emit(False)
        self.is_issued.emit(response.name)

    def on_error(self, error) -> None:
        """This method is used  handle onerror for the NIA issue page."""
        self.issue_button_clicked.emit(False)
        ToastManager.error(
            description=error.message,
        )

    def on_close_click(self) -> None:
        """This method is used for close the NIA issue page."""
        self._page_navigation.fungibles_asset_page()
