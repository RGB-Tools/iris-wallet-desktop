# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the SendBitcoinWidget class,
 which represents the UI for send bitcoin.
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from rgb_lib import Address
from rgb_lib import BitcoinNetwork
from rgb_lib import RgbLibError

import src.resources_rc
from src.data.repository.setting_card_repository import SettingCardRepository
from src.data.repository.setting_repository import SettingRepository
from src.model.setting_model import DefaultFeeRate
from src.utils.constant import FEE_RATE
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.send_asset import SendAssetWidget


class SendBitcoinWidget(QWidget):
    """This class represents all the UI elements of the send bitcoin page."""

    def __init__(self, view_model):
        super().__init__()
        self.render_timer = RenderTimer(task_name='BitcoinSendAsset Rendering')
        self._view_model: MainViewModel = view_model
        self.loading_performer = None
        self.send_bitcoin_fee_rate_loading_screen = None
        self.send_bitcoin_page = SendAssetWidget(self._view_model, 'address')
        self.value_of_default_fee_rate: DefaultFeeRate = SettingCardRepository.get_default_fee_rate()
        self.send_bitcoin_page.fee_rate_value.setText(
            str(self.value_of_default_fee_rate.fee_rate),
        )
        self.send_bitcoin_page.fee_rate_value.setAccessibleDescription(
            self.send_bitcoin_page.fee_rate_value.text(),
        )
        layout = QVBoxLayout()
        layout.addWidget(self.send_bitcoin_page)
        self.setLayout(layout)
        self.set_bitcoin_balance()
        self.setup_ui_connection()
        self._loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading',
        )

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.send_bitcoin_page.send_btn.setDisabled(True)
        self.send_bitcoin_page.asset_address_value.textChanged.connect(
            self.validate_bitcoin_address,
        )
        self.send_bitcoin_page.asset_address_value.textChanged.connect(
            self.handle_button_enabled,
        )
        self.send_bitcoin_page.asset_amount_value.textChanged.connect(
            self.handle_button_enabled,
        )
        self.send_bitcoin_page.send_btn.clicked.connect(
            self.send_bitcoin_button,
        )
        self.send_bitcoin_page.close_button.clicked.connect(
            self.bitcoin_page_navigation,
        )
        self._view_model.send_bitcoin_view_model.send_button_clicked.connect(
            self.update_loading_state,
        )

        self._view_model.bitcoin_view_model.loading_started.connect(
            self.update_loading_state,
        )
        self._view_model.bitcoin_view_model.loading_finished.connect(
            self.update_loading_state,
        )
        self.send_bitcoin_page.refresh_button.clicked.connect(
            self.refresh_bitcoin_balance,
        )
        self._view_model.bitcoin_view_model.transaction_loaded.connect(
            self.set_bitcoin_balance,
        )
        self._view_model.estimate_fee_view_model.loading_status.connect(
            self.update_loading_state,
        )
        self.send_bitcoin_page.fee_rate_value.textChanged.connect(
            self.handle_button_enabled,
        )

    def set_bitcoin_balance(self):
        """Set the bitcoin balance in the UI."""
        self.send_bitcoin_page.asset_balance_label_spendable.setText(
            self._view_model.bitcoin_view_model.spendable_bitcoin_balance_with_suffix,
        )
        self.send_bitcoin_page.asset_balance_label_total.setText(
            self._view_model.bitcoin_view_model.total_bitcoin_balance_with_suffix,
        )

    def bitcoin_page_navigation(self):
        """Navigate to the bitcoin page."""
        self._view_model.page_navigation.bitcoin_page()

    def send_bitcoin_button(self):
        """Handle the send bitcoin button click event
        and send the bitcoin on the particular address"""
        address = self.send_bitcoin_page.asset_address_value.text()
        amount = self.send_bitcoin_page.asset_amount_value.text()
        fee = self.send_bitcoin_page.fee_rate_value.text() or FEE_RATE
        self._view_model.send_bitcoin_view_model.on_send_click(
            address, amount, fee,
        )

    def update_loading_state(self, is_loading: bool, is_fee_rate_loading: bool = False):
        """Updates the loading state of the send button."""
        if is_fee_rate_loading:
            if is_loading:
                self.send_bitcoin_fee_rate_loading_screen = LoadingTranslucentScreen(
                    parent=self, description_text='Getting Fee Rate',
                )
                self.send_bitcoin_fee_rate_loading_screen.start()
                self.send_bitcoin_fee_rate_loading_screen.make_parent_disabled_during_loading(
                    True,
                )

            if is_loading is False:
                self.send_bitcoin_fee_rate_loading_screen.stop()
                self.send_bitcoin_fee_rate_loading_screen.make_parent_disabled_during_loading(
                    False,
                )

        else:
            if is_loading:
                if self.loading_performer == 'REFRESH_BUTTON':
                    self._loading_translucent_screen.start()
                    self._loading_translucent_screen.make_parent_disabled_during_loading(
                        True,
                    )
                else:
                    self.render_timer.start()
                    self.send_bitcoin_page.send_btn.start_loading()
                    self._loading_translucent_screen.make_parent_disabled_during_loading(
                        True,
                    )
            else:
                if self.loading_performer == 'REFRESH_BUTTON':
                    self._loading_translucent_screen.stop()
                    self._loading_translucent_screen.make_parent_disabled_during_loading(
                        False,
                    )
                    self.loading_performer = None
                else:
                    self.render_timer.stop()
                    self.send_bitcoin_page.send_btn.stop_loading()
                    self._loading_translucent_screen.make_parent_disabled_during_loading(
                        False,
                    )

    def handle_button_enabled(self):
        """Updates the enabled state of the send button."""

        def is_valid_value(value):
            """
                Checks if the given value is neither empty nor equal to '0'.

                Args:
                    value (str): The value to be checked.

                Returns:
                    bool: True if the value is not empty and not equal to '0', False otherwise.
            """
            return bool(value) and value != '0'

        is_address_valid = bool(
            self.send_bitcoin_page.asset_address_value.text(
            ),
        ) and not self.send_bitcoin_page.asset_address_validation_label.isVisible()
        is_amount_valid = is_valid_value(
            self.send_bitcoin_page.asset_amount_value.text(),
        )
        is_fee_valid = is_valid_value(
            self.send_bitcoin_page.fee_rate_value.text(),
        )

        pay_amount = self.send_bitcoin_page.pay_amount or 0
        spendable_amount = self.send_bitcoin_page.spendable_amount or 0
        is_payment_valid = pay_amount <= spendable_amount

        if is_address_valid and is_amount_valid and is_fee_valid and is_payment_valid:
            self.send_bitcoin_page.send_btn.setDisabled(False)
        else:
            self.send_bitcoin_page.send_btn.setDisabled(True)

    def refresh_bitcoin_balance(self):
        """This method handles the feature for refreshing the Bitcoin balance."""
        self.loading_performer = 'REFRESH_BUTTON'
        self._view_model.bitcoin_view_model.get_transaction_list()

    def validate_bitcoin_address(self):
        """
        Validates the Bitcoin address input.

        - Retrieves the wallet network from settings.
        - Checks if the entered address is valid for the given network.
        - Displays an error message if the address is invalid.
        """
        address = self.send_bitcoin_page.asset_address_value.text().strip()

        if not address:
            self.send_bitcoin_page.asset_address_validation_label.hide()
            return

        try:
            network_enum = SettingRepository.get_wallet_network()
            network_value = BitcoinNetwork[network_enum.value.upper()]

            # Validate the Bitcoin address
            Address(address, network_value)

            # Hide validation label if the address is valid
            self.send_bitcoin_page.asset_address_validation_label.hide()

        except RgbLibError.InvalidAddress:
            # Show error message if the address is invalid
            self.send_bitcoin_page.asset_address_validation_label.show()
            self.send_bitcoin_page.asset_address_validation_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'invalid_address',
                ),
            )
