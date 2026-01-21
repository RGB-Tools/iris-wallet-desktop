# pylint: disable=too-many-instance-attributes,too-many-public-methods
"""This module contains the PageNavigation class, which represents the navigation
logic for the application's pages.
"""
from __future__ import annotations

from src.model.rgb_model import RgbAssetPageLoadModel
from src.model.selection_page_model import SelectionPageModel
from src.model.success_model import SuccessPageModel
from src.model.transaction_detail_page_model import TransactionDetailPageModel
from src.utils.logging import logger
from src.utils.page_navigation_events import PageNavigationEventManager
from src.views.components.error_report_dialog_box import ErrorReportDialog
from src.views.main_window import MainWindow
from src.views.ui_about import AboutWidget
from src.views.ui_backup import Backup
from src.views.ui_bitcoin import BtcWidget
from src.views.ui_bitcoin_transaction import BitcoinTransactionDetail
from src.views.ui_channel_management import ChannelManagement
from src.views.ui_collectible_asset import CollectiblesAssetWidget
from src.views.ui_create_channel import CreateChannelWidget
from src.views.ui_create_ln_invoice import CreateLnInvoiceWidget
from src.views.ui_enter_wallet_password import EnterWalletPassword
from src.views.ui_faucets import FaucetsWidget
from src.views.ui_fungible_asset import FungibleAssetWidget
from src.views.ui_help import HelpWidget
from src.views.ui_issue_cfa import IssueCFAWidget
from src.views.ui_issue_nia import IssueNIAWidget
from src.views.ui_ln_endpoint import LnEndpointWidget
from src.views.ui_network_selection_page import NetworkSelectionWidget
from src.views.ui_receive_bitcoin import ReceiveBitcoinWidget
from src.views.ui_receive_rgb_asset import ReceiveRGBAssetWidget
from src.views.ui_rgb_asset_detail import RGBAssetDetailWidget
from src.views.ui_rgb_asset_transaction_detail import RGBAssetTransactionDetail
from src.views.ui_send_bitcoin import SendBitcoinWidget
from src.views.ui_send_ln_invoice import SendLnInvoiceWidget
from src.views.ui_send_rgb_asset import SendRGBAssetWidget
from src.views.ui_set_wallet_password import SetWalletPasswordWidget
from src.views.ui_settings import SettingsWidget
from src.views.ui_splash_screen import SplashScreenWidget
from src.views.ui_success import SuccessWidget
from src.views.ui_swap import SwapWidget
from src.views.ui_term_condition import TermConditionWidget
from src.views.ui_view_unspent_list import ViewUnspentList
from src.views.ui_wallet_or_transfer_selection import WalletOrTransferSelectionWidget
from src.views.ui_welcome import WelcomeWidget


class PageNavigation:
    """This class represents app navigation."""

    def __init__(self, _ui):
        self._ui: MainWindow = _ui
        self.current_stack = {}
        self.event_based_navigation = PageNavigationEventManager.get_instance()
        self.pages = {
            'Welcome': WelcomeWidget,
            'LnEndpoint': LnEndpointWidget,
            'WalletOrTransferSelectionWidget': WalletOrTransferSelectionWidget,
            'WalletConnectionTypePage': WalletOrTransferSelectionWidget,
            'TermCondition': TermConditionWidget,
            'FungibleAssetWidget': FungibleAssetWidget,
            'CollectiblesAssetWidget': CollectiblesAssetWidget,
            'SetWalletPassword': SetWalletPasswordWidget,
            'IssueNIA': IssueNIAWidget,
            'Bitcoin': BtcWidget,
            'IssueCFA': IssueCFAWidget,
            'SendCFA': SendRGBAssetWidget,
            'ReceiveCFA': ReceiveRGBAssetWidget,
            'CFADetail': RGBAssetDetailWidget,
            'SendBitcoin': SendBitcoinWidget,
            'ReceiveBitcoin': ReceiveBitcoinWidget,
            'ChannelManagement': ChannelManagement,
            'CreateChannel': CreateChannelWidget,
            'ViewUnspentList': ViewUnspentList,
            'EnterWalletPassword': EnterWalletPassword,
            'CFATransactionDetail': RGBAssetTransactionDetail,
            'BitcoinTransactionDetail': BitcoinTransactionDetail,
            'Backup': Backup,
            'Swap': SwapWidget,
            'SuccessWidget': SuccessWidget,
            'Settings': SettingsWidget,
            'CreateLnInvoiceWidget': CreateLnInvoiceWidget,
            'SendLnInvoiceWidget': SendLnInvoiceWidget,
            'SplashScreenWidget': SplashScreenWidget,
            'AboutWidget': AboutWidget,
            'FaucetsWidget': FaucetsWidget,
            'HelpWidget': HelpWidget,
            'NetworkSelectionWidget': NetworkSelectionWidget,
        }

        self.event_based_navigation.navigate_to_page_signal.connect(
            self.navigate_to_page,
        )
        self.event_based_navigation.toggle_sidebar_signal.connect(
            self.toggle_sidebar,
        )
        self.event_based_navigation.ln_endpoint_page_signal.connect(
            self.ln_endpoint_page,
        )
        self.event_based_navigation.splash_screen_page_signal.connect(
            self.splash_screen_page,
        )
        self.event_based_navigation.wallet_method_page_signal.connect(
            self.wallet_method_page,
        )
        self.event_based_navigation.network_selection_page_signal.connect(
            self.network_selection_page,
        )
        self.event_based_navigation.wallet_connection_page_signal.connect(
            self.wallet_connection_page,
        )
        self.event_based_navigation.welcome_page_signal.connect(
            self.welcome_page,
        )
        self.event_based_navigation.term_and_condition_page_signal.connect(
            self.term_and_condition_page,
        )
        self.event_based_navigation.fungibles_asset_page_signal.connect(
            self.fungibles_asset_page,
        )
        self.event_based_navigation.collectibles_asset_page_signal.connect(
            self.collectibles_asset_page,
        )
        self.event_based_navigation.set_wallet_password_page_signal.connect(
            self.set_wallet_password_page,
        )
        self.event_based_navigation.enter_wallet_password_page_signal.connect(
            self.enter_wallet_password_page,
        )
        self.event_based_navigation.issue_nia_asset_page_signal.connect(
            self.issue_nia_asset_page,
        )
        self.event_based_navigation.bitcoin_page_signal.connect(
            self.bitcoin_page,
        )
        self.event_based_navigation.issue_cfa_asset_page_signal.connect(
            self.issue_cfa_asset_page,
        )
        self.event_based_navigation.send_cfa_page_signal.connect(
            self.send_cfa_page,
        )
        self.event_based_navigation.receive_cfa_page_signal.connect(
            self.receive_cfa_page,
        )
        self.event_based_navigation.cfa_detail_page_signal.connect(
            self.cfa_detail_page,
        )
        self.event_based_navigation.send_bitcoin_page_signal.connect(
            self.send_bitcoin_page,
        )
        self.event_based_navigation.receive_bitcoin_page_signal.connect(
            self.receive_bitcoin_page,
        )
        self.event_based_navigation.channel_management_page_signal.connect(
            self.channel_management_page,
        )
        self.event_based_navigation.create_channel_page_signal.connect(
            self.create_channel_page,
        )
        self.event_based_navigation.view_unspent_list_page_signal.connect(
            self.view_unspent_list_page,
        )
        self.event_based_navigation.cfa_transaction_detail_page_signal.connect(
            self.cfa_transaction_detail_page,
        )
        self.event_based_navigation.bitcoin_transaction_detail_page_signal.connect(
            self.bitcoin_transaction_detail_page,
        )
        self.event_based_navigation.backup_page_signal.connect(
            self.backup_page,
        )
        self.event_based_navigation.swap_page_signal.connect(self.swap_page)
        self.event_based_navigation.settings_page_signal.connect(
            self.settings_page,
        )
        self.event_based_navigation.create_ln_invoice_page_signal.connect(
            self.create_ln_invoice_page,
        )
        self.event_based_navigation.send_ln_invoice_page_signal.connect(
            self.send_ln_invoice_page,
        )
        self.event_based_navigation.show_success_page_signal.connect(
            self.show_success_page,
        )
        self.event_based_navigation.about_page_signal.connect(self.about_page)
        self.event_based_navigation.faucets_page_signal.connect(
            self.faucets_page,
        )
        self.event_based_navigation.help_page_signal.connect(self.help_page)
        self.event_based_navigation.error_report_signal.connect(
            self.error_report_dialog_box,
        )

    def toggle_sidebar(self, show):
        """This method represents toggle the sidebar."""
        if show:
            self._ui.sidebar.show()
        else:
            self._ui.sidebar.hide()

    def show_current_page(self):
        """This method toggles the display of the current page."""
        if self.current_stack:
            page_name = self.current_stack['name']
            if page_name not in self._ui.stacked_widget.children():
                self._ui.stacked_widget.addWidget(self.current_stack['widget'])
            self._ui.stacked_widget.setCurrentWidget(
                self.current_stack['widget'],
            )
        else:
            logger.info('No current stack set.')

    def navigate_and_toggle(self, show_sidebar):
        """This method toggles the display of the current page and sidebar."""
        self.show_current_page()
        self.toggle_sidebar(show_sidebar)

    def navigate_to_page(self, page_name, show_sidebar=False):
        """This method displays the specified page."""
        if page_name in self.pages:
            self.current_stack = {
                'name': page_name,
                'widget': self.pages[page_name](self._ui.view_model),
            }
            self.navigate_and_toggle(show_sidebar)
        else:
            logger.error('Page %s not found.', page_name)

    def ln_endpoint_page(self, originating_page):
        """This method display enter lightning node endpoint page."""
        self.current_stack = {
            'name': 'LnEndpoint',
            'widget': self.pages['LnEndpoint'](self._ui.view_model, originating_page),
        }
        self.navigate_and_toggle(False)

    def splash_screen_page(self):
        """This method display splash screen page."""
        self.navigate_to_page('SplashScreenWidget')

    def wallet_method_page(self, params: SelectionPageModel):
        """This method display the wallet method page."""
        self.current_stack = {
            'name': 'WalletOrTransferSelectionWidget',
            'widget': self.pages['WalletOrTransferSelectionWidget'](self._ui.view_model, params),
        }
        self.navigate_and_toggle(False)

    def network_selection_page(self, originating_page, network):
        """This method display the wallet network selection page."""
        self.current_stack = {
            'name': 'NetworkSelectionWidget',
            'widget': self.pages['NetworkSelectionWidget'](self._ui.view_model, originating_page, network),
        }
        self.navigate_and_toggle(False)

    def wallet_connection_page(self, params: SelectionPageModel):
        """This method display the wallet connection page."""
        self.current_stack = {
            'name': 'WalletConnectionTypePage',
            'widget': self.pages['WalletConnectionTypePage'](self._ui.view_model, params),
        }
        self.navigate_and_toggle(False)

    def welcome_page(self):
        """This method display the welcome page."""
        self.navigate_to_page('Welcome')

    def term_and_condition_page(self):
        """This method display the term and condition page."""
        self.navigate_to_page('TermCondition')

    def fungibles_asset_page(self):
        """This method display the fungibles asset page."""
        self.navigate_to_page('FungibleAssetWidget', show_sidebar=True)

    def collectibles_asset_page(self):
        """This method display the collectibles asset page."""
        self.navigate_to_page('CollectiblesAssetWidget', show_sidebar=True)

    def set_wallet_password_page(self, params):
        """This method display the set wallet password page."""
        self.current_stack = {
            'name': 'SetWalletPassword',
            'widget': self.pages['SetWalletPassword'](self._ui.view_model, params),
        }
        self.navigate_and_toggle(False)

    def enter_wallet_password_page(self):
        """This method display the set wallet password page."""
        self.navigate_to_page('EnterWalletPassword')

    def issue_nia_asset_page(self):
        """This method display the issue nia asset page."""
        self.navigate_to_page('IssueNIA')

    def bitcoin_page(self):
        """This method display the bitcoin page."""
        self.navigate_to_page('Bitcoin')

    def issue_cfa_asset_page(self):
        """This method display the issue cfa page."""
        self.navigate_to_page('IssueCFA')

    def send_cfa_page(self):
        """This method display the send cfa page."""
        self.navigate_to_page('SendCFA')

    def receive_cfa_page(self, params):
        """This method display the receive cfa asset page."""
        self.current_stack = {
            'name': 'ReceiveCFA',
            'widget': self.pages['ReceiveCFA'](self._ui.view_model, params),
        }
        self.navigate_and_toggle(False)

    def cfa_detail_page(self, params: RgbAssetPageLoadModel):
        """This method display the cfa detail page."""
        self.current_stack = {
            'name': 'CFADetail',
            'widget': self.pages['CFADetail'](self._ui.view_model, params),
        }
        self.navigate_and_toggle(False)

    def send_bitcoin_page(self):
        """This method display the send bitcoin page."""
        self.navigate_to_page('SendBitcoin')

    def receive_bitcoin_page(self):
        """This method display the receive bitcoin page."""
        self.navigate_to_page('ReceiveBitcoin')

    def channel_management_page(self):
        """This method display the channel management page."""
        self.navigate_to_page('ChannelManagement', show_sidebar=True)

    def create_channel_page(self):
        """This method display the create channel page."""
        self.navigate_to_page('CreateChannel')

    def view_unspent_list_page(self):
        """This method display the view unspent list page."""
        self.navigate_to_page('ViewUnspentList', show_sidebar=True)

    def cfa_transaction_detail_page(self, params: TransactionDetailPageModel):
        """This method display the cfa transaction detail page."""
        self.current_stack = {
            'name': 'CFATransactionDetail',
            'widget': self.pages['CFATransactionDetail'](self._ui.view_model, params),
        }
        self.navigate_and_toggle(False)

    def bitcoin_transaction_detail_page(self, params: TransactionDetailPageModel):
        """This method display the bitcoin transaction detail page."""
        self.current_stack = {
            'name': 'BitcoinTransactionDetail',
            'widget': self.pages['BitcoinTransactionDetail'](self._ui.view_model, params),
        }
        self.navigate_and_toggle(False)

    def backup_page(self):
        """This method display the backup page."""
        self.navigate_to_page('Backup', show_sidebar=False)

    def swap_page(self):
        """This method display the swap page."""
        self.navigate_to_page('Swap', show_sidebar=False)

    def settings_page(self):
        """This method display the settings page"""
        self.navigate_to_page('Settings', show_sidebar=True)

    def create_ln_invoice_page(self, params, asset_name, asset_type=None):
        """This method display the create ln invoice page"""
        self.current_stack = {
            'name': 'CreateLnInvoiceWidget',
            'widget': self.pages['CreateLnInvoiceWidget'](self._ui.view_model, params, asset_name, asset_type),
        }
        self.navigate_and_toggle(False)

    def send_ln_invoice_page(self, asset_type=None):
        """This method display the send ln invoice page"""
        self.current_stack = {
            'name': 'SendLnInvoiceWidget',
            'widget': self.pages['SendLnInvoiceWidget'](self._ui.view_model, asset_type),
        }
        self.navigate_and_toggle(False)

    def show_success_page(self, params: SuccessPageModel):
        """This method display the success page."""
        self.current_stack = {
            'name': 'SuccessWidget',
            'widget': self.pages['SuccessWidget'](params),
        }
        self.navigate_and_toggle(False)

    def about_page(self):
        """This method display the about page."""
        self.navigate_to_page('AboutWidget', show_sidebar=True)

    def faucets_page(self):
        """This method display the faucets page."""
        self.navigate_to_page('FaucetsWidget', show_sidebar=True)

    def help_page(self):
        """This method display the help page."""
        self.navigate_to_page('HelpWidget', show_sidebar=True)

    def sidebar(self):
        """This method return the sidebar objects."""
        return self._ui.sidebar

    def error_report_dialog_box(self):
        """This method display the error report dialog box"""
        error_report_dialog = ErrorReportDialog()
        error_report_dialog.exec()
