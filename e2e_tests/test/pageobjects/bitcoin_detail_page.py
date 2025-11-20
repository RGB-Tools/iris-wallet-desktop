"""
Bitcoin detail page objects class.
"""
from __future__ import annotations

from accessible_constant import BITCOIN_BALANCE
from accessible_constant import BITCOIN_CLOSE_BUTTON
from accessible_constant import BITCOIN_REFRESH_BUTTON
from accessible_constant import BITCOIN_SPENDABLE_BALANCE
from accessible_constant import BITCOIN_TRANSACTION_DETAIL_FRAME
from accessible_constant import RECEIVE_BITCOIN_BUTTON
from accessible_constant import SEND_BITCOIN_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class BitcoinDetailPageObjects(BaseOperations):
    """
    Initialize bitcoin detail page objects.
    """

    def __init__(self, application):
        super().__init__(application)

        self.bitcoin_balance = lambda: self.perform_action_on_element(
            role_name='label', description=BITCOIN_BALANCE,
        )
        self.spendable_balance = lambda: self.perform_action_on_element(
            role_name='label', description=BITCOIN_SPENDABLE_BALANCE,
        )
        self.receive_bitcoin_button = lambda: self.perform_action_on_element(
            role_name='push button', name=RECEIVE_BITCOIN_BUTTON,
        )
        self.send_bitcoin_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SEND_BITCOIN_BUTTON,
        )
        self.bitcoin_close_button = lambda: self.perform_action_on_element(
            role_name='push button', description=BITCOIN_CLOSE_BUTTON,
        )
        self.bitcoin_refresh_button = lambda: self.perform_action_on_element(
            role_name='push button', name=BITCOIN_REFRESH_BUTTON,
        )
        self.bitcoin_transaction_frame = lambda: self.get_first_element(
            role_name='panel', name=BITCOIN_TRANSACTION_DETAIL_FRAME,
        )

    def get_total_balance(self):
        """
        Get total balance.
        """
        return self.do_get_text(self.bitcoin_balance()) if self.do_is_displayed(self.bitcoin_balance()) else str | None

    def get_spendable_balance(self):
        """
        Get spendable balance.
        """
        return self.do_get_text(self.spendable_balance()) if self.do_is_displayed(self.spendable_balance()) else str | None

    def click_receive_bitcoin_button(self):
        """
        Click get bitcoin address button.
        """
        return self.do_click(self.receive_bitcoin_button()) if self.do_is_displayed(self.receive_bitcoin_button()) else None

    def click_send_bitcoin_button(self):
        """
        Click send bitcoin button.
        """
        return self.do_click(self.send_bitcoin_button()) if self.do_is_displayed(self.send_bitcoin_button()) else None

    def click_bitcoin_close_button(self):
        """
        Click bitcoin close button.
        """
        return self.do_click(self.bitcoin_close_button()) if self.do_is_displayed(self.bitcoin_close_button()) else None

    def click_bitcoin_refresh_button(self):
        """
        Click bitcoin refresh button.
        """
        return self.do_click(self.bitcoin_refresh_button()) if self.do_is_displayed(self.bitcoin_refresh_button()) else None

    def click_bitcoin_transaction_frame(self):
        """
        Click bitcoin transaction frame.
        """
        return self.do_click(self.bitcoin_transaction_frame()) if self.do_is_displayed(self.bitcoin_transaction_frame()) else None
