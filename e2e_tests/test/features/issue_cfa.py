"""
Module for testing CFA asset issuance.
"""
from __future__ import annotations

import os

from e2e_tests.test.pageobjects.main_page_objects import MainPageObjects
from e2e_tests.test.utilities.asset_copy import copy_cfa_image_to_home_directory
from e2e_tests.test.utilities.base_operation import BaseOperations


class IssueCfa(MainPageObjects, BaseOperations):
    """
    Class for testing CFA asset issuance.
    """

    def __init__(self, application):
        """
        Initialize the IssueCfa class.
        """
        super().__init__(application)

    def issue_cfa_with_sufficient_sats_and_utxo(self, application, asset_name, asset_description, asset_amount, is_native_auth_enabled: bool = False):
        """
        Issue CFA asset with sufficient sats and utxo.
        """
        self.do_focus_on_application(application)
        copy_cfa_image_to_home_directory(os.getcwd())

        if self.do_is_displayed(self.sidebar_page_objects.collectibles_button()):
            self.sidebar_page_objects.click_collectibles_button()

        if self.do_is_displayed(self.collectible_page_objects.issue_cfa_button()):
            self.collectible_page_objects.click_issue_cfa_button()

        if self.do_is_displayed(self.issue_cfa_page_objects.asset_name()):
            self.issue_cfa_page_objects.enter_asset_name(asset_name)

        if self.do_is_displayed(self.issue_cfa_page_objects.asset_description()):
            self.issue_cfa_page_objects.enter_asset_description(
                asset_description,
            )

        if self.do_is_displayed(self.issue_cfa_page_objects.asset_amount()):
            self.issue_cfa_page_objects.enter_asset_amount(asset_amount)

        if self.do_is_displayed(self.issue_cfa_page_objects.upload_file_button()):
            self.issue_cfa_page_objects.click_upload_file_button()

        if self.do_is_displayed(self.issue_cfa_page_objects.cfa_asset_media()):
            self.issue_cfa_page_objects.click_cfa_asset_media()

        if self.do_is_displayed(self.issue_cfa_page_objects.issue_cfa_button()):
            self.issue_cfa_page_objects.click_issue_cfa_button()

        if is_native_auth_enabled is True:
            self.enter_native_password()

        if self.do_is_displayed(self.success_page_objects.home_button()):
            self.success_page_objects.click_home_button()

    def issue_cfa_asset_without_sat(self, application, asset_name, asset_description, asset_amount):
        """
        Issue CFA asset without sat.
        """
        description = None
        self.do_focus_on_application(application)
        copy_cfa_image_to_home_directory(os.getcwd())

        if self.do_is_displayed(self.sidebar_page_objects.collectibles_button()):
            self.sidebar_page_objects.click_collectibles_button()

        if self.do_is_displayed(self.collectible_page_objects.issue_cfa_button()):
            self.collectible_page_objects.click_issue_cfa_button()

        if self.do_is_displayed(self.issue_cfa_page_objects.asset_name()):
            self.issue_cfa_page_objects.enter_asset_name(asset_name)

        if self.do_is_displayed(self.issue_cfa_page_objects.asset_description()):
            self.issue_cfa_page_objects.enter_asset_description(
                asset_description,
            )

        if self.do_is_displayed(self.issue_cfa_page_objects.asset_amount()):
            self.issue_cfa_page_objects.enter_asset_amount(asset_amount)

        if self.do_is_displayed(self.issue_cfa_page_objects.upload_file_button()):
            self.issue_cfa_page_objects.click_upload_file_button()

        if self.do_is_displayed(self.issue_cfa_page_objects.cfa_asset_media()):
            self.issue_cfa_page_objects.click_cfa_asset_media()

        if self.do_is_displayed(self.issue_cfa_page_objects.issue_cfa_button()):
            self.issue_cfa_page_objects.click_issue_cfa_button()

        if self.do_is_displayed(self.toaster_page_objects.toaster_frame()):
            self.toaster_page_objects.click_toaster_frame()

        if self.do_is_displayed(self.toaster_page_objects.toaster_description()):
            description = self.toaster_page_objects.get_toaster_description()

        if self.do_is_displayed(self.issue_cfa_page_objects.close_button()):
            self.issue_cfa_page_objects.click_close_button()

        if self.do_is_displayed(self.sidebar_page_objects.fungibles_button()):
            self.sidebar_page_objects.click_fungibles_button()

        return description

    def issue_cfa_with_sufficient_sats_and_no_utxo(self, application, asset_name, asset_description, asset_amount):
        """
        Issue CFA asset with sufficient sats and no utxo.
        """
        self.do_focus_on_application(application)
        copy_cfa_image_to_home_directory(os.getcwd())

        if self.do_is_displayed(self.sidebar_page_objects.view_unspents_button()):
            self.sidebar_page_objects.click_view_unspents_button()

        if self.do_is_displayed(self.sidebar_page_objects.collectibles_button()):
            self.sidebar_page_objects.click_collectibles_button()

        if self.do_is_displayed(self.collectible_page_objects.issue_cfa_button()):
            self.collectible_page_objects.click_issue_cfa_button()

        if self.do_is_displayed(self.issue_cfa_page_objects.asset_name()):
            self.issue_cfa_page_objects.enter_asset_name(asset_name)

        if self.do_is_displayed(self.issue_cfa_page_objects.asset_description()):
            self.issue_cfa_page_objects.enter_asset_description(
                asset_description,
            )

        if self.do_is_displayed(self.issue_cfa_page_objects.asset_amount()):
            self.issue_cfa_page_objects.enter_asset_amount(asset_amount)

        if self.do_is_displayed(self.issue_cfa_page_objects.upload_file_button()):
            self.issue_cfa_page_objects.click_upload_file_button()

        if self.do_is_displayed(self.issue_cfa_page_objects.cfa_asset_media()):
            self.issue_cfa_page_objects.click_cfa_asset_media()

        if self.do_is_displayed(self.issue_cfa_page_objects.issue_cfa_button()):
            self.issue_cfa_page_objects.click_issue_cfa_button()

        if self.do_is_displayed(self.success_page_objects.home_button()):
            self.success_page_objects.click_home_button()
