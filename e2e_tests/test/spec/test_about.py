# pylint: disable=redefined-outer-name, unused-import
"""Test module for hiding exhausted asset"""
from __future__ import annotations

from pathlib import Path

import allure
import pytest

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from accessible_constant import TEST_ANNOUNCE_ADDRESS
from accessible_constant import TEST_ANNOUNCE_ALIAS
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.model import WalletTestSetup
from src.model.enums.enums_model import WalletType
from src.utils.info_message import INFO_LOG_SAVE_DESCRIPTION


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('About page tests')
@allure.story('Tests for copy buttons for node info')
def test_node_info(wallets_and_operations: WalletTestSetup):
    """Test asserting node info"""
    with allure.step('Create and fund first wallet for issue nia'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL, fund=False,
        )
    with allure.step('Asserting node pubkey'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_about_button()
        node_pubkey = wallets_and_operations.first_page_objects.about_page_objects.get_node_pubkey()
        wallets_and_operations.first_page_objects.about_page_objects.click_node_pubkey_button()
        copied_node_pubkey = wallets_and_operations.first_page_objects.about_page_objects.do_get_copied_address()

        assert copied_node_pubkey == node_pubkey

    if wallets_and_operations.wallet_mode == WalletType.EMBEDDED_TYPE_WALLET.value:
        with allure.step('LN peering listening port'):
            peer_listening_port = wallets_and_operations.first_page_objects.about_page_objects.get_peer_listening_port()
            wallets_and_operations.first_page_objects.about_page_objects.click_ln_peer_listening_port_copy_button()
            copied_ln_peer_listening_port = wallets_and_operations.first_page_objects.about_page_objects.do_get_copied_address()

            assert copied_ln_peer_listening_port == peer_listening_port


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.story('Tests for copy buttons for bitcoind host info')
def test_bitcoind_host_info(wallets_and_operations: WalletTestSetup):
    """Test asserting bitcoind host info"""
    with allure.step('Bitcoind host'):
        bitcoind_host = wallets_and_operations.first_page_objects.about_page_objects.get_bitcoind_host()
        wallets_and_operations.first_page_objects.about_page_objects.click_bitcoind_host_copy_button()
        copied_bitcoind_host = wallets_and_operations.first_page_objects.about_page_objects.do_get_copied_address()

        assert copied_bitcoind_host == bitcoind_host


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.story('Tests for copy buttons for bitcoind port info')
def test_bitcoind_port_info(wallets_and_operations: WalletTestSetup):
    """Test asserting bitcoind port info"""
    with allure.step('Bitcoind port'):
        bitcoind_port = wallets_and_operations.first_page_objects.about_page_objects.get_bitcoind_port()
        wallets_and_operations.first_page_objects.about_page_objects.click_bitcoind_port_copy_button()
        copied_bitcoind_port = wallets_and_operations.first_page_objects.about_page_objects.do_get_copied_address()

        assert copied_bitcoind_port == bitcoind_port


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.story('Tests for copy buttons for indexer info')
def test_indexer_info(wallets_and_operations: WalletTestSetup):
    """Test asserting indexer info"""
    with allure.step('Indexer URL'):
        indexer_url = wallets_and_operations.first_page_objects.about_page_objects.get_indexer_url()
        wallets_and_operations.first_page_objects.about_page_objects.click_indexer_url_copy_button()
        copied_indexer_url = wallets_and_operations.first_page_objects.about_page_objects.do_get_copied_address()

        assert copied_indexer_url == indexer_url


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.story('Tests for copy buttons for RGB proxy info')
def test_rgb_proxy_info(wallets_and_operations: WalletTestSetup):
    """Test asserting RGB proxy info"""
    with allure.step('RGB proxy URL'):
        rgb_proxy_url = wallets_and_operations.first_page_objects.about_page_objects.get_rgb_proxy_url()
        wallets_and_operations.first_page_objects.about_page_objects.click_rgb_proxy_url_copy_button()
        copied_rgb_proxy_url = wallets_and_operations.first_page_objects.about_page_objects.do_get_copied_address()

        assert copied_rgb_proxy_url == rgb_proxy_url


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.story('Tests for copy buttons for announce address info')
def test_announce_address_info(wallets_and_operations: WalletTestSetup):
    """Test asserting announce address info"""
    with allure.step('Announce address'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_specify_announce_address_frame()
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_ANNOUNCE_ADDRESS,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()

        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_about_button()
        announce_address = wallets_and_operations.first_page_objects.about_page_objects.get_announce_address()
        wallets_and_operations.first_page_objects.about_page_objects.click_announce_address_copy_button()
        copied_announce_address = wallets_and_operations.first_page_objects.about_page_objects.do_get_copied_address()

        assert copied_announce_address == announce_address


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.story('Tests for copy buttons for announce alias info')
def test_announce_alias_info(wallets_and_operations: WalletTestSetup):
    """Test asserting announce alias info"""
    with allure.step('Announce alias'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_specify_announce_alias()
        wallets_and_operations.first_page_objects.settings_page_objects.clear_input_box()
        wallets_and_operations.first_page_objects.settings_page_objects.enter_input_value(
            TEST_ANNOUNCE_ALIAS,
        )
        wallets_and_operations.first_page_objects.settings_page_objects.click_save_button()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_about_button()
        announce_alias = wallets_and_operations.first_page_objects.about_page_objects.get_announce_alias()
        wallets_and_operations.first_page_objects.about_page_objects.click_announce_alias_copy_button()
        copied_announce_alias = wallets_and_operations.first_page_objects.about_page_objects.do_get_copied_address()

        assert copied_announce_alias == announce_alias


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('About page tests')
@allure.story('Tests for download debug log')
def test_download_debug_log(wallets_and_operations: WalletTestSetup):
    """Test for downloading debug logs"""
    with allure.step('Download debug logs'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )

        wallets_and_operations.first_page_objects.about_page_objects.click_download_debug_log()
        file_name = wallets_and_operations.first_page_objects.about_page_objects.copying_logs_filename() + \
            '.zip'
        homepath = str(Path.home())
        complete_file_path = homepath+'/'+file_name
        wallets_and_operations.first_page_objects.about_page_objects.press_enter()

        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()

        toaster_desc = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()
        assert toaster_desc == INFO_LOG_SAVE_DESCRIPTION.format(
            complete_file_path,
        )
