# pylint: disable=redefined-outer-name, unused-import,unused-argument
"""Test module for the backup page functionality"""
from __future__ import annotations

import os

import allure
import pytest
from dotenv import load_dotenv

from accessible_constant import FIRST_APPLICATION
from accessible_constant import SECOND_APPLICATION
from e2e_tests.test.utilities.app_setup import load_qm_translation
from e2e_tests.test.utilities.app_setup import test_environment
from e2e_tests.test.utilities.app_setup import wallets_and_operations
from e2e_tests.test.utilities.app_setup import WalletTestSetup
from e2e_tests.test.utilities.translation_utils import TranslationManager
from src.utils.info_message import INFO_BACKUP_COMPLETED
from src.utils.info_message import INFO_RESTORE_COMPLETED
load_dotenv()
BACKUP_EMAIL_ID = os.getenv('BACKUP_EMAIL_ID')
BACKUP_EMAIL_PASSWORD = os.getenv('BACKUP_EMAIL_PASSWORD')
MNEMONIC = None
PASSWORD = None
NIA_ASSET_ID = None
CFA_ASSET_ID = None

pytestmark = pytest.mark.order(1)
NIA_TICKER = 'N20'
NIA_NAME = 'NIA_Asset_A'
NIA_TOTAL = '200'
NIA_SEND_AMOUNT = '20'

CFA_NAME = 'CFA_Asset'
CFA_DESC = 'CFA Asset'
CFA_TOTAL = '300'
CFA_SEND_AMOUNT = '25'


@pytest.mark.skip_for_remote
@allure.feature('Mnemonic and backup configuration')
@allure.story('Mnemonic and backup configuration functionality')
def test_mnemonic_and_backup_configure(wallets_and_operations: WalletTestSetup, load_qm_translation):
    """
    Test the mnemonic and backup configuration functionality.
    This test case covers the following scenarios:
    - Create a embedded wallet
    - Copy mnemonic from setting page
    - Assert copied mnemonic with backup page mnemonic
    - Verify the backup configuration functionality
    :param wallets_and_operations: WalletTestSetup instance
    :return: None
    """
    global MNEMONIC
    global PASSWORD
    with allure.step('Create a embedded wallet'):
        wallets_and_operations.first_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations,
            FIRST_APPLICATION,
        )
        wallets_and_operations.second_page_features.wallet_features.create_and_fund_wallet(
            wallets_and_operations,
            SECOND_APPLICATION,
        )

    with allure.step('Check the backup configuration'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        backup_tooltip = wallets_and_operations.first_page_objects.fungible_page_objects.get_backup_tooltip()
        assert backup_tooltip == TranslationManager.translate(
            'backup_tooltip_text',
        )
    with allure.step('Copy mnemonic from setting page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_keyring_toggle_button()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_keyring_mnemonic_copy_button()
        MNEMONIC = wallets_and_operations.first_page_objects.keyring_dialog_page_objects.do_get_copied_address()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_keyring_password_copy_button()
        PASSWORD = wallets_and_operations.first_page_objects.keyring_dialog_page_objects.do_get_copied_address()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_cancel_button()
    with allure.step('assert copied mnemonic with backup page mnemonic'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_backup_button()
        wallets_and_operations.first_page_objects.backup_page_objects.click_show_mnemonic_button()
        mnemonic = wallets_and_operations.first_page_objects.backup_page_objects.get_mnemonic()
        assert mnemonic == MNEMONIC
        wallets_and_operations.first_page_objects.backup_page_objects.click_backup_close_button()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@allure.feature('Backup/Restore with cross-wallet transfers')
@allure.story('Issue NIA/CFA, send between wallets, send BTC, backup and restore wallet A, then assert state')
@pytest.mark.skip_for_remote
def test_transfer_btc_and_asset(wallets_and_operations: WalletTestSetup, load_qm_translation, test_environment):
    """
    Scenario:
    - Launch two apps (A and B) and fund both wallets
    - In wallet A: issue NIA and send to wallet B (amount 20)
    - In wallet B: issue CFA and send to wallet A (amount 25)
    - Send BTC from A to B
    - Backup wallet A, restart env, restore wallet A
    - Assert wallet A shows received CFA and sent NIA, and BTC history reflects send
    """
    global NIA_ASSET_ID, CFA_ASSET_ID
    with allure.step('Wallet A issues NIA'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_features.issue_nia_features.issue_nia_with_sufficient_sats_and_utxo(
            application=FIRST_APPLICATION, asset_ticker=NIA_TICKER, asset_name=NIA_NAME, asset_amount=NIA_TOTAL,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            NIA_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_copy_button()
        NIA_ASSET_ID = wallets_and_operations.first_page_operations.do_get_copied_address()
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_close_button()

    with allure.step('Wallet B generates RGB receive invoice for NIA'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        invoice_b = wallets_and_operations.second_page_features.receive_features.receive_asset_from_sidebar(
            SECOND_APPLICATION,
        )

    with allure.step('Wallet A sends NIA to wallet B'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            NIA_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.first_page_features.send_features.send(
            application=FIRST_APPLICATION, receiver_invoice=invoice_b, amount=NIA_SEND_AMOUNT,
        )

    with allure.step('Wallet B issues CFA'):
        wallets_and_operations.second_page_features.issue_cfa_features.issue_cfa_with_sufficient_sats_and_utxo(
            application=SECOND_APPLICATION, asset_name=CFA_NAME, asset_description=CFA_DESC, asset_amount=CFA_TOTAL,
        )
        wallets_and_operations.second_page_objects.sidebar_page_objects.click_collectibles_button()
        wallets_and_operations.second_page_objects.collectible_page_objects.click_cfa_frame(
            CFA_NAME,
        )
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_copy_button()
        CFA_ASSET_ID = wallets_and_operations.second_page_operations.do_get_copied_address()
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_close_button()

    with allure.step('Wallet A generates RGB receive invoice for CFA'):
        invoice_a = wallets_and_operations.first_page_features.receive_features.receive_asset_from_sidebar(
            FIRST_APPLICATION,
        )

    with allure.step('Wallet B sends CFA to wallet A'):
        wallets_and_operations.second_page_operations.do_focus_on_application(
            SECOND_APPLICATION,
        )
        wallets_and_operations.second_page_objects.sidebar_page_objects.click_collectibles_button()
        wallets_and_operations.second_page_objects.collectible_page_objects.click_cfa_frame(
            CFA_NAME,
        )
        wallets_and_operations.second_page_objects.asset_detail_page_objects.click_send_button()
        wallets_and_operations.second_page_features.send_features.send(
            application=SECOND_APPLICATION, receiver_invoice=invoice_a, amount=CFA_SEND_AMOUNT,
        )


@allure.feature('Backup page')
@allure.story('Backup page functionality')
@pytest.mark.skip_for_remote
def test_backup(test_environment, wallets_and_operations: WalletTestSetup):
    """
    Test the backup page functionality.
    This test case covers the following scenarios:
    - Create a embedded wallet
    - Configure backup
    - Take a backup of wallet
    """
    description = None
    with allure.step('Configure backup'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_backup_button()
        wallets_and_operations.first_page_objects.backup_page_objects.click_configurable_button()
        wallets_and_operations.first_page_objects.backup_page_objects.click_backup_window()
        wallets_and_operations.first_page_objects.backup_page_objects.enter_email(
            BACKUP_EMAIL_ID,
        )
        wallets_and_operations.first_page_objects.backup_page_objects.click_next_button()
        wallets_and_operations.first_page_objects.backup_page_objects.enter_password(
            BACKUP_EMAIL_PASSWORD,
        )
        wallets_and_operations.first_page_objects.backup_page_objects.click_next_button()
        try:
            wallets_and_operations.first_page_objects.backup_page_objects.click_try_another_way_button()
        except Exception as _:
            pass
        wallets_and_operations.first_page_objects.backup_page_objects.click_google_authenticator_button()
        code = wallets_and_operations.first_page_objects.backup_page_objects.get_security_otp()
        wallets_and_operations.first_page_objects.backup_page_objects.enter_security_code(
            code,
        )
        wallets_and_operations.first_page_objects.backup_page_objects.click_next_button()
        wallets_and_operations.first_page_objects.backup_page_objects.click_continue_button()
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_close_button()
    with allure.step('Take a backup of wallet'):
        wallets_and_operations.first_page_objects.backup_page_objects.click_backup_node_data_button()
        wallets_and_operations.first_page_operations.wait_for_toaster_message()
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        description = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()
        assert description == INFO_BACKUP_COMPLETED
        test_environment.restart()


@allure.feature('Restore page')
@allure.story('Restore page functionality')
@pytest.mark.skip_for_remote
def test_restore(wallets_and_operations: WalletTestSetup):
    """
    This test case is used to restore the wallet from the backup.
    """
    description = None
    with allure.step('Restore the wallet'):
        wallets_and_operations.first_page_operations.do_focus_on_application(
            FIRST_APPLICATION,
        )
        wallets_and_operations.first_page_objects.term_and_condition_page_objects.scroll_to_end()
        wallets_and_operations.first_page_objects.term_and_condition_page_objects.click_accept_button()
        wallets_and_operations.first_page_objects.wallet_selection_page_objects.click_embedded_button()
        wallets_and_operations.first_page_objects.wallet_selection_page_objects.click_continue_button()
        wallets_and_operations.first_page_objects.welcome_page_objects.click_restore_button()
        wallets_and_operations.first_page_objects.restore_wallet_page_objects.enter_mnemonic_value(
            mnemonic=MNEMONIC,
        )
        wallets_and_operations.first_page_objects.restore_wallet_page_objects.enter_password_value(
            password=PASSWORD,
        )
        wallets_and_operations.first_page_objects.restore_wallet_page_objects.click_continue_button()
        wallets_and_operations.first_page_objects.backup_page_objects.click_backup_window()
        wallets_and_operations.first_page_objects.backup_page_objects.enter_email(
            BACKUP_EMAIL_ID,
        )
        wallets_and_operations.first_page_objects.backup_page_objects.click_next_button()
        wallets_and_operations.first_page_objects.backup_page_objects.enter_password(
            BACKUP_EMAIL_PASSWORD,
        )
        wallets_and_operations.first_page_objects.backup_page_objects.click_next_button()
        try:
            wallets_and_operations.first_page_objects.backup_page_objects.click_try_another_way_button()
        except Exception as _:
            pass
        wallets_and_operations.first_page_objects.backup_page_objects.click_google_authenticator_button()
        code = wallets_and_operations.first_page_objects.backup_page_objects.get_security_otp()
        wallets_and_operations.first_page_objects.backup_page_objects.enter_security_code(
            code,
        )
        wallets_and_operations.first_page_objects.backup_page_objects.click_next_button()
        wallets_and_operations.first_page_objects.backup_page_objects.click_continue_button()
        wallets_and_operations.first_page_operations.wait_for_toaster_message()
        wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        description = wallets_and_operations.first_page_objects.toaster_page_objects.get_toaster_description()
        assert description == INFO_RESTORE_COMPLETED
        wallets_and_operations.first_page_objects.enter_wallet_password_page_objects.enter_password(
            PASSWORD,
        )
        wallets_and_operations.first_page_objects.enter_wallet_password_page_objects.click_login_button()


@allure.feature('Restore page')
@allure.story('Restore page functionality')
@pytest.mark.skip_for_remote
def test_restore_asset(wallets_and_operations: WalletTestSetup):
    """
    This test case is used to restore the wallet from the backup.
    """
    with allure.step('assert the wallet assets'):
        wallets_and_operations.first_page_objects.fungible_page_objects.click_nia_frame(
            NIA_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_copy_button()
        nia_asset_id = wallets_and_operations.first_page_operations.do_get_copied_address()
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_rgb_transaction_on_chain_frame()
        nia_transferred_amount = wallets_and_operations.first_page_objects.asset_transaction_detail_page_objects.get_transferred_amount()
        wallets_and_operations.first_page_objects.asset_transaction_detail_page_objects.click_close_button()
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_close_button()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_collectibles_button()
        wallets_and_operations.first_page_objects.collectible_page_objects.click_cfa_frame(
            CFA_NAME,
        )
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_copy_button()
        cfa_asset_id = wallets_and_operations.first_page_operations.do_get_copied_address()
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_rgb_transaction_on_chain_frame()
        cfa_transferred_amount = wallets_and_operations.first_page_objects.asset_transaction_detail_page_objects.get_transferred_amount()
        wallets_and_operations.first_page_objects.asset_transaction_detail_page_objects.click_close_button()
        wallets_and_operations.first_page_objects.asset_detail_page_objects.click_close_button()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_collectibles_button()

        assert nia_asset_id == NIA_ASSET_ID
        assert cfa_asset_id == CFA_ASSET_ID
        assert nia_transferred_amount == f'-{NIA_SEND_AMOUNT}'
        assert cfa_transferred_amount == f'+{CFA_SEND_AMOUNT}'
