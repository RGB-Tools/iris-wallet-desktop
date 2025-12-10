"""
This module contains the ReceiveCFAViewModel class, which represents the view model
for the Receive CFA Asset page activities.
"""
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from src.data.repository.rgb_repository import RgbRepository
from src.model.enums.enums_model import ToastPreset
from src.model.rgb_model import RgbInvoiceDataResponseModel
from src.model.rgb_model import RgbInvoiceRequestModel
from src.utils.custom_exception import CommonException
from src.utils.worker import ThreadManager
from src.views.components.toast import ToastManager


class ReceiveCFAViewModel(QObject, ThreadManager):
    """This class represents the activities of the Receive CFA Asset page."""
    address = Signal(str)
    message = Signal(ToastPreset, str)
    show_loading = Signal(bool)
    hide_loading = Signal(bool)

    def __init__(self, page_navigation) -> None:
        super().__init__()
        self._page_navigation = page_navigation
        self.sidebar = None

    def get_rgb_invoice(self, minimum_confirmations: int, asset_id: str | None = None):
        """
        Retrieve the RGB invoice.

        Args:
            minimum_confirmations (int): Minimum confirmations required.
            asset_id (str | None): Optional asset ID.

        Returns:
            str: The invoice string.
        """
        self.show_loading.emit(True)
        self.run_in_thread(
            RgbRepository.rgb_invoice,
            {
                'args': [RgbInvoiceRequestModel(asset_id=asset_id, min_confirmations=minimum_confirmations)],
                'callback': self.on_success,
                'error_callback': self.on_error,
            },
        )

    def on_success(self, response: RgbInvoiceDataResponseModel):
        """Handles success logic."""
        if response.invoice:
            self.address.emit(response.invoice)
        self.hide_loading.emit(False)

    def on_error(self, error: CommonException):
        """Handles error logic."""
        ToastManager.error(description=error.message)
        self.hide_loading.emit(False)
        self._page_navigation.fungibles_asset_page()
        self.sidebar = self._page_navigation.sidebar()
        if self.sidebar is not None:
            self.sidebar.my_fungibles.setChecked(True)
