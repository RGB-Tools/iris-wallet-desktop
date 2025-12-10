"""
Fungible page objects class for interacting with the application.
"""
from __future__ import annotations

from accessible_constant import FUNGIBLES_SCROLL_WIDGETS
from accessible_constant import ISSUE_NIA_ASSET
from accessible_constant import NETWORK_AND_BACKUP_FRAME
from e2e_tests.test.utilities.base_operation import BaseOperations


class FungiblePageObjects(BaseOperations):
    """Fungible page objects class."""

    def __init__(self, application):
        """
        Initializes the FungiblePageObjects class with the application.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        # Define elements using lambdas for lazy evaluation
        self.nia_asset_name = None
        self.issue_nia_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ISSUE_NIA_ASSET,
        )
        self.bitcoin_frame = lambda: self.perform_action_on_element(
            role_name='label', name='regtest bitcoin',
        )
        self.backup_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=NETWORK_AND_BACKUP_FRAME,
        )
        self.fungibles_scroll_area = lambda: self.perform_action_on_element(
            role_name='filler', name=FUNGIBLES_SCROLL_WIDGETS,
        )

    def get_child_count(self):
        """Returns child count"""
        return self.do_get_child_count(self.fungibles_scroll_area()) if self.do_is_displayed(self.fungibles_scroll_area()) else None

    def click_issue_nia_button(self):
        """
        Clicks the issue NIA button if it is displayed.

        Returns:
            bool: True if the button is clicked, None otherwise.
        """
        return self.do_click(self.issue_nia_button()) if self.do_is_displayed(self.issue_nia_button()) else None

    def click_bitcoin_frame(self):
        """
        Clicks the bitcoin frame if it is displayed.

        Returns:
            bool: True if the frame is clicked, None otherwise.
        """
        return self.do_click(self.bitcoin_frame()) if self.do_is_displayed(self.bitcoin_frame()) else None

    def get_nia_asset_name(self, asset_name):
        """
        Retrieves the asset name if it is displayed.

        Args:
            asset_name (str): The name of the asset.

        Returns:
            str: The asset name if it is displayed, None otherwise.
        """
        self.nia_asset_name = self.perform_action_on_element(
            role_name='label', name=asset_name,
        )
        return self.do_get_text(self.nia_asset_name) if self.do_is_displayed(self.nia_asset_name) else None

    def click_nia_frame(self, asset_name):
        """
        Clicks the NIA frame if it is displayed.

        Args:
            asset_name (str): The name of the asset.

        Returns:
            bool: True if the frame is clicked, None otherwise.
        """
        self.nia_asset_name = self.perform_action_on_element(
            role_name='label', name=asset_name,
        )
        return self.do_click(self.nia_asset_name) if self.do_is_displayed(self.nia_asset_name) else None

    def get_backup_tooltip(self):
        """
        Retrieves the backup tooltip if it is displayed.
        """
        self.backup_frame().point()
        return self.backup_frame().description if self.do_is_displayed(self.backup_frame()) else None
