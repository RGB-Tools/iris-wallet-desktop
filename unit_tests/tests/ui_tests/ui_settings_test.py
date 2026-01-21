"""Unit test for Settings ui."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access,too-many-statements
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtGui import QIntValidator

from src.model.enums.enums_model import NetworkEnumModel
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.settings_helpers import check_keyring_state_for_password
from src.views.ui_settings import SettingsWidget


@pytest.fixture(autouse=True)
def reset_mocks(mocker):
    """Ensure mocks are reset after every test."""
    mock_network = MagicMock(spec=NetworkEnumModel)
    mock_network.reset_mock()
    yield mock_network
    mock_network.reset_mock()


@pytest.fixture
def setting_widget(qtbot, mocker, reset_mocks):
    """Fixture to create and return an instance of SettingsWidget."""
    mock_navigation = MagicMock()
    mock_view_model = MainViewModel(mock_navigation)

    # Mock SettingRepository.get_wallet_network to return a valid NetworkEnumModel value
    mocker.patch(
        'src.views.ui_settings.SettingRepository.get_wallet_network',
        return_value=NetworkEnumModel.MAINNET,
    )

    # Assign the mock network to the view model
    mock_view_model.network = reset_mocks
    reset_mocks.value = 'mainnet'

    widget = SettingsWidget(mock_view_model)
    qtbot.addWidget(widget)

    return widget


def test_retranslate_ui(setting_widget: SettingsWidget):
    """Test the retranslation of UI elements in SettingsWidget."""
    setting_widget.retranslate_ui()

    assert setting_widget.settings_label.text() == 'settings'
    assert setting_widget.imp_operation_label.text() == 'auth_important_ops'
    assert setting_widget.login_auth_label.text() == 'auth_login'
    assert setting_widget.hide_exhausted_label.text() == 'hide_exhausted_assets'
    assert setting_widget.hide_asset_desc.text() == 'hide_zero_balance_assets'
    assert setting_widget.keyring_label.text() == 'keyring_label'
    assert setting_widget.keyring_desc.text() == 'keyring_desc'


def test_handle_keyring_storage_enabled(setting_widget: SettingsWidget, mocker):
    """Test the handle_keyring_storage method when keyring storage is enabled."""

    # Mock necessary dependencies
    mocker.patch(
        'src.views.ui_settings.SettingRepository.get_keyring_status', return_value=True,
    )
    mocker.patch('src.views.ui_settings.SettingRepository.get_wallet_network')
    mocker.patch('src.views.ui_settings.get_value')

    # Mock RestoreMnemonicWidget and its exec method
    mock_mnemonic_dialog = mocker.patch(
        'src.views.ui_settings.RestoreMnemonicWidget',
    )
    mock_exec = mocker.patch.object(mock_mnemonic_dialog.return_value, 'exec')

    # Call the method
    setting_widget.handle_keyring_storage()

    # Verify the dialog was created and executed
    mock_mnemonic_dialog.assert_called_once_with(
        parent=setting_widget,
        view_model=setting_widget._view_model,
        origin_page='setting_page',
    )
    mock_exec.assert_called_once()

    # Verify that the toggle status handler was connected
    assert mock_mnemonic_dialog.return_value.finished.connect.called
    assert mock_mnemonic_dialog.return_value.finished.connect.call_args[0][0] == setting_widget.handle_keyring_toggle_status(
    )


def test_handle_keyring_storage_disabled(setting_widget: SettingsWidget, mocker):
    """Test the handle_keyring_storage method when keyring storage is disabled."""

    # Mock necessary dependencies
    mocker.patch(
        'src.views.ui_settings.SettingRepository.get_keyring_status', return_value=False,
    )
    mocker.patch(
        'src.views.ui_settings.SettingRepository.get_wallet_network',
        return_value=NetworkEnumModel.MAINNET,
    )
    mocker.patch(
        'src.views.ui_settings.get_value', side_effect=[
            'test_mnemonic', 'test_password',
        ],
    )

    # Mock KeyringErrorDialog and its exec method
    mock_keyring_dialog = mocker.patch(
        'src.views.ui_settings.KeyringErrorDialog',
    )
    mock_exec = mocker.patch.object(mock_keyring_dialog.return_value, 'exec')

    # Call the method
    setting_widget.handle_keyring_storage()

    # Verify the dialog was created and executed
    mock_keyring_dialog.assert_called_once_with(
        parent=setting_widget,
        mnemonic='test_mnemonic',
        password='test_password',
        originating_page='settings_page',
        navigate_to=setting_widget._view_model.page_navigation.settings_page,
    )
    mock_exec.assert_called_once()

    # Verify that the toggle status handler was connected
    assert mock_keyring_dialog.return_value.finished.connect.called
    assert mock_keyring_dialog.return_value.finished.connect.call_args[0][0] == setting_widget.handle_keyring_toggle_status(
    )


def test_show_loading_screen(setting_widget: SettingsWidget, mocker):
    """Test the show_loading_screen method."""

    # Mock the sidebar and loading screen
    mock_sidebar = mocker.patch.object(
        setting_widget._view_model.page_navigation, 'sidebar',
    )
    mock_start_loading = mocker.patch.object(
        setting_widget._SettingsWidget__loading_translucent_screen, 'start',
    )
    mock_stop_loading = mocker.patch.object(
        setting_widget._SettingsWidget__loading_translucent_screen, 'stop',
    )

    # Test the loading screen when status is True
    setting_widget.show_loading_screen(True)
    mock_sidebar().setDisabled.assert_called_once_with(True)
    mock_start_loading.assert_called_once()

    # Reset mocks for the next test
    mock_sidebar.reset_mock()
    mock_start_loading.reset_mock()

    # Test the loading screen when status is False
    setting_widget.show_loading_screen(False)
    mock_sidebar().setDisabled.assert_called_once_with(False)
    mock_stop_loading.assert_called_once()
    setting_widget._view_model.page_navigation.settings_page.assert_called_once()


def test_set_fee_rate_value(setting_widget):
    """Test setting fee rate value."""
    # Mock components
    setting_widget.set_fee_rate_frame = MagicMock()
    setting_widget.set_fee_rate_frame.input_value.text.return_value = '10'

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget._set_fee_rate_value()

    # Verify setting view model was called with correct value
    setting_widget._view_model.setting_view_model.set_default_fee_rate.assert_called_once_with(
        '10',
    )


def test_set_expiry_time(setting_widget):
    """Test setting expiry time."""
    # Mock components
    setting_widget.set_expiry_time_frame = MagicMock()
    setting_widget.set_expiry_time_frame.input_value.text.return_value = '24'
    setting_widget.set_expiry_time_frame.time_unit_combobox.currentText.return_value = 'hours'

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget._set_expiry_time()

    # Verify setting view model was called with correct values
    setting_widget._view_model.setting_view_model.set_default_expiry_time.assert_called_once_with(
        '24', 'hours',
    )


def test_set_indexer_url(setting_widget, mocker):
    """Test setting indexer URL."""
    # Mock components
    setting_widget.set_indexer_url_frame = MagicMock()
    setting_widget.set_indexer_url_frame.input_value.text.return_value = 'http://example.com'

    # Mock check_keyring_state_for_password
    mocker.patch(
        'src.views.ui_settings.check_keyring_state_for_password',
        return_value='password123',
    )

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget._set_indexer_url()

    # Verify setting view model was called with correct values
    setting_widget._view_model.setting_view_model.check_indexer_url_endpoint.assert_called_once_with(
        'http://example.com', 'password123',
    )


def test_set_proxy_endpoint(setting_widget, mocker):
    """Test setting proxy endpoint."""
    # Mock components
    setting_widget.set_proxy_endpoint_frame = MagicMock()
    setting_widget.set_proxy_endpoint_frame.input_value.text.return_value = 'http://proxy.com'

    # Mock check_keyring_state_for_password
    mocker.patch(
        'src.views.ui_settings.check_keyring_state_for_password',
        return_value='password123',
    )

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget._set_proxy_endpoint()

    # Verify setting view model was called with correct values
    setting_widget._view_model.setting_view_model.check_proxy_endpoint.assert_called_once_with(
        'http://proxy.com', 'password123',
    )


def test_set_bitcoind_host(setting_widget, mocker):
    """Test setting bitcoind host."""
    # Mock components
    setting_widget.set_bitcoind_rpc_host_frame = MagicMock()
    setting_widget.set_bitcoind_rpc_host_frame.input_value.text.return_value = 'localhost'

    # Mock check_keyring_state_for_password
    mocker.patch(
        'src.views.ui_settings.check_keyring_state_for_password',
        return_value='password123',
    )

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget._set_bitcoind_host()

    # Verify setting view model was called with correct values
    setting_widget._view_model.setting_view_model.set_bitcoind_host.assert_called_once_with(
        'localhost', 'password123',
    )


def test_set_bitcoind_port(setting_widget, mocker):
    """Test setting bitcoind port."""
    # Mock components
    setting_widget.set_bitcoind_rpc_port_frame = MagicMock()
    setting_widget.set_bitcoind_rpc_port_frame.input_value.text.return_value = '8332'

    # Mock check_keyring_state_for_password
    mocker.patch(
        'src.views.ui_settings.check_keyring_state_for_password',
        return_value='password123',
    )

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget._set_bitcoind_port()

    # Verify setting view model was called with correct values
    setting_widget._view_model.setting_view_model.set_bitcoind_port.assert_called_once_with(
        8332, 'password123',
    )


def test_set_announce_address(setting_widget, mocker):
    """Test setting announce address."""
    # Mock components
    setting_widget.set_announce_address_frame = MagicMock()
    setting_widget.set_announce_address_frame.input_value.text.return_value = 'example.com'

    # Mock check_keyring_state_for_password
    mocker.patch(
        'src.views.ui_settings.check_keyring_state_for_password',
        return_value='password123',
    )

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget._set_announce_address()

    # Verify setting view model was called with correct values
    setting_widget._view_model.setting_view_model.set_announce_address.assert_called_once_with(
        'example.com', 'password123',
    )


def test_set_announce_alias(setting_widget, mocker):
    """Test setting announce alias."""
    # Mock components
    setting_widget.set_announce_alias_frame = MagicMock()
    setting_widget.set_announce_alias_frame.input_value.text.return_value = 'my-node'

    # Mock check_keyring_state_for_password
    mocker.patch(
        'src.views.ui_settings.check_keyring_state_for_password',
        return_value='password123',
    )

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget._set_announce_alias()

    # Verify setting view model was called with correct values
    setting_widget._view_model.setting_view_model.set_announce_alias.assert_called_once_with(
        'my-node', 'password123',
    )


def test_set_min_confirmation(setting_widget):
    """Test setting minimum confirmation."""
    # Mock components
    setting_widget.set_minimum_confirmation_frame = MagicMock()
    setting_widget.set_minimum_confirmation_frame.input_value.text.return_value = '6'

    # Mock setting view model and toast manager
    setting_widget._view_model.setting_view_model = MagicMock()
    with patch('src.views.components.toast.ToastManager'):
        # Call method
        setting_widget._set_min_confirmation()

        # Verify setting view model was called with correct value
        setting_widget._view_model.setting_view_model.set_min_confirmation.assert_called_once_with(
            6,
        )


def test_handle_imp_operation_auth_toggle_button(setting_widget):
    """Test handling important operation authentication toggle."""
    # Mock toggle button
    setting_widget.imp_operation_auth_toggle_button = MagicMock()
    setting_widget.imp_operation_auth_toggle_button.isChecked.return_value = True

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget.handle_imp_operation_auth_toggle_button()

    # Verify setting view model was called with correct value
    setting_widget._view_model.setting_view_model.enable_native_authentication.assert_called_once_with(
        True,
    )


def test_handle_login_auth_toggle_button(setting_widget):
    """Test handling login authentication toggle."""
    # Mock toggle button
    setting_widget.login_auth_toggle_button = MagicMock()
    setting_widget.login_auth_toggle_button.isChecked.return_value = True

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget.handle_login_auth_toggle_button()

    # Verify setting view model was called with correct value
    setting_widget._view_model.setting_view_model.enable_native_logging.assert_called_once_with(
        True,
    )


def test_handle_hide_exhausted_asset_toggle_button(setting_widget):
    """Test handling hide exhausted assets toggle."""
    # Mock toggle button
    setting_widget.hide_exhausted_asset_toggle_button = MagicMock()
    setting_widget.hide_exhausted_asset_toggle_button.isChecked.return_value = True

    # Mock setting view model
    setting_widget._view_model.setting_view_model = MagicMock()

    # Call method
    setting_widget.handle_hide_exhausted_asset_toggle_button()

    # Verify setting view model was called with correct value
    setting_widget._view_model.setting_view_model.enable_exhausted_asset.assert_called_once_with(
        True,
    )


def test_handle_on_page_load(setting_widget):
    """Test handling of page load event."""
    # Create mock response data
    mock_response = MagicMock()

    # Set up mock values for the response
    mock_response.status_of_native_auth.is_enabled = True
    mock_response.status_of_native_logging_auth.is_enabled = False
    mock_response.status_of_exhausted_asset.is_enabled = True
    mock_response.value_of_default_fee.fee_rate = '10'
    mock_response.value_of_default_expiry_time.time = '24'
    mock_response.value_of_default_expiry_time.unit = 'hours'
    mock_response.value_of_default_indexer_url.url = 'http://example.com'
    mock_response.value_of_default_proxy_endpoint.endpoint = 'http://proxy.com'
    mock_response.value_of_default_bitcoind_rpc_host.host = 'localhost'
    mock_response.value_of_default_bitcoind_rpc_port.port = 8332
    mock_response.value_of_default_announce_address.address = 'example.com'
    mock_response.value_of_default_announce_alias.alias = 'my-node'
    mock_response.value_of_default_min_confirmation.min_confirmation = 6

    # Mock the toggle buttons
    setting_widget.imp_operation_auth_toggle_button = MagicMock()
    setting_widget.login_auth_toggle_button = MagicMock()
    setting_widget.hide_exhausted_asset_toggle_button = MagicMock()

    # Call the method
    setting_widget.handle_on_page_load(mock_response)

    # Verify toggle buttons were set correctly
    setting_widget.imp_operation_auth_toggle_button.setChecked.assert_called_once_with(
        True,
    )
    setting_widget.login_auth_toggle_button.setChecked.assert_called_once_with(
        False,
    )
    setting_widget.hide_exhausted_asset_toggle_button.setChecked.assert_called_once_with(
        True,
    )

    # Verify all values were set correctly
    assert setting_widget.fee_rate == '10'
    assert setting_widget.expiry_time == '24'
    assert setting_widget.expiry_time_unit == 'hours'
    assert setting_widget.indexer_url == 'http://example.com'
    assert setting_widget.proxy_endpoint == 'http://proxy.com'
    assert setting_widget.bitcoind_host == 'localhost'
    assert setting_widget.bitcoind_port == 8332
    assert setting_widget.announce_address == 'example.com'
    assert setting_widget.announce_alias == 'my-node'
    assert setting_widget.min_confirmation == 6


def test_handle_on_page_load_with_empty_response(setting_widget):
    """Test handling of page load event with empty/null values."""
    # Create mock response with None values
    mock_response = MagicMock()

    # Set up mock values with None
    mock_response.status_of_native_auth.is_enabled = False
    mock_response.status_of_native_logging_auth.is_enabled = False
    mock_response.status_of_exhausted_asset.is_enabled = False
    mock_response.value_of_default_fee.fee_rate = None
    mock_response.value_of_default_expiry_time.time = None
    mock_response.value_of_default_expiry_time.unit = None
    mock_response.value_of_default_indexer_url.url = None
    mock_response.value_of_default_proxy_endpoint.endpoint = None
    mock_response.value_of_default_bitcoind_rpc_host.host = None
    mock_response.value_of_default_bitcoind_rpc_port.port = None
    mock_response.value_of_default_announce_address.address = None
    mock_response.value_of_default_announce_alias.alias = None
    mock_response.value_of_default_min_confirmation.min_confirmation = None

    # Mock the toggle buttons
    setting_widget.imp_operation_auth_toggle_button = MagicMock()
    setting_widget.login_auth_toggle_button = MagicMock()
    setting_widget.hide_exhausted_asset_toggle_button = MagicMock()

    # Mock ToastManager
    with patch('src.views.components.toast.ToastManager'):
        # Call the method
        setting_widget.handle_on_page_load(mock_response)

        # Verify toggle buttons were set to False
        setting_widget.imp_operation_auth_toggle_button.setChecked.assert_called_once_with(
            False,
        )
        setting_widget.login_auth_toggle_button.setChecked.assert_called_once_with(
            False,
        )
        setting_widget.hide_exhausted_asset_toggle_button.setChecked.assert_called_once_with(
            False,
        )

        # Verify all values were set to None
        assert setting_widget.fee_rate is None
        assert setting_widget.expiry_time is None
        assert setting_widget.expiry_time_unit is None
        assert setting_widget.indexer_url is None
        assert setting_widget.proxy_endpoint is None
        assert setting_widget.bitcoind_host is None
        assert setting_widget.bitcoind_port is None
        assert setting_widget.announce_address is None
        assert setting_widget.announce_alias is None
        assert setting_widget.min_confirmation is None


def test_handle_on_error(setting_widget, mocker):
    """Test handling of error messages."""
    # Mock dependencies
    mock_toast = mocker.patch('src.views.ui_settings.ToastManager')
    setting_widget.handle_keyring_toggle_status = MagicMock()

    # Test error message
    error_message = 'Test error message'
    setting_widget.handle_on_error(error_message)

    # Verify keyring toggle status was handled
    setting_widget.handle_keyring_toggle_status.assert_called_once()

    # Verify error toast was shown with correct message
    mock_toast.error.assert_called_once_with(error_message)


def test_handle_on_error_empty_message(setting_widget, mocker):
    """Test handling of empty error messages."""
    # Mock dependencies
    mock_toast = mocker.patch('src.views.ui_settings.ToastManager')
    setting_widget.handle_keyring_toggle_status = MagicMock()

    # Test with empty message
    setting_widget.handle_on_error('')

    # Verify keyring toggle status was still handled
    setting_widget.handle_keyring_toggle_status.assert_called_once()

    # Verify error toast was shown with empty message
    mock_toast.error.assert_called_once_with('')


def test_handle_fee_rate_frame(setting_widget):
    """Test handling fee rate frame."""
    # Mock frame and components
    setting_widget.set_fee_rate_frame = MagicMock()
    setting_widget.fee_rate = 10

    # Call method
    setting_widget.handle_fee_rate_frame()

    # Verify QDoubleValidator was used
    assert isinstance(
        setting_widget.set_fee_rate_frame.input_value.setValidator.call_args[0][0],
        QIntValidator,
    )


def test_handle_expiry_time_frame(setting_widget):
    """Test handling expiry time frame."""
    # Mock frame and components
    setting_widget.set_expiry_time_frame = MagicMock()
    setting_widget.expiry_time = 24
    setting_widget.expiry_time_unit = 'hours'

    # Mock ToastManager
    with patch('src.views.components.toast.ToastManager'):
        # Call method
        setting_widget.handle_expiry_time_frame()

        # Verify QIntValidator was used and time unit was set
        assert isinstance(
            setting_widget.set_expiry_time_frame.input_value.setValidator.call_args[0][0],
            QIntValidator,
        )
        setting_widget.set_expiry_time_frame.time_unit_combobox.setCurrentText.assert_called_with(
            'hours',
        )


def test_handle_bitcoind_port_frame(setting_widget):
    """Test handling bitcoind port frame."""
    # Mock frame and components
    setting_widget.set_bitcoind_rpc_port_frame = MagicMock()
    setting_widget.bitcoind_port = 8332

    # Call method
    setting_widget.handle_bitcoind_port_frame()

    # Verify QIntValidator was used
    assert isinstance(
        setting_widget.set_bitcoind_rpc_port_frame.input_value.setValidator.call_args[0][0],
        QIntValidator,
    )


def test_handle_other_frames(setting_widget):
    """Test handling other simple frames."""
    # Test frames without special validators or components
    frames_to_test = [
        (
            'handle_indexer_url_frame', 'set_indexer_url_frame',
            'indexer_url', 'http://example.com',
        ),
        (
            'handle_proxy_endpoint_frame', 'set_proxy_endpoint_frame',
            'proxy_endpoint', 'http://proxy.com',
        ),
        (
            'handle_bitcoind_host_frame', 'set_bitcoind_rpc_host_frame',
            'bitcoind_host', 'localhost',
        ),
        (
            'handle_announce_address_frame', 'set_announce_address_frame',
            'announce_address', 'example.com',
        ),
        (
            'handle_announce_alias_frame',
            'set_announce_alias_frame', 'announce_alias', 'my-node',
        ),
        (
            'handle_minimum_confirmation_frame',
            'set_minimum_confirmation_frame', 'min_confirmation', 6,
        ),
    ]

    for method_name, frame_name, attr_name, value in frames_to_test:
        # Mock frame
        setattr(setting_widget, frame_name, MagicMock())
        setattr(setting_widget, attr_name, value)

        # Call method
        getattr(setting_widget, method_name)()

        # Verify frame was configured
        frame = getattr(setting_widget, frame_name)
        frame.input_value.setText.assert_called_with(str(value))
        frame.input_value.setPlaceholderText.assert_called_with(str(value))


def test_check_keyring_state_invalid(setting_widget, mocker):
    """Test checking keyring state with invalid keyring status."""
    # Mock dependencies
    mocker.patch(
        'src.views.ui_settings.SettingRepository.get_keyring_status', return_value=None,
    )

    # Call method
    result = check_keyring_state_for_password(
        setting_widget, setting_widget._view_model,
    )

    # Verify None is returned for invalid keyring status
    assert result is None


def test_update_loading_state_loading(setting_widget):
    """Test updating loading state when loading is True."""
    # Mock all frames
    frames = [
        'set_indexer_url_frame',
        'set_proxy_endpoint_frame',
        'set_bitcoind_rpc_host_frame',
        'set_bitcoind_rpc_port_frame',
        'set_announce_address_frame',
        'set_announce_alias_frame',
    ]

    for frame_name in frames:
        mock_frame = MagicMock()
        setattr(setting_widget, frame_name, mock_frame)

    # Call method with loading=True
    setting_widget._update_loading_state(True)

    # Verify start_loading was called on all frame save buttons
    for frame_name in frames:
        frame = getattr(setting_widget, frame_name)
        frame.save_button.start_loading.assert_called_once()
        assert not frame.save_button.stop_loading.called


def test_update_loading_state_not_loading(setting_widget):
    """Test updating loading state when loading is False."""
    # Mock all frames
    frames = [
        'set_indexer_url_frame',
        'set_proxy_endpoint_frame',
        'set_bitcoind_rpc_host_frame',
        'set_bitcoind_rpc_port_frame',
        'set_announce_address_frame',
        'set_announce_alias_frame',
    ]

    for frame_name in frames:
        mock_frame = MagicMock()
        setattr(setting_widget, frame_name, mock_frame)

    # Call method with loading=False
    setting_widget._update_loading_state(False)

    # Verify stop_loading was called on all frame save buttons
    for frame_name in frames:
        frame = getattr(setting_widget, frame_name)
        frame.save_button.stop_loading.assert_called_once()
        assert not frame.save_button.start_loading.called
