# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the SendRGBAssetWidget class,
 which represents the UI for send rgb assets
 """
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from rgb_lib import Invoice
from rgb_lib import RgbLibError

import src.resources_rc
from src.data.repository.rgb_repository import RgbRepository
from src.data.repository.setting_card_repository import SettingCardRepository
from src.model.enums.enums_model import ToastPreset
from src.model.rgb_model import DecodeRgbInvoiceRequestModel
from src.model.rgb_model import DecodeRgbInvoiceResponseModel
from src.model.rgb_model import ListTransferAssetWithBalanceResponseModel
from src.model.setting_model import DefaultFeeRate
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_SEND_ASSET
from src.utils.error_message import ERROR_UNEXPECTED
from src.utils.render_timer import RenderTimer
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.components.send_asset import SendAssetWidget
from src.views.components.toast import ToastManager


class SendRGBAssetWidget(QWidget):
    """This class represents all the UI elements of the send RGB assets page."""

    def __init__(self, view_model):
        self.render_timer = RenderTimer(task_name='RGBSendAsset Rendering')
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.asset_spendable_balance = None
        self.image_path = None
        self.asset_id = None
        self.asset_type = None
        self.asset_name = None
        self.loading_performer = None
        self.rgb_asset_fee_rate_loading_screen = None
        self.value_of_default_fee_rate: DefaultFeeRate = SettingCardRepository.get_default_fee_rate()
        self.send_rgb_asset_page = SendAssetWidget(
            self._view_model, 'blind_utxo',
        )
        self.send_rgb_asset_page.fee_rate_value.setText(
            str(self.value_of_default_fee_rate.fee_rate),
        )

        layout = QVBoxLayout()
        layout.addWidget(self.send_rgb_asset_page)
        self.setLayout(layout)
        self.set_originating_page(self._view_model.cfa_view_model.asset_type)
        self.setup_ui_connection()
        self.handle_button_enabled()
        self.set_asset_balance()
        self.handle_spendable_balance_validation()
        self.sidebar = None
        self.__loading_translucent_screen = LoadingTranslucentScreen(
            parent=self, description_text='Loading',
        )

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.send_rgb_asset_page.send_btn.clicked.connect(
            self.send_rgb_asset_button,
        )
        self.send_rgb_asset_page.close_button.clicked.connect(
            self.rgb_asset_page_navigation,
        )
        self._view_model.cfa_view_model.message.connect(
            self.show_cfa_message,
        )
        self.send_rgb_asset_page.asset_address_value.textChanged.connect(
            self.validate_rgb_invoice,
        )
        self.send_rgb_asset_page.asset_amount_value.textChanged.connect(
            self.handle_button_enabled,
        )
        self.send_rgb_asset_page.asset_address_value.textChanged.connect(
            self.handle_button_enabled,
        )
        self._view_model.cfa_view_model.is_loading.connect(
            self.update_loading_state,
        )
        self.send_rgb_asset_page.refresh_button.clicked.connect(
            self.refresh_asset,
        )
        self._view_model.cfa_view_model.txn_list_loaded.connect(
            self.set_asset_balance,
        )
        self._view_model.cfa_view_model.txn_list_loaded.connect(
            self.handle_spendable_balance_validation,
        )
        self._view_model.estimate_fee_view_model.loading_status.connect(
            self.fee_estimation_loader,
        )
        self.send_rgb_asset_page.fee_rate_value.textChanged.connect(
            self.handle_button_enabled,
        )

    def refresh_asset(self):
        """This method handle the refresh asset on send asset page"""
        self.loading_performer = 'REFRESH_BUTTON'
        view_model = self._view_model.cfa_view_model
        view_model.on_refresh_click()
        self.asset_id = view_model.asset_id
        self.asset_name = view_model.asset_name
        self.image_path = view_model.image_path
        self.asset_type = view_model.asset_type
        self._view_model.cfa_view_model.get_cfa_asset_detail(
            asset_id=self.asset_id, asset_name=self.asset_name, image_path=self.image_path, asset_type=self.asset_type,
        )

    def set_originating_page(self, asset_type):
        """This method sets the originating page for when closing send asset"""
        if asset_type == 'NIA':
            self.asset_type = 'NIA'

    def rgb_asset_page_navigation(self):
        """Navigate to the collectibles asset page."""
        self.sidebar = self._view_model.page_navigation.sidebar()
        if self.asset_type == 'NIA':
            self.sidebar.my_fungibles.setChecked(True)
            self._view_model.page_navigation.fungibles_asset_page()
        else:
            self.sidebar.my_collectibles.setChecked(True)
            self._view_model.page_navigation.collectibles_asset_page()

    def send_rgb_asset_button(self):
        """Handle the send RGB asset button click event
        and send the RGB asset to the particular address"""
        try:
            self.loading_performer = 'SEND_BUTTON'
            provided_invoice = self.send_rgb_asset_page.asset_address_value.text()
            amount = self.send_rgb_asset_page.asset_amount_value.text()
            fee_rate = self.send_rgb_asset_page.fee_rate_value.text()
            default_min_confirmation = SettingCardRepository.get_default_min_confirmation()

            # Attempt to decode the RGB invoice
            decoded_rgb_invoice: DecodeRgbInvoiceResponseModel = RgbRepository.decode_invoice(
                DecodeRgbInvoiceRequestModel(invoice=provided_invoice),
            )
            try:
                self._view_model.cfa_view_model.on_send_click(
                    amount, decoded_rgb_invoice.recipient_id, decoded_rgb_invoice.transport_endpoints, fee_rate, default_min_confirmation.min_confirmation,
                )
                # Success toast or indicator can be added here if needed
            except CommonException as e:
                # Handle any errors during the sending process
                ToastManager.error(
                    description=ERROR_SEND_ASSET.format(str(e)),
                )
        except CommonException as e:
            # Handle any unexpected errors during the button click processing
            ToastManager.error(
                description=ERROR_UNEXPECTED.format(str(e.message)),
            )

    def show_cfa_message(self, msg_type: ToastPreset, message: str):
        """Handle show message"""
        if msg_type == ToastPreset.ERROR:
            ToastManager.error(message)
        else:
            ToastManager.success(message)

    def handle_button_enabled(self):
        """Updates the enabled state of the send button."""

        def is_valid_value(value):
            """Checks if the given value is neither empty nor equal to '0'."""
            return bool(value) and value != '0'

        def is_spendable_amount_valid():
            """Checks if the spendable balance is greater than 0 and enough for the transaction."""
            return self.asset_spendable_balance > 0 and self.asset_spendable_balance >= self.send_rgb_asset_page.pay_amount

        def are_fields_valid():
            """Checks if required fields are filled and valid."""
            return (
                is_valid_value(self.send_rgb_asset_page.asset_address_value.text()) and
                # Check if the validation label is hidden
                not self.send_rgb_asset_page.asset_address_validation_label.isVisible() and
                is_valid_value(self.send_rgb_asset_page.asset_amount_value.text()) and
                is_valid_value(self.send_rgb_asset_page.fee_rate_value.text())
            )

        # Now use the helper functions for the condition
        if are_fields_valid() and is_spendable_amount_valid():
            self.send_rgb_asset_page.send_btn.setDisabled(False)
        else:
            self.send_rgb_asset_page.send_btn.setDisabled(True)

    def update_loading_state(self, is_loading: bool):
        """
        Updates the loading state of the proceed_wallet_password object.

        This method handles the loading state by starting or stopping
        the loading animation of the proceed_wallet_password object based
        on the value of is_loading.
        """
        def handle_refresh_button_loading(start: bool):
            """This method starts the loader when refresh button is clicked"""
            self.__loading_translucent_screen.make_parent_disabled_during_loading(
                start,
            )
            if start:
                self.__loading_translucent_screen.start()
            else:
                self.__loading_translucent_screen.stop()

        def handle_send_button_loading(start: bool):
            """This method starts the loader in the send button when it is clicked"""
            if start:
                self.render_timer.start()
                self.send_rgb_asset_page.send_btn.start_loading()
            else:
                self.render_timer.stop()
                self.send_rgb_asset_page.send_btn.stop_loading()

        def handle_fee_estimation_loading(start: bool):
            """This method starts the loader when fee estimation checkbox is clicked"""
            if start:
                self.rgb_asset_fee_rate_loading_screen = LoadingTranslucentScreen(
                    parent=self, description_text='Getting Fee Rate',
                )
                self.rgb_asset_fee_rate_loading_screen.start()
                self.rgb_asset_fee_rate_loading_screen.make_parent_disabled_during_loading(
                    True,
                )
            else:
                self.rgb_asset_fee_rate_loading_screen.stop()
                self.rgb_asset_fee_rate_loading_screen.make_parent_disabled_during_loading(
                    False,
                )

        if self.loading_performer == 'REFRESH_BUTTON':
            handle_refresh_button_loading(is_loading)
        elif self.loading_performer == 'SEND_BUTTON':
            handle_send_button_loading(is_loading)
        elif self.loading_performer == 'FEE_ESTIMATION':
            handle_fee_estimation_loading(is_loading)

    def handle_show_message(self, msg_type: ToastPreset, message: str):
        """Handle show message"""
        if msg_type == ToastPreset.ERROR:
            ToastManager.error(message)
        else:
            ToastManager.success(message)

    def set_asset_balance(self):
        """Set the spendable and total balance of the asset"""
        view_model = self._view_model.cfa_view_model
        asset_transactions: ListTransferAssetWithBalanceResponseModel = view_model.txn_list
        self.asset_spendable_balance = asset_transactions.asset_balance.spendable
        self.send_rgb_asset_page.asset_balance_label_total.setText(
            str(asset_transactions.asset_balance.future),
        )
        self.send_rgb_asset_page.asset_balance_label_spendable.setText(
            str(asset_transactions.asset_balance.spendable),
        )
        if asset_transactions.asset_balance.spendable == 0:
            self.send_rgb_asset_page.send_btn.setDisabled(True)
        else:
            self.send_rgb_asset_page.send_btn.setDisabled(False)

    def handle_spendable_balance_validation(self):
        """This method handle the spendable balance validation message visibility"""
        if self.asset_spendable_balance > 0:
            self.send_rgb_asset_page.spendable_balance_validation.hide()
            self.disable_buttons_on_fee_rate_loading(False)

        if self.asset_spendable_balance == 0:
            self.send_rgb_asset_page.spendable_balance_validation.show()
            self.disable_buttons_on_fee_rate_loading(True)

    def fee_estimation_loader(self, is_loading):
        """This method sets loading performer to FEE_ESTIMATION and starts or stops the loader"""
        self.loading_performer = 'FEE_ESTIMATION'
        self.update_loading_state(is_loading)

    def disable_buttons_on_fee_rate_loading(self, button_status: bool):
        'This method is used to disable the checkboxes and the send button on spendable validation'
        update_button_status = button_status
        if self.asset_spendable_balance == 0:
            update_button_status = True

        self.send_rgb_asset_page.slow_checkbox.setDisabled(
            update_button_status,
        )
        self.send_rgb_asset_page.medium_checkbox.setDisabled(
            update_button_status,
        )
        self.send_rgb_asset_page.fast_checkbox.setDisabled(
            update_button_status,
        )
        self.send_rgb_asset_page.custom_checkbox.setDisabled(
            update_button_status,
        )
        self.send_rgb_asset_page.send_btn.setDisabled(update_button_status)
        self.handle_button_enabled()

    def validate_rgb_invoice(self):
        """
        Validates the RGB invoice input.

        - Hides the validation label initially.
        - Checks if the entered invoice is valid.
        - Displays an error message if the invoice is invalid.
        """
        invoice = self.send_rgb_asset_page.asset_address_value.text().strip()

        if not invoice:
            self.send_rgb_asset_page.asset_address_validation_label.hide()
            return
        try:
            Invoice(invoice)
            self.send_rgb_asset_page.asset_address_validation_label.hide()

        except RgbLibError.InvalidInvoice:
            self.send_rgb_asset_page.asset_address_validation_label.show()
            self.send_rgb_asset_page.send_btn.setDisabled(True)
            self.send_rgb_asset_page.asset_address_validation_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'invalid_invoice',
                ),
            )
