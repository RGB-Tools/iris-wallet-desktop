# pylint: disable=redefined-outer-name, unused-import, unused-argument
"""Iris wallet send and receive operation automation test suite for nia asset"""
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
from src.model.enums.enums_model import TransactionStatusEnumModel

ASSET_TICKER = 'TTK'
NIA_ASSET_NAME = 'Tether'
ASSET_AMOUNT = '2000'
SEND_AMOUNT = '50'
INVOICE = 'rgb:~/~/utxob:2msKeFq-uPjwpYxVY-jKS2ymYBq-SqmyP3ovg-AGvth8491-J7seMBm?expiry=1709616110&endpoints=rpc://10.0.2.2:3000/json-rpc'


@allure.feature('Automation of send operation for NIA asset in iris wallet')
@allure.story('Testing send NIA asset with expired invoice')
def test_send_nia_with_expired_invoice(wallets_and_operations: WalletTestSetup, load_qm_translation):
    """Test send nia asset with expired invoice"""
    validation_label = None

    with allure.step('Create and fund first wallet for send and receive nia'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=FIRST_APPLICATION, application_url=FIRST_APPLICATION_URL,
        )
    with allure.step('Create and fund second wallet for send and receive nia'):
        wallets_and_operations.second_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations=wallets_and_operations, application=SECOND_APPLICATION, application_url=SECOND_APPLICATION_URL,
        )

    with allure.step('Issue NIA asset'):
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            application=FIRST_APPLICATION, asset_ticker=ASSET_TICKER, asset_name=NIA_ASSET_NAME, asset_amount=ASSET_AMOUNT,
        )

    with allure.step('Send NIA asset with expired invoice'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            NIA_ASSET_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.first_page_objects.send_asset_page_objects.enter_asset_invoice(
            INVOICE,
        )
        validation_label = wallets_and_operations.first_page_objects.send_asset_page_objects.get_asset_address_validation_label()
        wallets_and_operations.first_page_objects.send_asset_page_objects.click_send_asset_close_button()

    with allure.step('Verify error message for nia asset'):
        assert validation_label == TranslationManager.translate(
            'invalid_invoice',
        )


@allure.feature('Automation of receive, send, and transaction status for NIA asset in iris wallet')
@allure.story('End-to-End testing of receiving, sending, and verifying transaction status for NIA asset')
def test_send_and_receive_nia_asset_operation(wallets_and_operations: WalletTestSetup):
    """Test send and receive operation for nia asset"""

    with allure.step('Issue NIA asset'):
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            application=FIRST_APPLICATION, asset_ticker=ASSET_TICKER, asset_name=NIA_ASSET_NAME, asset_amount=ASSET_AMOUNT,
        )

    with allure.step('Generate invoice'):
        invoice = wallets_and_operations.second_page_features.receive_features.receive_asset_from_sidebar(
            SECOND_APPLICATION,
        )

    with allure.step('Send NIA asset'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            NIA_ASSET_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.first_page_features.send_features.send(
            application=FIRST_APPLICATION, receiver_invoice=invoice, amount=SEND_AMOUNT,
        )

    with allure.step('Verify transaction status'):
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            NIA_ASSET_NAME,
        )
        actual_transfer_status = wallets_and_operations.first_page_objects.asset_detail_page_objects.get_transfer_status()
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_close_button()

    with allure.step('Verify received amount'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.fungible_page_objects.click_refresh_button()
        wallets_and_operations.second_page_objects.fungible_page_objects.click_nia_frame(
            NIA_ASSET_NAME,
        )
        received_amount = wallets_and_operations.second_page_objects.asset_detail_page_objects.get_on_chain_total_balance()
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_close_button()

    with allure.step('Verify assertions'):
        assert received_amount == SEND_AMOUNT
        assert actual_transfer_status == TransactionStatusEnumModel.WAITING_COUNTERPARTY.value
