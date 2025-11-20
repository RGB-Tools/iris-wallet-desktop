# pylint:disable=too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""This module contains the welcomeViewModel class, which represents the view model
for the term and conditions page activities.
"""
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from src.model.enums.enums_model import WalletType


class WelcomeViewModel(QObject):
    """This class represents the activities of the welcome page."""

    create_button_clicked = Signal(bool)  # Signal to update in the view
    restore_button_clicked = Signal(str)

    def __init__(self, page_navigation):
        super().__init__()
        self._page_navigation = page_navigation

    def on_create_click(self):
        """This method handles the wallet creation process."""
        self._page_navigation.set_wallet_password_page(
            WalletType.EMBEDDED_TYPE_WALLET.value,
        )
