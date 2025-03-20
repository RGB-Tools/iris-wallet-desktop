"""
This module contains the ToasterPageObjects class, which provides methods for interacting with toaster page elements.
"""
from __future__ import annotations

from accessible_constant import TOASTER_CLOSE_BUTTON
from accessible_constant import TOASTER_DESCRIPTION
from accessible_constant import TOASTER_FRAME
from accessible_constant import TOASTER_TITLE
from e2e_tests.test.utilities.base_operation import BaseOperations


class ToasterPageObjects(BaseOperations):
    """
    A class representing toaster page objects.

    Attributes:
        application (object): The application instance.
        toaster_frame (lambda): A lambda function to get the toaster frame element.
        toaster_title (lambda): A lambda function to get the toaster title element.
        toaster_description (lambda): A lambda function to get the toaster description element.
        toaster_close_button (lambda): A lambda function to get the toaster close button element.
    """

    def __init__(self, application):
        """
        Initializes the ToasterPageObjects instance.

        Args:
            application (object): The application instance.
        """
        super().__init__(application)

        self.toaster_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=TOASTER_FRAME,
        )
        self.toaster_title = lambda: self.perform_action_on_element(
            role_name='label', description=TOASTER_TITLE,
        )
        self.toaster_description = lambda: self.perform_action_on_element(
            role_name='label', description=TOASTER_DESCRIPTION,
        )
        self.toaster_close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=TOASTER_CLOSE_BUTTON,
        )

    def click_toaster_frame(self):
        """
        Clicks the toaster frame element if it is displayed.

        Returns:
            bool: True if the element is clicked, False otherwise.
        """
        return self.do_click(self.toaster_frame()) if self.do_is_displayed(self.toaster_frame()) else None

    def get_toaster_title(self):
        """
        Gets the text of the toaster title element if it is displayed.

        Returns:
            str: The text of the element if it is displayed, None otherwise.
        """
        return self.do_get_text(self.toaster_title()) if self.do_is_displayed(self.toaster_title()) else None

    def get_toaster_description(self):
        """
        Gets the text of the toaster description element if it is displayed.

        Returns:
            str: The text of the element if it is displayed, None otherwise.
        """
        return self.do_get_text(self.toaster_description()) if self.do_is_displayed(self.toaster_description()) else None

    def click_toaster_close_button(self):
        """
        Clicks the toaster close button element if it is displayed.

        Returns:
            bool: True if the element is clicked, False otherwise.
        """
        return self.do_click(self.toaster_close_button()) if self.do_is_displayed(self.toaster_close_button()) else None
