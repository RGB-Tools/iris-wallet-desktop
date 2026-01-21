# pylint: disable = too-few-public-methods
"""Make page navigation global"""
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal


class PageNavigationEventManager(QObject):
    """Class that contains all page navigation-related signals to enable global navigation not only from ui."""

    # Define signals for various page navigation events
    _instance = None
    navigate_to_page_signal = Signal(str, bool)
    toggle_sidebar_signal = Signal(bool)
    ln_endpoint_page_signal = Signal(str)
    splash_screen_page_signal = Signal()
    wallet_method_page_signal = Signal(object)
    network_selection_page_signal = Signal(str, str)
    wallet_connection_page_signal = Signal(object)
    welcome_page_signal = Signal()
    term_and_condition_page_signal = Signal()
    fungibles_asset_page_signal = Signal()
    collectibles_asset_page_signal = Signal()
    set_wallet_password_page_signal = Signal(object)
    enter_wallet_password_page_signal = Signal()
    issue_nia_asset_page_signal = Signal()
    bitcoin_page_signal = Signal()
    issue_cfa_asset_page_signal = Signal()
    send_cfa_page_signal = Signal()
    receive_cfa_page_signal = Signal(object)
    cfa_detail_page_signal = Signal(str)
    send_bitcoin_page_signal = Signal()
    receive_bitcoin_page_signal = Signal()
    channel_management_page_signal = Signal()
    create_channel_page_signal = Signal()
    view_unspent_list_page_signal = Signal()
    cfa_transaction_detail_page_signal = Signal(object)
    bitcoin_transaction_detail_page_signal = Signal(object)
    backup_page_signal = Signal()
    swap_page_signal = Signal()
    settings_page_signal = Signal()
    create_ln_invoice_page_signal = Signal(object)
    send_ln_invoice_page_signal = Signal()
    show_success_page_signal = Signal(object)
    about_page_signal = Signal()
    faucets_page_signal = Signal()
    help_page_signal = Signal()
    error_report_signal = Signal()

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of LnNodeServerManager.

        Returns:
            PageNavigationEventManager: The singleton instance of the manager.
        """
        if PageNavigationEventManager._instance is None:
            PageNavigationEventManager._instance = PageNavigationEventManager()
        return PageNavigationEventManager._instance
