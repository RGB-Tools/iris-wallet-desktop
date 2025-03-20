# pylint: disable=redefined-outer-name, unused-import
"""Test module for help page"""
from __future__ import annotations

import allure
import pytest

from accessible_constant import FIRST_APPLICATION
from accessible_constant import FIRST_APPLICATION_URL
from e2e_tests.test.utilities.app_setup import load_qm_translation
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.model import WalletTestSetup
from e2e_tests.test.utilities.translation_utils import TranslationManager


@pytest.mark.parametrize('test_environment', [False], indirect=True)
@allure.feature('Help page test')
@allure.story('Tests for elements in help page')
def test_help_page(wallets_and_operations: WalletTestSetup):
    """Test help page"""
    with allure.step('Initialize the wallet'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations, FIRST_APPLICATION, FIRST_APPLICATION_URL, fund=False,
        )

    with allure.step('Navigating to help page'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_help_button()

    with allure.step('clicking the first card'):
        wallets_and_operations.first_page_objects.help_page_objects.click_learn_about_rgb()
        help_card_1_title = wallets_and_operations.first_page_objects.help_page_objects.get_learn_about_rgb_frame_title()

        assert help_card_1_title == TranslationManager.translate(
            'where_can_i_learn_more_about_rgb',
        )

    with allure.step('clicking the second card'):
        wallets_and_operations.first_page_objects.help_page_objects.click_bitcoin_txn()
        help_card_2_title = wallets_and_operations.first_page_objects.help_page_objects.get_bitcoin_txn_frame_label()

        assert help_card_2_title == TranslationManager.translate(
            'why_do_i_see_outgoing_bitcoin_transactions_that_i_did_not_authorize',
        )

    with allure.step('clicking the third card'):
        wallets_and_operations.first_page_objects.help_page_objects.click_minimum_balance()
        help_card_3_title = wallets_and_operations.first_page_objects.help_page_objects.get_minimum_balance_frame_title()

        assert help_card_3_title == TranslationManager.translate(
            'what_is_the_minimum_bitcoin_balance_needed_to_issue_and_receive_rgb_assets',
        )

    with allure.step('clicking the forth card'):
        wallets_and_operations.first_page_objects.help_page_objects.click_support_and_feedback()
        help_card_4_title = wallets_and_operations.first_page_objects.help_page_objects.get_support_and_feedback_title()

        assert help_card_4_title == TranslationManager.translate(
            'where_can_i_send_feedback_or_ask_for_support',
        )

    with allure.step('clicking the fifth card'):
        wallets_and_operations.first_page_objects.help_page_objects.click_regtest_bitcoin()
        help_card_5_title = wallets_and_operations.first_page_objects.help_page_objects.get_regtest_bitcoin_frame_title()

        assert help_card_5_title == TranslationManager.translate(
            'where_can_i_get_regtest_bitcoins',
        )
