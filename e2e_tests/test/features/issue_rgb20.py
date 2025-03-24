"""
This module contains the IssueRgb20 class, which provides methods for issuing RGB20 assets.
"""
from __future__ import annotations

from e2e_tests.test.pageobjects.main_page_objects import MainPageObjects
from e2e_tests.test.utilities.base_operation import BaseOperations


class IssueRgb20(MainPageObjects, BaseOperations):
    """
    This class provides methods for issuing RGB20 assets.
    """

    def __init__(self, application):
        """
        Initializes the IssueRgb20 class.
        """
        super().__init__(application)

    def issue_rgb20_with_sufficient_sats_and_no_utxo(self, application, asset_ticker, asset_name, asset_amount):
        """
        Issues an RGB20 asset with sufficient sats and no UTXO.
        """
        self.do_focus_on_application(application)

        if self.do_is_displayed(self.sidebar_page_objects.fungibles_button()):
            self.sidebar_page_objects.click_fungibles_button()

        if self.do_is_displayed(self.fungible_page_objects.issue_rgb20_button()):
            self.fungible_page_objects.click_issue_rgb20_button()

        if self.do_is_displayed(self.issue_rgb20_page_objects.asset_ticker()):
            self.issue_rgb20_page_objects.enter_asset_ticker(asset_ticker)

        if self.do_is_displayed(self.issue_rgb20_page_objects.asset_name()):
            self.issue_rgb20_page_objects.enter_asset_name(asset_name)

        if self.do_is_displayed(self.issue_rgb20_page_objects.asset_amount()):
            self.issue_rgb20_page_objects.enter_asset_amount(asset_amount)

        if self.do_is_displayed(self.issue_rgb20_page_objects.issue_rgb20_button()):
            self.issue_rgb20_page_objects.click_issue_rgb20_button()

        if self.do_is_displayed(self.success_page_objects.home_button()):
            self.success_page_objects.click_home_button()

    def issue_rgb20_asset_without_sat(self, application, asset_ticker, asset_name, asset_amount):
        """
        Issues an RGB20 asset without sufficient sats.
        """
        description = None
        self.do_focus_on_application(application)
        if self.do_is_displayed(self.fungible_page_objects.issue_rgb20_button()):
            self.fungible_page_objects.click_issue_rgb20_button()

        if self.do_is_displayed(self.issue_rgb20_page_objects.asset_ticker()):
            self.issue_rgb20_page_objects.enter_asset_ticker(asset_ticker)

        if self.do_is_displayed(self.issue_rgb20_page_objects.asset_name()):
            self.issue_rgb20_page_objects.enter_asset_name(asset_name)

        if self.do_is_displayed(self.issue_rgb20_page_objects.asset_amount()):
            self.issue_rgb20_page_objects.enter_asset_amount(asset_amount)

        if self.do_is_displayed(self.issue_rgb20_page_objects.issue_rgb20_button()):
            self.issue_rgb20_page_objects.click_issue_rgb20_button()

        if self.do_is_displayed(self.toaster_page_objects.toaster_frame()):
            self.toaster_page_objects.click_toaster_frame()

        if self.do_is_displayed(self.toaster_page_objects.toaster_description()):
            description = self.toaster_page_objects.get_toaster_description()

        if self.do_is_displayed(self.issue_rgb20_page_objects.close_button()):
            self.issue_rgb20_page_objects.click_close_button()

        return description

    def issue_rgb20_with_sufficient_sats_and_utxo(self, application, asset_ticker, asset_name, asset_amount, is_native_auth_enabled: bool = False):
        """
        Issues an RGB20 asset with sufficient sats and UTXO.
        """
        self.do_focus_on_application(application)
        if self.do_is_displayed(self.fungible_page_objects.issue_rgb20_button()):
            self.fungible_page_objects.click_issue_rgb20_button()

        if self.do_is_displayed(self.issue_rgb20_page_objects.asset_ticker()):
            self.issue_rgb20_page_objects.enter_asset_ticker(asset_ticker)

        if self.do_is_displayed(self.issue_rgb20_page_objects.asset_name()):
            self.issue_rgb20_page_objects.enter_asset_name(asset_name)

        if self.do_is_displayed(self.issue_rgb20_page_objects.asset_amount()):
            self.issue_rgb20_page_objects.enter_asset_amount(asset_amount)

        if self.do_is_displayed(self.issue_rgb20_page_objects.issue_rgb20_button()):
            self.issue_rgb20_page_objects.click_issue_rgb20_button()

        if is_native_auth_enabled is True:
            self.enter_native_password()

        if self.do_is_displayed(self.success_page_objects.home_button()):
            self.success_page_objects.click_home_button()
