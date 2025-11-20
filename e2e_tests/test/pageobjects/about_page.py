# pylint: disable=too-many-instance-attributes
"""This module contains the page object for about page"""
from __future__ import annotations

from dogtail.rawinput import keyCombo
from dogtail.tree import root

from accessible_constant import ANNOUNCE_ADDRESS_ACCESSIBLE_DESCRIPTION
from accessible_constant import ANNOUNCE_ADDRESS_COPY_BUTTON
from accessible_constant import ANNOUNCE_ALIAS_ACCESSIBLE_DESCRIPTION
from accessible_constant import ANNOUNCE_ALIAS_COPY_BUTTON
from accessible_constant import BITCOIND_HOST_ACCESSIBLE_DESCRIPTION
from accessible_constant import BITCOIND_HOST_COPY_BUTTON
from accessible_constant import BITCOIND_PORT_ACCESSIBLE_DESCRIPTION
from accessible_constant import BITCOIND_PORT_COPY_BUTTON
from accessible_constant import DOWNLOAD_DEBUG_LOG
from accessible_constant import FILE_CHOOSER
from accessible_constant import INDEXER_URL_ACCESSIBLE_DESCRIPTION
from accessible_constant import INDEXER_URL_COPY_BUTTON
from accessible_constant import LN_PEER_LISTENING_PORT_ACCESSIBLE_DESCRIPTION
from accessible_constant import LN_PEER_LISTENING_PORT_COPY_BUTTON
from accessible_constant import NODE_PUBKEY_ACCESSIBLE_DESCRIPTION
from accessible_constant import NODE_PUBKEY_COPY_BUTTON
from accessible_constant import RGB_PROXY_URL_ACCESSIBLE_DESCRIPTION
from accessible_constant import RGB_PROXY_URL_COPY_BUTTON
from e2e_tests.test.utilities.base_operation import BaseOperations


class AboutPageObjects(BaseOperations):
    """Class for about page object"""

    def __init__(self, application):
        super().__init__(application)

        self.announce_address_label = lambda: self.perform_action_on_element(
            role_name='label', description=ANNOUNCE_ADDRESS_ACCESSIBLE_DESCRIPTION,
        )
        self.announce_alias_label = lambda: self.perform_action_on_element(
            role_name='label', description=ANNOUNCE_ALIAS_ACCESSIBLE_DESCRIPTION,
        )
        self.indexer_url_label = lambda: self.perform_action_on_element(
            role_name='label', description=INDEXER_URL_ACCESSIBLE_DESCRIPTION,
        )
        self.rgb_proxy_url = lambda: self.perform_action_on_element(
            role_name='label', description=RGB_PROXY_URL_ACCESSIBLE_DESCRIPTION,
        )
        self.node_pubkey = lambda: self.perform_action_on_element(
            role_name='label', description=NODE_PUBKEY_ACCESSIBLE_DESCRIPTION,
        )
        self.peer_listening_port = lambda: self.perform_action_on_element(
            role_name='label', description=LN_PEER_LISTENING_PORT_ACCESSIBLE_DESCRIPTION,
        )
        self.bitcoind_host = lambda: self.perform_action_on_element(
            role_name='label', description=BITCOIND_HOST_ACCESSIBLE_DESCRIPTION,
        )
        self.bitcoind_port = lambda: self.perform_action_on_element(
            role_name='label', description=BITCOIND_PORT_ACCESSIBLE_DESCRIPTION,
        )
        self.node_pubkey_copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=NODE_PUBKEY_COPY_BUTTON,
        )
        self.ln_peer_listening_port_copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=LN_PEER_LISTENING_PORT_COPY_BUTTON,
        )
        self.bitcoind_host_copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=BITCOIND_HOST_COPY_BUTTON,
        )
        self.bitcoind_port_copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=BITCOIND_PORT_COPY_BUTTON,
        )
        self.indexer_url_copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=INDEXER_URL_COPY_BUTTON,
        )
        self.rgb_proxy_url_copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=RGB_PROXY_URL_COPY_BUTTON,
        )
        self.announce_address_copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ANNOUNCE_ADDRESS_COPY_BUTTON,
        )
        self.announce_alias_copy_button = lambda: self.perform_action_on_element(
            role_name='push button', name=ANNOUNCE_ALIAS_COPY_BUTTON,
        )
        self.download_debug_log = lambda: self.perform_action_on_element(
            role_name='push button', name=DOWNLOAD_DEBUG_LOG,
        )
        self.file_explorer = lambda: root.child(
            roleName=FILE_CHOOSER,
        )

    def _click_button_element(self, copy_button):
        """Helper method to click a button element."""
        if self.do_is_displayed(copy_button):
            return copy_button.click()
        return False

    def get_node_pubkey(self):
        """Returns node pubkey"""
        return self.do_get_text(self.node_pubkey()) if self.do_is_displayed(self.node_pubkey()) else None

    def get_peer_listening_port(self):
        """Returns peer listening port"""
        return self.do_get_text(self.peer_listening_port()) if self.do_is_displayed(self.peer_listening_port()) else None

    def get_bitcoind_host(self):
        """Returns bitcoind host"""
        return self.do_get_text(self.bitcoind_host()) if self.do_is_displayed(self.bitcoind_host()) else None

    def get_bitcoind_port(self):
        """Returns bitcoind port"""
        return self.do_get_text(self.bitcoind_port()) if self.do_is_displayed(self.bitcoind_port()) else None

    def get_announce_address(self):
        """Returns the announce address"""
        return self.do_get_text(self.announce_address_label()) if self.do_is_displayed(self.announce_address_label()) else None

    def get_announce_alias(self):
        """Returns the announce alias"""
        return self.do_get_text(self.announce_alias_label()) if self.do_is_displayed(self.announce_alias_label()) else None

    def get_indexer_url(self):
        """Returns the indexer url"""
        return self.do_get_text(self.indexer_url_label()) if self.do_is_displayed(self.indexer_url_label()) else None

    def get_rgb_proxy_url(self):
        """Returns the rgb proxy url"""
        return self.do_get_text(self.rgb_proxy_url()) if self.do_is_displayed(self.rgb_proxy_url()) else None

    def click_node_pubkey_button(self):
        """Clicks the node pubkey copy button"""
        return self._click_button_element(self.node_pubkey_copy_button())

    def click_ln_peer_listening_port_copy_button(self):
        """Clicks the ln peer listening port copy button"""
        return self._click_button_element(self.ln_peer_listening_port_copy_button())

    def click_bitcoind_host_copy_button(self):
        """Clicks on the bitcoind host copy button"""
        return self._click_button_element(self.bitcoind_host_copy_button())

    def click_bitcoind_port_copy_button(self):
        """Clicks on the bitcoind port copy button"""
        return self._click_button_element(self.bitcoind_port_copy_button())

    def click_announce_address_copy_button(self):
        """Clicks on Announce address copy button"""
        return self._click_button_element(self.announce_address_copy_button())

    def click_announce_alias_copy_button(self):
        """Clicks on Announce alias copy button"""
        return self._click_button_element(self.announce_alias_copy_button())

    def click_indexer_url_copy_button(self):
        """Clicks on Indexer url copy button"""
        return self._click_button_element(self.indexer_url_copy_button())

    def click_rgb_proxy_url_copy_button(self):
        """Clicks on RGB proxy url copy button"""
        return self._click_button_element(self.rgb_proxy_url_copy_button())

    def click_download_debug_log(self):
        """Clicks on the download debug log button"""
        return self.do_click(self.download_debug_log()) if self.do_is_displayed(self.download_debug_log()) else None

    def press_enter(self):
        """Presses the enter key"""
        if self.do_is_displayed(self.file_explorer()):
            self.file_explorer().grabFocus()
            keyCombo('enter')
            return True
        return False

    def copying_logs_filename(self):
        """Returns the filename of the copying logs"""
        if self.do_is_displayed(self.file_explorer()):
            self.file_explorer().grabFocus()
            keyCombo('<Control>c')

            return self.do_get_copied_address()

        return None
