# pylint: disable=redefined-outer-name, unused-import
"""
Tests for view unspent list.
"""
from __future__ import annotations

import allure
import pytest

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('View unspent list')
@allure.story('Verify outpoint in unspent list')
def test_view_unspent_list(wallets_and_operations: WalletTestSetup):
    """
    Test view unspent list.
    """

    with allure.step('Create and fund first wallet for view unspent'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL,
        )

    with allure.step('verifies the outpoint'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_view_unspents_button()
        wallets_and_operations.first_page_objects.view_unspent_list_page_objects.click_unspent_frame()
        actual_outpoint = wallets_and_operations.first_page_objects.view_unspent_list_page_objects.get_unspent_utxo_outpoint()
        outpoint = wallets_and_operations.first_page_operations.do_get_copied_address()

        assert actual_outpoint == outpoint
