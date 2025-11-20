# pylint: disable=too-many-instance-attributes
"""
Keyring dialog box page objects for E2E tests.
"""
from __future__ import annotations

from dogtail.tree import root

from accessible_constant import KEYRING_CANCEL_BUTTON
from accessible_constant import KEYRING_CONTINUE_BUTTON
from accessible_constant import KEYRING_DIALOG_BOX
from accessible_constant import KEYRING_MNEMONIC_COPY_BUTTON
from accessible_constant import KEYRING_MNEMONIC_VALUE_LABEL
from accessible_constant import KEYRING_MNEMONICS_FRAME
from accessible_constant import KEYRING_PASSWORD_COPY_BUTTON
from accessible_constant import KEYRING_PASSWORD_FRAME
from accessible_constant import KEYRING_PASSWORD_VALUE_LABEL
from accessible_constant import SAVE_CREDENTIALS_CHECK_BOX
from e2e_tests.test.utilities.base_operation import BaseOperations


class KeyringDialogBoxPageObjects(BaseOperations):
    """
    Keyring dialog box page objects for E2E tests.
    """

    def __init__(self, application):
        """
        Initializes the keyring dialog box page objects.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.keyring_dialog = lambda: root.child(
            roleName='dialog', name=KEYRING_DIALOG_BOX,
        )
        self.keyring_mnemonic_copy_button = lambda: self.keyring_dialog().child(
            roleName='push button', name=KEYRING_MNEMONIC_COPY_BUTTON,
        )
        self.keyring_mnemonic_value_label = lambda: self.keyring_dialog().child(
            roleName='label', description=KEYRING_MNEMONIC_VALUE_LABEL,
        )
        self.keyring_mnemonics_frame = lambda: self.keyring_dialog().child(
            roleName='frame', name=KEYRING_MNEMONICS_FRAME,
        )
        self.keyring_password_copy_button = lambda: self.keyring_dialog().child(
            roleName='push button', name=KEYRING_PASSWORD_COPY_BUTTON,
        )
        self.keyring_password_frame = lambda: self.keyring_dialog().child(
            roleName='frame', name=KEYRING_PASSWORD_FRAME,
        )
        self.keyring_password_value_label = lambda: self.keyring_dialog().child(
            roleName='label', description=KEYRING_PASSWORD_VALUE_LABEL,
        )
        self.keyring_check_box = lambda: self.keyring_dialog().child(
            roleName='check box', name=SAVE_CREDENTIALS_CHECK_BOX,
        )
        self.continue_button = lambda: self.keyring_dialog().child(
            roleName='push button', name=KEYRING_CONTINUE_BUTTON,
        )
        self.cancel_button = lambda: self.keyring_dialog().child(
            roleName='push button', name=KEYRING_CANCEL_BUTTON,
        )

    def click_keyring_dialog(self):
        """
        Clicks the keyring dialog box.

        Returns:
            bool: True if the click is successful, False otherwise.
        """
        return self.do_click(self.keyring_dialog()) if self.do_is_displayed(self.keyring_dialog()) else None

    def click_keyring_mnemonic_copy_button(self):
        """
        Clicks the keyring mnemonic copy button.

        Returns:
            bool: True if the click is successful, False otherwise.
        """
        return self.do_click(self.keyring_mnemonic_copy_button()) if self.do_is_displayed(self.keyring_mnemonic_copy_button()) else None

    def get_keyring_mnemonic_value(self):
        """
        Gets the keyring mnemonic value.

        Returns:
            str: The keyring mnemonic value if it exists, None otherwise.
        """
        return self.do_get_text(self.keyring_mnemonic_value_label()) if self.do_is_displayed(self.keyring_mnemonic_value_label()) else None

    def click_keyring_password_copy_button(self):
        """
        Clicks the keyring password copy button.

        Returns:
            bool: True if the click is successful, False otherwise.
        """
        return self.do_click(self.keyring_password_copy_button()) if self.do_is_displayed(self.keyring_password_copy_button()) else None

    def get_keyring_password_value(self):
        """
        Gets the keyring password value.

        Returns:
            str: The keyring password Value if it exists, None otherwise.
        """
        return self.do_get_text(self.keyring_password_value_label()) if self.do_is_displayed(self.keyring_password_value_label()) else None

    def click_check_box(self):
        """
        Clicks the check box.
        """
        if self.do_is_displayed(self.keyring_check_box()):
            return self.keyring_check_box().queryAction().doAction(0)
        return None

    def click_continue_button(self):
        """
        Clicks the continue button.
        """
        return self.do_click(self.continue_button()) if self.do_is_displayed(self.continue_button()) else None

    def click_cancel_button(self):
        """
        Clicks the close button.
        """
        return self.do_click(self.cancel_button()) if self.do_is_displayed(self.cancel_button()) else None
