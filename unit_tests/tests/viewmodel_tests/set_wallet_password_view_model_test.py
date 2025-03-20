"""Unit test for SetWalletPasswordViewModel"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QLineEdit

from src.data.repository.setting_repository import SettingRepository
from src.model.common_operation_model import InitResponseModel
from src.model.enums.enums_model import ToastPreset
from src.model.enums.enums_model import WalletType
from src.utils.custom_exception import CommonException
from src.utils.local_store import local_store
from src.viewmodels.set_wallet_password_view_model import SetWalletPasswordViewModel


@pytest.fixture
def mock_page_navigation(mocker):
    """Fixture to create a mock page navigation object."""
    return mocker.MagicMock()


@pytest.fixture
def mock_keyring_and_storage(monkeypatch):
    """Ensure tests use dummy values for keyring and local storage."""

    # Dummy test values
    dummy_mnemonic = 'dummy_mnemonic'
    dummy_password = 'dummy_password'
    dummy_native_login = False
    dummy_native_auth = False

    # Mock methods that retrieve data from keyring/local storage
    monkeypatch.setattr(
        local_store, 'get_value', lambda key: {
            'mnemonic': dummy_mnemonic,
            'wallet_password': dummy_password,
            'nativeLoginEnabled': dummy_native_login,
            'isNativeAuthenticationEnabled': dummy_native_auth,
        }.get(key, None),
    )

    # Mock methods that store data to keyring/local storage
    monkeypatch.setattr(local_store, 'set_value', lambda key, value: None)

    # Mock SettingRepository methods if needed
    monkeypatch.setattr(
        SettingRepository,
        'get_wallet_network', lambda: 'test_network',
    )


@pytest.fixture
def init_mock(mocker):
    """Fixture to create a mock CommonOperationRepository init method."""
    mock_response = InitResponseModel(
        mnemonic='skill lamp please gown put season degree collect decline account monitor insane',
    )
    return mocker.patch(
        'src.data.repository.common_operations_repository.CommonOperationRepository.init',
        return_value=mock_response,
    )


@pytest.fixture
def set_wallet_initialized_mock(mocker):
    """Fixture to create a mock SettingRepository set_wallet_initialized method."""
    return mocker.patch(
        'src.data.repository.setting_repository.SettingRepository.set_wallet_initialized',
    )


@pytest.fixture
def unlock_mock(mocker):
    """Fixture to create a mock CommonOperationRepository unlock method."""
    return mocker.patch(
        'src.data.repository.common_operations_repository.CommonOperationRepository.unlock',
    )


@pytest.fixture
def set_value_mock(mocker):
    """Fixture to create a mock set_value."""
    return mocker.patch('src.utils.keyring_storage.set_value')


@pytest.fixture
def set_wallet_password_view_model(mock_page_navigation):
    """Fixture to create an instance of the SetWalletPasswordViewModel class."""
    return SetWalletPasswordViewModel(mock_page_navigation)


@pytest.fixture
def mocks(
    init_mock,
    set_wallet_initialized_mock,
    unlock_mock,
    set_value_mock,
):
    """Fixture to create an object of the multiple mocks."""
    return {
        'init_mock': init_mock,
        'set_wallet_initialized_mock': set_wallet_initialized_mock,
        'unlock_mock': unlock_mock,
        'set_value_mock': set_value_mock,
    }


def test_toggle_password_visibility(set_wallet_password_view_model, mocker):
    """"Test for toggle visibility work as expected"""
    line_edit_mock = mocker.MagicMock(spec=QLineEdit)
    initial_echo_mode = QLineEdit.Password

    assert (
        set_wallet_password_view_model.toggle_password_visibility(
            line_edit_mock,
        )
        is False
    )
    line_edit_mock.setEchoMode.assert_called_once_with(QLineEdit.Normal)

    assert (
        set_wallet_password_view_model.toggle_password_visibility(
            line_edit_mock,
        )
        is True
    )
    line_edit_mock.setEchoMode.assert_called_with(initial_echo_mode)


def test_generate_password(set_wallet_password_view_model):
    """"Test for generate work as expected"""
    generated_password = set_wallet_password_view_model.generate_password(
        length=12,
    )
    assert len(generated_password) == 12

    generated_password_invalid = set_wallet_password_view_model.generate_password(
        length=2,
    )
    assert 'Error' in generated_password_invalid


def test_set_wallet_password_common_exception(set_wallet_password_view_model, mocker, mocks):
    """"Test for set wallet password work as expected in exception scenario"""
    enter_password_input_mock = mocker.MagicMock(spec=QLineEdit)
    confirm_password_input_mock = mocker.MagicMock(spec=QLineEdit)
    validation_mock = mocker.MagicMock()

    init_mock = mocks['init_mock']
    mock_message = Mock()
    set_wallet_password_view_model.message.connect(mock_message)

    def call_set_wallet_password(enter_password: str, confirm_password: str):
        enter_password_input_mock.text.return_value = enter_password
        confirm_password_input_mock.text.return_value = confirm_password

        set_wallet_password_view_model.set_wallet_password_in_thread(
            enter_password_input_mock,
            confirm_password_input_mock,
            validation_mock,
        )

    init_mock.side_effect = CommonException('Test exception')
    call_set_wallet_password('validpassword', 'validpassword')
    set_wallet_password_view_model.worker.error.emit(init_mock.side_effect)
    mock_message.assert_called_once_with(ToastPreset.ERROR, 'Test exception')


def test_set_wallet_password_short_password(set_wallet_password_view_model, mocker):
    """Test for set wallet password when the password length is less than 8 characters."""
    enter_password_input_mock = mocker.MagicMock(spec=QLineEdit)
    confirm_password_input_mock = mocker.MagicMock(spec=QLineEdit)
    validation_mock = mocker.MagicMock()

    # Set password length less than 8 characters
    enter_password_input_mock.text.return_value = 'short'
    confirm_password_input_mock.text.return_value = 'short'

    # Call the method
    set_wallet_password_view_model.set_wallet_password_in_thread(
        enter_password_input_mock,
        confirm_password_input_mock,
        validation_mock,
    )

    # Validation mock should be called with the appropriate message
    validation_mock.assert_called_once_with(
        'Minimum password length is 8 characters.',
    )


def test_set_wallet_password_special_characters(set_wallet_password_view_model, mocker):
    """Test for set wallet password when the password contains special characters."""
    enter_password_input_mock = mocker.MagicMock(spec=QLineEdit)
    confirm_password_input_mock = mocker.MagicMock(spec=QLineEdit)
    validation_mock = mocker.MagicMock()

    # Set password with special characters
    enter_password_input_mock.text.return_value = 'password!'
    confirm_password_input_mock.text.return_value = 'password!'

    # Call the method
    set_wallet_password_view_model.set_wallet_password_in_thread(
        enter_password_input_mock,
        confirm_password_input_mock,
        validation_mock,
    )

    # Validation mock should be called with the appropriate message
    validation_mock.assert_called_once_with(
        'Password cannot contain special characters.',
    )


def test_set_wallet_password_passwords_do_not_match(set_wallet_password_view_model, mocker):
    """Test for set wallet password when the passwords do not match."""
    enter_password_input_mock = mocker.MagicMock(spec=QLineEdit)
    confirm_password_input_mock = mocker.MagicMock(spec=QLineEdit)
    validation_mock = mocker.MagicMock()

    # Set different passwords
    enter_password_input_mock.text.return_value = 'password1'
    confirm_password_input_mock.text.return_value = 'password2'

    # Call the method
    set_wallet_password_view_model.set_wallet_password_in_thread(
        enter_password_input_mock,
        confirm_password_input_mock,
        validation_mock,
    )

    # Validation mock should be called with the appropriate message
    validation_mock.assert_called_once_with('Passwords must be the same!')


@patch('src.data.repository.setting_repository.SettingRepository')
@patch('src.utils.keyring_storage.set_value')
@patch('src.views.components.toast.ToastManager')
@patch('src.views.components.keyring_error_dialog.KeyringErrorDialog')
def test_on_success(mock_keyring_error_dialog, mock_toast_manager, mock_set_value, mock_setting_repository, set_wallet_password_view_model, mock_keyring_and_storage):
    """Test the on_success method."""

    # Create a mock InitResponseModel with mnemonic
    mock_response = MagicMock()
    mock_response.mnemonic = 'test mnemonic'

    # Mock SettingRepository methods
    mock_setting_repository.get_wallet_network.return_value = MagicMock(
        value='test_network',
    )
    mock_setting_repository.get_wallet_type.return_value = MagicMock(
        value=WalletType.EMBEDDED_TYPE_WALLET.value,
    )

    # Mock os.path.exists
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True

        # Call the on_success method
        set_wallet_password_view_model.on_success(mock_response)

        mock_keyring_error_dialog.assert_not_called()


@patch('src.data.repository.setting_repository.SettingRepository')
@patch('src.utils.keyring_storage.set_value')
@patch('src.views.components.toast.ToastManager')
@patch('src.views.components.keyring_error_dialog.KeyringErrorDialog')
def test_on_success_keyring_error(mock_keyring_error_dialog, mock_toast_manager, mock_set_value, mock_setting_repository, set_wallet_password_view_model):
    """Test the on_success method with keyring storage error."""

    # Create a mock InitResponseModel with mnemonic
    mock_response = MagicMock()
    mock_response.mnemonic = 'test mnemonic'

    # Mock SettingRepository methods
    mock_setting_repository.get_wallet_network.return_value = MagicMock(
        value='test_network',
    )
    mock_setting_repository.get_wallet_type.return_value = MagicMock(
        value=WalletType.EMBEDDED_TYPE_WALLET.value,
    )

    # Mock set_value to return False (indicating failure to store value)
    mock_set_value.side_effect = [True, False]

    # Call the on_success method
    set_wallet_password_view_model.on_success(mock_response)

    mock_toast_manager.show_toast.assert_not_called()
