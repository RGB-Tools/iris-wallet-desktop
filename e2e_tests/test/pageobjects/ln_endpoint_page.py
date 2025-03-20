"""
E2E tests for lightning network endpoint page objects.
"""
from __future__ import annotations

from accessible_constant import LN_ENDPOINT_CLOSE_BUTTON
from accessible_constant import LN_NODE_URL
from accessible_constant import PROCEED_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class LnEndpointPageObjects(BaseOperations):
    """
    Page objects for lightning network endpoint.
    """

    def __init__(self, application):
        """
        Initializes the LnEndpointPageObjects.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.ln_node_url = lambda: self.perform_action_on_element(
            role_name='text', name=LN_NODE_URL,
        )
        self.proceed_button = lambda: self.perform_action_on_element(
            role_name='push button', name=PROCEED_BUTTON,
        )
        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=LN_ENDPOINT_CLOSE_BUTTON,
        )

    def enter_ln_node_url(self, url):
        """
        Enters the lightning network node URL.

        Args:
            url (str): The URL to enter.

        Returns:
            None
        """
        if self.do_is_displayed(self.ln_node_url()):
            self.do_clear_text(self.ln_node_url())
            self.do_set_value(self.ln_node_url(), url)

    def click_proceed_button(self):
        """
        Clicks the proceed button.

        Returns:
            None
        """
        return self.do_click(self.proceed_button()) if self.do_is_displayed(self.proceed_button()) else None

    def click_close_button(self):
        """
        Clicks the close button.

        Returns:
            None
        """
        return self.do_click(self.close_button()) if self.do_is_displayed(self.close_button()) else None
