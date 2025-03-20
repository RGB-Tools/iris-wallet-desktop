"""
Send asset page objects class for interacting with the send asset page.
"""
from __future__ import annotations

from accessible_constant import ASSET_ADDRESS_VALIDATION_LABEL
from accessible_constant import ASSET_AMOUNT_VALIDATION
from accessible_constant import ENTER_RECEIVER_ADDRESS
from accessible_constant import FEE_RATE_INPUT
from accessible_constant import PAY_AMOUNT
from accessible_constant import SEND_ASSET_BUTTON
from accessible_constant import SEND_ASSET_CLOSE_BUTTON
from accessible_constant import SEND_ASSET_REFRESH_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class SendAssetPageObjects(BaseOperations):
    """
    Send asset page objects class for interacting with the send asset page.
    """

    def __init__(self, application):
        """
        Initializes the SendAssetPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        # Lazy evaluation of elements using lambdas
        self.invoice_input = lambda: self.perform_action_on_element(
            role_name='text', name=ENTER_RECEIVER_ADDRESS,
        )
        self.asset_amount_input = lambda: self.perform_action_on_element(
            role_name='text', name=PAY_AMOUNT,
        )
        self.send_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SEND_ASSET_BUTTON,
        )
        self.send_asset_refresh_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SEND_ASSET_REFRESH_BUTTON,
        )
        self.send_asset_close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SEND_ASSET_CLOSE_BUTTON,
        )
        self.amount_validation = lambda: self.perform_action_on_element(
            role_name='label', description=ASSET_AMOUNT_VALIDATION,
        )
        self.fee_rate_input = lambda: self.perform_action_on_element(
            role_name='text', name=FEE_RATE_INPUT,
        )
        self.asset_address_validation = lambda: self.perform_action_on_element(
            role_name='label', description=ASSET_ADDRESS_VALIDATION_LABEL,
        )

    def enter_asset_invoice(self, address):
        """
        Enters the asset invoice address.

        Args:
            address: The invoice address.

        Returns:
            The result of the action.
        """
        return self.do_set_text(self.invoice_input(), address) if self.do_is_displayed(self.invoice_input()) else None

    def enter_asset_amount(self, amount):
        """
        Enters the asset amount.

        Args:
            amount: The asset amount.

        Returns:
            The result of the action.
        """
        return self.do_set_value(self.asset_amount_input(), amount) if self.do_is_displayed(self.asset_amount_input()) else None

    def click_send_button(self):
        """
        Clicks the send button.

        Returns:
            The result of the action.
        """
        return self.do_click(self.send_button()) if self.do_is_displayed(self.send_button()) else None

    def click_send_asset_refresh_button(self):
        """
        Clicks the send asset refresh button.

        Returns:
            The result of the action.
        """
        return self.do_click(self.send_asset_refresh_button()) if self.do_is_displayed(self.send_asset_refresh_button()) else None

    def click_send_asset_close_button(self):
        """
        Clicks the send asset close button.

        Returns:
            The result of the action.
        """
        return self.do_click(self.send_asset_close_button()) if self.do_is_displayed(self.send_asset_close_button()) else None

    def get_amount_validation(self):
        """
        Gets the amount validation text.

        Returns:
            The amount validation text.
        """
        return self.do_get_text(self.amount_validation()) if self.do_is_displayed(self.amount_validation()) else None

    def enter_fee_rate(self, fee_rate):
        """
        Enters the fee rate.

        Args:
            fee_rate: The fee rate.

        Returns:
            The result of the action.
        """
        return self.do_set_value(self.fee_rate_input(), fee_rate) if self.do_is_displayed(self.fee_rate_input()) else None

    def get_fee_rate_text(self):
        """Gets the fee rate from the input field."""
        return self.get_text(self.fee_rate_input()) if self.do_is_displayed(self.fee_rate_input()) else None

    def get_asset_address_validation_label(self):
        """
        Gets the asset address validation label.
        """
        return self.do_get_text(self.asset_address_validation()) if self.do_is_displayed(self.asset_address_validation()) else None
