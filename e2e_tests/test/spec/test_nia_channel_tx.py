# pylint: disable=redefined-outer-name, unused-import, too-many-statements,unused-argument
"""Tests for send/receive NIA asset with channel"""
from __future__ import annotations

import re

import allure

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from accessible_constant import LN_PORT
from accessible_constant import SECOND_APPLICATION
from accessible_constant import SECOND_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import load_qm_translation
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup
from e2e_tests.test.utilities.model import TransferType
from e2e_tests.test.utilities.translation_utils import TranslationManager
ASSET_TICKER = 'TTK'
ASSET_NAME = 'Tether'
ASSET_AMOUNT = '2000'
CREATE_ASSET_CHANNEL_WITH_AMOUNT = '100'
INVOICE_AMOUNT = '10'
CHANNEL_CAPACITY = '30010'
IP_ADDRESS = '127.0.0.1'
CHANNEL_STATUS = 'Opening'
TEST_NODE_URI = '1234@l:97'
INVALID_AMOUNT = '120'


@allure.feature('Channel send and receive for NIA asset')
@allure.story('Send and receive with correct invoice for NIA asset')
def test_send_and_receive_with_correct_invoice_for_nia(wallets_and_operations: WalletTestSetup):
    """Test sending and receiving with correct invoice for NIA"""
    node_uri = None
    with allure.step('Create and fund first wallet for nia channel'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL,
        )
    with allure.step('Create and fund second wallet for nia channel'):
        wallets_and_operations.second_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=SECOND_APPLICATION, application_url=SECOND_APPLICATION_URL,
        )
    with allure.step('Issue NIA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            application=FIRST_APPLICATION, asset_ticker=ASSET_TICKER, asset_name=ASSET_NAME, asset_amount=ASSET_AMOUNT,
        )
    with allure.step('Get node URI for nia channel'):
        if wallets_and_operations.wallet_mode == 'embedded':
            node_uri = wallets_and_operations.second_page_features.channel_features.get_node_uri_for_embedded(
                application=SECOND_APPLICATION, ip_address=IP_ADDRESS,
            )
        else:
            node_uri = wallets_and_operations.second_page_features.channel_features.get_node_uri_for_remote(
                application=SECOND_APPLICATION, ip_address=IP_ADDRESS, ln_port=LN_PORT,
            )
    with allure.step('Create channel for nia'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        _channel_status = wallets_and_operations.first_page_features.channel_features.create_channel(
            application=FIRST_APPLICATION, node_uri=node_uri, asset_ticker=ASSET_TICKER, asset_amount=CREATE_ASSET_CHANNEL_WITH_AMOUNT, channel_capacity=CHANNEL_CAPACITY,
        )
    with allure.step('Create invoice'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_objects.fungible_page_objects.click_nia_frame(
            asset_name=ASSET_NAME,
        )
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_receive_button()
        _, invoice = wallets_and_operations.second_page_features.receive_features.receive(
            application=SECOND_APPLICATION, transfer_type=TransferType.LIGHTNING.value, value=INVOICE_AMOUNT,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_refresh_button()
    with allure.step('Send with invoice'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            asset_name=ASSET_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.first_page_features.send_features.send(
            application=FIRST_APPLICATION, receiver_invoice=invoice, transfer_type=TransferType.LIGHTNING.value,
        )
    with allure.step('validate transaction amount'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_objects.fungible_page_objects.click_nia_frame(
            asset_name=ASSET_NAME,
        )
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_refresh_button()
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_rgb_transaction_lightning_frame()
        transferred_amount = wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.get_transferred_amount()
        wallets_and_operations.second_page_objects.asset_transaction_detail_page_objects.click_close_button()
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_close_button()
        transferred_amount = re.sub(r'[^\d.]', '', transferred_amount)
        assert transferred_amount == INVOICE_AMOUNT


@allure.feature('Create wrong ln invoice')
@allure.story('Create wrong ln invoice with insufficient amount')
def test_create_wrong_amount_invoice(wallets_and_operations: WalletTestSetup, load_qm_translation):
    """
    Test case to create wrong ln invoice with insufficient amount
    """
    with allure.step('Create invoice'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_objects.fungible_page_objects.click_nia_frame(
            asset_name=ASSET_NAME,
        )
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_receive_button()
        error_label = wallets_and_operations.second_page_features.receive_features.create_wrong_ln_invoice(
            application=SECOND_APPLICATION, amount=INVALID_AMOUNT,
        )
        assert error_label == TranslationManager.translate(
            'asset_amount_validation_invoice',
        )
