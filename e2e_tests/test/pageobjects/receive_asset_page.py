"""
Receive aset page objects class to handle receive asset page operations.
"""
from __future__ import annotations

from accessible_constant import INVOICE_COPY_BUTTON
from accessible_constant import RECEIVE_ASSET_CLOSE_BUTTON
from accessible_constant import RECEIVER_ADDRESS
from e2e_tests.test.utilities.base_operation import BaseOperations


class ReceiveAssetPageObjects(BaseOperations):
    """Receive asset page objects class to handle receive asset page operations."""

    def __init__(self, application):
        """
        Initialize ReceiveAssetPageObjects with application.

        Args:
            application: The application instance.
        """
        super().__init__(application)
        # Lazy evaluation with lambda
        self.receiver_invoice = lambda: self.perform_action_on_element(
            role_name='label', description=RECEIVER_ADDRESS,
        )
        self.receive_asset_close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=RECEIVE_ASSET_CLOSE_BUTTON,
        )
        self.invoice_copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=INVOICE_COPY_BUTTON,
        )

    def get_receiver_invoice(self):
        """
        Get the receiver invoice text if it's displayed.

        Returns:
            str: The receiver invoice text or None if not displayed.
        """
        return self.do_get_text(self.receiver_invoice()) if self.do_is_displayed(self.receiver_invoice()) else None

    def click_receive_asset_close_button(self):
        """
        Click the receive asset close button if it's displayed.

        Returns:
            bool: True if clicked, None if not displayed.
        """
        return self.do_click(self.receive_asset_close_button()) if self.do_is_displayed(self.receive_asset_close_button()) else None

    def click_invoice_copy_button(self):
        """
        Click the invoice copy button if it's displayed.

        Returns:
            bool: True if clicked, None if not displayed.
        """
        if self.do_is_displayed(self.invoice_copy_button()):
            return self.invoice_copy_button().click()
        return None
