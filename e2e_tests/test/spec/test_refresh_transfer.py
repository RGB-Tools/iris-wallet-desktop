# pylint: disable=redefined-outer-name, unused-import, too-many-statements
"""Tests for refresh transfer"""
from __future__ import annotations

import allure

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from accessible_constant import SECOND_APPLICATION
from accessible_constant import SECOND_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup
from src.model.enums.enums_model import TransactionStatusEnumModel

ASSET_TICKER = 'TTK'
ASSET_NAME = 'Tether'
ASSET_AMOUNT = '2000'
SEND_AMOUNT = '50'


@allure.feature('Test for refresh transfer')
@allure.story('Test for refresh transfer from home refresh and then check the status to success after mine the transaction')
def test_refresh_transfer(wallets_and_operations: WalletTestSetup):
    """Test for refresh transfer"""

    with allure.step('Create and fund first wallet for refresh transfer'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL,
        )

    with allure.step('Create and fund second wallet for refresh transfer'):
        wallets_and_operations.second_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=SECOND_APPLICATION, application_url=SECOND_APPLICATION_URL,
        )

    with allure.step('Issue NIA asset for refresh transfer'):
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            application=FIRST_APPLICATION, asset_ticker=ASSET_TICKER, asset_name=ASSET_NAME, asset_amount=ASSET_AMOUNT,
        )

    with allure.step('Generate invoice'):
        invoice = wallets_and_operations.second_page_features.receive_features.receive_asset_from_sidebar(
            SECOND_APPLICATION,
        )

    with allure.step('Send NIA asset to correct invoice'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )

        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            ASSET_NAME,
        )

        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()

        wallets_and_operations.first_page_features.send_features.send(
            application=FIRST_APPLICATION, receiver_invoice=invoice, amount=SEND_AMOUNT,
        )

    with allure.step('Refresh transfer'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_refresh_button()

    with allure.step('Validate transfer status'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            ASSET_NAME,
        )
        actual_transfer_status_first_app = wallets_and_operations.first_page_objects.asset_detail_page_objects.get_transfer_status()
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_close_button()
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_nia_frame(
            ASSET_NAME,
        )
        actual_transfer_status_second_app = wallets_and_operations.second_page_objects.asset_detail_page_objects.get_transfer_status()
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_close_button()

        assert actual_transfer_status_first_app == TransactionStatusEnumModel.WAITING_CONFIRMATIONS.value
        assert actual_transfer_status_second_app == TransactionStatusEnumModel.WAITING_CONFIRMATIONS.value
