"""
Channel detail dialog page objects module.
"""
from __future__ import annotations

from dogtail.tree import root

from accessible_constant import CLOSE_CHANNEL_CONTINUE_BUTTON
from accessible_constant import CLOSE_CHANNEL_DIALOG
from e2e_tests.test.utilities.base_operation import BaseOperations


class CloseChannelDialogPageObjects(BaseOperations):
    """
    Channel detail dialog page objects class.
    """

    def __init__(self, application):
        """
        Initializes the ChannelDetailDialogPageObjects class.

        Args:
            application: The application instance.
        """
        super().__init__(application)

        self.close_channel_dialog = lambda: root.child(
            roleName='dialog', name=CLOSE_CHANNEL_DIALOG,
        )
        self.continue_button = lambda: self.close_channel_dialog().child(
            roleName='push button', name=CLOSE_CHANNEL_CONTINUE_BUTTON,
        )

    def click_close_channel_dialog(self):
        """
        Clicks the close channel dialog and returns the result of the click action.

        Returns:
            The result of the click action or None if the dialog is not displayed.
        """
        return self.do_click(self.close_channel_dialog()) if self.do_is_displayed(self.close_channel_dialog()) else None

    def click_continue_button(self):
        """
        Clicks the continue button and returns the result of the click action.

        Returns:
            The result of the click action or None if the button is not displayed.
        """
        return self.do_click(self.continue_button()) if self.do_is_displayed(self.continue_button()) else None
