"""Unit test for issue ln endpoint view model"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument,too-many-arguments,protected-access
from __future__ import annotations

from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QCoreApplication

from src.data.repository.common_operations_repository import CommonOperationRepository
from src.model.common_operation_model import UnlockResponseModel
from src.model.enums.enums_model import WalletType
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import LIGHTNING_URL_KEY
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.custom_exception import CommonException
from src.utils.local_store import local_store
from src.viewmodels.ln_endpoint_view_model import LnEndpointViewModel


@pytest.fixture
def mock_page_navigation(mocker):
    """Fixture to create a mock page navigation object."""
    return mocker.MagicMock()


@pytest.fixture
def mock_validation_label():
    """Fixture to create a mock validation label object."""
    return Mock()


@pytest.fixture
def ln_endpoint_vm(mock_page_navigation):
    """Fixture to create an instance of LnEndpointViewModel."""
    return LnEndpointViewModel(mock_page_navigation)


@patch.object(local_store, 'set_value')
def test_set_ln_endpoint_invalid(mock_set_value, ln_endpoint_vm, mock_page_navigation, mock_validation_label):
    """Test set_ln_endpoint with an invalid URL."""
    node_url = 'invalid_url'
    # Capture stdout to check the printed message
    with pytest.raises(ValueError, match='Invalid URL. Please enter a valid URL.'):
        ln_endpoint_vm.set_ln_endpoint(node_url, mock_validation_label)
    mock_set_value.assert_not_called()
    mock_page_navigation.set_wallet_password_page.assert_not_called()
    mock_validation_label.assert_called_once()


def test_validate_url_valid(ln_endpoint_vm, mock_validation_label):
    """Test validate_url with a valid URL."""
    valid_url = 'https://valid.url'
    assert ln_endpoint_vm.validate_url(
        valid_url, mock_validation_label,
    ) is True
    mock_validation_label.assert_not_called()


def test_validate_url_invalid(ln_endpoint_vm, mock_validation_label):
    """Test validate_url with an invalid URL."""
    invalid_url = 'invalid_url'
    with pytest.raises(ValueError, match='Invalid URL. Please enter a valid URL.'):
        ln_endpoint_vm.validate_url(invalid_url, mock_validation_label)
    mock_validation_label.assert_called_once()


def test_on_success_method_called(ln_endpoint_vm):
    """Test when on success method called."""
    ln_endpoint_vm.stop_loading_message = MagicMock()
    ln_endpoint_vm._page_navigation = MagicMock()

    # Mock SettingRepository.get_keyring_status()
    with patch('src.viewmodels.ln_endpoint_view_model.SettingRepository') as mock_setting_repo:
        mock_setting_repo.get_keyring_status.return_value = False

        # Mock set_value from keyring_storage
        with patch('src.viewmodels.ln_endpoint_view_model.set_value') as mock_set_value:
            # Call on_success method
            ln_endpoint_vm.on_success()

            # Verify set_value was called with correct args when keyring status is False
            mock_set_value.assert_called_once_with(
                WALLET_PASSWORD_KEY, 'random@123',
            )

    # Verify other assertions
    ln_endpoint_vm.stop_loading_message.emit.assert_called_once_with(False)
    ln_endpoint_vm._page_navigation.fungibles_asset_page.assert_called_once()


@patch('src.data.repository.common_operations_repository.CommonOperationRepository')
def test_lock_wallet(mock_common_operation_repo):
    """Test the lock_wallet method."""
    # Create an instance of the view model
    ln_endpoint_vm = LnEndpointViewModel(page_navigation=mock_page_navigation)

    # Mock the run_in_thread method
    ln_endpoint_vm.run_in_thread = MagicMock()

    # Ensure that lock is a function mock
    mock_lock = MagicMock()
    mock_common_operation_repo.lock = mock_lock

    # Call the lock_wallet method
    ln_endpoint_vm.lock_wallet()

    # Verify run_in_thread was called
    ln_endpoint_vm.run_in_thread.assert_called_once()


def test_on_success_lock(ln_endpoint_vm, mock_page_navigation):
    """Test the on_success_lock method."""
    # Create a mock UnlockResponseModel with status True
    response = UnlockResponseModel(status=True)

    # Call the on_success_lock method
    ln_endpoint_vm.on_success_lock(response)

    # Check that the correct navigation method was called
    mock_page_navigation.enter_wallet_password_page.assert_called_once()


@patch('src.viewmodels.ln_endpoint_view_model.ToastManager')
@patch('src.viewmodels.ln_endpoint_view_model.logger')
@patch('src.viewmodels.ln_endpoint_view_model.QCoreApplication')
def test_on_error_wallet_not_initialized(mock_qcore, mock_logger, mock_toast_manager, mock_page_navigation):
    """Test the on_error method when error is ERROR_NODE_WALLET_NOT_INITIALIZED"""
    ln_endpoint_vm = LnEndpointViewModel(page_navigation=mock_page_navigation)
    ln_endpoint_vm.stop_loading_message = MagicMock()

    # Mock translate to return 'not_initialized'
    mock_qcore.translate.return_value = 'not_initialized'
    error = CommonException('not_initialized')

    ln_endpoint_vm.on_error(error)

    # Verify stop_loading_message signal
    ln_endpoint_vm.stop_loading_message.emit.assert_called_once_with(False)

    # Verify navigation page change
    mock_page_navigation.set_wallet_password_page.assert_called_once_with(
        WalletType.REMOTE_TYPE_WALLET.value,
    )

    # Verify ToastManager call
    mock_toast_manager.info.assert_called_once_with(
        description='not_initialized',
    )

    # Verify logger call
    mock_logger.error.assert_called_once_with(
        'Exception occurred: %s, Message: %s',
        type(error).__name__,
        str(error),
    )


@patch('src.viewmodels.ln_endpoint_view_model.ToastManager')
def test_on_error_lock(mock_toast_manager, ln_endpoint_vm):
    """Test the on_error_lock method."""
    # Setup
    ln_endpoint_vm.stop_loading_message = MagicMock()
    error = CommonException('test error message')

    # Call the method
    ln_endpoint_vm.on_error_lock(error)

    # Verify stop_loading_message signal
    ln_endpoint_vm.stop_loading_message.emit.assert_called_once_with(False)

    # Verify ToastManager call
    mock_toast_manager.error.assert_called_once_with(
        description='test error message',
    )


@patch('src.viewmodels.ln_endpoint_view_model.get_bitcoin_config')
@patch('src.utils.local_store.LocalStore.set_value')
def test_set_ln_endpoint_success(mock_set_value, mock_get_bitcoin_config, ln_endpoint_vm):
    """Test set_ln_endpoint method with valid URL."""
    # Setup
    ln_endpoint_vm.loading_message = MagicMock()
    ln_endpoint_vm.validate_url = MagicMock(return_value=True)
    ln_endpoint_vm.run_in_thread = MagicMock()
    mock_validation_label = MagicMock()

    test_url = 'test_url'
    test_config = MagicMock()  # Mock UnlockRequestModel instead of instantiating
    mock_get_bitcoin_config.return_value = test_config

    # Execute
    ln_endpoint_vm.set_ln_endpoint(test_url, mock_validation_label)

    # Assert
    ln_endpoint_vm.loading_message.emit.assert_has_calls([
        call(True),
        call(True),
    ])
    ln_endpoint_vm.validate_url.assert_called_once_with(
        test_url, mock_validation_label,
    )
    mock_set_value.assert_called_once_with(LIGHTNING_URL_KEY, test_url)
    mock_get_bitcoin_config.assert_called_once_with(
        network=ln_endpoint_vm.network, password='random@123',
    )

    # Verify run_in_thread call
    ln_endpoint_vm.run_in_thread.assert_called_once()
    run_thread_args = ln_endpoint_vm.run_in_thread.call_args[0]
    run_thread_kwargs = ln_endpoint_vm.run_in_thread.call_args[0][1]

    assert run_thread_args[0] is CommonOperationRepository.unlock
    assert run_thread_kwargs['args'] == [test_config]
    assert run_thread_kwargs['callback'] == ln_endpoint_vm.on_success
    assert run_thread_kwargs['error_callback'] == ln_endpoint_vm.on_error


def test_set_ln_endpoint_invalid_url(ln_endpoint_vm):
    """Test set_ln_endpoint method with invalid URL."""
    # Setup
    ln_endpoint_vm.loading_message = MagicMock()
    ln_endpoint_vm.validate_url = MagicMock(return_value=False)
    ln_endpoint_vm.run_in_thread = MagicMock()
    mock_validation_label = MagicMock()

    test_url = 'invalid_url'

    # Execute
    ln_endpoint_vm.set_ln_endpoint(test_url, mock_validation_label)

    # Assert
    ln_endpoint_vm.loading_message.emit.assert_called_once_with(True)
    ln_endpoint_vm.validate_url.assert_called_once_with(
        test_url, mock_validation_label,
    )
    ln_endpoint_vm.run_in_thread.assert_not_called()


def test_on_error_common_exception_not_initialized(ln_endpoint_vm, mocker):
    """Test on_error method with CommonException and not_initialized message."""
    # Setup
    ln_endpoint_vm.stop_loading_message = MagicMock()
    mock_toast_manager = mocker.patch(
        'src.views.components.toast.ToastManager.info',
    )
    mock_logger = mocker.patch(
        'src.viewmodels.ln_endpoint_view_model.logger.error',
    )
    error_msg = QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'not_initialized', None,
    )
    error = CommonException(error_msg)

    # Execute
    ln_endpoint_vm.on_error(error)

    # Assert
    ln_endpoint_vm.stop_loading_message.emit.assert_called_once_with(False)
    ln_endpoint_vm._page_navigation.set_wallet_password_page.assert_called_once_with(
        WalletType.REMOTE_TYPE_WALLET.value,
    )
    mock_toast_manager.assert_called_once_with(description=error_msg)
    mock_logger.assert_called_once_with(
        'Exception occurred: %s, Message: %s',
        'CommonException', str(error),
    )


def test_on_error_common_exception_wrong_password(ln_endpoint_vm, mocker):
    """Test on_error method with CommonException and wrong_password message."""
    # Setup
    ln_endpoint_vm.stop_loading_message = MagicMock()
    mock_toast_manager = mocker.patch(
        'src.views.components.toast.ToastManager.info',
    )
    mock_logger = mocker.patch(
        'src.viewmodels.ln_endpoint_view_model.logger.error',
    )
    error_msg = QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'wrong_password', None,
    )
    error = CommonException(error_msg)

    # Execute
    ln_endpoint_vm.on_error(error)

    # Assert
    ln_endpoint_vm.stop_loading_message.emit.assert_called_once_with(False)
    ln_endpoint_vm._page_navigation.enter_wallet_password_page.assert_called_once()
    mock_toast_manager.assert_called_once_with(description=error_msg)
    mock_logger.assert_called_once_with(
        'Exception occurred: %s, Message: %s',
        'CommonException', str(error),
    )


def test_on_error_common_exception_unlocked_node(ln_endpoint_vm, mocker):
    """Test on_error method with CommonException and unlocked_node message."""
    # Setup
    ln_endpoint_vm.stop_loading_message = MagicMock()
    ln_endpoint_vm.lock_wallet = MagicMock()
    mock_toast_manager = mocker.patch(
        'src.views.components.toast.ToastManager.info',
    )
    mock_logger = mocker.patch(
        'src.viewmodels.ln_endpoint_view_model.logger.error',
    )
    error_msg = QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'already_unlocked', None,
    )
    error = CommonException(error_msg)

    # Execute
    ln_endpoint_vm.on_error(error)

    # Assert
    ln_endpoint_vm.stop_loading_message.emit.assert_called_once_with(False)
    ln_endpoint_vm.lock_wallet.assert_called_once()
    mock_toast_manager.assert_called_once_with(description=error_msg)
    mock_logger.assert_called_once_with(
        'Exception occurred: %s, Message: %s',
        'CommonException', str(error),
    )


def test_on_error_common_exception_locked_node(ln_endpoint_vm, mocker):
    """Test on_error method with CommonException and locked_node message."""
    # Setup
    ln_endpoint_vm.stop_loading_message = MagicMock()
    mock_toast_manager = mocker.patch(
        'src.views.components.toast.ToastManager.info',
    )
    mock_logger = mocker.patch(
        'src.viewmodels.ln_endpoint_view_model.logger.error',
    )
    error_msg = QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'locked_node', None,
    )
    error = CommonException(error_msg)

    # Execute
    ln_endpoint_vm.on_error(error)

    # Assert
    ln_endpoint_vm.stop_loading_message.emit.assert_called_once_with(False)
    ln_endpoint_vm._page_navigation.enter_wallet_password_page.assert_called_once()
    mock_toast_manager.assert_called_once_with(description=error_msg)
    mock_logger.assert_called_once_with(
        'Exception occurred: %s, Message: %s',
        'CommonException', str(error),
    )


def test_on_error_generic_exception(ln_endpoint_vm, mocker):
    """Test on_error method with generic Exception."""
    # Setup
    mock_logger = mocker.patch(
        'src.viewmodels.ln_endpoint_view_model.logger.error',
    )
    error = Exception('Test error')

    # Execute
    ln_endpoint_vm.on_error(error)

    # Assert
    mock_logger.assert_called_once_with(
        'Exception occurred: %s, Message: %s',
        'Exception', str(error),
    )
