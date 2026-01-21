# pylint: disable=redefined-outer-name, unused-import
"""
Tests for nia asset issuance.
"""
from __future__ import annotations

import allure
import pytest

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup

ASSET_TICKER = 'TTK'
NIA_ASSET_NAME = 'Tether'
ASSET_AMOUNT = '2000'
ISSUE_NIA_TOASTER_MESSAGE = 'You have insufficient funds'


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Issue nia asset without sufficient sats')
@allure.story('Issue nia asset without sufficient sats which will produce error toaster')
def test_issue_nia_without_sufficient_sats(wallets_and_operations: WalletTestSetup):
    """
    Test nia asset issuance without sufficient sats.
    """

    with allure.step('Create and fund first wallet for issue nia'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL, fund=False,
        )

    with allure.step('Issue nia asset without sufficient sats'):
        description = wallets_and_operations.first_page_features.issue_nia_features.issue_nia_asset_without_sat(
            FIRST_APPLICATION, ASSET_TICKER, NIA_ASSET_NAME, ASSET_AMOUNT,
        )

    assert description == ISSUE_NIA_TOASTER_MESSAGE


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Issue nia asset with sufficient sats and no utxo')
@allure.story('Issue nia asset with sufficient sats which will create utxo and create asset')
def test_issue_nia_with_sufficient_sats_and_no_utxo(wallets_and_operations: WalletTestSetup):
    """
    Test nia asset issuance with sufficient sats and no utxo.
    """

    with allure.step('Fund wallet for issue nia asset'):
        wallets_and_operations.first_page_features.wallet_features.fund_wallet(
            FIRST_APPLICATION,
        )

    with allure.step('Verifies there is no utxo for issue nia asset'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_view_unspents_button()
        count = wallets_and_operations.first_page_objects.view_unspent_list_page_objects.get_unspent_widget()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        assert count == 1

    with allure.step('Issue nia asset with sufficient sats and no utxo'):
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_no_utxo(
            FIRST_APPLICATION, ASSET_TICKER, NIA_ASSET_NAME, ASSET_AMOUNT,
        )

    with allure.step('Verify asset name'):
        asset_name = wallets_and_operations.first_page_objects.fungible_page_objects.get_nia_asset_name(
            NIA_ASSET_NAME,
        )
        assert asset_name == NIA_ASSET_NAME


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Issue nia asset with sufficient sats')
@allure.story('Issue nia asset with sufficient sats which will create asset')
def test_issue_nia_with_sufficient_sats_and_utxo(wallets_and_operations: WalletTestSetup):
    """
    Test nia asset issuance with sufficient sats and utxo.
    """

    with allure.step('Verified that one utxo exists for issue nia asset'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_view_unspents_button()
        count = wallets_and_operations.first_page_objects.view_unspent_list_page_objects.get_unspent_widget()
        nia_asset_id = wallets_and_operations.first_page_objects.view_unspent_list_page_objects.get_unspent_utxo_asset_id(
            'NA',
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        assert count == 3
        assert nia_asset_id == 'NA'

    with allure.step('Issue nia asset with sufficient sats and utxo'):
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            FIRST_APPLICATION, ASSET_TICKER, NIA_ASSET_NAME, ASSET_AMOUNT,
        )

    with allure.step('Verify asset name'):
        asset_name = wallets_and_operations.first_page_objects.fungible_page_objects.get_nia_asset_name(
            NIA_ASSET_NAME,
        )
        assert asset_name == NIA_ASSET_NAME
