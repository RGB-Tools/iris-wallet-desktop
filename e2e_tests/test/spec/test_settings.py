# pylint: disable=redefined-outer-name, unused-import
"""Test module for the settings page functionality"""
from __future__ import annotations

import allure
import pytest

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from accessible_constant import LOCAL_BITCOIND_RPC_HOST_REGTEST
from accessible_constant import LOCAL_BITCOIND_RPC_PORT_REGTEST
from accessible_constant import LOCAL_INDEXER_URL_REGTEST
from accessible_constant import LOCAL_PROXY_ENDPOINT_REGTEST
from accessible_constant import TEST_ANNOUNCE_ADDRESS
from accessible_constant import TEST_ANNOUNCE_ALIAS
from accessible_constant import TOASTER_DESCRIPTION
from e2e_tests.test.utilities.app_setup import load_qm_translation
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup
from e2e_tests.test.utilities.translation_utils import TranslationManager
from src.utils.error_message import ERROR_UNABLE_TO_SET_INDEXER_URL
from src.utils.error_message import ERROR_UNABLE_TO_SET_PROXY_ENDPOINT
from src.utils.info_message import INFO_SET_ENDPOINT_SUCCESSFULLY
from src.utils.info_message import INFO_SET_EXPIRY_TIME_SUCCESSFULLY
from src.utils.info_message import INFO_SET_MIN_CONFIRMATION_SUCCESSFULLY

TEST_INVALID_ANNOUNCE_ADDRESS = 'example'
TEST_INDEXER_URL = 'electrum.rgbtools.org:50041'
TEST_INVALID_INDEXER_URL = 'test.indexer'
TEST_RGB_PROXY_URL = 'rpcs://proxy.iriswallet.com/0.2/json-rpc'
TEST_INVALID_RGB_PROXY_URL = 'test.rgb.proxy'
TEST_INVALID_BITCOIND_HOST = 'test.bitcoind.host'
TEST_INVALID_BITCOIND_PORT = '12345'
TEST_FEE_RATE = '20'
TEST_FEE_RATE_TOAST_DESC_SUCCESS = 'Fee rate set successfully'
TEST_MIN_CONFIRMATION = '6'
TEST_EXPIRY_MINUTES = '1440'
TEST_EXPIRY_HOURS = '24'
TEST_EXPIRY_DAYS = '1'

pytestmark = pytest.mark.order(2)


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set default fee rate')
@allure.story('Sets default fee rate for sending assets')
def test_set_default_fee_rate(wallets_and_operations: WalletTestSetup):
    """Test setting a default fee rate

    Tests that a user can:
    1. Navigate to settings
    2. Set a new default fee rate
    3. Verify the fee rate is saved and applied
    """
    with allure.step('Create and fund first wallet for setting'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL, fund=False,
        )

    with allure.step('Navigating to set default fee rate frame in settings'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_default_fee_rate_frame()

    with allure.step('Entering a new default fee rate and saving'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_FEE_RATE,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()
        toast_description = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern=TEST_FEE_RATE_TOAST_DESC_SUCCESS,
        )

    assert toast_description == TEST_FEE_RATE_TOAST_DESC_SUCCESS

    with allure.step('Navigating to send bitcoin page to see the new default fee rate'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        wallets_and_operations.first_page_objects.fungible_page_objects.click_bitcoin_frame()
        wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_send_bitcoin_button()
        wallets_and_operations.first_page_objects.wallet_transfer_page_objects.click_on_chain_button()
        new_default_fee_rate = wallets_and_operations.first_page_objects.send_asset_page_objects.get_fee_rate_text()

    assert new_default_fee_rate == TEST_FEE_RATE

    with allure.step('Navigating back to fungibles page'):
        wallets_and_operations.first_page_objects.send_asset_page_objects.click_send_asset_close_button()
        wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_bitcoin_close_button()
        if wallets_and_operations.first_page_operations.do_is_displayed(
            wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.bitcoin_close_button(),
        ):
            wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_bitcoin_close_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set default expiry time')
@allure.story('Sets default expiry time For lightning invoice')
def test_default_expiry_time_minute(wallets_and_operations: WalletTestSetup):
    """
    Test setting a default expiry time in minutes for lightning invoices.

    Tests that a user can:
    1. Navigate to settings
    2. Set a new default expiry time in minutes
    3. Verify the expiry time is saved and applied
    """
    with allure.step('Navigating to the settings page and clearing default fee rate input'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_default_exp_time_frame()

    with allure.step('Entering the new value for the expiry time'):
        wallets_and_operations.first_page_objects.settings_page_objects.click_on_combo_box()
        wallets_and_operations.first_page_objects.settings_page_objects.click_on_minute()
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_EXPIRY_MINUTES,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

    # Checking the changes in create invoice page
    wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
    wallets_and_operations.first_page_objects.fungible_page_objects.click_bitcoin_frame()
    wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_receive_bitcoin_button()
    wallets_and_operations.first_page_objects.wallet_transfer_page_objects.click_lightning_button()

    # Getting the expiry time
    expiry_time = wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.get_expiry_amount()
    expiry_time_unit = wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.get_expiry_time_unit()
    wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.click_close_button()
    if wallets_and_operations.first_page_operations.do_is_displayed(
        wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.close_button(),
    ):
        wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.click_close_button()

    assert expiry_time == TEST_EXPIRY_MINUTES
    assert expiry_time_unit == TranslationManager.translate('minutes')

    with allure.step('Navigating to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set default expiry time')
@allure.story('Sets default expiry time For lightning invoice')
def test_default_expiry_time_hour(wallets_and_operations: WalletTestSetup):
    """
    Test setting a default expiry time in hours for lightning invoices.

    Tests that a user can:
    1. Navigate to settings
    2. Set a new default expiry time in hours
    3. Verify the expiry time is saved and applied
    """
    with allure.step('Navigating to the settings page and clearing default fee rate input'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_default_exp_time_frame()

    with allure.step('Entering the new value for the expiry time'):
        wallets_and_operations.first_page_objects.settings_page_objects.click_on_combo_box()
        wallets_and_operations.first_page_objects.settings_page_objects.click_on_hour()
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_EXPIRY_HOURS,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

    # Checking the changes in create invoice page
    wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
    wallets_and_operations.first_page_objects.fungible_page_objects.click_bitcoin_frame()
    wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_receive_bitcoin_button()
    wallets_and_operations.first_page_objects.wallet_transfer_page_objects.click_lightning_button()

    # Getting the expiry time
    expiry_time = wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.get_expiry_amount()
    expiry_time_unit = wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.get_expiry_time_unit()
    wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.click_close_button()
    if wallets_and_operations.first_page_operations.do_is_displayed(
        wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.close_button(),
    ):
        wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.click_close_button()

    assert expiry_time == TEST_EXPIRY_HOURS
    assert expiry_time_unit == TranslationManager.translate('hours')

    with allure.step('Navigating back to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set default expiry time')
@allure.story('Sets default expiry time For lightning invoice')
def test_default_expiry_time_days(wallets_and_operations: WalletTestSetup):
    """
    Test setting a default expiry time in days for lightning invoices.

    Tests that a user can:
    1. Navigate to settings
    2. Set a new default expiry time in days
    3. Verify the expiry time is saved and applied
    """
    with allure.step('Navigating to the settings page and clearing default fee rate input'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_default_exp_time_frame()

    with allure.step('Entering the new value for the expiry time'):
        wallets_and_operations.first_page_objects.settings_page_objects.click_on_combo_box()
        wallets_and_operations.first_page_objects.settings_page_objects.click_on_days()
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_EXPIRY_DAYS,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

    with allure.step('Checking the change in create ln invoice page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        wallets_and_operations.first_page_objects.fungible_page_objects.click_bitcoin_frame()
        wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_receive_bitcoin_button()
        wallets_and_operations.first_page_objects.wallet_transfer_page_objects.click_lightning_button()

    # Getting the expiry time
    expiry_time = wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.get_expiry_amount()
    expiry_time_unit = wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.get_expiry_time_unit()
    wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.click_close_button()
    if wallets_and_operations.first_page_operations.do_is_displayed(
        wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.close_button(),
    ):
        wallets_and_operations.first_page_objects.create_ln_invoice_page_objects.click_close_button()

    assert expiry_time == TEST_EXPIRY_DAYS
    assert expiry_time_unit == TranslationManager.translate('days')

    with allure.step('Navigating to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set default minimum confirmation')
@allure.story('Sets default minimum confirmation For sending assets')
def test_set_default_min_confirmation(wallets_and_operations: WalletTestSetup):
    """Test for setting default minimum confirmation"""
    with allure.step('Navigating to set default fee rate frame in settings'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_set_min_confirmation_frame()

    with allure.step('Entering a new default fee rate and saving'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_MIN_CONFIRMATION,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()
        toast_description = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern=INFO_SET_MIN_CONFIRMATION_SUCCESSFULLY,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_set_min_confirmation_frame()
        min_confirmation = wallets_and_operations.first_page_objects.settings_page_objects.get_input_box_value()

    assert toast_description == INFO_SET_MIN_CONFIRMATION_SUCCESSFULLY or min_confirmation == TEST_MIN_CONFIRMATION


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set announce address')
@allure.story('Setting an announce address for this')
@allure.description('Testing with an invalid announce address')
def test_set_valid_announce_address(wallets_and_operations: WalletTestSetup):
    """Test setting a valid announce address

    Tests that a user can:
    1. Navigate to settings
    2. Set a valid announce address
    3. Verify the address is saved correctly
    """

    with allure.step('Navigating to set announce address frame'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_specify_announce_address_frame()

    with allure.step('Enter a new announce address'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_ANNOUNCE_ADDRESS,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

        announce_add_toast_desc = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern=INFO_SET_ENDPOINT_SUCCESSFULLY.format(
                TranslationManager.translate('announce_address_endpoint'),
            ),
        )

    with allure.step('Navigating to about page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_about_button()
        test_announce_address = wallets_and_operations.first_page_objects.about_page_objects.get_announce_address()

    assert test_announce_address == TEST_ANNOUNCE_ADDRESS or announce_add_toast_desc == INFO_SET_ENDPOINT_SUCCESSFULLY.format(
        TranslationManager.translate('announce_address_endpoint'),
    )

    with allure.step('Navigating back to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set announce alias')
@allure.story('Setting an announce alias for this')
def test_set_announce_alias(wallets_and_operations: WalletTestSetup):
    """Test setting an announce alias

    Tests that a user can:
    1. Navigate to settings
    2. Set an announce alias
    3. Verify the alias is saved correctly
    """

    with allure.step('Navigating to set announce alias frame'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_specify_announce_alias()

    with allure.step('Enter a new announce alias'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_ANNOUNCE_ALIAS,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

        announce_add_toast_desc = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern=INFO_SET_ENDPOINT_SUCCESSFULLY.format(
                TranslationManager.translate('announce_alias_endpoint'),
            ),
        )

    with allure.step('Navigating to about page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_about_button()
        test_announce_address = wallets_and_operations.first_page_objects.about_page_objects.get_announce_alias()

    assert test_announce_address == TEST_ANNOUNCE_ALIAS or announce_add_toast_desc == INFO_SET_ENDPOINT_SUCCESSFULLY.format(
        TranslationManager.translate('announce_alias_endpoint'),
    )

    with allure.step('Navigating to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set a bitcoind host')
@allure.story('Setting an invalid bitcoind host for the wallet')
def test_set_invalid_bitcoind_host(wallets_and_operations: WalletTestSetup):
    """Test setting an invalid bitcoind host

    Tests that when a user:
    1. Navigates to settings
    2. Attempts to set an invalid bitcoind host
    3. The system shows appropriate error message
    """

    with allure.step('Navigating to set bitcoind host frame'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_specify_bitcoind_host_frame()

    with allure.step('Enter an invalid bitcoind host'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_INVALID_BITCOIND_HOST,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

        announce_add_toast_desc = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern='Unlock failed: Unable to connect to the Bitcoin daemon',
        )

        wallets_and_operations.first_page_objects.settings_page_objects.click_specify_bitcoind_host_frame()
        bitcoind_host = wallets_and_operations.first_page_objects.settings_page_objects.get_input_box_value()

    assert announce_add_toast_desc == 'Unlock failed: Unable to connect to the Bitcoin daemon' or bitcoind_host == LOCAL_BITCOIND_RPC_HOST_REGTEST

    with allure.step('Navigating to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set a Bitcoind Port')
@allure.story('Setting an invalid bitcoind port for the wallet')
def test_set_invalid_bitcoind_port(wallets_and_operations: WalletTestSetup):
    """Test setting an invalid bitcoind port

    Tests that when a user:
    1. Navigates to settings
    2. Attempts to set an invalid bitcoind port
    3. The system shows appropriate error message
    """

    with allure.step('Navigating to set bitcoind port frame'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_specify_bitcoind_port_frame()

    with allure.step('Enter an invalid bitcoind port'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_INVALID_BITCOIND_PORT,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

        announce_add_toast_desc = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern='Unlock failed: Unable to connect to the Bitcoin daemon',
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_specify_bitcoind_port_frame()
        bitcoind_port = wallets_and_operations.first_page_objects.settings_page_objects.get_input_box_value()

    assert announce_add_toast_desc == 'Unlock failed: Unable to connect to the Bitcoin daemon' or bitcoind_port == LOCAL_BITCOIND_RPC_PORT_REGTEST

    with allure.step('Navigating to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set indexer URL')
@allure.story('Setting an invalid indexer url for the wallet')
def test_set_invalid_electrum_url(wallets_and_operations: WalletTestSetup):
    """Test setting an invalid electrum URL

    Tests that when a user:
    1. Navigates to settings
    2. Attempts to set an invalid electrum URL
    3. The system shows appropriate error message
    """

    with allure.step('Navigating to set electrum URL frame'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_set_indexer_url_frame()

    with allure.step('Enter a new electrum URL'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_INVALID_INDEXER_URL,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

        announce_add_toast_desc = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern=ERROR_UNABLE_TO_SET_INDEXER_URL,
        )

        wallets_and_operations.first_page_objects.settings_page_objects.click_set_indexer_url_frame()
        indexer_url = wallets_and_operations.first_page_objects.settings_page_objects.get_input_box_value()

    assert announce_add_toast_desc == ERROR_UNABLE_TO_SET_INDEXER_URL or indexer_url == LOCAL_INDEXER_URL_REGTEST

    with allure.step('Navigating to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set RGB proxy URL')
@allure.story('Setting a RGB proxy url for the wallet')
def test_set_rgb_proxy_url(wallets_and_operations: WalletTestSetup):
    """Test setting a valid RGB proxy URL

    Tests that a user can:
    1. Navigate to settings
    2. Set a valid RGB proxy URL
    3. Verify the URL is saved correctly
    """

    with allure.step('Navigating to set RGB proxy URL frame'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_set_rgb_proxy_url_frame()

    with allure.step('Enter a new RGB proxy URL'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_RGB_PROXY_URL,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

        announce_add_toast_desc = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern=INFO_SET_ENDPOINT_SUCCESSFULLY.format(
                TranslationManager.translate('proxy_endpoint'),
            ),
        )

    with allure.step('Navigating to about page to see the changes'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_about_button()
        proxy_url = wallets_and_operations.first_page_objects.about_page_objects.get_rgb_proxy_url()

    assert proxy_url == TEST_RGB_PROXY_URL or announce_add_toast_desc == INFO_SET_ENDPOINT_SUCCESSFULLY.format(
        TranslationManager.translate('proxy_endpoint'),
    )

    with allure.step('Navigating to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set RGB proxy URL')
@allure.story('Setting an invalid RGB proxy url for the wallet')
def test_set_invalid_rgb_proxy_url(wallets_and_operations: WalletTestSetup):
    """Test setting an invalid RGB proxy URL

    Tests that when a user:
    1. Navigates to settings
    2. Attempts to set an invalid RGB proxy URL
    3. The system shows appropriate error message
    """

    with allure.step('Navigating to set RGB proxy URL frame'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_set_rgb_proxy_url_frame()

    with allure.step('Enter an invalid RGB proxy URL'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_INVALID_RGB_PROXY_URL,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

        announce_add_toast_desc = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern=ERROR_UNABLE_TO_SET_PROXY_ENDPOINT,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_set_rgb_proxy_url_frame()
        rgb_proxy_url = wallets_and_operations.first_page_objects.settings_page_objects.get_input_box_value()

    assert announce_add_toast_desc == ERROR_UNABLE_TO_SET_PROXY_ENDPOINT or rgb_proxy_url == TEST_RGB_PROXY_URL

    with allure.step('Navigating to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Set indexer URL')
@allure.story('Setting an indexer url for the wallet')
def test_set_valid_electrum_url(wallets_and_operations: WalletTestSetup):
    """Test setting a valid electrum URL

    Tests that a user can:
    1. Navigate to settings
    2. Set a valid electrum URL
    3. Verify the URL is saved correctly
    """

    with allure.step('Navigating to set electrum URL frame'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_set_indexer_url_frame()

    with allure.step('Enter a new electrum URL'):
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_INDEXER_URL,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

        announce_add_toast_desc = wallets_and_operations.first_page_objects.toaster_page_objects.click_and_get_description(
            filter_pattern=INFO_SET_ENDPOINT_SUCCESSFULLY.format(
                TranslationManager.translate('indexer_endpoint'),
            ),
        )

    with allure.step('Navigating to about page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_about_button()
        test_announce_address = wallets_and_operations.first_page_objects.about_page_objects.get_indexer_url()

    assert test_announce_address == TEST_INDEXER_URL or announce_add_toast_desc == INFO_SET_ENDPOINT_SUCCESSFULLY.format(
        TranslationManager.translate('indexer_endpoint'),
    )

    with allure.step('Navigating to fungibles page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
