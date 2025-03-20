"""
Channel management page objects module.
"""
from __future__ import annotations

from accessible_constant import CHANNEL_STATUS
from accessible_constant import CREATE_CHANNEL_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class ChannelManagementPageObjects(BaseOperations):
    """
    Channel management page objects class.
    """

    def __init__(self, application):
        """
        Initializes the ChannelManagementPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.asset_id = None

        self.create_channel_button = lambda: self.perform_action_on_element(
            role_name='push button', name=CREATE_CHANNEL_BUTTON,
        )
        self.channel_status = lambda: self.perform_action_on_element(
            role_name='image', name=CHANNEL_STATUS,
        )

    def click_create_channel_button(self):
        """
        Clicks the create channel button.

        Returns:
            The result of the click action if the button is displayed, otherwise None.
        """
        return self.do_click(self.create_channel_button()) if self.do_is_displayed(self.create_channel_button()) else None

    def click_channel_frame(self, asset_id):
        """
        Clicks the channel frame.

        Args:
            asset_id: The asset ID.

        Returns:
            The result of the click action if the frame is displayed, otherwise None.
        """
        self.asset_id = lambda: self.perform_action_on_element(
            role_name='label', name=asset_id,
        )
        return self.do_click(self.asset_id()) if self.do_is_displayed(self.asset_id()) else None

    def get_channel_status(self):
        """
        Clicks the channel status.

        Returns:
            The result of the click action if the status is displayed, otherwise None.
        """
        self.channel_status().grabFocus()
        return self.channel_status().description if self.do_is_displayed(self.channel_status()) else None
