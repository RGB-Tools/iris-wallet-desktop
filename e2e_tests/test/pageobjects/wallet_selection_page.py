"""
Wallet selection page objects module.
"""
from __future__ import annotations

from accessible_constant import OPTION_1_FRAME
from accessible_constant import OPTION_2_FRAME
from accessible_constant import WALLET_OR_TRANSFER_SELECTION_CONTINUE_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class WalletSelectionPageObjects(BaseOperations):
    """
    Wallet selection page objects class.
    """

    def __init__(self, application):
        """
        Initializes the WalletSelectionPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        # Lazy evaluation of elements using lambdas
        self.embedded_button = lambda: self.perform_action_on_element(
            role_name='panel', name=OPTION_1_FRAME,
        )
        self.remote_button = lambda: self.perform_action_on_element(
            role_name='panel', name=OPTION_2_FRAME,
        )
        self.continue_button = lambda: self.perform_action_on_element(
            role_name='push button', name=WALLET_OR_TRANSFER_SELECTION_CONTINUE_BUTTON,
        )

    def click_embedded_button(self):
        """
        Clicks the embedded button if it is displayed.

        Returns:
            True if the button was clicked and continue button appeared, False otherwise.
        """
        if not self.do_is_displayed(self.embedded_button()):
            return False

        self.do_click(self.embedded_button())

        # Retry logic: ensure the selection registered (max 2 attempts)
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            if self.do_is_displayed(self.continue_button()):
                return True  # Success - continue button is visible

            print(
                f"[RETRY] Continue button not visible after embedded selection, retrying... (attempt {
                    retry_count + 1
                }/{max_retries})",
            )
            self.do_click(self.embedded_button())
            retry_count += 1

        # Final check after retries
        return self.do_is_displayed(self.continue_button())

    def click_remote_button(self):
        """
        Clicks the remote button if it is displayed.

        Returns:
            True if the button was clicked and continue button appeared, False otherwise.
        """
        if not self.do_is_displayed(self.remote_button()):
            return False

        self.do_click(self.remote_button())

        # Retry logic: ensure the selection registered (max 2 attempts)
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            if self.do_is_displayed(self.continue_button()):
                return True  # Success - continue button is visible

            print(
                f"[RETRY] Continue button not visible after remote selection, retrying... (attempt {
                    retry_count + 1
                }/{max_retries})",
            )
            self.do_click(self.remote_button())
            retry_count += 1

        # Final check after retries
        return self.do_is_displayed(self.continue_button())

    def click_continue_button(self):
        """
        Clicks the continue button if it is displayed.
        """
        return self.do_click(self.continue_button()) if self.do_is_displayed(self.continue_button()) else None
