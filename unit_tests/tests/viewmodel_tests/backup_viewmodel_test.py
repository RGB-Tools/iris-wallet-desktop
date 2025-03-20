"""Unit test for backup view model"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import Mock

import pytest

from src.data.repository.setting_repository import SettingRepository
from src.data.service.backup_service import BackupService
from src.model.enums.enums_model import NetworkEnumModel
from src.utils.constant import MNEMONIC_KEY
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.handle_exception import CommonException
from src.utils.info_message import INFO_BACKUP_COMPLETED
from src.utils.info_message import INFO_BACKUP_COMPLETED_KEYRING_LOCKED
from src.viewmodels.backup_view_model import BackupViewModel
from src.views.components.toast import ToastManager


@pytest.fixture
def mock_page_navigation(mocker):
    """Fixture to create a mock page navigation object."""
    return mocker.MagicMock()


@pytest.fixture
def backup_view_model(mock_page_navigation):
    """Fixture to create an instance of the BackupViewModel class."""
    return BackupViewModel(mock_page_navigation)


def test_on_success(backup_view_model, mocker):
    """Test for on_success method"""
    mock_is_loading = Mock()
    mock_toast = mocker.patch.object(ToastManager, 'info')
    mock_toast_error = mocker.patch.object(ToastManager, 'error')

    backup_view_model.is_loading.connect(mock_is_loading)

    # Test successful backup
    backup_view_model.on_success(True)
    mock_is_loading.assert_called_with(False)
    mock_toast.assert_called_once_with(description=INFO_BACKUP_COMPLETED)

    # Test failed backup
    backup_view_model.on_success(False)
    mock_toast_error.assert_called_once()


def test_on_error(backup_view_model, mocker):
    """Test for on_error method"""
    mock_is_loading = Mock()
    mock_toast = mocker.patch.object(ToastManager, 'error')

    backup_view_model.is_loading.connect(mock_is_loading)

    error = CommonException('Test error')
    backup_view_model.on_error(error)

    mock_is_loading.assert_called_once_with(False)
    mock_toast.assert_called_once_with(description=error.message)


def test_backup_when_keyring_unaccessible(backup_view_model, mocker):
    """Test backup_when_keyring_unaccessible method"""
    SettingRepository.get_wallet_network = MagicMock(
        return_value='test_network',
    )
    mock_run_thread = mocker.patch.object(
        backup_view_model, 'run_backup_service_thread',
    )

    backup_view_model.backup_when_keyring_unaccessible(
        'test_mnemonic', 'test_password',
    )

    mock_run_thread.assert_called_once_with(
        mnemonic='test_mnemonic',
        password='test_password',
        is_keyring_accessible=False,
    )


def test_on_success_from_backup_page(backup_view_model, mocker):
    """Test on_success_from_backup_page method"""
    mock_toast = mocker.patch.object(ToastManager, 'success')

    backup_view_model.on_success_from_backup_page()

    mock_toast.assert_called_once_with(
        description=INFO_BACKUP_COMPLETED_KEYRING_LOCKED,
    )
    backup_view_model._page_navigation.enter_wallet_password_page.assert_called_once()


def test_run_backup_service_thread(backup_view_model, mocker):
    """Test run_backup_service_thread method"""
    mock_run_in_thread = mocker.patch.object(
        backup_view_model, 'run_in_thread',
    )
    mock_is_loading = Mock()
    backup_view_model.is_loading.connect(mock_is_loading)

    backup_view_model.run_backup_service_thread(
        'test_mnemonic', 'test_password',
    )

    mock_is_loading.assert_called_once_with(True)
    mock_run_in_thread.assert_called_once()
    assert mock_run_in_thread.call_args[0][0] is BackupService.backup


def test_backup(backup_view_model, mocker):
    """Test the backup method"""
    # Mock dependencies
    mock_get_wallet_network = mocker.patch.object(
        SettingRepository, 'get_wallet_network',
    )
    mock_get_value = mocker.patch('src.viewmodels.backup_view_model.get_value')
    mock_run_backup_service_thread = mocker.patch.object(
        backup_view_model, 'run_backup_service_thread',
    )

    # Set mock return values
    mock_get_wallet_network.return_value = NetworkEnumModel.MAINNET
    mock_get_value.side_effect = lambda key=None, network=None: {
        (MNEMONIC_KEY, NetworkEnumModel.MAINNET.value): 'mock_mnemonic',
        (WALLET_PASSWORD_KEY, NetworkEnumModel.MAINNET.value): 'mock_password',
    }[(key, network)]

    # Call the method under test
    backup_view_model.backup()

    # Assertions
    mock_get_wallet_network.assert_called_once()
    mock_get_value.assert_any_call(
        MNEMONIC_KEY, NetworkEnumModel.MAINNET.value,
    )
    mock_get_value.assert_any_call(
        key=WALLET_PASSWORD_KEY, network=NetworkEnumModel.MAINNET.value,
    )
    mock_run_backup_service_thread.assert_called_once_with(
        mnemonic='mock_mnemonic',
        password='mock_password',
    )
