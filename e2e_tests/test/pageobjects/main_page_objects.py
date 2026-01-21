# pylint: disable = too-few-public-methods, too-many-instance-attributes
"""
Main page objects module.
Contains MainPageObjects class for handling main page functionality.
"""
from __future__ import annotations

from e2e_tests.test.pageobjects.about_page import AboutPageObjects
from e2e_tests.test.pageobjects.asset_detail_page import AssetDetailPageObjects
from e2e_tests.test.pageobjects.asset_transaction_detail_page import AssetTransactionDetailPageObjects
from e2e_tests.test.pageobjects.backup_page import BackupPageObjects
from e2e_tests.test.pageobjects.bitcoin_detail_page import BitcoinDetailPageObjects
from e2e_tests.test.pageobjects.bitcoin_transaction_detail_page import BitcoinTransactionDetailPageObjects
from e2e_tests.test.pageobjects.channel_detail_dialog_page import ChannelDetailDialogPageObjects
from e2e_tests.test.pageobjects.channel_management_page import ChannelManagementPageObjects
from e2e_tests.test.pageobjects.close_channel_dialog_page import CloseChannelDialogPageObjects
from e2e_tests.test.pageobjects.collectible_page import CollectiblePageObjects
from e2e_tests.test.pageobjects.create_channel_page import CreateChannelPageObjects
from e2e_tests.test.pageobjects.create_ln_invoice_page import CreateLnInvoicePageObjects
from e2e_tests.test.pageobjects.enter_wallet_password_page import EnterWalletPasswordPageObjects
from e2e_tests.test.pageobjects.fungible_page import FungiblePageObjects
from e2e_tests.test.pageobjects.help_page import HelpPageObjects
from e2e_tests.test.pageobjects.issue_cfa_page import IssueCfaPageObjects
from e2e_tests.test.pageobjects.issue_nia_page import IssueNiaPageObjects
from e2e_tests.test.pageobjects.keyring_dialog_page import KeyringDialogBoxPageObjects
from e2e_tests.test.pageobjects.ln_endpoint_page import LnEndpointPageObjects
from e2e_tests.test.pageobjects.receive_asset_page import ReceiveAssetPageObjects
from e2e_tests.test.pageobjects.restore_mnemonic_page import RestoreWalletPageObjects
from e2e_tests.test.pageobjects.send_asset_page import SendAssetPageObjects
from e2e_tests.test.pageobjects.send_ln_invoice_page import SendLnInvoicePageObjects
from e2e_tests.test.pageobjects.set_password_page import SetPasswordPageObjects
from e2e_tests.test.pageobjects.settings_page_object import SettingsPageObjects
from e2e_tests.test.pageobjects.sidebar_page import SidebarPageObjects
from e2e_tests.test.pageobjects.success_page import SuccessPageObjects
from e2e_tests.test.pageobjects.term_and_condition_page import TermAndConditionPageObjects
from e2e_tests.test.pageobjects.toaster_page import ToasterPageObjects
from e2e_tests.test.pageobjects.view_unspent_list_page import ViewUnspentListPageObjects
from e2e_tests.test.pageobjects.wallet_selection_page import WalletSelectionPageObjects
from e2e_tests.test.pageobjects.wallet_transfer_page import WalletTransferPageObjects
from e2e_tests.test.pageobjects.welcome_page import WelcomePageObjects


class MainPageObjects():
    """
    MainPageObjects class for handling main page functionality.
    """

    def __init__(self, application):
        """
        Initializes MainPageObjects instance.

        Args:
            application: The application instance.
        """
        self.application = application

        self.term_and_condition_page_objects = TermAndConditionPageObjects(
            self.application,
        )

        self.wallet_selection_page_objects = WalletSelectionPageObjects(
            self.application,
        )

        self.welcome_page_objects = WelcomePageObjects(self.application)

        self.set_password_page_objects = SetPasswordPageObjects(
            self.application,
        )

        self.fungible_page_objects = FungiblePageObjects(self.application)

        self.collectible_page_objects = CollectiblePageObjects(
            self.application,
        )

        self.bitcoin_detail_page_objects = BitcoinDetailPageObjects(
            self.application,
        )

        self.wallet_transfer_page_objects = WalletTransferPageObjects(
            self.application,
        )

        self.receive_asset_page_objects = ReceiveAssetPageObjects(
            self.application,
        )

        self.send_asset_page_objects = SendAssetPageObjects(self.application)

        self.issue_nia_page_objects = IssueNiaPageObjects(self.application)

        self.success_page_objects = SuccessPageObjects(self.application)

        self.toaster_page_objects = ToasterPageObjects(self.application)

        self.sidebar_page_objects = SidebarPageObjects(self.application)

        self.issue_cfa_page_objects = IssueCfaPageObjects(self.application)

        self.asset_detail_page_objects = AssetDetailPageObjects(
            self.application,
        )

        self.send_ln_invoice_page_objects = SendLnInvoicePageObjects(
            self.application,
        )

        self.create_ln_invoice_page_objects = CreateLnInvoicePageObjects(
            self.application,
        )

        self.bitcoin_transaction_detail_page_objects = BitcoinTransactionDetailPageObjects(
            self.application,
        )

        self.create_channel_page_objects = CreateChannelPageObjects(
            self.application,
        )

        self.channel_management_page_objects = ChannelManagementPageObjects(
            self.application,
        )

        self.close_channel_detail_dialog_page_objects = CloseChannelDialogPageObjects(
            self.application,
        )

        self.channel_detail_dialog_page_objects = ChannelDetailDialogPageObjects(
            self.application,
        )

        self.about_page_objects = AboutPageObjects(self.application)

        self.settings_page_objects = SettingsPageObjects(self.application)

        self.asset_transaction_detail_page_objects = AssetTransactionDetailPageObjects(
            self.application,
        )

        self.view_unspent_list_page_objects = ViewUnspentListPageObjects(
            self.application,
        )

        self.ln_endpoint_page_objects = LnEndpointPageObjects(self.application)

        self.backup_page_objects = BackupPageObjects(self.application)

        self.keyring_dialog_page_objects = KeyringDialogBoxPageObjects(
            self.application,
        )

        self.restore_wallet_page_objects = RestoreWalletPageObjects(
            self.application,
        )

        self.enter_wallet_password_page_objects = EnterWalletPasswordPageObjects(
            self.application,
        )

        self.help_page_objects = HelpPageObjects(self.application)
