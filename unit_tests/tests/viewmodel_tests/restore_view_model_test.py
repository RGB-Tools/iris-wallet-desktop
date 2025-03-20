"""Tests for the RestoreViewModel class.
"""
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from enum import Enum
from unittest.mock import MagicMock

import pytest

from src.model.enums.enums_model import ToastPreset
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_GOOGLE_CONFIGURE_FAILED
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.error_message import ERROR_WHILE_RESTORE
from src.viewmodels.restore_view_model import RestoreViewModel


@pytest.fixture
def restore_view_model():
    """Fixture that creates a RestoreViewModel instance with mocked page navigation."""
    page_navigation = MagicMock()
    return RestoreViewModel(page_navigation)


def test_forward_to_fungibles_page(restore_view_model):
    """Test navigation to fungibles page."""
    # Arrange
    mock_sidebar = MagicMock()
    restore_view_model._page_navigation.sidebar.return_value = mock_sidebar

    # Act
    restore_view_model.forward_to_fungibles_page()

    # Assert
    mock_sidebar.my_fungibles.setChecked.assert_called_once_with(True)
    restore_view_model._page_navigation.enter_wallet_password_page.assert_called_once()


def test_on_success_restore_successful(restore_view_model, mocker):
    """Test successful restore with keyring storage working."""
    # Arrange
    restore_view_model.is_loading = MagicMock()
    restore_view_model.message = MagicMock()
    restore_view_model.forward_to_fungibles_page = MagicMock()
    mock_set_wallet_initialized = mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.set_wallet_initialized',
    )
    mock_set_backup_configured = mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.set_backup_configured',
    )
    mock_set_keyring_status = mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.set_keyring_status',
    )
    mocker.patch('src.utils.keyring_storage.set_value', return_value=True)
    test_network_enum = Enum(
        'TestNetworkEnum', {'TEST_NETWORK': 'test_network'},
    )
    mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.get_wallet_network',
        return_value=test_network_enum.TEST_NETWORK,
    )

    restore_view_model.mnemonic = 'test mnemonic'
    restore_view_model.password = 'test password'

    # Act
    restore_view_model.on_success(True)

    # Assert
    restore_view_model.is_loading.emit.assert_called_once_with(False)
    mock_set_wallet_initialized.assert_called_once()
    mock_set_backup_configured.assert_called_once_with(True)
    mock_set_keyring_status.assert_called_once_with(status=False)
    restore_view_model.message.emit.assert_called_once_with(
        ToastPreset.SUCCESS, 'Restore process completed.',
    )
    restore_view_model.forward_to_fungibles_page.assert_called_once()


def test_on_success_restore_failed(restore_view_model):
    """Test failed restore."""
    # Arrange
    restore_view_model.is_loading = MagicMock()
    restore_view_model.message = MagicMock()

    # Act
    restore_view_model.on_success(False)

    # Assert
    restore_view_model.is_loading.emit.assert_called_once_with(False)
    restore_view_model.message.emit.assert_called_once_with(
        ToastPreset.ERROR, ERROR_WHILE_RESTORE,
    )


def test_on_error_common_exception(restore_view_model):
    """Test error handling with CommonException."""
    # Arrange
    restore_view_model.is_loading = MagicMock()
    restore_view_model.message = MagicMock()
    error_message = 'Test error'
    error = CommonException(error_message)

    # Act
    restore_view_model.on_error(error)

    # Assert
    restore_view_model.is_loading.emit.assert_called_once_with(False)
    restore_view_model.message.emit.assert_called_once_with(
        ToastPreset.ERROR, error_message,
    )


def test_on_error_generic_exception(restore_view_model):
    """Test error handling with generic Exception."""
    # Arrange
    restore_view_model.is_loading = MagicMock()
    restore_view_model.message = MagicMock()
    error = Exception('Test error')

    # Act
    restore_view_model.on_error(error)

    # Assert
    restore_view_model.is_loading.emit.assert_called_once_with(False)
    restore_view_model.message.emit.assert_called_once_with(
        ToastPreset.ERROR, ERROR_SOMETHING_WENT_WRONG,
    )


def test_restore_google_auth_failed(restore_view_model, mocker):
    """Test restore when Google authentication fails."""
    # Arrange
    restore_view_model.is_loading = MagicMock()
    restore_view_model.message = MagicMock()
    mock_authenticate = mocker.patch(
        'src.viewmodels.restore_view_model.authenticate', return_value=False,
    )
    mock_app = MagicMock()
    mocker.patch(
        'PySide6.QtWidgets.QApplication.instance',
        return_value=mock_app,
    )

    # Act
    restore_view_model.restore('test mnemonic', 'test password')

    # Assert
    restore_view_model.is_loading.emit.assert_has_calls([
        mocker.call(True),
        mocker.call(False),
    ])
    mock_authenticate.assert_called_once_with(mock_app)
    restore_view_model.message.emit.assert_called_once_with(
        ToastPreset.ERROR,
        ERROR_GOOGLE_CONFIGURE_FAILED,
    )


def test_restore_success(restore_view_model, mocker):
    """Test successful restore flow."""
    # Arrange
    restore_view_model.is_loading = MagicMock()
    restore_view_model.run_in_thread = MagicMock()
    mock_authenticate = mocker.patch(
        'src.viewmodels.restore_view_model.authenticate', return_value=True,
    )
    mock_app = MagicMock()
    mocker.patch(
        'PySide6.QtWidgets.QApplication.instance',
        return_value=mock_app,
    )
    test_mnemonic = 'test mnemonic'
    test_password = 'test password'

    # Act
    restore_view_model.restore(test_mnemonic, test_password)

    # Assert
    restore_view_model.is_loading.emit.assert_called_once_with(True)
    mock_authenticate.assert_called_once_with(mock_app)
    assert restore_view_model.mnemonic == test_mnemonic
    assert restore_view_model.password == test_password
    restore_view_model.run_in_thread.assert_called_once()


def test_restore_generic_exception(restore_view_model, mocker):
    """Test restore handling of generic exception."""
    # Arrange
    restore_view_model.is_loading = MagicMock()
    restore_view_model.message = MagicMock()
    mocker.patch(
        'src.viewmodels.restore_view_model.authenticate',
        return_value=True,
    )
    mock_app = MagicMock()
    mocker.patch(
        'PySide6.QtWidgets.QApplication.instance',
        return_value=mock_app,
    )
    error = Exception('Unexpected error')
    restore_view_model.run_in_thread = MagicMock(side_effect=error)

    # Act
    restore_view_model.restore('test mnemonic', 'test password')

    # Assert
    restore_view_model.is_loading.emit.assert_has_calls([
        mocker.call(True),
        mocker.call(False),
    ])
    restore_view_model.message.emit.assert_called_once_with(
        ToastPreset.ERROR,
        ERROR_SOMETHING_WENT_WRONG,
    )
