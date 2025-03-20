# pylint: disable=too-many-instance-attributes
"""This module represents the page object for the sidebar
Contains methods for interacting with the sidebar page elements."""
from __future__ import annotations

from accessible_constant import ABOUT_BUTTON
from accessible_constant import BACKUP_BUTTON
from accessible_constant import CHANNEL_MANAGEMENT_BUTTON
from accessible_constant import COLLECTIBLE_BUTTON
from accessible_constant import FAUCET_BUTTON
from accessible_constant import FUNGIBLE_BUTTON
from accessible_constant import HELP_BUTTON
from accessible_constant import SETTINGS_BUTTON
from accessible_constant import SIDEBAR_RECEIVE_ASSET_BUTTON
from accessible_constant import VIEW_UNSPENT_LIST_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class SidebarPageObjects(BaseOperations):
    """This class represents the page object for the sidebar"""

    def __init__(self, application):
        """Class for the sidebar page object."""
        super().__init__(application)

        self.fungibles_button = lambda: self.perform_action_on_element(
            role_name='radio button', name=FUNGIBLE_BUTTON,
        )
        self.collectibles_button = lambda: self.perform_action_on_element(
            role_name='radio button', name=COLLECTIBLE_BUTTON,
        )
        self.channel_management_button = lambda: self.perform_action_on_element(
            role_name='radio button', name=CHANNEL_MANAGEMENT_BUTTON,
        )
        self.view_unspents_button = lambda: self.perform_action_on_element(
            role_name='radio button', name=VIEW_UNSPENT_LIST_BUTTON,
        )
        self.faucet_button = lambda: self.perform_action_on_element(
            role_name='push button', name=FAUCET_BUTTON,
        )
        self.backup_button = lambda: self.perform_action_on_element(
            role_name='push button', name=BACKUP_BUTTON,
        )
        self.settings_button = lambda: self.perform_action_on_element(
            role_name='radio button', name=SETTINGS_BUTTON,
        )
        self.help_button = lambda: self.perform_action_on_element(
            role_name='radio button', name=HELP_BUTTON,
        )
        self.about_button = lambda: self.perform_action_on_element(
            role_name='radio button', name=ABOUT_BUTTON,
        )
        self.receive_asset_button = lambda: self.perform_action_on_element(
            role_name='push button', name=SIDEBAR_RECEIVE_ASSET_BUTTON,
        )

    def click_fungibles_button(self):
        """Clicks the fungibles button if it is displayed."""
        return self.do_click(self.fungibles_button()) if self.do_is_displayed(self.fungibles_button()) else None

    def click_collectibles_button(self):
        """Clicks the collectibles button if it is displayed."""
        return self.do_click(self.collectibles_button()) if self.do_is_displayed(self.collectibles_button()) else None

    def click_channel_management_button(self):
        """Clicks the channel management button if it is displayed."""
        return self.do_click(self.channel_management_button()) if self.do_is_displayed(self.channel_management_button()) else None

    def click_view_unspents_button(self):
        """Clicks the view unspents button if it is displayed."""
        return self.do_click(self.view_unspents_button()) if self.do_is_displayed(self.view_unspents_button()) else None

    def click_faucet_button(self):
        """Clicks the faucet button if it is displayed."""
        return self.do_click(self.faucet_button()) if self.do_is_displayed(self.faucet_button()) else None

    def click_backup_button(self):
        """Clicks the backup button if it is displayed."""
        return self.do_click(self.backup_button()) if self.do_is_displayed(self.backup_button()) else None

    def click_settings_button(self):
        """Clicks the settings button if it is displayed."""
        return self.do_click(self.settings_button()) if self.do_is_displayed(self.settings_button()) else None

    def click_help_button(self):
        """Clicks the help button if it is displayed."""
        return self.do_click(self.help_button()) if self.do_is_displayed(self.help_button()) else None

    def click_about_button(self):
        """Clicks the about button if it is displayed."""
        return self.do_click(self.about_button()) if self.do_is_displayed(self.about_button()) else None

    def click_receive_asset_button(self):
        """Clicks the receive asset button if it is displayed."""
        return self.do_click(self.receive_asset_button()) if self.do_is_displayed(self.receive_asset_button()) else None
