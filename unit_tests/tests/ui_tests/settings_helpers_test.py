"""Unit tests for settings helper functions."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QDialog

from src.model.enums.enums_model import NetworkEnumModel
from src.views.components.settings_helpers import check_keyring_state_for_password
from src.views.components.settings_helpers import set_endpoint_based_on_network
from src.views.components.settings_helpers import set_frame_content
from src.views.components.settings_helpers import update_save_button


def test_set_endpoint_based_on_network_mainnet(mocker):
    """Test setting endpoints for mainnet network."""
    # Mock SettingRepository to return mainnet
    mocker.patch(
        'src.views.components.settings_helpers.SettingRepository.get_wallet_network',
        return_value=NetworkEnumModel.MAINNET,
    )

    # Call function
    indexer_url, proxy_endpoint, bitcoind_host, bitcoind_port = set_endpoint_based_on_network()

    # Verify correct endpoints were returned
    assert indexer_url == 'http://127.0.0.1:50003'
    assert proxy_endpoint == 'http://127.0.0.1:3002/json-rpc'
    assert bitcoind_host == 'localhost'
    assert bitcoind_port == 18447


def test_set_endpoint_based_on_network_testnet(mocker):
    """Test setting endpoints for testnet network."""
    # Mock SettingRepository to return testnet
    mocker.patch(
        'src.views.components.settings_helpers.SettingRepository.get_wallet_network',
        return_value=NetworkEnumModel.TESTNET,
    )

    # Call function
    indexer_url, proxy_endpoint, bitcoind_host, bitcoind_port = set_endpoint_based_on_network()

    # Verify correct endpoints were returned
    assert indexer_url == 'ssl://electrum.iriswallet.com:50013'
    assert proxy_endpoint == 'rpcs://proxy.iriswallet.com/0.2/json-rpc'
    assert bitcoind_host == 'electrum.iriswallet.com'
    assert bitcoind_port == 18332


def test_set_endpoint_based_on_network_testnet4(mocker):
    """Test setting endpoints for testnet4 network."""
    # Mock SettingRepository to return testnet4
    mocker.patch(
        'src.views.components.settings_helpers.SettingRepository.get_wallet_network',
        return_value=NetworkEnumModel.TESTNET4,
    )

    # Call function
    indexer_url, proxy_endpoint, bitcoind_host, bitcoind_port = set_endpoint_based_on_network()

    # Verify correct endpoints were returned
    assert indexer_url == 'ssl://electrum.iriswallet.com:50053'
    assert proxy_endpoint == 'rpcs://proxy.iriswallet.com/0.2/json-rpc'
    assert bitcoind_host == 'electrum.iriswallet.com'
    assert bitcoind_port == 48332


def test_set_endpoint_based_on_network_regtest(mocker):
    """Test setting endpoints for regtest network."""
    # Mock SettingRepository to return regtest
    mocker.patch(
        'src.views.components.settings_helpers.SettingRepository.get_wallet_network',
        return_value=NetworkEnumModel.REGTEST,
    )

    # Call function
    indexer_url, proxy_endpoint, bitcoind_host, bitcoind_port = set_endpoint_based_on_network()

    # Verify correct endpoints were returned
    assert indexer_url == 'electrum.rgbtools.org:50041'
    assert proxy_endpoint == 'rpcs://proxy.iriswallet.com/0.2/json-rpc'
    assert bitcoind_host == 'regtest-bitcoind.rgbtools.org'
    assert bitcoind_port == 80


def test_set_endpoint_based_on_network_invalid(mocker):
    """Test setting endpoints with invalid network type."""
    # Mock SettingRepository to return invalid network
    mocker.patch(
        'src.views.components.settings_helpers.SettingRepository.get_wallet_network',
        return_value='invalid_network',
    )

    # Verify ValueError is raised
    with pytest.raises(ValueError) as exc_info:
        set_endpoint_based_on_network()

    assert 'Unsupported network type' in str(exc_info.value)


def test_set_frame_content_basic():
    """Test setting frame content with basic configuration."""
    # Create mock frame and components
    mock_frame = MagicMock()
    mock_frame.input_value = MagicMock()
    mock_frame.suggestion_desc = MagicMock()
    mock_frame.time_unit_combobox = MagicMock()
    mock_frame.save_button = MagicMock()

    # Test with float input that's an integer
    set_frame_content(mock_frame, 10.0, 'hours')
    mock_frame.input_value.setText.assert_called_with('10')
    mock_frame.input_value.setPlaceholderText.assert_called_with('10')
    mock_frame.suggestion_desc.hide.assert_called_once()
    mock_frame.time_unit_combobox.hide.assert_called_once()


def test_set_frame_content_with_validator():
    """Test setting frame content with validator."""
    mock_frame = MagicMock()
    mock_validator = MagicMock()

    set_frame_content(mock_frame, 10, 'hours', validator=mock_validator)
    mock_frame.input_value.setValidator.assert_called_with(mock_validator)


def test_set_frame_content_with_time_unit_combobox():
    """Test setting frame content with time unit combobox."""
    mock_frame = MagicMock()
    mock_combobox = MagicMock()
    mock_combobox.findText.return_value = 1

    set_frame_content(
        mock_frame, 10, 'hours', time_unit_combobox=mock_combobox,
    )
    mock_combobox.setCurrentIndex.assert_called_with(1)


def test_update_save_button_value_changed():
    """Test updating save button when input value has changed."""
    mock_frame = MagicMock()
    mock_frame.input_value.text.return_value = '20'
    mock_frame.time_unit_combobox.currentText.return_value = 'hours'

    update_save_button(mock_frame, '10', 'hours')
    mock_frame.save_button.setDisabled.assert_called_with(False)


def test_update_save_button_value_unchanged():
    """Test updating save button when input value hasn't changed."""
    mock_frame = MagicMock()
    mock_frame.input_value.text.return_value = '10'
    mock_frame.time_unit_combobox.currentText.return_value = 'hours'

    update_save_button(mock_frame, '10', 'hours')
    mock_frame.save_button.setDisabled.assert_called_with(True)


def test_update_save_button_time_unit_changed():
    """Test updating save button with time unit change."""
    mock_frame = MagicMock()
    mock_frame.input_value.text.return_value = '10'
    mock_frame.time_unit_combobox.currentText.return_value = 'hours'

    update_save_button(
        mock_frame, '10', 'minutes', mock_frame.time_unit_combobox,
    )
    mock_frame.save_button.setDisabled.assert_called_with(False)


def test_check_keyring_state_disabled(mocker):
    """Test checking keyring state when keyring is disabled."""
    # Mock dependencies
    mocker.patch(
        'src.views.components.settings_helpers.SettingRepository.get_keyring_status',
        return_value=False,
    )
    mocker.patch(
        'src.views.components.settings_helpers.SettingRepository.get_wallet_network',
        return_value=NetworkEnumModel.MAINNET,
    )
    mock_get_value = mocker.patch(
        'src.views.components.settings_helpers.get_value',
        return_value='test_password',
    )

    # Call function
    result = check_keyring_state_for_password(None, None)

    # Verify password was retrieved from storage
    mock_get_value.assert_called_once_with('wallet_password', 'mainnet')
    assert result == 'test_password'


def test_check_keyring_state_enabled_accepted(mocker):
    """Test checking keyring state when keyring is enabled and dialog is accepted."""
    # Mock dependencies
    mocker.patch(
        'src.views.components.settings_helpers.SettingRepository.get_keyring_status',
        return_value=True,
    )
    mock_dialog = MagicMock()
    mock_dialog.exec.return_value = QDialog.Accepted
    mock_dialog.password_input.text.return_value = 'dialog_password'
    mock_dialog_class = mocker.patch(
        'src.views.components.settings_helpers.RestoreMnemonicWidget',
        return_value=mock_dialog,
    )

    # Call function
    parent_mock = MagicMock()
    view_model_mock = MagicMock()
    result = check_keyring_state_for_password(parent_mock, view_model_mock)

    # Verify dialog was created with correct parameters
    mock_dialog_class.assert_called_once_with(
        parent=parent_mock,
        view_model=view_model_mock,
        origin_page='setting_card',
        mnemonic_visibility=False,
    )

    # Verify dialog was configured correctly
    mock_dialog.mnemonic_detail_text_label.setText.assert_called_once()
    mock_dialog.mnemonic_detail_text_label.setFixedHeight.assert_called_once_with(
        40,
    )

    # Verify password was retrieved from dialog
    assert result == 'dialog_password'


def test_check_keyring_state_enabled_rejected(mocker):
    """Test checking keyring state when keyring is enabled and dialog is rejected."""
    # Mock dependencies
    mocker.patch(
        'src.views.components.settings_helpers.SettingRepository.get_keyring_status',
        return_value=True,
    )
    mock_dialog = MagicMock()
    mock_dialog.exec.return_value = QDialog.Rejected
    mocker.patch(
        'src.views.components.settings_helpers.RestoreMnemonicWidget',
        return_value=mock_dialog,
    )

    # Call function
    result = check_keyring_state_for_password(None, None)

    # Verify None is returned when dialog is rejected
    assert result is None
