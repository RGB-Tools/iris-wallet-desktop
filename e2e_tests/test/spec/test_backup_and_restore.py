# pylint: disable=redefined-outer-name, unused-import,unused-argument
"""Test module for the backup page functionality"""
from __future__ import annotations

import os

import allure
import pytest
from dotenv import load_dotenv

from accessible_constant import FIRST_APPLICATION
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

pytestmark = pytest.mark.order(1)


@pytest.mark.skip_for_remote
@pytest.mark.parametrize('test_environment', [False], indirect=True)
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
        wallets_and_operations.first_page_features.wallet_features.create_embedded_wallet(
            FIRST_APPLICATION,
        )
    with allure.step('Check the backup configuration'):
        backup_tooltip = wallets_and_operations.first_page_objects.fungible_page_objects.get_backup_tooltip()
        assert backup_tooltip == TranslationManager.translate(
            'backup_tooltip_text',
        )
    with allure.step('Copy mnemonic from setting page'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_settings_button()
        wallets_and_operations.first_page_objects.settings_page_objects.click_keyring_toggle_button()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_keyring_mnemonic_copy_button()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_keyring_password_copy_button()
        MNEMONIC = wallets_and_operations.first_page_objects.keyring_dialog_page_objects.get_keyring_mnemonic_value()
        PASSWORD = wallets_and_operations.first_page_objects.keyring_dialog_page_objects.get_keyring_password_value()
        wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_cancel_button()
        if wallets_and_operations.first_page_operations.do_is_displayed(wallets_and_operations.first_page_objects.keyring_dialog_page_objects.keyring_dialog()):
            wallets_and_operations.first_page_objects.keyring_dialog_page_objects.click_cancel_button()
    with allure.step('assert copied mnemonic with backup page mnemonic'):
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_backup_button()
        wallets_and_operations.first_page_objects.backup_page_objects.click_show_mnemonic_button()
        mnemonic = wallets_and_operations.first_page_objects.backup_page_objects.get_mnemonic()
        assert mnemonic == MNEMONIC
        wallets_and_operations.first_page_objects.backup_page_objects.click_backup_close_button()
        wallets_and_operations.first_page_objects.sidebar_page_objects.click_fungibles_button()


@allure.feature('Backup page')
@allure.story('Backup page functionality')
@pytest.mark.skip_for_remote
@pytest.mark.parametrize('test_environment', [False], indirect=True)
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
        except Exception:
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
        _, description = wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        assert description == INFO_BACKUP_COMPLETED
        test_environment.restart()


@allure.feature('Restore page')
@allure.story('Restore page functionality')
@pytest.mark.skip_for_remote
@pytest.mark.parametrize('test_environment', [False], indirect=True)
def test_restore(wallets_and_operations: WalletTestSetup):
    """
    This test case is used to restore the wallet from the backup.
    """
    description = None
    with allure.step('Restore the wallet'):
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
        except Exception:
            pass
        wallets_and_operations.first_page_objects.backup_page_objects.click_google_authenticator_button()
        code = wallets_and_operations.first_page_objects.backup_page_objects.get_security_otp()
        wallets_and_operations.first_page_objects.backup_page_objects.enter_security_code(
            code,
        )
        wallets_and_operations.first_page_objects.backup_page_objects.click_next_button()
        wallets_and_operations.first_page_objects.backup_page_objects.click_continue_button()
        wallets_and_operations.first_page_operations.wait_for_toaster_message()
        _, description = wallets_and_operations.first_page_objects.toaster_page_objects.click_toaster_frame()
        assert description == INFO_RESTORE_COMPLETED
