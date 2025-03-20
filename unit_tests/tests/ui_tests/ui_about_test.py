"""Unit test for about UI"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

import os
import shutil
import sys
import zipfile
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QDir
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from src.model.enums.enums_model import WalletType
from src.utils.common_utils import network_info
from src.utils.constant import ANNOUNCE_ALIAS
from src.utils.constant import BITCOIND_RPC_HOST_REGTEST
from src.utils.constant import BITCOIND_RPC_PASSWORD_REGTEST
from src.utils.constant import BITCOIND_RPC_PORT_REGTEST
from src.utils.constant import BITCOIND_RPC_USER_REGTEST
from src.utils.constant import SAVED_ANNOUNCE_ADDRESS
from src.utils.constant import SAVED_ANNOUNCE_ALIAS
from src.utils.constant import SAVED_BITCOIND_RPC_HOST
from src.utils.constant import SAVED_BITCOIND_RPC_PASSWORD
from src.utils.constant import SAVED_BITCOIND_RPC_PORT
from src.utils.constant import SAVED_BITCOIND_RPC_USER
from src.utils.custom_exception import CommonException
from src.utils.info_message import INFO_DOWNLOAD_CANCELED
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.toast import ToastManager
from src.views.components.toast import ToastPreset
from src.views.ui_about import AboutWidget


@pytest.fixture
def mock_about_view_model():
    """Fixture to create a MainViewModel instance."""
    return MainViewModel(MagicMock())  # Mock the page navigation


@pytest.fixture
def about_widget(mock_about_view_model, qtbot, mocker):
    """Fixture to create the AboutWidget instance with mocked dependencies."""
    mock_config_values = {
        'password': 'test_password',
        'bitcoind_rpc_username': 'test_user',
        'bitcoind_rpc_password': 'password',
        'bitcoind_rpc_host': 'test_host',
        'bitcoind_rpc_port': 18443,
        'indexer_url': 'test_url',
        'proxy_endpoint': 'test_endpoint',
        'announce_addresses': 'pub.addr.example.com:9735',
        'announce_alias': 'nodeAlias',
    }

    with patch('src.data.repository.setting_repository.SettingRepository.get_wallet_type') as mock_get_wallet_type, \
            patch('src.utils.local_store.local_store.get_value') as mock_get_value, \
            patch('src.views.ui_about.NodeInfoModel') as mock_node_info_model, \
            patch('src.utils.common_utils.zip_logger_folder') as mock_zip_logger_folder, \
            patch('src.utils.helpers.SettingRepository.get_config_value') as mock_get_config_value:

        mock_get_wallet_type.return_value = WalletType.EMBEDDED_TYPE_WALLET
        mock_get_value.return_value = True
        mock_node_info = mock_node_info_model.return_value
        mock_node_info.node_info = type(
            'NodeInfo', (), {
                'pubkey': '02270dadcd6e7ba0ef707dac72acccae1a3607453a8dd2aef36ff3be4e0d31f043',
            },
        )
        mock_zip_logger_folder.return_value = (
            '/mock/logs.zip', '/mock/output/dir',
        )

        mock_get_config_value.side_effect = lambda key, default=None: mock_config_values.get(
            key, default,
        )

        widget = AboutWidget(mock_about_view_model)
        qtbot.addWidget(widget)

    return widget


def test_widget_initialization(about_widget):
    """Test the initialization of the widget."""
    assert isinstance(about_widget.app_version_label, QLabel)
    assert about_widget.app_version_label.text().startswith('app_version')


def test_retranslate_ui(about_widget):
    """Test the retranslate_ui method."""
    about_widget.retranslate_ui()
    assert 'privacy_policy' in about_widget.privacy_policy_label.text()
    assert 'terms_of_service' in about_widget.terms_service_label.text()


def test_download_logs_button_click(about_widget, qtbot, mocker):
    """Test the download_logs button click event."""
    mock_download_logs = mocker.patch.object(about_widget, 'download_logs')
    qtbot.mouseClick(about_widget.download_log, Qt.LeftButton)
    mock_download_logs.assert_called_once()


def test_network_info_success(about_widget, mocker):
    """Test the network_info method with successful network retrieval."""
    mock_network = mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.get_wallet_network',
    )
    mock_network.return_value.value = 'testnet'
    network_info(about_widget)
    assert about_widget.network == 'testnet'


def test_network_info_common_exception(about_widget, mocker):
    """Test the network_info method with a CommonException."""
    mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.get_wallet_network',
        side_effect=CommonException('Test exception'),
    )

    mock_toast = mocker.patch(
        'src.views.components.toast.ToastManager.error',
    )
    network_info(about_widget)

    assert about_widget.network == 'regtest'
    mock_toast.assert_called_once_with(
        parent=None, title=None, description='Test exception',
    )


def test_network_info_generic_exception(about_widget, mocker):
    """Test the network_info method with a generic exception."""
    mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.get_wallet_network',
        side_effect=Exception('Generic error'),
    )

    mock_toast = mocker.patch(
        'src.views.components.toast.ToastManager.error',
    )
    network_info(about_widget)

    assert about_widget.network == 'regtest'
    mock_toast.assert_called_once_with(
        parent=None, title=None, description='Something went wrong',
    )


def test_ldk_port_visibility(about_widget, mocker):
    """Test if LDK port frame is visible for embedded wallet type."""
    mock_wallet_type = mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.get_wallet_type',
    )
    mock_wallet_type.return_value = WalletType.EMBEDDED_TYPE_WALLET

    mock_node_info = mocker.patch('src.views.ui_about.NodeInfoModel')
    mock_node_info.node_info = type(
        'NodeInfo', (), {
            'pubkey': '02270dadcd6e7ba0ef707dac72acccae1a3607453a8dd2aef36ff3be4e0d31f043',
        },
    )
    # Reinitialize the widget to reflect changes
    about_widget = AboutWidget(about_widget._view_model)
    assert about_widget.ldk_port_frame is not None


def test_announce_addresses_empty(about_widget):
    """Test behavior when announce_addresses is empty."""
    about_widget.get_bitcoin_config.announce_addresses = []
    about_widget.retranslate_ui()
    assert not hasattr(about_widget, 'announce_address_frame')


def test_announce_alias_empty(about_widget):
    """Test behavior when announce_alias is the default value."""
    about_widget.get_bitcoin_config.announce_alias = 'DefaultAlias'
    about_widget.retranslate_ui()
    assert not hasattr(about_widget, 'announce_alias_frame')


def test_download_logs_with_save_path(about_widget, qtbot, mocker):
    """Test the download_logs method when a save path is provided."""
    # Mock dependencies
    base_path = '/mock/base/path'
    mock_get_path = mocker.patch(
        'src.utils.local_store.local_store.get_path', return_value=base_path,
    )

    # Mock filesystem operations
    mocker.patch('os.makedirs')
    mock_rmtree = mocker.patch('shutil.rmtree')  # Mock directly
    mocker.patch('shutil.make_archive')
    mocker.patch('os.stat')
    mocker.patch('os.path.isdir', return_value=False)
    mocker.patch('shutil.copy')
    mocker.patch(
        'os.walk', return_value=[
            ('/mock/output/dir', [], ['file1', 'file2']),
        ],
    )
    mocker.patch('zipfile.ZipFile', autospec=True)

    # Mock download_file to ensure it's called
    def mock_download_file(save_path, output_dir):
        # Simulate the behavior of the actual download_file function
        with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zip_file.write(file_path, arcname)
        # Simulate the finally block
        shutil.rmtree(output_dir)
        # Simulate success toast
        ToastManager.success(description='Logs saved successfully.')

    mocker.patch(
        'src.views.ui_about.download_file',
        side_effect=mock_download_file,
    )

    # Mock zip_logger_folder at the module level
    zip_filename = 'mock/logs.zip'
    output_dir = '/mock/output/dir'
    mock_zip_logger = mocker.patch(
        'src.views.ui_about.zip_logger_folder', autospec=True,
    )
    mock_zip_logger.return_value = (zip_filename, output_dir)

    # Mock file dialog
    save_path = '/mock/save/path.zip'
    mock_file_dialog = mocker.patch(
        'PySide6.QtWidgets.QFileDialog.getSaveFileName',
        return_value=(save_path, 'Zip Files (*.zip)'),
    )

    # Mock ToastManager
    mock_toast_success = mocker.patch(
        'src.views.components.toast.ToastManager.success',
    )
    mock_toast_error = mocker.patch(
        'src.views.components.toast.ToastManager.error',
    )

    # Call the method
    about_widget.download_logs()

    # Verify calls
    mock_get_path.assert_called_once()
    mock_zip_logger.assert_called_once_with(base_path)
    mock_file_dialog.assert_called_once_with(
        about_widget, 'Save logs File', QDir.homePath(
        )+'/'+zip_filename, 'Zip Files (*.zip)',
    )
    mock_rmtree.assert_called_once_with(output_dir)
    mock_toast_error.assert_not_called()
    mock_toast_success.assert_called_once()


def test_download_logs_cancelled(about_widget, qtbot, mocker):
    """Test the download_logs method when the user cancels the save dialog."""
    # Mock dependencies
    base_path = '/mock/base/path'
    mock_get_path = mocker.patch(
        'src.utils.local_store.local_store.get_path', return_value=base_path,
    )

    # Mock filesystem operations
    mocker.patch('os.makedirs')
    mock_rmtree = mocker.patch('shutil.rmtree')  # Mock directly
    mocker.patch('shutil.make_archive')
    mocker.patch('os.stat')
    mocker.patch('os.path.isdir', return_value=False)
    mocker.patch('shutil.copy')

    # Mock zip_logger_folder at the module level
    zip_filename = 'mock/logs.zip'
    output_dir = '/mock/output/dir'
    mock_zip_logger = mocker.patch(
        'src.views.ui_about.zip_logger_folder', autospec=True,
    )
    mock_zip_logger.return_value = (zip_filename, output_dir)

    # Mock file dialog to simulate cancellation
    mock_file_dialog = mocker.patch(
        'PySide6.QtWidgets.QFileDialog.getSaveFileName',
        return_value=('', ''),
    )

    # Mock ToastManager
    mock_toast = mocker.patch(
        'src.views.components.toast.ToastManager.show_toast',
    )

    # Call the method
    about_widget.download_logs()

    # Verify calls
    mock_get_path.assert_called_once()
    mock_zip_logger.assert_called_once_with(base_path)
    mock_file_dialog.assert_called_once_with(
        about_widget, 'Save logs File', QDir.homePath(
        )+'/'+zip_filename, 'Zip Files (*.zip)',
    )
    # rmtree should not be called if download is cancelled
    mock_rmtree.assert_not_called()
    mock_toast.assert_called_once_with(
        about_widget,
        ToastPreset.ERROR,
        description=INFO_DOWNLOAD_CANCELED,
    )


def test_download_logs_button_functionality(about_widget, qtbot, mocker):
    """Test that the download logs button triggers the download_logs method."""
    # Mock the download_logs method
    mock_download_logs = mocker.patch.object(about_widget, 'download_logs')

    # Click the download button
    qtbot.mouseClick(about_widget.download_log, Qt.LeftButton)

    # Verify the method was called
    mock_download_logs.assert_called_once()


@pytest.fixture
def mock_node_info_model(mocker):
    """Fixture to provide a mocked NodeInfoModel."""
    mock_model = mocker.patch('src.views.ui_about.NodeInfoModel')
    mock_model.return_value.node_info = type(
        'NodeInfo', (), {'pubkey': 'mock_pubkey'},
    )
    return mock_model


@pytest.fixture
def mock_node_info_widget(mocker):
    """Fixture to provide a mocked NodeInfoWidget."""
    # Try to find where NodeInfoWidget is imported from
    for name, module in sys.modules.items():
        if hasattr(module, 'NodeInfoWidget'):
            print(f"Found NodeInfoWidget in module: {name}")

    # Mock NodeInfoWidget where it's actually found
    mock = mocker.patch(
        'src.views.components.wallet_detail_frame.NodeInfoWidget', autospec=True,
    )
    mock_instance = mock.return_value
    mock_instance.key_label = mocker.MagicMock()
    mocker.patch('src.views.ui_about.NodeInfoWidget', mock)
    mock_instance = mock.return_value
    mock_instance.node_pub_key_copy_button = mocker.Mock()
    mock_instance.value_label = mocker.Mock()
    # Print mock details
    print(f"Created mock with id: {id(mock)}")

    return mock


@pytest.fixture
def mock_bitcoin_config(mocker):
    """Fixture to provide a mocked bitcoin config."""
    mock_config = mocker.MagicMock()
    mock_config.announce_addresses = []  # Default value
    mock_config.announce_alias = ANNOUNCE_ALIAS  # Default value
    return mock_config


def test_announce_addresses_custom(about_widget, mocker, mock_node_info_widget, mock_node_info_model, mock_bitcoin_config):
    """Test behavior when announce_addresses is not the default value."""
    # Set up the mock for announce_addresses with a different value
    custom_address = 'CustomAddress'

    # Mock SettingRepository.get_config_value to return appropriate values
    def mock_get_config_value(key, default_value):
        config_values = {
            SAVED_ANNOUNCE_ADDRESS: custom_address,
            SAVED_BITCOIND_RPC_USER: BITCOIND_RPC_USER_REGTEST,
            SAVED_BITCOIND_RPC_PASSWORD: BITCOIND_RPC_PASSWORD_REGTEST,
            SAVED_BITCOIND_RPC_HOST: BITCOIND_RPC_HOST_REGTEST,
            SAVED_BITCOIND_RPC_PORT: BITCOIND_RPC_PORT_REGTEST,
        }
        return config_values.get(key, default_value)

    mocker.patch(
        'src.utils.helpers.SettingRepository.get_config_value',
        side_effect=mock_get_config_value,
    )

    # Create a new instance of AboutWidget after mocking
    about_widget = AboutWidget(about_widget._view_model)

    # Call the method that uses announce_addresses
    about_widget.retranslate_ui()

    # Verify that the announce_address_frame is created
    assert any(
        call.kwargs.get('translation_key') == 'announce_address' and
        call.kwargs.get('value') == custom_address and
        call.kwargs.get('v_layout') == about_widget.about_vertical_layout
        for call in mock_node_info_widget.call_args_list
    ), 'Expected a NodeInfoWidget call with announce_address translation key'


def test_announce_alias_custom(about_widget, mocker, mock_node_info_widget, mock_node_info_model, mock_bitcoin_config):
    """Test behavior when announce_alias is not the default value."""
    # Set up the mock for announce_alias with a different value
    custom_alias = 'CustomAlias'

    # Mock SettingRepository.get_config_value to return appropriate values
    def mock_get_config_value(key, default_value):
        config_values = {
            SAVED_ANNOUNCE_ALIAS: custom_alias,
            SAVED_BITCOIND_RPC_USER: BITCOIND_RPC_USER_REGTEST,
            SAVED_BITCOIND_RPC_PASSWORD: BITCOIND_RPC_PASSWORD_REGTEST,
            SAVED_BITCOIND_RPC_HOST: BITCOIND_RPC_HOST_REGTEST,
            SAVED_BITCOIND_RPC_PORT: BITCOIND_RPC_PORT_REGTEST,
        }
        return config_values.get(key, default_value)

    mocker.patch(
        'src.utils.helpers.SettingRepository.get_config_value',
        side_effect=mock_get_config_value,
    )

    # Create a new instance of AboutWidget after mocking
    about_widget = AboutWidget(about_widget._view_model)

    # Call the method that uses announce_alias
    about_widget.retranslate_ui()

    # Verify that the announce_alias_frame is created
    assert any(
        call.kwargs.get('translation_key') == 'announce_alias' and
        call.kwargs.get('value') == custom_alias and
        call.kwargs.get('v_layout') == about_widget.about_vertical_layout
        for call in mock_node_info_widget.call_args_list
    ), 'Expected a NodeInfoWidget call with announce_alias translation key'
