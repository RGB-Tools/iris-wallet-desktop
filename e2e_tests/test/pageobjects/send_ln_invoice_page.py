"""
SendLnInvoicePageObjects class for interacting with send ln invoice page elements.
"""
from __future__ import annotations

from accessible_constant import AMOUNT_VALIDATION_ERROR_LABEL
from accessible_constant import LN_INVOICE_INPUT
from accessible_constant import SEND_LN_INVOICE_BUTTON
from accessible_constant import SEND_LN_INVOICE_CLOSE_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class SendLnInvoicePageObjects(BaseOperations):
    """
    A class representing the SendLnInvoicePageObjects.

    It provides methods to interact with the send ln invoice page elements.
    """

    def __init__(self, application):
        """
        Initializes the SendLnInvoicePageObjects.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SEND_LN_INVOICE_CLOSE_BUTTON,
        )
        self.invoice_input = lambda: self.perform_action_on_element(
            role_name='text', name=LN_INVOICE_INPUT,
        )
        self.send_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SEND_LN_INVOICE_BUTTON,
        )
        self.error_label = lambda: self.perform_action_on_element(
            role_name='label', description=AMOUNT_VALIDATION_ERROR_LABEL,
        )

    def click_close_button(self):
        """
        Clicks the close button on the send ln invoice page.

        Returns:
            bool: True if the button is clicked successfully, None otherwise.
        """
        return self.do_click(self.close_button()) if self.do_is_displayed(self.close_button()) else None

    def enter_asset_invoice(self, ln_invoice):
        """
        Enters the ln invoice in the ln invoice input field.
        Args:
        ln_invoice (str): The ln invoice to be entered.
        Returns:
        bool: True if the ln invoice is entered successfully, None otherwise.
        """
        return self.do_set_text(self.invoice_input(), ln_invoice) if self.do_is_displayed(self.invoice_input()) else None

    def click_send_button(self):
        """
        Clicks the send button on the send ln invoice page.
        Returns:
        bool: True if the button is clicked successfully, None otherwise.
        """
        return self.do_click(self.send_button()) if self.do_is_displayed(self.send_button()) else None

    def get_error_label(self):
        """
        Retrieves the error label text if it is displayed.

        Returns:
            str: The error label text, or None if it is not displayed.
        """
        return self.do_get_text(self.error_label()) if self.do_is_displayed(self.error_label()) else None
