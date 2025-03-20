"""
Wallet transfer page objects module.
"""
from __future__ import annotations

from accessible_constant import OPTION_1_FRAME
from accessible_constant import OPTION_2_FRAME
from e2e_tests.test.utilities.base_operation import BaseOperations


class WalletTransferPageObjects(BaseOperations):
    """
    A class representing Wallet transfer page objects.
    """

    def __init__(self, application):
        """
        Initializes the WalletTransferPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        # Lazy evaluation of elements using lambdas
        self.on_chain_button = lambda: self.perform_action_on_element(
            role_name='panel', name=OPTION_1_FRAME,
        )
        self.lightning_button = lambda: self.perform_action_on_element(
            role_name='panel', name=OPTION_2_FRAME,
        )

    def click_on_chain_button(self):
        """
        Clicks the on-chain button if it is displayed.

        Returns:
            The result of the click action or None if the button is not displayed.
        """
        return self.do_click(self.on_chain_button()) if self.do_is_displayed(self.on_chain_button()) else None

    def click_lightning_button(self):
        """
        Clicks the lightning button if it is displayed.

        Returns:
            The result of the click action or None if the button is not displayed.
        """
        return self.do_click(self.lightning_button()) if self.do_is_displayed(self.lightning_button()) else None
