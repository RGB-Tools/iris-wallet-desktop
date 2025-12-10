# pylint: disable=redefined-outer-name, unused-import
"""
Tests for issuing cfa assets with different scenarios.
"""
from __future__ import annotations

import allure
import pytest

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup

CFA_ASSET_NAME = 'Cfa'
ASSET_DESCRIPTION = 'This is Cfa asset'
ASSET_AMOUNT = '2000'
ISSUE_CFA_TOASTER_MESSAGE = 'You have insufficient funds'


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Issue cfa asset without sufficient sats')
@allure.story('Issue cfa asset without sufficient sats which will produce error toaster')
def test_issue_cfa_without_sufficient_sats(wallets_and_operations: WalletTestSetup):
    """
    Test issuing cfa asset without sufficient sats.
    """

    with allure.step('Create and fund first wallet for issue cfa'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL, fund=False,
        )

    with allure.step('Issue cfa asset without sat'):
        description = wallets_and_operations.first_page_features.issue_cfa_features.issue_cfa_asset_without_sat(
            FIRST_APPLICATION, CFA_ASSET_NAME, ASSET_DESCRIPTION, ASSET_AMOUNT,
        )

    with allure.step('Verify toaster title and message'):
        assert description == ISSUE_CFA_TOASTER_MESSAGE


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Issue cfa asset with sufficient sats but no utxo')
@allure.story('Issue cfa asset with sufficient sats and no utxo which will first create utxo and then create asset')
def test_issue_cfa_with_sufficient_sats_and_no_utxo(wallets_and_operations: WalletTestSetup):
    """
    Test issuing cfa asset with sufficient sats but no utxo.
    """

    with allure.step('Fund wallet for issue cfa asset'):
        wallets_and_operations.first_page_features.wallet_features.fund_wallet(
            FIRST_APPLICATION,
        )

    with allure.step('Verifies there is no utxo for issue cfa asset'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_view_unspents_button()
        count = wallets_and_operations.first_page_objects.view_unspent_list_page_objects.get_unspent_widget()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()
        assert count == 1

    with allure.step('Issue cfa with sufficient sats and no utxo'):
        wallets_and_operations.first_page_features.issue_cfa_features.issue_cfa_with_sufficient_sats_and_no_utxo(
            FIRST_APPLICATION, CFA_ASSET_NAME, ASSET_DESCRIPTION, ASSET_AMOUNT,
        )

    with allure.step('Verify asset name'):
        asset_name = wallets_and_operations.first_page_objects.collectible_page_objects.get_cfa_asset_name(
            CFA_ASSET_NAME,
        )
        assert asset_name == CFA_ASSET_NAME


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Issue cfa asset with sufficient sats and utxo')
@allure.story('Issue cfa asset with sufficient sats and utxo which will create asset')
def test_issue_cfa_with_sufficient_sats_and_utxo(wallets_and_operations: WalletTestSetup):
    """
    Test issuing cfa asset with sufficient sats and utxo.
    """

    with allure.step('Verified that one utxo exists for issue cfa asset'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_view_unspents_button()

        count = wallets_and_operations.first_page_objects.view_unspent_list_page_objects.get_unspent_widget()

        asset_id = wallets_and_operations.first_page_objects.view_unspent_list_page_objects.get_unspent_utxo_asset_id(
            'NA',
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()

        assert count == 3
        assert asset_id == 'NA'

    with allure.step('Issue cfa with sufficient sats and utxo'):
        wallets_and_operations.first_page_features.issue_cfa_features.issue_cfa_with_sufficient_sats_and_utxo(
            FIRST_APPLICATION, CFA_ASSET_NAME, ASSET_DESCRIPTION, ASSET_AMOUNT,
        )

    with allure.step('Verify asset name'):
        asset_name = wallets_and_operations.first_page_objects.collectible_page_objects.get_cfa_asset_name(
            CFA_ASSET_NAME,
        )
        assert asset_name == CFA_ASSET_NAME
