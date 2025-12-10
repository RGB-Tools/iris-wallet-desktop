# pylint: disable=redefined-outer-name, unused-import
"""Test module for hiding exhausted asset"""
from __future__ import annotations

import re

import allure
import keyring as kr

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from accessible_constant import FIRST_SERVICE
from accessible_constant import NATIVE_AUTH_ENABLE
from accessible_constant import SECOND_APPLICATION
from accessible_constant import SECOND_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.model import WalletTestSetup
from src.data.repository.setting_repository import SettingRepository
from src.utils.info_message import INFO_ASSET_SENT
from src.utils.info_message import INFO_BITCOIN_SENT

ASSET_TICKER = 'TTK'
ASSET_NAME_1 = 'Tether'
ASSET_AMOUNT = '2000'
ASSET_DESCRIPTION = 'CFA asset'
ASSET_NAME_2 = 'Test asset'


@allure.feature('Ask authorization for important operations')
@allure.story('Toggling on ask authorization for import operations')
def test_ask_auth_for_imp_question_send_bitcoin_on(wallets_and_operations: WalletTestSetup):
    """Test for hiding exhausted asset"""
    with allure.step('Initializing the wallet'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations, FIRST_APPLICATION, FIRST_APPLICATION_URL,
        )
        wallets_and_operations.second_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations, SECOND_APPLICATION, SECOND_APPLICATION_URL,
        )

    with allure.step('Turning on ask authorization for import operations'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()

        is_on_or_not = kr.get_password(FIRST_SERVICE, NATIVE_AUTH_ENABLE)
        native_status_casted: bool = SettingRepository.str_to_bool(
            is_on_or_not,
        )

        if native_status_casted is not True:
            wallets_and_operations.first_page_objects.settings_page_objects.click_ask_auth_imp_question()
            wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()

    with allure.step('Getting the receiver\'s address'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_bitcoin_frame()
        wallets_and_operations.second_page_objects.bitcoin_detail_page_objects.click_receive_bitcoin_button()
        address, _ = wallets_and_operations.second_page_features.receive_features.receive(
            SECOND_APPLICATION, transfer_type='bitcoin',
        )

    with allure.step('Sending the bitcoin'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        wallets_and_operations.first_page_objects.fungible_page_objects.click_bitcoin_frame()
        wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_send_bitcoin_button()
        wallets_and_operations.first_page_features.send_features.send(
            FIRST_APPLICATION, address, ASSET_AMOUNT, transfer_type='bitcoin', is_native_auth_enabled=True,
        )
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        toaster_description = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()
        wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_bitcoin_close_button()

    with allure.step('asserting tx id'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.bitcoin_detail_page_objects.click_bitcoin_refresh_button()
        wallets_and_operations.second_page_objects.bitcoin_detail_page_objects.click_bitcoin_transaction_frame()
        bitcoin_tx_id = wallets_and_operations.second_page_objects.bitcoin_transaction_detail_page_objects.get_bitcoin_tx_id()
        wallets_and_operations.second_page_objects.bitcoin_transaction_detail_page_objects.click_close_button()
        wallets_and_operations.second_page_objects.bitcoin_detail_page_objects.click_bitcoin_close_button()
        bitcoin_tx_id = re.sub(
            r'[\u200B\u200C\u200D\u2060\uFEFF]', '', bitcoin_tx_id,
        )
        assert toaster_description == INFO_BITCOIN_SENT.format(bitcoin_tx_id)


@allure.story('Issuing and sending the RGB assets')
def test_ask_auth_for_imp_question_issue_nia_on(wallets_and_operations: WalletTestSetup):
    """Issuing NIA asset with ask auth for important operations on"""
    with allure.step('Issuing NIA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            FIRST_APPLICATION, ASSET_TICKER, ASSET_NAME_1, ASSET_AMOUNT, is_native_auth_enabled=True,
        )


@allure.story('Sending NIA asset')
def test_ask_auth_for_imp_question_send_nia_on(wallets_and_operations: WalletTestSetup):
    """Sending NIA asset with ask auth for important operations on"""
    with allure.step('Getting an RGB invoice'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        nia_invoice = wallets_and_operations.second_page_features.receive_features.receive_asset_from_sidebar(
            SECOND_APPLICATION,
        )

    with allure.step('Sending the NIA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            ASSET_AMOUNT,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.first_page_features.send_features.send(
            FIRST_APPLICATION, nia_invoice, ASSET_AMOUNT, is_native_auth_enabled=True,
        )
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        toaster_description = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()
    with allure.step('asserting tx id'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_objects.fungible_page_objects.click_nia_frame(
            ASSET_NAME_1,
        )
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_rgb_transaction_on_chain_frame()
        tx_id = wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.get_tx_id()
        wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.click_close_button()
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_close_button()
        tx_id = re.sub(r'[\u200B\u200C\u200D\u2060\uFEFF]', '', tx_id)
        assert toaster_description == INFO_ASSET_SENT.format(tx_id)


@allure.story('Issuing CFA asset')
def test_ask_auth_for_imp_question_issue_cfa_on(wallets_and_operations: WalletTestSetup):
    """Issuing CFA asset with ask auth for important operations on"""
    with allure.step('Issuing CFA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_features.issue_cfa_features.issue_cfa_with_sufficient_sats_and_utxo(
            FIRST_APPLICATION, ASSET_NAME_1, ASSET_DESCRIPTION, ASSET_AMOUNT, is_native_auth_enabled=True,
        )


@allure.story('Sending CFA asset')
def test_ask_auth_for_imp_question_send_cfa_on(wallets_and_operations: WalletTestSetup):
    """Sending CFA asset with ask auth for important operations on"""
    with allure.step('Getting an RGB invoice'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        cfa_invoice = wallets_and_operations.second_page_features.receive_features.receive_asset_from_sidebar(
            SECOND_APPLICATION,
        )

    with allure.step('Sending the CFA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_collectibles_button()
        wallets_and_operations.first_page_objects.collectible_page_objects.click_cfa_frame(
            ASSET_NAME_1,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.first_page_features.send_features.send(
            FIRST_APPLICATION, cfa_invoice, ASSET_AMOUNT, is_native_auth_enabled=True,
        )
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        toaster_description = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()
    with allure.step('asserting tx id'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.sidebar_page_objects.click_collectibles_button()
        wallets_and_operations.second_page_objects.collectible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_objects.collectible_page_objects.click_cfa_frame(
            ASSET_NAME_1,
        )
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_rgb_transaction_on_chain_frame()
        tx_id = wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.get_tx_id()
        wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.click_close_button()
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_close_button()
        tx_id = re.sub(r'[\u200B\u200C\u200D\u2060\uFEFF]', '', tx_id)
        assert toaster_description == INFO_ASSET_SENT.format(tx_id)


@allure.feature('Ask authorization for important operations')
@allure.story('Toggling off ask authorization for import operations')
def test_ask_auth_for_imp_question_send_bitcoin_off(wallets_and_operations: WalletTestSetup):
    """test native auth for important operations (send btc) off"""
    with allure.step('Toggling off native auth'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()

        is_on_or_not_1 = kr.get_password(FIRST_SERVICE, NATIVE_AUTH_ENABLE)
        native_status_casted: bool = SettingRepository.str_to_bool(
            is_on_or_not_1,
        )

        if native_status_casted is True:
            wallets_and_operations.first_page_objects.settings_page_objects.click_ask_auth_imp_question()
            wallets_and_operations.first_page_operations.enter_native_password()

    with allure.step('getting address'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.sidebar_page_objects.click_fungibles_button()
        wallets_and_operations.second_page_objects.fungible_page_objects.click_bitcoin_frame()
        wallets_and_operations.second_page_objects.bitcoin_detail_page_objects.click_receive_bitcoin_button()
        address, _ = wallets_and_operations.second_page_features.receive_features.receive(
            SECOND_APPLICATION, transfer_type='bitcoin',
        )
        wallets_and_operations.second_page_objects.bitcoin_detail_page_objects.click_bitcoin_close_button()

    with allure.step('Sending bitcoin'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        wallets_and_operations.first_page_objects.fungible_page_objects.click_bitcoin_frame()
        wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_send_bitcoin_button()
        wallets_and_operations.first_page_features.send_features.send(
            FIRST_APPLICATION, address, ASSET_AMOUNT, transfer_type='bitcoin',
        )
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        toaster_title = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_title()
        wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_bitcoin_close_button()

        assert toaster_title == 'Success'


@allure.story('Issuing NIA asset')
def test_ask_auth_for_imp_question_issue_nia_off(wallets_and_operations: WalletTestSetup):
    """Issuing NIA asset with ask auth for important operations off"""
    with allure.step('Issuing NIA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            FIRST_APPLICATION, ASSET_TICKER, ASSET_NAME_2, ASSET_AMOUNT,
        )


@allure.story('Sending NIA asset')
def test_ask_auth_for_imp_question_send_nia_off(wallets_and_operations: WalletTestSetup):
    """Sending NIA asset with ask auth for important operations off"""
    with allure.step('Getting an RGB invoice'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        nia_invoice = wallets_and_operations.second_page_features.receive_features.receive_asset_from_sidebar(
            SECOND_APPLICATION,
        )

    with allure.step('Sending the NIA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            ASSET_NAME_2,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.first_page_features.send_features.send(
            FIRST_APPLICATION, nia_invoice, ASSET_AMOUNT,
        )
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        toaster_description = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()
        wallets_and_operations.first_page_objects.fungible_page_objects.click_refresh_button()
    with allure.step('asserting tx id'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_objects.fungible_page_objects.click_nia_frame(
            ASSET_NAME_2,
        )
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_rgb_transaction_on_chain_frame()
        tx_id = wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.get_tx_id()
        wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.click_close_button()
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_close_button()
        tx_id = re.sub(r'[\u200B\u200C\u200D\u2060\uFEFF]', '', tx_id)
        assert toaster_description == INFO_ASSET_SENT.format(tx_id)


@allure.story('Issuing CFA asset')
def test_ask_auth_for_imp_question_issue_cfa_off(wallets_and_operations: WalletTestSetup):
    """Issuing NIA asset with ask auth for important operations off"""
    with allure.step('Issuing CFA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.first_page_features.issue_cfa_features.issue_cfa_with_sufficient_sats_and_utxo(
            FIRST_APPLICATION, ASSET_NAME_2, ASSET_DESCRIPTION, ASSET_AMOUNT,
        )


@allure.story('Sending CFA asset')
def test_ask_auth_for_imp_question_send_cfa_off(wallets_and_operations: WalletTestSetup):
    """Sending CFA asset with ask auth for important operations off"""
    with allure.step('Getting an RGB invoice'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        cfa_invoice = wallets_and_operations.second_page_features.receive_features.receive_asset_from_sidebar(
            SECOND_APPLICATION,
        )

    with allure.step('Sending the CFA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.collectible_page_objects.click_refresh_button()
        wallets_and_operations.first_page_objects.collectible_page_objects.click_cfa_frame(
            ASSET_NAME_2,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.first_page_features.send_features.send(
            FIRST_APPLICATION, cfa_invoice, ASSET_AMOUNT,
        )
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        toaster_description = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()
    with allure.step('asserting tx id'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.sidebar_page_objects.click_collectibles_button()
        wallets_and_operations.second_page_objects.collectible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_objects.collectible_page_objects.click_cfa_frame(
            ASSET_NAME_2,
        )
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_rgb_transaction_on_chain_frame()
        tx_id = wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.get_tx_id()
        wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.click_close_button()
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_close_button()
        tx_id = re.sub(r'[\u200B\u200C\u200D\u2060\uFEFF]', '', tx_id)
        assert toaster_description == INFO_ASSET_SENT.format(tx_id)
