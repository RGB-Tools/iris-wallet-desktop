# pylint: disable=too-many-instance-attributes, too-many-public-methods
"""This module represents the page object for the settings page"""
from __future__ import annotations

from accessible_constant import ASK_AUTH_FOR_APP_LOGIN_TOGGLE
from accessible_constant import ASK_AUTH_FOR_IMPORTANT_QUESTION_TOGGLE
from accessible_constant import EXPIRY_TIME_COMBO_BOX
from accessible_constant import HIDE_EXHAUSTED_ASSETS_TOGGLE
from accessible_constant import INPUT_BOX_NAME
from accessible_constant import KEYRING_TOGGLE_BUTTON
from accessible_constant import SET_DEFAULT_EXP_TIME
from accessible_constant import SET_DEFAULT_FEE_RATE
from accessible_constant import SET_DEFAULT_MIN_EXPIRATION
from accessible_constant import SPECIFY_ANNOUNCE_ADD
from accessible_constant import SPECIFY_ANNOUNCE_ALIAS
from accessible_constant import SPECIFY_BITCOIND_HOST
from accessible_constant import SPECIFY_BITCOIND_PORT
from accessible_constant import SPECIFY_INDEXER_URL
from accessible_constant import SPECIFY_RGB_PROXY_URL
from e2e_tests.test.utilities.base_operation import BaseOperations


class SettingsPageObjects(BaseOperations):
    """Class for settings page objects"""

    def __init__(self, application):
        """Class for the settings page object"""

        super().__init__(application)

        # Settings frames
        self.keyring_toggle_button = lambda: self.perform_action_on_element(
            role_name='check box', name=KEYRING_TOGGLE_BUTTON,
        )
        self.login_auth_toggle_button = lambda: self.perform_action_on_element(
            role_name='check box', name=ASK_AUTH_FOR_APP_LOGIN_TOGGLE,
        )
        self.default_fee_rate_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=SET_DEFAULT_FEE_RATE,
        )
        self.default_exp_time_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=SET_DEFAULT_EXP_TIME,
        )
        self.set_min_confirmation_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=SET_DEFAULT_MIN_EXPIRATION,
        )
        self.specify_indexer_url_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=SPECIFY_INDEXER_URL,
        )
        self.specify_rgb_proxy_url_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=SPECIFY_RGB_PROXY_URL,
        )
        self.specify_bitcoind_host_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=SPECIFY_BITCOIND_HOST,
        )
        self.specify_bitcoind_port_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=SPECIFY_BITCOIND_PORT,
        )
        self.specify_announce_address_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=SPECIFY_ANNOUNCE_ADD,
        )
        self.specify_announce_alias_frame = lambda: self.perform_action_on_element(
            role_name='panel', name=SPECIFY_ANNOUNCE_ALIAS,
        )
        self.save_button = lambda: self.perform_action_on_element(
            role_name='push button', name='Save',
        )
        self.expiry_combo_box = lambda: self.perform_action_on_element(
            role_name='combo box', description=EXPIRY_TIME_COMBO_BOX,
        )
        self.hour_list_item = lambda: self.perform_action_on_element(
            role_name='list item', name='Hours',
        )
        self.minute_list_item = lambda: self.perform_action_on_element(
            role_name='list item', name='Minutes',
        )
        self.days_list_item = lambda: self.perform_action_on_element(
            role_name='list item', name='Days',
        )

        self.hide_exhausted_asset_toggle_button = lambda: self.perform_action_on_element(
            role_name='check box', name=HIDE_EXHAUSTED_ASSETS_TOGGLE,
        )

        self.ask_auth_for_imp_question_toggle = lambda: self.perform_action_on_element(
            role_name='check box', name=ASK_AUTH_FOR_IMPORTANT_QUESTION_TOGGLE,
        )

        # Input Boxes in Frames
        self.input_box = lambda: self.perform_action_on_element(
            role_name='text', name=INPUT_BOX_NAME,
        )

    def clear_input_box(self):
        """Clears the input box."""
        return self.do_clear_text(self.input_box()) if self.do_is_displayed(self.input_box()) else None

    def enter_input_value(self, value):
        """Enters a value in the input box."""
        return self.do_set_value(self.input_box(), value) if self.do_is_displayed(self.input_box()) else None

    def click_keyring_toggle_button(self):
        """Click on keyring toggle button"""
        return self.do_click(self.keyring_toggle_button()) if self.do_is_displayed(self.keyring_toggle_button()) else None

    def click_login_app_toggle_button(self):
        """Click on login app toggle button"""
        return self.do_click(self.login_auth_toggle_button()) if self.do_is_displayed(self.login_auth_toggle_button()) else None

    # Default Fee Rate
    def click_default_fee_rate_frame(self):
        """Click on the default fee rate frame"""
        return self.do_click(self.default_fee_rate_frame()) if self.do_is_displayed(self.default_fee_rate_frame()) else None

    # Default Expiry Time

    def click_default_exp_time_frame(self):
        """Click on the default expiry time frame"""
        return self.do_click(self.default_exp_time_frame()) if self.do_is_displayed(self.default_exp_time_frame()) else None

    # Minimum Confirmation

    def click_set_min_confirmation_frame(self):
        """Click on the set minimum confirmation frame"""
        return self.do_click(self.set_min_confirmation_frame()) if self.do_is_displayed(self.set_min_confirmation_frame()) else None

    # Indexer URL

    def click_set_indexer_url_frame(self):
        """Click on the indexer URL frame"""
        return self.do_click(self.specify_indexer_url_frame()) if self.do_is_displayed(self.specify_indexer_url_frame()) else None

    # RGB Proxy URL

    def click_set_rgb_proxy_url_frame(self):
        """Click on the RGB proxy URL frame"""
        return self.do_click(self.specify_rgb_proxy_url_frame()) if self.do_is_displayed(self.specify_rgb_proxy_url_frame()) else None

    # Bitcoind Host

    def click_specify_bitcoind_host_frame(self):
        """Click on the bitcoind host frame"""
        return self.do_click(self.specify_bitcoind_host_frame()) if self.do_is_displayed(self.specify_bitcoind_host_frame()) else None

    # Bitcoind Port

    def click_specify_bitcoind_port_frame(self):
        """Click on the bitcoind port frame"""
        return self.do_click(self.specify_bitcoind_port_frame()) if self.do_is_displayed(self.specify_bitcoind_port_frame()) else None

    # Announce Address

    def click_specify_announce_address_frame(self):
        """Click on the announce address frame"""
        return self.do_click(self.specify_announce_address_frame()) if self.do_is_displayed(self.specify_announce_address_frame()) else None

    # Announce Alias

    def click_specify_announce_alias(self):
        """Click on the announce alias frame"""
        return self.do_click(self.specify_announce_alias_frame()) if self.do_is_displayed(self.specify_announce_alias_frame()) else None

    # Combo box

    def click_on_combo_box(self):
        """Click on the expiry time combo box"""
        return self.do_click(self.expiry_combo_box()) if self.do_is_displayed(self.expiry_combo_box()) else None

    def click_on_hour(self):
        """Click on the hour option in the combo box"""
        return self.do_click(self.hour_list_item()) if self.do_is_displayed(self.hour_list_item()) else None

    def click_on_minute(self):
        """Click on the minute option in the combo box"""
        return self.do_click(self.minute_list_item()) if self.do_is_displayed(self.minute_list_item()) else None

    def click_on_days(self):
        """Click on the days option in the combo box"""
        return self.do_click(self.days_list_item()) if self.do_is_displayed(self.days_list_item()) else None

    # Save Button

    def click_save_button(self):
        """Click on the save button to save settings"""
        return self.do_click(self.save_button()) if self.do_is_displayed(self.save_button()) else None

    def click_hide_exhausted_asset_toggle_button(self):
        """Click on the Hide exhausted asset toggle button"""
        return self.do_click(self.hide_exhausted_asset_toggle_button()) if self.do_is_displayed(self.hide_exhausted_asset_toggle_button()) else None

    def click_ask_auth_imp_question(self):
        """Click on the ask auth imp question toggle button"""
        return self.do_click(self.ask_auth_for_imp_question_toggle()) if self.do_is_displayed(self.ask_auth_for_imp_question_toggle()) else None
