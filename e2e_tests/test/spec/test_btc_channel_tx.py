# pylint: disable=redefined-outer-name, unused-import
"""Tests for create channel"""
from __future__ import annotations

import allure

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from accessible_constant import LN_PORT
from accessible_constant import SECOND_APPLICATION
from accessible_constant import SECOND_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup
from e2e_tests.test.utilities.model import TransferType
from src.model.enums.enums_model import WalletType
from src.utils.info_message import INFO_ASSET_SENT_SUCCESSFULLY

ASSET_TICKER = 'rBTC'
CHANNEL_CAPACITY = '99999'
PAY_AMOUNT = '10000'
IP_ADDRESS = '127.0.0.1'


@allure.feature('Channel creation for BTC')
@allure.story('Send and receive with correct invoice for BTC')
def test_send_and_receive_with_correct_invoice_for_btc(wallets_and_operations: WalletTestSetup):
    """
    Test sending and receiving with correct invoice.

    This test case creates embedded wallets, funds them, gets the node URI, creates a channel,
    creates an invoice, sends the asset with the invoice, and verifies the success message.

    Args:
        wallets_and_operations (tuple): A tuple containing the page features, objects, and operations for the first and second applications.

    Returns:
        None
    """
    node_uri = None

    with allure.step('Create and fund first wallet for btc channel'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL,
        )

    with allure.step('Create and fund second wallet for btc channel'):
        wallets_and_operations.second_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=SECOND_APPLICATION, application_url=SECOND_APPLICATION_URL,
        )

    with allure.step('Get node URI for btc channel'):
        if wallets_and_operations.wallet_mode == WalletType.REMOTE_TYPE_WALLET.value:
            node_uri = wallets_and_operations.second_page_features.channel_features.get_node_uri_for_remote(
                application=SECOND_APPLICATION, ip_address=IP_ADDRESS, ln_port=LN_PORT,
            )
        else:
            node_uri = wallets_and_operations.second_page_features.channel_features.get_node_uri_for_embedded(
                application=SECOND_APPLICATION, ip_address=IP_ADDRESS,
            )

    with allure.step('Create channel for btc'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        _channel_status = wallets_and_operations.first_page_features.channel_features.create_channel(
            application=FIRST_APPLICATION, node_uri=node_uri, asset_ticker=ASSET_TICKER, channel_capacity=CHANNEL_CAPACITY,
        )

    with allure.step('Create invoice'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_bitcoin_frame()
        wallets_and_operations.second_page_objects.bitcoin_detail_page_objects.click_receive_bitcoin_button()
        _, btc_invoice = wallets_and_operations.second_page_features.receive_features.receive(
            application=SECOND_APPLICATION, transfer_type=TransferType.LIGHTNING.value, value=PAY_AMOUNT,
        )

    wallets_and_operations.first_page_operations.do_focus_on_application(
        FIRST_APPLICATION,
    )
    with allure.step('Send btc with correct invoice'):
        wallets_and_operations.first_page_objects.fungible_page_objects.click_bitcoin_frame()
        wallets_and_operations.first_page_objects.bitcoin_detail_page_objects.click_send_bitcoin_button()
        wallets_and_operations.first_page_features.send_features.send(
            application=FIRST_APPLICATION, receiver_invoice=btc_invoice, transfer_type=TransferType.LIGHTNING.value,
        )
        _, description = wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()

        assert description == INFO_ASSET_SENT_SUCCESSFULLY
