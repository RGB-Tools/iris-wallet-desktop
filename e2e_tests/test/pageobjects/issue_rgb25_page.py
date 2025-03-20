"""
IssueRgb25PageObjects class provides methods to interact with the issue RGB25 page.
"""
from __future__ import annotations

from dogtail.rawinput import keyCombo
from dogtail.tree import root

from accessible_constant import FILE_CHOOSER
from accessible_constant import ISSUE_RGB25_ASSET_CLOSE_BUTTON
from accessible_constant import ISSUE_RGB25_BUTTON
from accessible_constant import RGB25_ASSET_AMOUNT
from accessible_constant import RGB25_ASSET_DESCRIPTION
from accessible_constant import RGB25_ASSET_NAME
from accessible_constant import RGB25_UPLOAD_FILE_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class IssueRgb25PageObjects(BaseOperations):
    """
    Initialize the IssueRgb25PageObjects class.

    Args:
        application: The application instance.
    """

    def __init__(self, application):
        """
        Initialize the IssueRgb25PageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ISSUE_RGB25_ASSET_CLOSE_BUTTON,
        )
        self.asset_name = lambda: self.perform_action_on_element(
            role_name='text', name=RGB25_ASSET_NAME,
        )
        self.asset_description = lambda: self.perform_action_on_element(
            role_name='text', name=RGB25_ASSET_DESCRIPTION,
        )
        self.asset_amount = lambda: self.perform_action_on_element(
            role_name='text', name=RGB25_ASSET_AMOUNT,
        )
        self.issue_rgb25_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ISSUE_RGB25_BUTTON,
        )
        self.upload_file_button = lambda: self.perform_action_on_element(
            role_name='push button', name=RGB25_UPLOAD_FILE_BUTTON,
        )
        self.file_dialog = lambda: root.child(roleName=FILE_CHOOSER)
        self.rgb25_asset_media = lambda: self.file_dialog().child(
            roleName='table cell', name='sample.png',
        )

    def click_close_button(self):
        """
        Click the close button on the issue RGB25 page.

        Returns:
            bool: True if the button is clicked, None otherwise.
        """
        return self.do_click(self.close_button()) if self.do_is_displayed(self.close_button()) else None

    def enter_asset_name(self, asset_name):
        """
        Enter the asset name on the issue RGB25 page.

        Args:
            asset_name (str): The asset name to enter.

        Returns:
            bool: True if the asset name is entered, None otherwise.
        """
        return self.do_set_value(self.asset_name(), asset_name) if self.do_is_displayed(self.asset_name()) else None

    def enter_asset_description(self, asset_description):
        """
        Enter the asset description on the issue RGB25 page.

        Args:
            asset_description (str): The asset description to enter.

        Returns:
            bool: True if the asset description is entered, None otherwise.
        """
        return self.do_set_value(self.asset_description(), asset_description) if self.do_is_displayed(self.asset_description()) else None

    def enter_asset_amount(self, asset_amount):
        """
        Enter the asset amount on the issue RGB25 page.

        Args:
            asset_amount (str): The asset amount to enter.

        Returns:
            bool: True if the asset amount is entered, None otherwise.
        """
        return self.do_set_value(self.asset_amount(), asset_amount) if self.do_is_displayed(self.asset_amount()) else None

    def click_issue_rgb25_button(self):
        """
        Click the issue RGB25 button on the issue RGB25 page.

        Returns:
            bool: True if the button is clicked, None otherwise.
        """
        return self.do_click(self.issue_rgb25_button()) if self.do_is_displayed(self.issue_rgb25_button()) else None

    def click_upload_file_button(self):
        """
        Click the upload file button on the issue RGB25 page.

        Returns:
            bool: True if the button is clicked, None otherwise.
        """
        return self.do_click(self.upload_file_button()) if self.do_is_displayed(self.upload_file_button()) else None

    def click_rgb25_asset_media(self):
        """
        Select the RGB25 asset by focusing on it and pressing Enter.

        Returns:
            bool: True if the asset is selected, False otherwise.
        """
        if self.do_is_displayed(self.rgb25_asset_media()):
            self.rgb25_asset_media().grabFocus()
            keyCombo('enter')
            return True
        return False  # Return False if the element is not displayed
