"""
Collectible page objects class for handling page elements and actions.
"""
from __future__ import annotations

from accessible_constant import ISSUE_CFA_ASSET
from e2e_tests.test.utilities.base_operation import BaseOperations


class CollectiblePageObjects(BaseOperations):
    """Collectible page objects class."""

    def __init__(self, application):
        """
        Initialize CollectiblePageObjects with application.
        """
        super().__init__(application)

        self.cfa_asset_name = None
        # Define elements using lambdas for lazy evaluation
        self.issue_cfa_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ISSUE_CFA_ASSET,
        )

    def click_issue_cfa_button(self):
        """
        Click the issue CFA button if it's displayed.
        """
        return self.do_click(self.issue_cfa_button()) if self.do_is_displayed(self.issue_cfa_button()) else None

    def get_cfa_asset_name(self, asset_name):
        """
        Get the asset name if it's displayed.
        """
        self.cfa_asset_name = self.perform_action_on_element(
            role_name='label', name=asset_name,
        )
        return self.do_get_text(self.cfa_asset_name) if self.do_is_displayed(self.cfa_asset_name) else None

    def click_cfa_frame(self, asset_name):
        """
        Click the CFA frame if it's displayed.
        """
        self.cfa_asset_name = self.perform_action_on_element(
            role_name='label', name=asset_name,
        )
        return self.do_click(self.cfa_asset_name) if self.do_is_displayed(self.cfa_asset_name) else None
