"""
E2E tests for unspent list page objects.
"""
from __future__ import annotations

from accessible_constant import UNSPENT_CLICKABLE_FRAME
from accessible_constant import UNSPENT_UTXO_OUTPOINT
from accessible_constant import UNSPENT_WIDGET
from e2e_tests.test.utilities.base_operation import BaseOperations


class ViewUnspentListPageObjects(BaseOperations):
    """
    Page objects for the unspent list page.
    """

    def __init__(self, application):
        """
        Initializes the page objects.

        Args:
            application: The application instance.
        """
        self.unspent_utxo_asset_id = None
        super().__init__(application)

        self.unspent_widget = lambda: self.perform_action_on_element(
            role_name='filler', name=UNSPENT_WIDGET,
        )
        self.unspent_frame = lambda: self.get_first_element(
            role_name='panel', name=UNSPENT_CLICKABLE_FRAME,
        )
        self.unspent_utxo_outpoint = lambda: self.get_first_element(
            role_name='label', description=UNSPENT_UTXO_OUTPOINT,
        )

    def click_unspent_frame(self):
        """
        Clicks the unspent frame.

        Returns:
            The result of the click action or None if the element is not displayed.
        """
        return self.do_click(self.unspent_frame()) if self.do_is_displayed(self.unspent_frame()) else None

    def get_unspent_utxo_asset_id(self, asset_id):
        """
        Gets the unspent UTXO asset ID.

        Returns:
            The text of the element or None if the element is not displayed.
        """
        self.unspent_utxo_asset_id = lambda: self.perform_action_on_element(
            role_name='label', name=asset_id,
        )

        return self.do_get_text(self.unspent_utxo_asset_id()) if self.do_is_displayed(self.unspent_utxo_asset_id()) else None

    def get_unspent_utxo_outpoint(self):
        """
        Gets the unspent UTXO outpoint.

        Returns:
            The text of the element or None if the element is not displayed.
        """
        return self.do_get_text(self.unspent_utxo_outpoint()) if self.do_is_displayed(self.unspent_utxo_outpoint()) else None

    def get_unspent_widget(self):
        """
        Gets the number of children in the unspent widget.

        Returns:
            The number of children in the element or None if the element is not displayed.
        """
        return len(self.unspent_widget()) if self.do_is_displayed(self.unspent_widget()) else None
