# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument
"""
This module contains unit tests for the SplashViewModel class from the
src.viewmodels.splash_view_model module. It tests the behavior of various methods
including authentication, error handling, and application startup flows.
"""
from __future__ import annotations

from unittest.mock import Mock
from unittest.mock import patch

from src.model.enums.enums_model import WalletType
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_CONNECTION_FAILED_WITH_LN
from src.utils.error_message import ERROR_NATIVE_AUTHENTICATION
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.viewmodels.splash_view_model import SplashViewModel


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_on_success_response_false(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests the on_success method with a False response."""
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)

    view_model.on_success(False)

    page_navigation.fungibles_asset_page.assert_not_called()
    mock_toast_manager.error.assert_called_once_with(
        description=ERROR_NATIVE_AUTHENTICATION,
    )


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_on_error_common_exception(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests the on_error method with a CommonException."""
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    exception = CommonException('Custom error message')

    view_model.on_error(exception)

    mock_toast_manager.error.assert_called_once_with(
        description='Custom error message',
    )
    mock_qapp.instance().exit.assert_called_once()


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_on_error_general_exception(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests the on_error method with a general Exception."""
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    exception = Exception('General error message')

    view_model.on_error(exception)

    mock_toast_manager.error.assert_called_once_with(
        description=ERROR_SOMETHING_WENT_WRONG,
    )
    mock_qapp.instance().exit.assert_called_once()


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_is_login_authentication_enabled_true(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests the is_login_authentication_enabled method when native login is enabled."""
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    mock_setting_repo.native_login_enabled.return_value = Mock(
        is_enabled=True,
    )

    with patch.object(view_model, 'run_in_thread') as mock_run_in_thread:
        view_model.is_login_authentication_enabled(view_model)

    mock_run_in_thread.assert_called_once()
    mock_toast_manager.show_toast.assert_not_called()


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_is_login_authentication_enabled_false(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests the is_login_authentication_enabled method when native login is not enabled."""
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    mock_setting_repo.native_login_enabled.return_value = False

    view_model.is_login_authentication_enabled(view_model)
    # mock_toast_manager.show_toast.assert_not_called()


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_is_login_authentication_enabled_common_exception(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests the is_login_authentication_enabled method with a CommonException."""
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    mock_setting_repo.native_login_enabled.side_effect = CommonException(
        'Custom error message',
    )

    view_model.is_login_authentication_enabled(view_model)

    page_navigation.fungibles_asset_page.assert_not_called()
    mock_toast_manager.error.assert_called_once_with(
        description='Custom error message',
    )


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_is_login_authentication_enabled_general_exception(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests the is_login_authentication_enabled method with a general Exception."""
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    mock_setting_repo.native_login_enabled.side_effect = Exception(
        'General error message',
    )

    view_model.is_login_authentication_enabled(view_model)

    page_navigation.fungibles_asset_page.assert_not_called()
    mock_toast_manager.error.assert_called_once_with(
        description=ERROR_SOMETHING_WENT_WRONG,
    )


@patch('src.viewmodels.splash_view_model.CommonOperationRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
# Mock MessageBox
@patch('src.viewmodels.splash_view_model.MessageBox', autospec=True)
def test_on_error_of_unlock_api_connection_failed(
    mock_message_box, mock_qapp, mock_toast_manager, mock_common_repo,
):
    """Tests the on_error_of_unlock_api method for connection failure."""
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    error = CommonException(ERROR_CONNECTION_FAILED_WITH_LN)

    # Act
    view_model.on_error_of_unlock_api(error)

    # Assert that MessageBox was called with correct arguments
    mock_message_box.assert_called_once_with(
        'critical', ERROR_CONNECTION_FAILED_WITH_LN,
    )

    # Assert that ToastManager.error was called
    mock_toast_manager.error.assert_called_once_with(
        description=ERROR_CONNECTION_FAILED_WITH_LN,
    )

    # Assert that page navigation went to the enter wallet password page
    page_navigation.enter_wallet_password_page.assert_called_once()


@patch('src.viewmodels.splash_view_model.CommonOperationRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_on_error_of_unlock_api_not_initialized(mock_qapp, mock_toast_manager, mock_common_repo):
    """Tests the on_error_of_unlock_api method for node not initialized error."""
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    error = CommonException('not_initialized')

    view_model.on_error_of_unlock_api(error)

    page_navigation.term_and_condition_page.assert_called_once()


@patch('src.viewmodels.splash_view_model.CommonOperationRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
@patch('src.utils.local_store.LocalStore.set_value')
def test_on_success_of_unlock_api(mock_set_value, mock_qapp, mock_toast_manager, mock_common_repo):
    """Tests the on_success_of_unlock_api method."""
    # Arrange
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    view_model.render_timer = Mock()
    mock_node_info = Mock()
    mock_node_info.pubkey = 'test_pubkey'
    mock_common_repo.node_info.return_value = mock_node_info

    # Act
    view_model.on_success_of_unlock_api()

    # Assert
    view_model.render_timer.stop.assert_called_once()
    page_navigation.fungibles_asset_page.assert_called_once()
    mock_common_repo.node_info.assert_called_once()
    mock_set_value.assert_called_once_with('node_pub_key', 'test_pubkey')


@patch('src.viewmodels.splash_view_model.CommonOperationRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
@patch('src.utils.local_store.LocalStore.set_value')
def test_on_success_of_unlock_api_no_node_info(mock_set_value, mock_qapp, mock_toast_manager, mock_common_repo):
    """Tests the on_success_of_unlock_api method when node_info returns None."""
    # Arrange
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    view_model.render_timer = Mock()
    mock_common_repo.node_info.return_value = None

    # Act
    view_model.on_success_of_unlock_api()

    # Assert
    view_model.render_timer.stop.assert_called_once()
    page_navigation.fungibles_asset_page.assert_called_once()
    mock_common_repo.node_info.assert_called_once()
    mock_set_value.assert_not_called()


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_handle_application_open_embedded_wallet(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests handle_application_open method with embedded wallet type."""
    # Arrange
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    view_model.splash_screen_message = Mock()
    view_model.wallet_transfer_selection_view_model = Mock()
    mock_setting_repo.get_wallet_type.return_value = WalletType.EMBEDDED_TYPE_WALLET

    # Act
    view_model.handle_application_open()

    # Assert
    mock_setting_repo.get_wallet_type.assert_called_once()
    view_model.splash_screen_message.emit.assert_called_once()
    view_model.wallet_transfer_selection_view_model.start_node_for_embedded_option.assert_called_once()


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_handle_application_open_common_exception(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests handle_application_open method when CommonException occurs."""
    # Arrange
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    error_message = 'Test error'
    mock_setting_repo.get_wallet_type.side_effect = CommonException(
        error_message,
    )

    # Act
    view_model.handle_application_open()

    # Assert
    mock_setting_repo.get_wallet_type.assert_called_once()
    mock_toast_manager.error.assert_called_once_with(description=error_message)


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_handle_application_open_generic_exception(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests handle_application_open method when generic Exception occurs."""
    # Arrange
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    mock_setting_repo.get_wallet_type.side_effect = Exception(
        'Unexpected error',
    )

    # Act
    view_model.handle_application_open()

    # Assert
    mock_setting_repo.get_wallet_type.assert_called_once()
    mock_toast_manager.error.assert_called_once_with(
        description=ERROR_SOMETHING_WENT_WRONG,
    )


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
def test_handle_application_open_keyring_enabled(mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests handle_application_open method when keyring is enabled."""
    # Arrange
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    mock_setting_repo.get_wallet_type.return_value = WalletType.REMOTE_TYPE_WALLET
    mock_setting_repo.get_keyring_status.return_value = True

    # Act
    view_model.handle_application_open()

    # Assert
    mock_setting_repo.get_keyring_status.assert_called_once()
    page_navigation.enter_wallet_password_page.assert_called_once()


@patch('src.viewmodels.splash_view_model.SettingRepository')
@patch('src.viewmodels.splash_view_model.ToastManager')
@patch('src.viewmodels.splash_view_model.QApplication')
@patch('src.viewmodels.splash_view_model.get_value')
@patch('src.viewmodels.splash_view_model.get_bitcoin_config')
@patch('src.viewmodels.splash_view_model.CommonOperationRepository')
def test_handle_application_open_keyring_disabled(mock_common_repo, mock_bitcoin_config, mock_get_value, mock_qapp, mock_toast_manager, mock_setting_repo):
    """Tests handle_application_open method when keyring is disabled."""
    # Arrange
    page_navigation = Mock()
    view_model = SplashViewModel(page_navigation)
    view_model.splash_screen_message = Mock()
    view_model.sync_chain_info_label = Mock()
    mock_setting_repo.get_wallet_type.return_value = WalletType.REMOTE_TYPE_WALLET
    mock_setting_repo.get_keyring_status.return_value = False
    mock_wallet_password = 'test_password'
    mock_get_value.return_value = mock_wallet_password
    mock_bitcoin_config.return_value = 'test_config'

    # Act
    view_model.handle_application_open()

    # Assert
    mock_setting_repo.get_keyring_status.assert_called_once()
    view_model.splash_screen_message.emit.assert_called_once()
    view_model.sync_chain_info_label.emit.assert_called_once_with(True)
    mock_get_value.assert_called_once()
    mock_bitcoin_config.assert_called_once()
    assert hasattr(view_model, 'worker')
