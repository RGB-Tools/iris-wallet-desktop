# pylint: disable=redefined-outer-name, unused-import
"""E2E test for fail transfer"""
from __future__ import annotations

import allure
import pytest

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.model import WalletTestSetup
from src.utils.info_message import INFO_FAIL_TRANSFER_SUCCESSFULLY


ASSET_TICKER = 'TTK'
NIA_ASSET_NAME = 'Tether'
ASSET_AMOUNT = '2000'


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Fail transfer feature')
@allure.story('Test for fail transfer')
def test_fail_transfer(wallets_and_operations: WalletTestSetup):
    """Test for fail transfer"""

    with allure.step('Creating and funding the wallet'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL,
        )

    with allure.step('Issuing an RGB asset'):
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            FIRST_APPLICATION, ASSET_TICKER, NIA_ASSET_NAME, ASSET_AMOUNT,
        )

    with allure.step('Generating an invoice'):
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            asset_name=NIA_ASSET_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_receive_button()
        wallets_and_operations.first_page_features.receive_features.receive(
            application=FIRST_APPLICATION,
        )

    with allure.step('Failing the transfer'):
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            asset_name=NIA_ASSET_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_fail_transfer_button()
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_confirmation_continue_button()

    toaster_description = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()

    assert toaster_description == INFO_FAIL_TRANSFER_SUCCESSFULLY
