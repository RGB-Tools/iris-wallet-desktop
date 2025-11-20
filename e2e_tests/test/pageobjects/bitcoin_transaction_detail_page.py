"""
This module contains the page objects for the bitcoin transaction detail page.
"""
from __future__ import annotations

from accessible_constant import BITCOIN_AMOUNT_VALUE
from accessible_constant import BITCOIN_TX_ID
from accessible_constant import BITCOIN_TX_PAGE_CLOSE_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class BitcoinTransactionDetailPageObjects(BaseOperations):
    """
    This class represents the page objects for the bitcoin transaction detail page.
    It provides methods to interact with the page elements.
    """

    def __init__(self, application):
        """
        Initializes the page objects with the given application.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=BITCOIN_TX_PAGE_CLOSE_BUTTON,
        )
        self.bitcoin_tx_id = lambda: self.perform_action_on_element(
            role_name='label', description=BITCOIN_TX_ID,
        )
        self.bitcoin_amount_value = lambda: self.perform_action_on_element(
            role_name='label', description=BITCOIN_AMOUNT_VALUE,
        )

    def click_close_button(self):
        """
        Clicks the close button on the page.
        """
        return self.do_click(self.close_button()) if self.do_is_displayed(self.close_button()) else None

    def get_bitcoin_tx_id(self):
        """
        Gets the value of the bitcoin transaction ID on the page.

        Returns:
            str: The bitcoin transaction ID.
        """
        return self.do_get_text(self.bitcoin_tx_id()) if self.do_is_displayed(self.bitcoin_tx_id()) else str | None

    def get_bitcoin_amount_value(self):
        """
        Gets the value of the bitcoin transaction amount on the page.
        """
        return self.do_get_text(self.bitcoin_amount_value()) if self.do_is_displayed(self.bitcoin_amount_value()) else str | None
