"""
Wallet password page objects for E2E tests
"""
from __future__ import annotations

from accessible_constant import ENTER_WALLET_PASSWORD
from accessible_constant import LOGIN_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class EnterWalletPasswordPageObjects(BaseOperations):
    """Wallet password page objects for E2E tests"""

    def __init__(self, application):
        """
        Initialize the EnterWalletPasswordPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.password_input = lambda: self.perform_action_on_element(
            role_name='password text', name=ENTER_WALLET_PASSWORD,
        )
        self.login_button = lambda: self.perform_action_on_element(
            role_name='push button', name=LOGIN_BUTTON,
        )

    def enter_password(self, password):
        """
        Enter password in the password input field.

        Args:
            password (str): The password to enter.

        Returns:
            bool: True if the password is entered successfully, False otherwise.
        """
        return self.do_set_value(self.password_input(), password) if self.do_is_displayed(self.password_input()) else None

    def click_login_button(self):
        """
        Click on the login button.

        Returns:
            bool: True if the button is clicked successfully, False otherwise.
        """
        return self.do_click(self.login_button()) if self.do_is_displayed(self.login_button()) else None
