# pylint:disable=too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""This module help to emit toast message from outside ui based on condition"""
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from src.model.enums.enums_model import ToastPreset
from src.views.components.toast import ToastManager


class GlobalToast(QObject):
    """Class help to manage event and handler of toaster visibility from anywhere"""
    _instance = None
    cache_error_event = Signal(str)

    def __init__(self):
        super().__init__()
        self.cache_error_event.connect(
            self.handle_cache_error_notification_toast,
        )

    def handle_cache_error_notification_toast(self, message: str):
        """Handle cache class error message to show user throw toaster"""
        ToastManager.show_toast(
            parent=None, preset=ToastPreset.WARNING, title=None, description=message,
        )


global_toaster = GlobalToast()
