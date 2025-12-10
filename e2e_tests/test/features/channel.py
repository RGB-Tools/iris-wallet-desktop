# pylint:disable=too-many-branches
"""
This module contains the Channel class, which provides methods for channel operations.
"""
from __future__ import annotations

from dogtail.rawinput import keyCombo
from dogtail.rawinput import typeText

from e2e_tests.test.pageobjects.main_page_objects import MainPageObjects
from e2e_tests.test.utilities.base_operation import BaseOperations
from e2e_tests.test.utilities.executable_shell_script import mine


class Channel(MainPageObjects, BaseOperations):
    """This class represents the channel feature"""

    def __init__(self, application):
        super().__init__(application)

    def create_channel(self, application, node_uri, asset_ticker, channel_capacity, asset_amount=None):
        """
        This method creates a new channel with the given name.
        """
        channel_status = None
        self.do_focus_on_application(application)
        if self.do_is_displayed(self.sidebar_page_objects.channel_management_button()):
            self.sidebar_page_objects.click_channel_management_button()

        if self.do_is_displayed(self.channel_management_page_objects.create_channel_button()):
            self.channel_management_page_objects.click_create_channel_button()

        if self.do_is_displayed(self.create_channel_page_objects.node_uri_input()):
            self.create_channel_page_objects.enter_node_uri_input(node_uri)

        if self.do_is_displayed(self.create_channel_page_objects.channel_next_button()):
            self.create_channel_page_objects.click_channel_next_button()

        if self.do_is_displayed(self.create_channel_page_objects.channel_combobox()):
            self.create_channel_page_objects.click_channel_combobox()
            typeText(asset_ticker)
            keyCombo('enter')
        if asset_amount is not None:
            if self.do_is_displayed(self.create_channel_page_objects.channel_asset_amount()):
                self.create_channel_page_objects.enter_channel_asset_amount(
                    asset_amount,
                )

        if self.do_is_displayed(self.create_channel_page_objects.channel_capacity_sat()):
            self.create_channel_page_objects.enter_channel_capacity_sat(
                channel_capacity,
            )

        if self.do_is_displayed(self.create_channel_page_objects.channel_next_button()):
            self.create_channel_page_objects.click_channel_next_button()

        if self.do_is_displayed(self.success_page_objects.home_button()):
            self.success_page_objects.click_home_button()

        if self.do_is_displayed(self.channel_management_page_objects.refresh_button()):
            self.channel_management_page_objects.click_refresh_button()

        mine(12)

        if self.do_is_displayed(self.channel_management_page_objects.refresh_button()):
            self.channel_management_page_objects.click_refresh_button()

        if self.do_is_displayed(self.channel_management_page_objects.refresh_button()):
            self.channel_management_page_objects.click_refresh_button()

        if self.do_is_displayed(self.channel_management_page_objects.channel_status()):
            channel_status = self.channel_management_page_objects.get_channel_status()

        if self.do_is_displayed(self.sidebar_page_objects.fungibles_button()):
            self.sidebar_page_objects.click_fungibles_button()

        return channel_status

    def create_channel_with_wrong_node_uri(self, application, node_uri):
        """Create a channel with wrong node uri"""
        error_label = None
        self.do_focus_on_application(application)
        if self.do_is_displayed(self.sidebar_page_objects.channel_management_button()):
            self.sidebar_page_objects.click_channel_management_button()

        if self.do_is_displayed(self.channel_management_page_objects.create_channel_button()):
            self.channel_management_page_objects.click_create_channel_button()

        if self.do_is_displayed(self.create_channel_page_objects.node_uri_input()):
            self.create_channel_page_objects.enter_node_uri_input(node_uri)

        if self.do_is_displayed(self.create_channel_page_objects.create_channel_error_label()):
            error_label = self.create_channel_page_objects.get_create_channel_error_label_text()

        if self.do_is_displayed(self.create_channel_page_objects.close_button()):
            self.create_channel_page_objects.click_close_button()

        if self.do_is_displayed(self.sidebar_page_objects.fungibles_button()):
            self.sidebar_page_objects.click_fungibles_button()

        return error_label

    def close_channel(self, application, asset_id):
        """Close the channel"""
        description = None
        self.do_focus_on_application(application)

        if self.do_is_displayed(self.sidebar_page_objects.channel_management_button()):
            self.sidebar_page_objects.click_channel_management_button()

        if self.do_is_displayed(self.channel_management_page_objects.channel_status()):
            self.channel_management_page_objects.click_channel_frame(asset_id)

        if self.do_is_displayed(self.channel_detail_dialog_page_objects.close_channel_button()):
            self.channel_detail_dialog_page_objects.click_close_channel_button()

        if self.do_is_displayed(self.close_channel_detail_dialog_page_objects.continue_button()):
            self.close_channel_detail_dialog_page_objects.click_continue_button()

        if self.do_is_displayed(self.toaster_page_objects.toaster_frame()):
            self.toaster_page_objects.click_toaster_frame()

        if self.do_is_displayed(self.toaster_page_objects.toaster_description()):
            description = self.toaster_page_objects.get_toaster_description()

        if self.do_is_displayed(self.sidebar_page_objects.fungibles_button()):
            self.sidebar_page_objects.click_fungibles_button()

        return description

    def get_node_uri_for_embedded(self, application, ip_address):
        """Get the node URI for embedded"""
        node_pubkey, ln_port, embedded_node_uri = None, None, None
        self.do_focus_on_application(application)

        if self.do_is_displayed(self.sidebar_page_objects.about_button()):
            self.sidebar_page_objects.click_about_button()

        if self.do_is_displayed(self.about_page_objects.node_pubkey_copy_button()):
            self.about_page_objects.click_node_pubkey_button()
            node_pubkey = self.about_page_objects.do_get_copied_address()

        if self.do_is_displayed(self.about_page_objects.ln_peer_listening_port_copy_button()):
            self.about_page_objects.click_ln_peer_listening_port_copy_button()
            ln_port = self.about_page_objects.do_get_copied_address()

        if self.do_is_displayed(self.sidebar_page_objects.fungibles_button()):
            self.sidebar_page_objects.click_fungibles_button()

        embedded_node_uri = f'{node_pubkey}@{ip_address}:{ln_port}'

        return embedded_node_uri

    def get_node_uri_for_remote(self, application, ip_address, ln_port):
        """Get the node URI for remote"""
        node_pubkey, remote_node_uri = None, None
        self.do_focus_on_application(application)

        if self.do_is_displayed(self.sidebar_page_objects.about_button()):
            self.sidebar_page_objects.click_about_button()

        if self.do_is_displayed(self.about_page_objects.node_pubkey_copy_button()):
            self.about_page_objects.click_node_pubkey_button()
            node_pubkey = self.about_page_objects.do_get_copied_address()

        if self.do_is_displayed(self.sidebar_page_objects.fungibles_button()):
            self.sidebar_page_objects.click_fungibles_button()

        remote_node_uri = f'{node_pubkey}@{ip_address}:{ln_port}'

        return remote_node_uri
