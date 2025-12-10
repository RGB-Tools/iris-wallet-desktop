# pylint: disable=too-many-instance-attributes, too-few-public-methods
"""This module contains the MainViewModel class, which represents the main view model
of the application, containing a collection of all page view models.
"""
from __future__ import annotations

from PySide6.QtCore import QObject

from src.viewmodels.backup_view_model import BackupViewModel
from src.viewmodels.bitcoin_view_model import BitcoinViewModel
from src.viewmodels.cfa_view_model import CFAViewModel
from src.viewmodels.channel_management_viewmodel import ChannelManagementViewModel
from src.viewmodels.enter_password_view_model import EnterWalletPasswordViewModel
from src.viewmodels.faucets_view_model import FaucetsViewModel
from src.viewmodels.fee_rate_view_model import EstimateFeeViewModel
from src.viewmodels.header_frame_view_model import HeaderFrameViewModel
from src.viewmodels.issue_cfa_view_model import IssueCFAViewModel
from src.viewmodels.issue_nia_view_model import IssueNIAViewModel
from src.viewmodels.ln_endpoint_view_model import LnEndpointViewModel
from src.viewmodels.ln_offchain_view_model import LnOffChainViewModel
from src.viewmodels.main_asset_view_model import MainAssetViewModel
from src.viewmodels.receive_bitcoin_view_model import ReceiveBitcoinViewModel
from src.viewmodels.receive_cfa_view_model import ReceiveCFAViewModel
from src.viewmodels.restore_view_model import RestoreViewModel
from src.viewmodels.send_bitcoin_view_model import SendBitcoinViewModel
from src.viewmodels.set_wallet_password_view_model import SetWalletPasswordViewModel
from src.viewmodels.setting_view_model import SettingViewModel
from src.viewmodels.splash_view_model import SplashViewModel
from src.viewmodels.term_view_model import TermsViewModel
from src.viewmodels.view_unspent_view_model import UnspentListViewModel
from src.viewmodels.wallet_and_transfer_selection_viewmodel import WalletTransferSelectionViewModel
from src.viewmodels.welcome_view_model import WelcomeViewModel


class MainViewModel(QObject):
    """This class contains a collection of all page view models."""

    def __init__(self, page_navigation):
        super().__init__()
        self.page_navigation = page_navigation

        self.welcome_view_model = WelcomeViewModel(self.page_navigation)

        self.terms_view_model = TermsViewModel(self.page_navigation)

        self.main_asset_view_model = MainAssetViewModel(self.page_navigation)

        self.issue_nia_asset_view_model = IssueNIAViewModel(
            self.page_navigation,
        )
        self.set_wallet_password_view_model = SetWalletPasswordViewModel(
            self.page_navigation,
        )
        self.bitcoin_view_model = BitcoinViewModel(self.page_navigation)
        self.receive_bitcoin_view_model = ReceiveBitcoinViewModel(
            self.page_navigation,
        )
        self.send_bitcoin_view_model = SendBitcoinViewModel(
            self.page_navigation,
        )

        self.channel_view_model = ChannelManagementViewModel(
            self.page_navigation,
        )

        self.unspent_view_model = UnspentListViewModel(self.page_navigation)

        self.issue_cfa_asset_view_model = IssueCFAViewModel(
            self.page_navigation,
        )
        self.ln_endpoint_view_model = LnEndpointViewModel(
            self.page_navigation,
        )
        self.cfa_view_model = CFAViewModel(
            self.page_navigation,
        )

        self.enter_wallet_password_view_model = EnterWalletPasswordViewModel(
            self.page_navigation,
        )
        self.receive_cfa_view_model = ReceiveCFAViewModel(
            self.page_navigation,
        )

        self.backup_view_model = BackupViewModel(
            self.page_navigation,
        )
        self.setting_view_model = SettingViewModel(
            self.page_navigation,
        )
        self.ln_offchain_view_model = LnOffChainViewModel(
            self.page_navigation,
        )

        self.splash_view_model = SplashViewModel(
            self.page_navigation,
        )

        self.restore_view_model = RestoreViewModel(
            self.page_navigation,
        )
        self.wallet_transfer_selection_view_model = WalletTransferSelectionViewModel(
            self.page_navigation,
            self.splash_view_model,
        )

        self.faucets_view_model = FaucetsViewModel(
            self.page_navigation,
        )

        self.estimate_fee_view_model = EstimateFeeViewModel()

        self.header_frame_view_model = HeaderFrameViewModel()
