"""
Term and condition page objects module.
"""
from __future__ import annotations

import time

from accessible_constant import ACCEPT_BUTTON
from accessible_constant import DECLINE_BUTTON
from accessible_constant import TNC_TXT_DESCRIPTION
from e2e_tests.test.utilities.base_operation import BaseOperations


class TermAndConditionPageObjects(BaseOperations):
    """
    Term and condition page objects class.
    """

    def __init__(self, application):
        """
        Initializes the TermAndConditionPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        # Lazy evaluation of elements using lambdas
        self.accept_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ACCEPT_BUTTON,
        )
        self.decline_button = lambda: self.perform_action_on_element(
            role_name='push button', name=DECLINE_BUTTON,
        )
        self.title = lambda: self.perform_action_on_element(
            role_name='label', name='Terms and Conditions',
        )
        self.tnc_description = lambda: self.perform_action_on_element(
            role_name='label', name=TNC_TXT_DESCRIPTION,
        )

        self.tnc_scrollbar_list = lambda: list(self._get_scrollbars())

        self.tnc_scrollbar = lambda: (
            self.tnc_scrollbar_list()[1]
            if self.tnc_scrollbar_list() and len(self.tnc_scrollbar_list()) > 1
            else self.tnc_scrollbar_list()[0]
            if self.tnc_scrollbar_list()
            else None
        )

    def _get_scrollbars(self):
        """
        Get the scrollbars from the terms and conditions description.

        Returns:
            list: List of scrollbars.
        """
        desc = self.tnc_description()
        if not desc:
            return []
        children = desc.findChildren(
            lambda node: node.roleName == 'scroll bar',
        )
        return children or []

    def click_accept_button(self):
        """
        Clicks the accept button if it is displayed.

        Returns:
            The result of the click action or None if the button is not displayed.
        """
        return self.do_click(self.accept_button()) if self.do_is_displayed(self.accept_button()) else None

    def click_decline_button(self):
        """
        Clicks the decline button if it is displayed.

        Returns:
            The result of the click action or None if the button is not displayed.
        """
        return self.do_click(self.decline_button()) if self.do_is_displayed(self.decline_button()) else None

    def scroll_to_end(self):
        """
        Smoothly scrolls to the end of the terms and conditions page.
        """
        if self.tnc_scrollbar() and self.do_is_displayed(self.tnc_scrollbar()):
            scrollbar = self.tnc_scrollbar()
            while scrollbar.value < scrollbar.maxValue:
                scrollbar.value += 50  # Increment the value gradually
                # Pause for a short time to allow the scroll to happen smoothly
                time.sleep(0.01)
