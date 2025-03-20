"""
Set password page objects class for interacting with the set password page.
"""
from __future__ import annotations

from accessible_constant import CONFIRM_PASSWORD_INPUT
from accessible_constant import CONFIRM_PASSWORD_VISIBILITY_BUTTON
from accessible_constant import PASSWORD_INPUT
from accessible_constant import PASSWORD_SUGGESTION_BUTTON
from accessible_constant import PASSWORD_VISIBILITY_BUTTON
from accessible_constant import SET_WALLET_PASSWORD_CLOSE_BUTTON
from accessible_constant import SET_WALLET_PASSWORD_PROCEED_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class SetPasswordPageObjects(BaseOperations):
    """
    Set password page objects class for interacting with the set password page.
    """

    def __init__(self, application):
        """
        Initializes the SetPasswordPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        # Lazy evaluation of elements using lambdas
        self.password_input = lambda: self.perform_action_on_element(
            role_name='password text', name=PASSWORD_INPUT,
        )
        self.confirm_password_input = lambda: self.perform_action_on_element(
            role_name='password text', name=CONFIRM_PASSWORD_INPUT,
        )
        self.password_visibility_button = lambda: self.perform_action_on_element(
            role_name='push button', name=PASSWORD_VISIBILITY_BUTTON,
        )
        self.confirm_password_visibility_button = lambda: self.perform_action_on_element(
            role_name='push button', name=CONFIRM_PASSWORD_VISIBILITY_BUTTON,
        )
        self.password_suggestion_button = lambda: self.perform_action_on_element(
            role_name='push button', name=PASSWORD_SUGGESTION_BUTTON,
        )
        self.proceed_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SET_WALLET_PASSWORD_PROCEED_BUTTON,
        )
        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SET_WALLET_PASSWORD_CLOSE_BUTTON,
        )

    def enter_password(self, password):
        """
        Enters the password in the password input field.

        Args:
            password (str): The password to enter.

        Returns:
            bool: True if the password is entered successfully, False otherwise.
        """
        return self.do_set_value(self.password_input(), password) if self.do_is_displayed(self.password_input()) else None

    def enter_confirm_password(self, password):
        """
        Enters the confirm password in the confirm password input field.

        Args:
            password (str): The confirm password to enter.

        Returns:
            bool: True if the confirm password is entered successfully, False otherwise.
        """
        return self.do_set_value(self.confirm_password_input(), password) if self.do_is_displayed(self.confirm_password_input()) else None

    def click_password_visibility_button(self):
        """
        Clicks the password visibility button.

        Returns:
            bool: True if the button is clicked successfully, False otherwise.
        """
        return self.do_click(self.password_visibility_button()) if self.do_is_displayed(self.password_visibility_button()) else None

    def click_confirm_password_visibility_button(self):
        """
        Clicks the confirm password visibility button.

        Returns:
            bool: True if the button is clicked successfully, False otherwise.
        """
        return self.do_click(self.confirm_password_visibility_button()) if self.do_is_displayed(self.confirm_password_visibility_button()) else None

    def click_password_suggestion_button(self):
        """
        Clicks the password suggestion button.

        Returns:
            bool: True if the button is clicked successfully, False otherwise.
        """
        return self.do_click(self.password_suggestion_button()) if self.do_is_displayed(self.password_suggestion_button()) else None

    def click_proceed_button(self):
        """
        Clicks the proceed button.

        Returns:
            bool: True if the button is clicked successfully, False otherwise.
        """
        return self.do_click(self.proceed_button()) if self.do_is_displayed(self.proceed_button()) else None
