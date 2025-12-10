# pylint: disable=redefined-outer-name, unused-import,too-many-statements, unused-argument
"""Tests for channel"""
from __future__ import annotations

import allure

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from accessible_constant import SECOND_APPLICATION
from accessible_constant import SECOND_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import load_qm_translation
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup
from e2e_tests.test.utilities.translation_utils import TranslationManager
from src.model.enums.enums_model import WalletType
from src.utils.info_message import INFO_CHANNEL_DELETED

ASSET_TICKER = 'TTK'
ASSET_NAME = 'Tether'
ASSET_AMOUNT = '2000'
CREATE_ASSET_CHANNEL_WITH_AMOUNT = '100'
CHANNEL_CAPACITY = '30010'
IP_ADDRESS = '127.0.0.1'
CHANNEL_STATUS = 'Opening'
TEST_NODE_URI = '1234@l:97'
LN_PORT = '9736'


@allure.feature('Create channel for embedded')
@allure.story('Create channel with actual value and then close it for embedded')
def test_create_channel_with_actual_value(wallets_and_operations: WalletTestSetup):
    """Test creating channel with actual value."""
    node_uri = None

    with allure.step('Create and fund first wallet for create channel'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL,
        )

    with allure.step('Create and fund second wallet for create channel'):
        wallets_and_operations.second_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=SECOND_APPLICATION, application_url=SECOND_APPLICATION_URL,
        )

    with allure.step('Issue NIA asset for nia channel creation'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            application=FIRST_APPLICATION, asset_ticker=ASSET_TICKER, asset_name=ASSET_NAME, asset_amount=ASSET_AMOUNT,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            asset_name=ASSET_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_copy_button()
        asset_id = wallets_and_operations.first_page_operations.do_get_copied_address()
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_close_button()

    with allure.step('Get node URI for create channel'):
        if wallets_and_operations.wallet_mode == WalletType.EMBEDDED_TYPE_WALLET.value:
            node_uri = wallets_and_operations.second_page_features.channel_features.get_node_uri_for_embedded(
                application=SECOND_APPLICATION, ip_address=IP_ADDRESS,
            )
        elif wallets_and_operations.wallet_mode == WalletType.REMOTE_TYPE_WALLET.value:
            node_uri = wallets_and_operations.second_page_features.channel_features.get_node_uri_for_remote(
                application=SECOND_APPLICATION, ip_address=IP_ADDRESS, ln_port=LN_PORT,
            )

    with allure.step('Create channel'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        channel_status = wallets_and_operations.first_page_features.channel_features.create_channel(
            application=FIRST_APPLICATION, node_uri=node_uri, asset_ticker=ASSET_TICKER, asset_amount=CREATE_ASSET_CHANNEL_WITH_AMOUNT, channel_capacity=CHANNEL_CAPACITY,
        )

    assert channel_status == CHANNEL_STATUS

    with allure.step('Close channel'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_channel_management_button()
        wallets_and_operations.first_page_objects.channel_management_page_objects.click_channel_frame(
            asset_id=asset_id,
        )
        wallets_and_operations.first_page_objects.channel_detail_dialog_page_objects.click_copy_button()
        pub_key = wallets_and_operations.first_page_operations.do_get_copied_address()
        wallets_and_operations.first_page_objects.channel_detail_dialog_page_objects.click_close_channel_button()
        wallets_and_operations.first_page_objects.close_channel_detail_dialog_page_objects.click_continue_button()
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        description = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()

        assert description == INFO_CHANNEL_DELETED.format(pub_key)


@allure.feature('Create channel')
@allure.story('Create channel with wrong node URI')
def test_create_channel_with_wrong_node_uri(wallets_and_operations: WalletTestSetup, load_qm_translation):
    """
    Test the creation of a channel with a wrong node URI.
    """

    with allure.step('Try to create channel with wrong node URI'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        error_label = wallets_and_operations.first_page_features.channel_features.create_channel_with_wrong_node_uri(
            application=FIRST_APPLICATION, node_uri=TEST_NODE_URI,
        )

    assert error_label == TranslationManager.translate('valid_node_prompt')
