"""
Channel detail dialog page objects.
"""
from __future__ import annotations

from dogtail.tree import root

from accessible_constant import BTC_LOCAL_VALUE_LABEL
from accessible_constant import BTC_REMOTE_VALUE_LABEL
from accessible_constant import CHANNEL_DETAIL_CLOSE_BUTTON
from accessible_constant import CHANNEL_DETAIL_DIALOG
from accessible_constant import CHANNEL_PEER_PUBKEY_COPY_BUTTON
from accessible_constant import CLOSE_CHANNEL_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class ChannelDetailDialogPageObjects(BaseOperations):
    """
    channel detail dialog page objects class.
    """

    def __init__(self, application):
        """
        Initializes the ChannelDetailDialogPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.channel_detail_dialog = lambda: root.child(
            roleName='dialog', name=CHANNEL_DETAIL_DIALOG,
        )
        self.copy_button = lambda: self.channel_detail_dialog().child(
            roleName='push button', name=CHANNEL_PEER_PUBKEY_COPY_BUTTON,
        )
        self.close_channel_button = lambda: self.channel_detail_dialog().child(
            roleName='push button', name=CLOSE_CHANNEL_BUTTON,
        )
        self.channel_detail_close_button = lambda: self.channel_detail_dialog().child(
            roleName='push button', name=CHANNEL_DETAIL_CLOSE_BUTTON,
        )
        self.btc_local_value = lambda: self.channel_detail_dialog().child(
            roleName='label', description=BTC_LOCAL_VALUE_LABEL,
        )
        self.btc_remote_value = lambda: self.channel_detail_dialog().child(
            roleName='label', description=BTC_REMOTE_VALUE_LABEL,
        )

    def click_channel_detail_dialog(self):
        """
        Clicks the channel detail dialog.

        Returns:
            The result of the click action or None if the dialog is not displayed.
        """
        return self.do_click(self.channel_detail_dialog()) if self.do_is_displayed(self.channel_detail_dialog()) else None

    def click_copy_button(self):
        """
        Clicks the copy button.

        Returns:
            The result of the click action or None if the button is not displayed.
        """
        if self.do_is_displayed(self.copy_button()):
            return self.copy_button().click()
        return None

    def click_close_channel_button(self):
        """
        Clicks the close channel button.

        Returns:
            The result of the click action or None if the button is not displayed.
        """
        return self.do_click(self.close_channel_button()) if self.do_is_displayed(self.close_channel_button()) else None

    def click_channel_detail_close_button(self):
        """
        Clicks the channel detail close button.

        Returns:
            The result of the click action or None if the button is not displayed.
        """
        return self.do_click(self.channel_detail_close_button()) if self.do_is_displayed(self.channel_detail_close_button()) else None

    def get_btc_local_value(self):
        """
        Gets the local value of the channel.
        """
        self.do_click(self.btc_local_value())
        return self.do_get_text(self.btc_local_value()) if self.do_is_displayed(self.btc_local_value()) else None

    def get_btc_remote_value(self):
        """
        Gets the remote value of the channel.
        """
        self.do_click(self.btc_remote_value())
        return self.do_get_text(self.btc_remote_value()) if self.do_is_displayed(self.btc_remote_value()) else None
