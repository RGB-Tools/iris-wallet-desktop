# pylint: disable=redefined-outer-name,unused-argument,protected-access,too-many-arguments
# Unit tests often require multiple mock dependencies and parameters to simulate
# realistic service calls and behaviors. Reducing arguments would compromise test coverage
# and clarity, so this rule is intentionally disabled for test functions.
"""
This module contains unit tests for the WalletTransfeSelectionViewModel
"""
from __future__ import annotations

from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.viewmodels.wallet_and_transfer_selection_viewmodel import WalletTransferSelectionViewModel
from src.views.components.toast import ToastManager


@pytest.fixture
def wallet_transfer_selection_view_model(mocker):
    """Fixture for WalletTransferSelectionViewModel"""
    mock_page_navigation = mocker.Mock()
    mock_splash_view_model = mocker.Mock()

    # Mock LnNodeServerManager to prevent Qt signal connection
    mock_ln_node_manager = mocker.Mock()
    mocker.patch(
        'src.viewmodels.wallet_and_transfer_selection_viewmodel.LnNodeServerManager.get_instance',
        return_value=mock_ln_node_manager,
    )

    return WalletTransferSelectionViewModel(mock_page_navigation, mock_splash_view_model)


def test_on_ln_node_stop(wallet_transfer_selection_view_model):
    """Test the on_ln_node_stop method"""
    with patch('src.views.components.toast.ToastManager.info') as mock_show_toast:
        wallet_transfer_selection_view_model.on_ln_node_stop()
        mock_show_toast.assert_called_once_with(
            description='Ln node stopped...',
        )


def test_on_ln_node_error(wallet_transfer_selection_view_model):
    """Test the on_ln_node_error method"""
    with patch('src.viewmodels.wallet_and_transfer_selection_viewmodel.logger') as mock_logger:
        wallet_transfer_selection_view_model.ln_node_process_status = Mock()
        wallet_transfer_selection_view_model.splash_view_model = Mock()

        wallet_transfer_selection_view_model.on_ln_node_error(
            1, 'Error occurred',
        )

        wallet_transfer_selection_view_model.ln_node_process_status.emit.assert_called_once_with(
            False,
        )
        mock_logger.error.assert_called_once_with(
            'Exception occurred while stating ln node:Message: %s,Code:%s',
            'Error occurred', '1',
        )
        wallet_transfer_selection_view_model.splash_view_model.restart_ln_node_after_crash.assert_called_once()


def test_on_ln_node_already_running(wallet_transfer_selection_view_model):
    """Test the on_ln_node_already_running method"""
    with patch('src.views.components.toast.ToastManager.info') as mock_show_toast:
        wallet_transfer_selection_view_model.on_ln_node_already_running()
        mock_show_toast.assert_called_once_with(
            description='Ln node already running',
        )


def test_start_node_for_embedded_option_exception_handling(wallet_transfer_selection_view_model):
    """Test exception handling in start_node_for_embedded_option method"""
    with patch.object(wallet_transfer_selection_view_model.ln_node_manager, 'start_server') as mock_start_server:
        with patch('src.views.components.toast.ToastManager.error') as mock_show_toast:
            with patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network') as mock_get_wallet_network:
                mock_get_wallet_network.side_effect = CommonException(
                    'Custom error',
                )

                wallet_transfer_selection_view_model.start_node_for_embedded_option()

                mock_show_toast.assert_called_once_with(
                    description='Custom error',
                )
                mock_start_server.assert_not_called()


def test_start_node_for_embedded_option_generic_exception(wallet_transfer_selection_view_model):
    """Test generic exception handling in start_node_for_embedded_option method"""
    with patch.object(wallet_transfer_selection_view_model.ln_node_manager, 'start_server') as mock_start_server:
        with patch('src.views.components.toast.ToastManager.error') as mock_show_toast:
            with patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network') as mock_get_wallet_network:
                mock_get_wallet_network.side_effect = Exception(
                    'Unexpected error',
                )

                wallet_transfer_selection_view_model.start_node_for_embedded_option()

                mock_show_toast.assert_called_once_with(
                    description=ERROR_SOMETHING_WENT_WRONG,
                )
                mock_start_server.assert_not_called()


@patch('src.viewmodels.wallet_and_transfer_selection_viewmodel.ThreadManager.run_in_thread')
@patch('src.data.repository.setting_repository.SettingRepository.is_wallet_initialized')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status', return_value=True)
@patch('src.utils.logging.logger.info')
@patch('src.utils.local_store.LocalStore.get_value')
@patch('src.viewmodels.wallet_and_transfer_selection_viewmodel.get_bitcoin_config')
def test_on_ln_node_start_success_with_keyring_enabled(
    mock_bitcoin_config, mock_get_value, mock_logger,
    mock_get_keyring_status, mock_is_wallet_initialized, mock_run_in_thread, wallet_transfer_selection_view_model,
):
    """Test on_ln_node_start success path with keyring enabled"""
    # Mock dependencies
    wallet_transfer_selection_view_model.ln_node_process_status = Mock()
    wallet_transfer_selection_view_model.is_node_data_exits = True
    wallet_transfer_selection_view_model.splash_view_model = Mock()
    mock_sidebar = Mock()
    wallet_transfer_selection_view_model._page_navigation.sidebar.return_value = mock_sidebar

    with patch('src.views.components.toast.ToastManager.info') as mock_toast:
        with patch('src.data.repository.setting_repository.SettingRepository') as mock_setting_repo:
            with patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network') as mock_get_network:
                # Configure mocks
                mock_is_wallet_initialized.return_value = Mock(
                    is_wallet_initialized=True,
                )
                mock_get_keyring_status.return_value = True
                mock_get_network.return_value = 'regtest'
                mock_setting_repo.get_config_value.return_value = 'test_value'
                mock_bitcoin_config.return_value = {
                    'bitcoind_rpc_username': 'test_user',
                    'bitcoind_rpc_password': 'test_pass',
                    'bitcoind_rpc_host': 'localhost',
                    'bitcoind_rpc_port': 18443,
                    'indexer_url': 'http://localhost:3000',
                    'proxy_endpoint': 'http://localhost:8080',
                    'announce_addresses': ['127.0.0.1'],
                    'announce_alias': 'test_node',
                    'password': 'test_password',
                }
                mock_get_value.return_value = True

                # Execute
                wallet_transfer_selection_view_model.on_ln_node_start()

                # Assert
                mock_logger.assert_called_once_with('Ln node started')
                wallet_transfer_selection_view_model.ln_node_process_status.emit.assert_called_once_with(
                    False,
                )
                mock_toast.assert_called_once_with(
                    description='Ln node server started',
                )
                wallet_transfer_selection_view_model._page_navigation.enter_wallet_password_page.assert_called_once()


@patch('src.utils.logging.logger.error')
def test_on_ln_node_start_common_exception(mock_logger, wallet_transfer_selection_view_model):
    """Test on_ln_node_start with CommonException"""
    wallet_transfer_selection_view_model.ln_node_process_status = Mock()
    error_message = 'Something went wrong'

    with patch.object(ToastManager, 'error') as mock_toast:
        with patch(
            'src.data.repository.setting_repository.SettingRepository.is_wallet_initialized',
            side_effect=CommonException(error_message),
        ):

            wallet_transfer_selection_view_model.on_ln_node_start()

            mock_toast.assert_called_once_with(
                description=error_message,
            )  # Verify toast
            mock_logger.assert_called_once()


@patch('src.utils.logging.logger.error')
def test_on_ln_node_start_generic_exception(mock_logger, wallet_transfer_selection_view_model):
    """Test on_ln_node_start with generic Exception"""
    wallet_transfer_selection_view_model.ln_node_process_status = Mock()

    with patch.object(ToastManager, 'error') as mock_toast:
        with patch(
            'src.data.repository.setting_repository.SettingRepository.is_wallet_initialized',
            side_effect=Exception('Unexpected error'),
        ) as mock_setting_repo:
            mock_setting_repo.is_wallet_initialized.side_effect = Exception(
                'Unexpected error',
            )

            wallet_transfer_selection_view_model.on_ln_node_start()

            mock_toast.assert_called_once_with(
                description=ERROR_SOMETHING_WENT_WRONG,
            )
            mock_logger.assert_called_once()


@patch('src.utils.logging.logger.error')
def test_start_node_for_embedded_option(mock_logger, wallet_transfer_selection_view_model):
    """Test start_node_for_embedded_option method"""
    # Setup
    wallet_transfer_selection_view_model.ln_node_process_status = Mock()
    wallet_transfer_selection_view_model.ln_node_manager = Mock()
    mock_network = Mock()
    mock_node_config = ('/path/to/config', 'other_args')

    with patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network') as mock_get_network:
        with patch('src.viewmodels.wallet_and_transfer_selection_viewmodel.get_node_arg_config') as mock_get_config:
            with patch('os.path.exists') as mock_exists:
                with patch('src.views.components.toast.ToastManager.error'):
                    # Configure mocks
                    mock_get_network.return_value = mock_network
                    mock_get_config.return_value = mock_node_config
                    mock_exists.return_value = True

                    # Execute
                    wallet_transfer_selection_view_model.start_node_for_embedded_option()

                    # Assert
                    wallet_transfer_selection_view_model.ln_node_process_status.emit.assert_called_once_with(
                        True,
                    )
                    mock_get_network.assert_called_once()
                    mock_get_config.assert_called_once_with(mock_network)
                    mock_exists.assert_called_once_with(mock_node_config[0])
                    wallet_transfer_selection_view_model.ln_node_manager.start_server.assert_called_once_with(
                        arguments=mock_node_config,
                    )
                    assert wallet_transfer_selection_view_model.is_node_data_exits is True


@patch('src.utils.logging.logger.error')
def test_on_error_of_unlock_node(mock_logger, wallet_transfer_selection_view_model):
    """Test on_error_of_unlock_node method"""
    # Test with CommonException
    with patch('src.views.components.toast.ToastManager.error') as mock_toast:
        custom_error = CommonException('Custom error message')
        wallet_transfer_selection_view_model.on_error_of_unlock_node(
            custom_error,
        )
        mock_toast.assert_called_once_with(description='Custom error message')

    # Test with generic Exception
    with patch('src.views.components.toast.ToastManager.error') as mock_toast:
        generic_error = Exception('Generic error')
        wallet_transfer_selection_view_model.on_error_of_unlock_node(
            generic_error,
        )
        mock_toast.assert_called_once_with(
            description=ERROR_SOMETHING_WENT_WRONG,
        )
