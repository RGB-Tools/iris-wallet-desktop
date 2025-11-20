# pylint: disable=redefined-outer-name, unused-import
"""
    E2E test for login app authentication
"""
from __future__ import annotations

import allure
import pytest

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup


@allure.feature('Login app')
@allure.story('Test login app toggle button')
@pytest.mark.parametrize('test_environment', [False], indirect=True)
def test_login_app_toggle_button_on(test_environment, wallets_and_operations: WalletTestSetup):
    """
    Test the login app toggle button functionality.

    This test case creates first wallet,
    toggles the login app auth button to on, and restarts the application.

    Args:
        test_environment: The test environment setup.
        wallets_and_operations: The wallets and operations setup.

    Returns:
        None
    """
    with allure.step('Create and fund first wallet'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL, fund=False,
        )

    with allure.step('Toggle the login app auth button to on and restart the application'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_login_app_toggle_button()
        if not wallets_and_operations.first_page_operations.wait_for_toggle_state(
            wallets_and_operations.first_page_objects.settings_page_objects.login_auth_toggle_button,
            expected_checked=True,
            timeout=5,
        ):
            wallets_and_operations.first_page_objects.settings_page_objects.click_login_app_toggle_button()

        test_environment.restart(reset_data=False)


@allure.feature('Login app')
@allure.story('Test login app with authentication')
@pytest.mark.parametrize('test_environment', [False], indirect=True)
def test_login_app_with_authentication(wallets_and_operations: WalletTestSetup):
    """
    Test the login app with authentication functionality.

    This test case types the login password, asserts the state of the toggle button,
    toggles it to off, and types the login password again.

    Args:
        test_environment: The test environment setup.
        wallets_and_operations: The wallets and operations setup.

    Returns:
        None
    """
    with allure.step('assert the state of toggle button and toggle it to off'):
        wallets_and_operations.first_page_operations.enter_native_password()

        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()

        # Wait for toggle to be in checked=True state
        assert wallets_and_operations.first_page_operations.wait_for_toggle_state(
            wallets_and_operations.first_page_objects.settings_page_objects.login_auth_toggle_button,
            expected_checked=True,
            timeout=5,
        )

        if wallets_and_operations.first_page_operations.wait_for_toggle_state(
            wallets_and_operations.first_page_objects.settings_page_objects.login_auth_toggle_button,
            expected_checked=True,
            timeout=5,
        ):
            wallets_and_operations.first_page_objects.settings_page_objects.click_login_app_toggle_button()

        wallets_and_operations.first_page_operations.enter_native_password()

        if not wallets_and_operations.first_page_operations.wait_for_toggle_state(
            wallets_and_operations.first_page_objects.settings_page_objects.login_auth_toggle_button,
            expected_checked=False,
            timeout=5,
        ):
            wallets_and_operations.first_page_objects.settings_page_objects.click_login_app_toggle_button()
            wallets_and_operations.first_page_operations.enter_native_password()

        # Wait for toggle to be in checked=False state
        assert wallets_and_operations.first_page_operations.wait_for_toggle_state(
            wallets_and_operations.first_page_objects.settings_page_objects.login_auth_toggle_button,
            expected_checked=False,
            timeout=5,
        )
