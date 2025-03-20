"""
Create channel page objects class for interacting with the create channel page.
"""
from __future__ import annotations

from accessible_constant import CHANNEL_ASSET_AMOUNT
from accessible_constant import CHANNEL_CAPACITY_SAT
from accessible_constant import CHANNEL_COMBOBOX
from accessible_constant import CHANNEL_NEXT_BUTTON
from accessible_constant import CHANNEL_PREV_BUTTON
from accessible_constant import CREATE_CHANNEL_CLOSE_BUTTON
from accessible_constant import CREATE_CHANNEL_ERROR_LABEL
from accessible_constant import NODE_URI_INPUT
from accessible_constant import PUSH_MSAT_VALUE
from e2e_tests.test.utilities.base_operation import BaseOperations


class CreateChannelPageObjects(BaseOperations):
    """
    Create channel page objects class for interacting with the create channel page.
    """

    def __init__(self, application):
        """
        Initialize the create channel Page Objects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.close_button = lambda: self.perform_action_on_element(
            role_name='push button', name=CREATE_CHANNEL_CLOSE_BUTTON,
        )
        self.node_uri_input = lambda: self.perform_action_on_element(
            role_name='text', name=NODE_URI_INPUT,
        )
        self.create_channel_error_label = lambda: self.perform_action_on_element(
            role_name='label', description=CREATE_CHANNEL_ERROR_LABEL,
        )
        self.channel_next_button = lambda: self.perform_action_on_element(
            role_name='push button', name=CHANNEL_NEXT_BUTTON,
        )
        self.channel_prev_button = lambda: self.perform_action_on_element(
            role_name='push button', name=CHANNEL_PREV_BUTTON,
        )
        self.channel_combobox = lambda: self.perform_action_on_element(
            role_name='combo box', description=CHANNEL_COMBOBOX,
        )
        self.channel_capacity_sat = lambda: self.perform_action_on_element(
            role_name='text', name=CHANNEL_CAPACITY_SAT,
        )
        self.channel_asset_amount = lambda: self.perform_action_on_element(
            role_name='text', name=CHANNEL_ASSET_AMOUNT,
        )
        self.push_msat_value = lambda: self.perform_action_on_element(
            role_name='text', name=PUSH_MSAT_VALUE,
        )

    def click_close_button(self):
        """
        Click the close button if it's displayed.

        Returns:
            None if the button is not displayed, otherwise the result of the click action.
        """
        return self.do_click(self.close_button()) if self.do_is_displayed(self.close_button()) else None

    def click_channel_next_button(self):
        """
        Click the channel next button if it's displayed.

        Returns:
            None if the button is not displayed, otherwise the result of the click action.
        """
        return self.do_click(self.channel_next_button()) if self.do_is_displayed(self.channel_next_button()) else None

    def click_channel_prev_button(self):
        """
        Click the channel prev button if it's displayed.

        Returns:
            None if the button is not displayed, otherwise the result of the click action.
        """
        return self.do_click(self.channel_prev_button()) if self.do_is_displayed(self.channel_prev_button()) else None

    def enter_node_uri_input(self, text):
        """
        Enter text into the node uri input if it's displayed.

        Args:
            text: The text to enter.

        Returns:
            None if the input is not displayed, otherwise the result of the set value action.
        """
        return self.do_set_value(self.node_uri_input(), text) if self.do_is_displayed(self.node_uri_input()) else None

    def get_create_channel_error_label_text(self):
        """
        Get the text of the create channel error label if it's displayed.

        Returns:
            None if the label is not displayed, otherwise the text of the label.
        """
        return self.do_get_text(self.create_channel_error_label()) if self.do_is_displayed(self.create_channel_error_label()) else None

    def click_channel_combobox(self):
        """
        Select the specified text in the channel combobox if it's displayed.

        Args:
            text: The text to select.

        Returns:
            None if the combobox is not displayed, otherwise the result of the click action.
        """
        return self.do_click(self.channel_combobox()) if self.do_is_displayed(self.channel_combobox()) else None

    def enter_channel_capacity_sat(self, text):
        """
        Enter text into the channel capacity sat if it's displayed.

        Args:
            text: The text to enter.

        Returns:
            None if the input is not displayed, otherwise the result of the set value action.
        """
        return self.do_set_value(self.channel_capacity_sat(), text) if self.do_is_displayed(self.channel_capacity_sat()) else None

    def enter_channel_asset_amount(self, text):
        """
        Enter text into the channel asset amount if it's displayed.

        Args:
            text: The text to enter.

        Returns:
            None if the input is not displayed, otherwise the result of the set value action.
        """
        return self.do_set_value(self.channel_asset_amount(), text) if self.do_is_displayed(self.channel_asset_amount()) else None

    def enter_push_msat_value(self, text):
        """
        Enter text into the push msat value if it's displayed.

        Args:
            text: The text to enter.

        Returns:
            None if the input is not displayed, otherwise the result of the set value action.
        """
        return self.do_set_value(self.push_msat_value(), text) if self.do_is_displayed(self.push_msat_value()) else None
