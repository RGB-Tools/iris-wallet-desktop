"""
Success page objects Module.
"""
from __future__ import annotations

from accessible_constant import SUCCESS_PAGE_CLOSE_BUTTON
from accessible_constant import SUCCESS_PAGE_HOME_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class SuccessPageObjects(BaseOperations):
    """
    Success page objects class.
    """

    def __init__(self, application):
        """
        Initializes the success page objects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SUCCESS_PAGE_CLOSE_BUTTON,
        )
        self.home_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SUCCESS_PAGE_HOME_BUTTON,
        )

    def click_close_button(self):
        """
        Clicks the close button on the success page.

        Returns:
            bool: True if the button is clicked, None otherwise.
        """
        return self.do_click(self.close_button()) if self.do_is_displayed(self.close_button()) else None

    def click_home_button(self):
        """
        Clicks the home button on the success page.

        Returns:
            bool: True if the button is clicked, None otherwise.
        """
        return self.do_click(self.home_button()) if self.do_is_displayed(self.home_button()) else None
