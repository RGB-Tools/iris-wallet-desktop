# pylint: disable=redefined-outer-name, unused-import
"""
This file contains test cases for the keyring functionality in the application.
"""
from __future__ import annotations

import allure
import pytest

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup

MNEMONIC = None
PASSWORD = None


@allure.feature('Keyring')
@allure.story('Keyring Dialog')
@pytest.mark.parametrize('test_environment', [False], indirect=True)
def test_keyring_dialog(test_environment, wallets_and_operations: WalletTestSetup):
    """
    Test the keyring dialog functionality by restarting the application within the same test.

    :param test_environment: The test environment fixture.
    :param wallets_and_operations: The wallets and operations fixture.
    """
    with allure.step('Create and fund first wallet'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL, fund=False,
        )

    with allure.step('toggle the keyring button and save the mnemonic and password'):
        global MNEMONIC, PASSWORD
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_keyring_toggle_button()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_keyring_mnemonic_copy_button()
        MNEMONIC = wallets_and_operations.first_page_operations.do_get_copied_address()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_keyring_password_copy_button()
        PASSWORD = wallets_and_operations.first_page_operations.do_get_copied_address()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_check_box()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_continue_button()
        test_environment.restart(reset_data=False)


@allure.feature('Keyring')
@allure.story('Keyring option')
@pytest.mark.parametrize('test_environment', [False], indirect=True)
def test_keyring_option(wallets_and_operations: WalletTestSetup):
    """
    Test the keyring option by restarting the app and verifying the keyring toggle button state.

    :param wallets_and_operations: The wallets and operations fixture.
    """
    with allure.step('Restart the app for testing keyring option'):

        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.enter_wallet_password_page_objects.password_input().click()
        wallets_and_operations.first_page_objects.enter_wallet_password_page_objects.enter_password(
            password=PASSWORD,
        )
        wallets_and_operations.first_page_objects.enter_wallet_password_page_objects.click_login_button()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        assert False is wallets_and_operations.first_page_objects.settings_page_objects.keyring_toggle_button().checked
        wallets_and_operations.first_page_objects.settings_page_objects.click_keyring_toggle_button()
        wallets_and_operations.first_page_objects.restore_wallet_page_objects.enter_mnemonic_value(
            MNEMONIC,
        )
        wallets_and_operations.first_page_objects.restore_wallet_page_objects.enter_password_value(
            PASSWORD,
        )
        wallets_and_operations.first_page_objects.restore_wallet_page_objects.click_continue_button()
        assert True is wallets_and_operations.first_page_objects.settings_page_objects.keyring_toggle_button().checked
