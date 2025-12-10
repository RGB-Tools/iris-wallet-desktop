"""This module contains the test fixtures for the setting repository."""
from __future__ import annotations

import pytest


@pytest.fixture
def mock_get_wallet_type(mocker):
    """Mocked get wallet type"""
    def _mock_get_wallet_type(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.get_wallet_type',
            return_value=value,
        )

    return _mock_get_wallet_type


@pytest.fixture
def mock_set_wallet_type(mocker):
    """Mocked set wallet type"""
    def _mock_set_wallet_type(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.set_wallet_type',
            return_value=value,
        )

    return _mock_set_wallet_type


@pytest.fixture
def mock_get_wallet_network(mocker):
    """Mocked get wallet network"""
    def _mock_get_wallet_network(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.get_wallet_network',
            return_value=value,
        )

    return _mock_get_wallet_network


@pytest.fixture
def mock_is_wallet_initialized(mocker):
    """Mocked is wallet initialized"""
    def _mock_is_wallet_initialized(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.is_wallet_initialized',
            return_value=value,
        )

    return _mock_is_wallet_initialized


@pytest.fixture
def mock_set_wallet_initialized(mocker):
    """Mocked set wallet initialized"""
    def _mock_set_wallet_initialized(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.set_wallet_initialized',
            return_value=value,
        )

    return _mock_set_wallet_initialized


@pytest.fixture
def mock_unset_wallet_initialized(mocker):
    """Mocked unset wallet initialized"""
    def _mock_unset_wallet_initialized(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.unset_wallet_initialized',
            return_value=value,
        )

    return _mock_unset_wallet_initialized


@pytest.fixture
def mock_is_backup_configured(mocker):
    """Mocked is backup configured"""
    def _mock_is_backup_configured(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.is_backup_configured',
            return_value=value,
        )

    return _mock_is_backup_configured


@pytest.fixture
def mock_set_backup_configured(mocker):
    """Mocked set backup configured"""
    def _mock_set_backup_configured(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.set_backup_configured',
            return_value=value,
        )

    return _mock_set_backup_configured


@pytest.fixture
def mock_is_exhausted_asset_enabled(mocker):
    """Mocked is exhausted asset enabled"""
    def _mock_is_exhausted_asset_enabled(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.is_exhausted_asset_enabled',
            return_value=value,
        )

    return _mock_is_exhausted_asset_enabled


@pytest.fixture
def mock_enable_exhausted_asset(mocker):
    """Mocked enable exhausted asset"""
    def _mock_enable_exhausted_asset(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.enable_exhausted_asset',
            return_value=value,
        )

    return _mock_enable_exhausted_asset


@pytest.fixture
def mock_is_show_hidden_assets_enabled(mocker):
    """Mocked is show hidden assets enabled"""
    def _mock_is_show_hidden_assets_enabled(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.is_show_hidden_assets_enabled',
            return_value=value,
        )

    return _mock_is_show_hidden_assets_enabled


@pytest.fixture
def mock_enable_show_hidden_asset(mocker):
    """Mocked enable show hidden asset"""
    def _mock_enable_show_hidden_asset(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.enable_show_hidden_asset',
            return_value=value,
        )

    return _mock_enable_show_hidden_asset


@pytest.fixture
def mock_set_keyring_status(mocker):
    """Mocked set keyring status"""
    def _mock_set_keyring_status(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.set_keyring_status',
            return_value=value,
        )

    return _mock_set_keyring_status


@pytest.fixture
def mock_get_keyring_status(mocker):
    """Mocked get keyring status"""
    def _mock_get_keyring_status(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.get_keyring_status',
            return_value=value,
        )

    return _mock_get_keyring_status


@pytest.fixture
def mock_get_native_authentication_status(mocker):
    """Mocked get native authentication status"""
    def _mock_get_native_authentication_status(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.get_native_authentication_status',
            return_value=value,
        )

    return _mock_get_native_authentication_status


@pytest.fixture
def mock_set_native_authentication_status(mocker):
    """Mocked set native authentication status"""
    def _mock_set_native_authentication_status(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.set_native_authentication_status',
            return_value=value,
        )

    return _mock_set_native_authentication_status


@pytest.fixture
def mock_native_login_enabled(mocker):
    """Mocked native login enabled"""
    def _mock_native_login_enabled(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.native_login_enabled',
            return_value=value,
        )

    return _mock_native_login_enabled


@pytest.fixture
def mock_enable_logging_native_authentication(mocker):
    """Mocked enable logging native authentication"""
    def _mock_enable_logging_native_authentication(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.enable_logging_native_authentication',
            return_value=value,
        )

    return _mock_enable_logging_native_authentication


@pytest.fixture
def mock_native_authentication(mocker):
    """Mocked native authentication"""
    def _mock_native_authentication(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.native_authentication',
            return_value=value,
        )

    return _mock_native_authentication


@pytest.fixture
def mock_get_ln_endpoint(mocker):
    """Mocked get LN endpoint"""
    def _mock_get_ln_endpoint(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.get_ln_endpoint',
            return_value=value,
        )

    return _mock_get_ln_endpoint


@pytest.fixture
def mock_get_config_value(mocker):
    """Mocked get config value"""
    def _mock_get_config_value(value):
        return mocker.patch(
            'src.data.repository.setting_repository.SettingRepository.get_config_value',
            return_value=value,
        )

    return _mock_get_config_value


@pytest.fixture
def mock_get_value(mocker):
    """Mocked get value"""
    def _mock_get_value(value):
        return mocker.patch(
            'src.utils.keyring_storage.get_value',
            return_value=value,
        )

    return _mock_get_value


@pytest.fixture
def mock_set_value(mocker):
    """Mocked set value"""
    def _mock_set_value(value):
        return mocker.patch(
            'src.utils.keyring_storage.set_value',
            return_value=value,
        )

    return _mock_set_value


@pytest.fixture
def mock_handle_exceptions(mocker):
    """Mocked handle exceptions"""
    def _mock_handle_exceptions(value):
        return mocker.patch(
            'src.utils.handle_exception.handle_exceptions',
            return_value=value,
        )

    return _mock_handle_exceptions


@pytest.fixture
def mock_window_native_authentication(mocker):
    """Mocked Window native authentication"""
    def _mock_window_native_authentication(value):
        return mocker.patch(
            'src.utils.native_windows_auth.WindowNativeAuthentication.start_windows_native_auth',
            return_value=value,
        )

    return _mock_window_native_authentication
