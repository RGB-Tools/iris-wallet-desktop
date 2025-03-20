"""
CreateLnInvoicePageObjects class provides methods to interact with the create LN invoice page.
"""
from __future__ import annotations

from accessible_constant import ASSET_AMOUNT_LN
from accessible_constant import CREATE_LN_INVOICE_AMOUNT_VALIDATION
from accessible_constant import CREATE_LN_INVOICE_BUTTON
from accessible_constant import CREATE_LN_INVOICE_CLOSE_BUTTON
from accessible_constant import EXPIRY_TIME
from accessible_constant import EXPIRY_TIME_COMBO_BOX
from accessible_constant import MSAT_AMOUNT
from e2e_tests.test.utilities.base_operation import BaseOperations


class CreateLnInvoicePageObjects(BaseOperations):
    """
    Initialize the CreateLnInvoicePageObjects class.

    Args:
        application: The application instance.
    """

    def __init__(self, application):
        """Initializer for create LN invoice page objects."""
        super().__init__(application)

        self.asset_amount = lambda: self.perform_action_on_element(
            role_name='text', name=ASSET_AMOUNT_LN,
        )
        self.expiry_input = lambda: self.perform_action_on_element(
            role_name='text', name=EXPIRY_TIME,
        )
        self.msat_amount = lambda: self.perform_action_on_element(
            role_name='text', name=MSAT_AMOUNT,
        )
        self.create_button = lambda: self.perform_action_on_element(
            role_name='push button', name=CREATE_LN_INVOICE_BUTTON,
        )
        self.combo_box = lambda: self.perform_action_on_element(
            role_name='combo box', description=EXPIRY_TIME_COMBO_BOX,
        )
        self.error_label = lambda: self.perform_action_on_element(
            role_name='label', description=CREATE_LN_INVOICE_AMOUNT_VALIDATION,
        )
        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=CREATE_LN_INVOICE_CLOSE_BUTTON,
        )

    def get_expiry_time_unit(self):
        """
        Get the expiry time unit(Days, Hours, Minute)

        Returns:
            The expiry time unit if the combo box is displayed, otherwise None.
        """
        return self.do_get_text(self.combo_box()) if self.do_is_displayed(self.combo_box()) else None

    def get_expiry_amount(self):
        """
        Get the expiry amount from the expiry input field.

        Returns:
            The expiry amount if the field is displayed, otherwise None.
        """
        return self.expiry_input().text if self.do_is_displayed(self.expiry_input()) else None

    def enter_expiry_amount(self, value):
        """
        Enter the expiry amount in the expiry input field.

        Returns:
            The result of setting the value if the field is displayed, otherwise None.
        """
        return self.do_set_value(self.expiry_input(), value) if self.do_is_displayed(self.expiry_input()) else None

    def enter_asset_amount(self, value):
        """
        Enter the asset amount in the asset amount field.

        Returns:
            The result of setting the value if the field is displayed, otherwise None.
        """
        return self.do_set_value(self.asset_amount(), value) if self.do_is_displayed(self.asset_amount()) else None

    def click_create_button(self):
        """
        Click the create button.

        Returns:
            The result of clicking the button if it is displayed, otherwise None.
        """
        return self.do_click(self.create_button()) if self.do_is_displayed(self.create_button()) else None

    def get_error_label(self):
        """
        Retrieves the error label text if it is displayed.

        Returns:
            str: The error label text, or None if it is not displayed.
        """
        return self.do_get_text(self.error_label()) if self.do_is_displayed(self.error_label()) else None

    def click_close_button(self):
        """
        Clicks the close button on the send ln invoice page.

        Returns:
            bool: True if the button is clicked successfully, None otherwise.
        """
        return self.do_click(self.close_button()) if self.do_is_displayed(self.close_button()) else None
