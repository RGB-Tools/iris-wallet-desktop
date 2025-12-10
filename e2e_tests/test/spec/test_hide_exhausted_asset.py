# pylint: disable=redefined-outer-name, unused-import
"""Test module for hiding exhausted asset"""
from __future__ import annotations

import allure

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from accessible_constant import SECOND_APPLICATION
from accessible_constant import SECOND_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.model import WalletTestSetup

ASSET_TICKER = 'TTK'
ASSET_NAME = 'Tether'
ASSET_AMOUNT = '2000'
ISSUE_NIA_TOASTER_MESSAGE = 'You have insufficient funds'


@allure.feature('Hide exhausted asset')
@allure.story('Toggling on hide exhausted asset')
def test_hide_exhausted_asset_on(wallets_and_operations: WalletTestSetup):
    """Test for hiding exhausted asset"""
    with allure.step('Initializing the wallets and funding them'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations, FIRST_APPLICATION, FIRST_APPLICATION_URL,
        )

        wallets_and_operations.second_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations, SECOND_APPLICATION, SECOND_APPLICATION_URL,
        )

    with allure.step('Navigating to settings page'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_hide_exhausted_asset_toggle_button()

    with allure.step('Issuing a asset'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            FIRST_APPLICATION, ASSET_TICKER, ASSET_NAME, ASSET_AMOUNT,
        )

    with allure.step('Generating a RGB invoice'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        invoice = wallets_and_operations.second_page_features.receive_features.receive_asset_from_sidebar(
            SECOND_APPLICATION,
        )

    with allure.step('Send asset to the second page'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            ASSET_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.first_page_features.send_features.send(
            FIRST_APPLICATION, invoice, ASSET_AMOUNT,
        )

        child_count = wallets_and_operations.first_page_objects.fungible_page_objects.get_child_count()

        assert len(child_count) == 3


@allure.feature('Hide exhausted asset')
@allure.story('Toggling off hide exhausted asset')
def test_hide_exhausted_asset_off(wallets_and_operations: WalletTestSetup):
    """Test for hiding exhausted asset"""

    with allure.step('Navigating to settings page'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_hide_exhausted_asset_toggle_button()

    with allure.step('Send asset to the second page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        wallets_and_operations.first_page_objects.fungible_page_objects.click_refresh_button()
        child_count = wallets_and_operations.first_page_objects.fungible_page_objects.get_child_count()

        assert len(child_count) == 4
