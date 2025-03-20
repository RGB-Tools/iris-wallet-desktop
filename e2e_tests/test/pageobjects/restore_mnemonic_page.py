"""
Restore wallet page objects module.
"""
from __future__ import annotations

from dogtail.tree import root

from accessible_constant import RESTORE_CONTINUE_BUTTON
from accessible_constant import RESTORE_DIALOG_BOX
from accessible_constant import RESTORE_MNEMONIC_INPUT
from accessible_constant import RESTORE_PASSWORD_INPUT
from e2e_tests.test.utilities.base_operation import BaseOperations


class RestoreWalletPageObjects(BaseOperations):
    """
    A class to represent Restore wallet page objects.
    """

    def __init__(self, application):
        """
        Initializes the RestoreWalletPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.restore_dialog_box = lambda: root.child(
            roleName='dialog', name=RESTORE_DIALOG_BOX,
        )
        self.restore_mnemonic_input = lambda: self.restore_dialog_box().child(
            roleName='text', name=RESTORE_MNEMONIC_INPUT,
        )
        self.restore_password_input = lambda: self.restore_dialog_box().child(
            roleName='password text', name=RESTORE_PASSWORD_INPUT,
        )
        self.restore_continue_button = lambda: self.restore_dialog_box().child(
            roleName='push button', name=RESTORE_CONTINUE_BUTTON,
        )

    def enter_mnemonic_value(self, mnemonic):
        """
        Enters the mnemonic value in the restore mnemonic input field.

        Args:
            mnemonic (str): The mnemonic value to be entered.

        Returns:
            bool: True if the mnemonic value is entered successfully, False otherwise.
        """
        return self.do_set_value(self.restore_mnemonic_input(), mnemonic) if self.do_is_displayed(self.restore_mnemonic_input()) else None

    def enter_password_value(self, password):
        """
        Enters the password value in the restore password input field.

        Args:
            password (str): The password value to be entered.

        Returns:
            bool: True if the password value is entered successfully, False otherwise.
        """
        return self.do_set_value(self.restore_password_input(), password) if self.do_is_displayed(self.restore_password_input()) else None

    def click_continue_button(self):
        """
        Clicks the continue button.

        Returns:
            bool: True if the continue button is clicked successfully, False otherwise.
        """
        return self.do_click(self.restore_continue_button()) if self.do_is_displayed(self.restore_continue_button()) else None
