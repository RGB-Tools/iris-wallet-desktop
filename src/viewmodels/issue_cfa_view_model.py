"""
This module contains the IssueCFAViewModel class, which represents the view model
for the Issue CFA Asset page activities.
"""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog

from src.data.repository.setting_repository import SettingRepository
from src.data.service.issue_asset_service import IssueAssetService
from src.model.enums.enums_model import NativeAuthType
from src.model.rgb_model import IssueAssetCfaRequestModel
from src.model.rgb_model import IssueAssetResponseModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_AUTHENTICATION
from src.utils.error_message import ERROR_FIELD_MISSING
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.error_message import ERROR_UNEXPECTED
from src.utils.info_message import INFO_ASSET_ISSUED
from src.utils.info_message import INFO_NO_FILE
from src.utils.worker import ThreadManager
from src.views.components.toast import ToastManager


class IssueCFAViewModel(QObject, ThreadManager):
    """This class represents the activities of the Issue CFA Asset page."""
    is_loading = Signal(bool)
    file_upload_message = Signal(str)
    success_page_message = Signal(str)
    cfa_success_message = Signal(str)

    def __init__(self, page_navigation) -> None:
        """
        Initialize the view model with page navigation.

        Args:
            page_navigation: The navigation object to handle page changes.
        """
        super().__init__()
        self._page_navigation = page_navigation
        self.uploaded_file_path: str | None = None
        self.asset_ticker = None
        self.amount = None
        self.asset_name = None

    def on_success_native_auth_cfa(self, success: bool):
        """Callback function after native authentication successful"""
        try:
            if self.amount is None or self.asset_name is None or self.asset_ticker is None:
                raise CommonException(ERROR_FIELD_MISSING)
            if not success:
                raise CommonException(ERROR_AUTHENTICATION)
            amount_num = int(self.amount)
            formatted_amount = [amount_num]
            if self.uploaded_file_path is None:
                ToastManager.error(
                    description=INFO_NO_FILE,
                )
                self.is_loading.emit(False)
                return
            request_model = IssueAssetCfaRequestModel(
                amounts=formatted_amount,
                ticker=self.asset_ticker,
                name=self.asset_name,
                file_path=self.uploaded_file_path,
            )
            self.run_in_thread(
                IssueAssetService.issue_asset_cfa,
                {
                    'args': [request_model],
                    'callback': self.on_success,
                    'error_callback': self.on_error,
                },
            )
        except CommonException as exc:
            self.is_loading.emit(False)
            ToastManager.error(
                description=exc.message,
            )
        except Exception:
            self.is_loading.emit(False)
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def on_error_native_auth_cfa(self, error: Exception):
        """Callback function on error"""
        self.is_loading.emit(False)
        err_message = error.message if isinstance(
            error, CommonException,
        ) else ERROR_SOMETHING_WENT_WRONG
        ToastManager.error(description=err_message)

    def open_file_dialog(self) -> None:
        """
        Open a file dialog to select an image file.
        """
        try:
            file_dialog = QFileDialog()
            home_dir = str(Path.home())
            file_dialog.setDirectory(home_dir)  # Open dialog in this directory
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter('Images (*.png *.jpg *.jpeg)')
            if file_dialog.exec_():
                self.uploaded_file_path = file_dialog.selectedFiles()[0]
                self.file_upload_message.emit(self.uploaded_file_path)
        except CommonException as error:
            error_message = ERROR_UNEXPECTED.format(error.message)
            ToastManager.error(
                description=error_message,
            )

    def on_success(self, response: IssueAssetResponseModel):
        """on success callback of issue cfa """
        ToastManager.success(
            description=INFO_ASSET_ISSUED.format(response.asset_id),
        )
        self.success_page_message.emit(response.name)
        self.is_loading.emit(False)

    def on_error(self, error: CommonException):
        """on error callback of issue cfa """
        ToastManager.error(
            description=error.message,
        )
        self.is_loading.emit(False)

    def issue_cfa_asset(
            self, asset_ticker,
            asset_name,
            amount,
    ):
        """Issue an CFA asset with the provided details."""
        self.is_loading.emit(True)
        self.asset_name = asset_name
        self.asset_ticker = asset_ticker
        self.amount = amount
        self.run_in_thread(
            SettingRepository.native_authentication,
            {
                'args': [NativeAuthType.MAJOR_OPERATION],
                'callback': self.on_success_native_auth_cfa,
                'error_callback': self.on_error_native_auth_cfa,
            },
        )
