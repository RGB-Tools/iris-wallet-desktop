"""
Welcome page objects module.
"""
from __future__ import annotations

from accessible_constant import CREATE_BUTTON
from accessible_constant import RESTORE_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class WelcomePageObjects(BaseOperations):
    """
    Welcome page objects class.
    """

    def __init__(self, application):
        """
        Initialize welcome page objects.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        # Lazy evaluation of elements using lambdas
        self.create_button = lambda: self.perform_action_on_element(
            role_name='push button', name=CREATE_BUTTON,
        )
        self.restore_button = lambda: self.perform_action_on_element(
            role_name='push button', name=RESTORE_BUTTON,
        )

    def click_create_button(self):
        """
        Click the create button.

        Returns:
            The result of the click action if the button is displayed, otherwise None.
        """
        return self.do_click(self.create_button()) if self.do_is_displayed(self.create_button()) else None

    def click_restore_button(self):
        """
        Click the restore button.

        Returns:
            The result of the click action if the button is displayed, otherwise None.
        """
        return self.do_click(self.restore_button()) if self.do_is_displayed(self.restore_button()) else None
