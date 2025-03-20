"""
IssueRgb20PageObjects class provides methods to interact with issue RGB20 page elements.
"""
from __future__ import annotations

from accessible_constant import ISSUE_RGB20_ASSET_CLOSE_BUTTON
from accessible_constant import ISSUE_RGB20_BUTTON
from accessible_constant import RGB20_ASSET_AMOUNT
from accessible_constant import RGB20_ASSET_NAME
from accessible_constant import RGB20_ASSET_TICKER
from e2e_tests.test.utilities.base_operation import BaseOperations


class IssueRgb20PageObjects(BaseOperations):
    """
    IssueRgb20PageObjects class provides methods to interact with issue RGB20 page elements.
    """

    def __init__(self, application):
        """
        Initializes the IssueRgb20PageObjects class with the application object.

        Args:
            application (object): The application object.
        """
        super().__init__(application)

        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ISSUE_RGB20_ASSET_CLOSE_BUTTON,
        )
        self.asset_name = lambda: self.perform_action_on_element(
            role_name='text', name=RGB20_ASSET_NAME,
        )
        self.asset_ticker = lambda: self.perform_action_on_element(
            role_name='text', name=RGB20_ASSET_TICKER,
        )
        self.asset_amount = lambda: self.perform_action_on_element(
            role_name='text', name=RGB20_ASSET_AMOUNT,
        )
        self.issue_rgb20_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ISSUE_RGB20_BUTTON,
        )

    def click_close_button(self):
        """
        Clicks the close button on the issue RGB20 page.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return self.do_click(self.close_button()) if self.do_is_displayed(self.close_button()) else None

    def enter_asset_name(self, asset_name):
        """
        Enters the asset name on the issue RGB20 page.

        Args:
            asset_name (str): The asset name to enter.

        Returns:
            bool: True if the asset name is entered, False otherwise.
        """
        return self.do_set_value(self.asset_name(), asset_name) if self.do_is_displayed(self.asset_name()) else None

    def enter_asset_ticker(self, asset_ticker):
        """
        Enters the asset ticker on the issue RGB20 page.

        Args:
            asset_ticker (str): The asset ticker to enter.

        Returns:
            bool: True if the asset ticker is entered, False otherwise.
        """
        return self.do_set_value(self.asset_ticker(), asset_ticker) if self.do_is_displayed(self.asset_ticker()) else None

    def enter_asset_amount(self, asset_amount):
        """
        Enters the asset amount on the issue RGB20 page.

        Args:
            asset_amount (str): The asset amount to enter.

        Returns:
            bool: True if the asset amount is entered, False otherwise.
        """
        return self.do_set_value(self.asset_amount(), asset_amount) if self.do_is_displayed(self.asset_amount()) else None

    def click_issue_rgb20_button(self):
        """
        Clicks the issue RGB20 button on the issue RGB20 page.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return self.do_click(self.issue_rgb20_button()) if self.do_is_displayed(self.issue_rgb20_button()) else None
