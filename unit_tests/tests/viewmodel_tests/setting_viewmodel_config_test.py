"""Unit tests for the configuration functionality of the SettingViewModel.

This test module focuses on the configurable settings cards in the SettingViewModel, including:
- Fee rate configuration
- Lightning invoice expiry time configuration
- Minimum confirmation configuration
- Proxy endpoint configuration
- Indexer URL configuration
- Bitcoin RPC host/port configuration
- Lightning node announcement settings

The tests are separated from the main SettingViewModel tests due to the large number
of test cases and to maintain better organization.
"""
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QCoreApplication

from src.model.common_operation_model import CheckIndexerUrlRequestModel
from src.model.common_operation_model import CheckProxyEndpointRequestModel
from src.model.setting_model import IsDefaultEndpointSet
from src.model.setting_model import IsDefaultExpiryTimeSet
from src.model.setting_model import IsDefaultFeeRateSet
from src.model.setting_model import IsDefaultMinConfirmationSet
from src.utils.constant import FEE_RATE
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import LN_INVOICE_EXPIRY_TIME
from src.utils.constant import LN_INVOICE_EXPIRY_TIME_UNIT
from src.utils.constant import MIN_CONFIRMATION
from src.utils.constant import SAVED_ANNOUNCE_ADDRESS
from src.utils.constant import SAVED_ANNOUNCE_ALIAS
from src.utils.constant import SAVED_BITCOIND_RPC_HOST
from src.utils.constant import SAVED_BITCOIND_RPC_PORT
from src.utils.constant import SAVED_INDEXER_URL
from src.utils.constant import SAVED_PROXY_ENDPOINT
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.error_message import ERROR_UNABLE_TO_SET_EXPIRY_TIME
from src.utils.error_message import ERROR_UNABLE_TO_SET_FEE
from src.utils.error_message import ERROR_UNABLE_TO_SET_INDEXER_URL
from src.utils.error_message import ERROR_UNABLE_TO_SET_MIN_CONFIRMATION
from src.utils.error_message import ERROR_UNABLE_TO_SET_PROXY_ENDPOINT
from src.utils.info_message import INFO_SET_EXPIRY_TIME_SUCCESSFULLY
from src.utils.info_message import INFO_SET_MIN_CONFIRMATION_SUCCESSFULLY
from src.viewmodels.setting_view_model import SettingViewModel


@pytest.fixture
def mock_page_navigation(mocker):
    """Fixture to create a mock page navigation object."""
    return mocker.MagicMock()


@pytest.fixture
def setting_view_model(mock_page_navigation):
    """Fixture to create an instance of the SettingViewModel class."""
    return SettingViewModel(mock_page_navigation)


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_default_fee_rate_true(mock_toast_manager, mock_setting_card_repository, setting_view_model):
    """Test the set_default_fee_rate method when success fully set."""
    mock_setting_card_repository.set_default_fee_rate.return_value = IsDefaultFeeRateSet(
        is_enabled=True,
    )

    # Connect the signal to a mock slot
    fee_rate_set_event_slot = Mock()
    setting_view_model.fee_rate_set_event.connect(fee_rate_set_event_slot)

    setting_view_model.set_default_fee_rate('0.5')

    mock_setting_card_repository.set_default_fee_rate.assert_called_once_with(
        '0.5',
    )
    fee_rate_set_event_slot.assert_called_once_with('0.5')

    # Test exception handling
    mock_setting_card_repository.set_default_fee_rate.side_effect = CommonException(
        'Error',
    )
    setting_view_model.set_default_fee_rate('0.5')
    fee_rate_set_event_slot.assert_called_with(str(FEE_RATE))
    mock_toast_manager.error.assert_called_with(
        description='Error',
    )

    mock_setting_card_repository.set_default_fee_rate.side_effect = Exception
    setting_view_model.set_default_fee_rate('0.5')
    fee_rate_set_event_slot.assert_called_with(str(FEE_RATE))
    mock_toast_manager.error.assert_called_with(
        description=ERROR_SOMETHING_WENT_WRONG,
    )


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_default_fee_rate_false(mock_toast_manager, mock_setting_card_repository, setting_view_model):
    """Test the set_default_fee_rate method when not set."""
    mock_setting_card_repository.set_default_fee_rate.return_value = IsDefaultFeeRateSet(
        is_enabled=False,
    )

    # Connect the signal to a mock slot
    fee_rate_set_event_slot = Mock()
    setting_view_model.fee_rate_set_event.connect(fee_rate_set_event_slot)

    setting_view_model.set_default_fee_rate('0.5')

    mock_setting_card_repository.set_default_fee_rate.assert_called_once_with(
        '0.5',
    )
    fee_rate_set_event_slot.assert_called_once_with(str(FEE_RATE))

    mock_toast_manager.error.assert_called_with(
        description=ERROR_UNABLE_TO_SET_FEE,
    )


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_default_expiry_time_true(mock_toast_manager, mock_setting_card_repository, setting_view_model):
    """Test the set_default_expiry_time method when successfully set."""
    mock_setting_card_repository.set_default_expiry_time.return_value = IsDefaultExpiryTimeSet(
        is_enabled=True,
    )
    setting_view_model.expiry_time_set_event = Mock()
    setting_view_model.on_page_load = Mock()

    setting_view_model.set_default_expiry_time(600, 'seconds')

    mock_setting_card_repository.set_default_expiry_time.assert_called_once_with(
        600, 'seconds',
    )
    setting_view_model.expiry_time_set_event.emit.assert_called_once_with(
        600, 'seconds',
    )
    mock_toast_manager.success.assert_called_once_with(
        description=INFO_SET_EXPIRY_TIME_SUCCESSFULLY,
    )
    setting_view_model.on_page_load.assert_called_once()

    # Test exception handling
    mock_setting_card_repository.set_default_expiry_time.side_effect = CommonException(
        'Error',
    )
    setting_view_model.set_default_expiry_time(600, 'seconds')
    setting_view_model.expiry_time_set_event.emit.assert_called_with(
        str(LN_INVOICE_EXPIRY_TIME),
        str(LN_INVOICE_EXPIRY_TIME_UNIT),
    )
    mock_toast_manager.error.assert_called_with(description='Error')

    mock_setting_card_repository.set_default_expiry_time.side_effect = Exception
    setting_view_model.set_default_expiry_time(600, 'seconds')
    setting_view_model.expiry_time_set_event.emit.assert_called_with(
        str(LN_INVOICE_EXPIRY_TIME),
        str(LN_INVOICE_EXPIRY_TIME_UNIT),
    )
    mock_toast_manager.error.assert_called_with(
        description=ERROR_SOMETHING_WENT_WRONG,
    )


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_default_expiry_time_false(mock_toast_manager, mock_setting_card_repository, setting_view_model):
    """Test the set_default_expiry_time method when not set."""
    mock_setting_card_repository.set_default_expiry_time.return_value = IsDefaultExpiryTimeSet(
        is_enabled=False,
    )
    setting_view_model.expiry_time_set_event = Mock()

    setting_view_model.set_default_expiry_time(600, 'minutes')

    mock_setting_card_repository.set_default_expiry_time.assert_called_once_with(
        600, 'minutes',
    )
    setting_view_model.expiry_time_set_event.emit.assert_called_once_with(
        str(LN_INVOICE_EXPIRY_TIME),
        str(LN_INVOICE_EXPIRY_TIME_UNIT),
    )
    mock_toast_manager.error.assert_called_once_with(
        description=ERROR_UNABLE_TO_SET_EXPIRY_TIME,
    )


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
def test_on_success_of_indexer_url_set(mock_setting_card_repository, setting_view_model):
    """Test on_success_of_indexer_url_set method."""
    setting_view_model.unlock_the_wallet = Mock(return_value=True)
    setting_view_model.indexer_url_set_event = Mock()
    mock_setting_card_repository.set_default_endpoints.return_value = IsDefaultEndpointSet(
        is_enabled=True,
    )

    indexer_url = 'http://test.url'
    setting_view_model.on_success_of_indexer_url_set(indexer_url)

    setting_view_model.unlock_the_wallet.assert_called_once_with(
        SAVED_INDEXER_URL, indexer_url,
    )
    mock_setting_card_repository.set_default_endpoints.assert_called_once_with(
        SAVED_INDEXER_URL, indexer_url,
    )
    setting_view_model.indexer_url_set_event.emit.assert_called_once_with(
        indexer_url,
    )


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_on_error_of_indexer_url_set(mock_toast_manager, setting_view_model):
    """Test on_error_of_indexer_url_set method."""
    setting_view_model._page_navigation = Mock()
    setting_view_model.unlock_the_wallet = Mock(
        side_effect=CommonException('Unlock error'),
    )
    setting_view_model.on_error_of_indexer_url_set()

    mock_toast_manager.error.assert_has_calls([
        call(description=ERROR_UNABLE_TO_SET_INDEXER_URL),
        call(description='Unlock failed: Unlock error'),
    ])
    setting_view_model._page_navigation.settings_page.assert_called_once()


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
def test_check_indexer_url_endpoint(mock_setting_card_repository, setting_view_model):
    """Test check_indexer_url_endpoint method."""
    setting_view_model.is_loading = Mock()
    setting_view_model.run_in_thread = Mock()

    indexer_url = '  http://test.url  '
    password = 'test_password'

    setting_view_model.check_indexer_url_endpoint(indexer_url, password)

    setting_view_model.is_loading.emit.assert_called_once_with(True)
    assert setting_view_model.password == password
    setting_view_model.run_in_thread.assert_called_once()
    call_args = setting_view_model.run_in_thread.call_args[0][1]
    assert isinstance(call_args['args'][0], CheckIndexerUrlRequestModel)
    assert call_args['args'][0].indexer_url == indexer_url.strip()


@patch('src.viewmodels.setting_view_model.CommonOperationRepository')
@patch('src.viewmodels.setting_view_model.SettingRepository')
@patch('src.viewmodels.setting_view_model.get_bitcoin_config')
def test_unlock_the_wallet(mock_get_bitcoin_config, mock_setting_repository, mock_common_operation_repository, setting_view_model):
    """Test unlock_the_wallet method."""
    setting_view_model.password = 'test_password'
    setting_view_model.run_in_thread = Mock()
    mock_setting_repository.get_wallet_network.return_value = 'test_network'
    mock_get_bitcoin_config.return_value = {'config': 'test'}

    # Create a mock dictionary with copy method that returns a new dict
    mock_config = MagicMock()
    mock_config.copy.return_value = {
        'config': 'test', 'test_key': 'test_value',
    }
    mock_get_bitcoin_config.return_value = mock_config

    setting_view_model.unlock_the_wallet('test_key', 'test_value')

    mock_setting_repository.get_wallet_network.assert_called_once()
    mock_get_bitcoin_config.assert_called_once_with(
        'test_network', 'test_password',
    )
    setting_view_model.run_in_thread.assert_called_once()


@patch('src.viewmodels.setting_view_model.ToastManager')
@patch('src.viewmodels.setting_view_model.local_store')
@patch('src.viewmodels.setting_view_model.QCoreApplication')
def test_on_success_of_unlock(mock_qcore_application, mock_local_store, mock_toast_manager, setting_view_model):
    """Test _on_success_of_unlock method."""
    setting_view_model.is_loading = Mock()
    setting_view_model.on_page_load = Mock()
    mock_qcore_application.translate.return_value = 'translated_key'

    # Test with regular string value
    setting_view_model._on_success_of_unlock(SAVED_INDEXER_URL, 'test_value')
    mock_local_store.set_value.assert_called_with(
        SAVED_INDEXER_URL, 'test_value',
    )

    # Test with list value
    test_list = ['item1', 'item2', 'item3']
    setting_view_model._on_success_of_unlock(SAVED_INDEXER_URL, test_list)
    mock_local_store.set_value.assert_called_with(
        SAVED_INDEXER_URL, 'item1, item2, item3',
    )

    mock_toast_manager.success.assert_called()
    setting_view_model.is_loading.emit.assert_called_with(False)
    setting_view_model.on_page_load.assert_called()


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_on_error_of_unlock_wrong_password(mock_toast_manager, setting_view_model):
    """Test _on_error_of_unlock method with wrong password."""
    setting_view_model.is_loading = Mock()
    setting_view_model._page_navigation = Mock()
    setting_view_model.unlock_the_wallet = Mock()
    error = CommonException(
        QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'wrong_password', None,
        ),
    )

    setting_view_model._on_error_of_unlock(error)

    mock_toast_manager.error.assert_called_once_with(description=error.message)
    setting_view_model._page_navigation.enter_wallet_password_page.assert_called_once()
    setting_view_model.unlock_the_wallet.assert_not_called()
    setting_view_model.is_loading.emit.assert_not_called()


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_on_error_of_unlock_other_error(mock_toast_manager, setting_view_model):
    """Test _on_error_of_unlock method with non-password error."""
    setting_view_model.is_loading = Mock()
    setting_view_model.unlock_the_wallet = Mock()
    error = CommonException('Some other error')

    setting_view_model._on_error_of_unlock(error)

    mock_toast_manager.error.assert_called_once_with(
        description=f"Unlock failed: {error.message}",
    )
    setting_view_model.is_loading.emit.assert_has_calls([call(False)])
    setting_view_model.unlock_the_wallet.assert_called_once()


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_on_error_of_unlock_exception_in_handler(mock_toast_manager, setting_view_model):
    """Test _on_error_of_unlock method when handler raises exception."""
    setting_view_model.is_loading = Mock()
    setting_view_model.unlock_the_wallet = Mock(
        side_effect=CommonException('Handler error'),
    )
    error = CommonException('Initial error')

    setting_view_model._on_error_of_unlock(error)

    mock_toast_manager.error.assert_has_calls([
        call(description='Unlock failed: Initial error'),
        call(description='Unlock failed: Handler error'),
    ])
    setting_view_model.is_loading.emit.assert_has_calls(
        [call(False), call(False)],
    )


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
def test_on_success_of_proxy_endpoint_set(mock_setting_card_repository, setting_view_model):
    """Test _on_success_of_proxy_endpoint_set method."""
    setting_view_model.unlock_the_wallet = Mock(return_value=True)
    setting_view_model.proxy_endpoint_set_event = Mock()
    mock_setting_card_repository.set_default_endpoints.return_value = IsDefaultEndpointSet(
        is_enabled=True,
    )

    proxy_endpoint = 'http://test.proxy'
    setting_view_model._on_success_of_proxy_endpoint_set(proxy_endpoint)

    setting_view_model.unlock_the_wallet.assert_called_once_with(
        SAVED_PROXY_ENDPOINT, proxy_endpoint,
    )
    mock_setting_card_repository.set_default_endpoints.assert_called_once_with(
        SAVED_PROXY_ENDPOINT, proxy_endpoint,
    )
    setting_view_model.proxy_endpoint_set_event.emit.assert_called_once_with(
        proxy_endpoint,
    )


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_on_error_of_proxy_endpoint_set(mock_toast_manager, setting_view_model):
    """Test _on_error_of_proxy_endpoint_set method."""
    setting_view_model._page_navigation = Mock()
    setting_view_model.unlock_the_wallet = Mock(
        side_effect=CommonException('Unlock error'),
    )

    setting_view_model._on_error_of_proxy_endpoint_set()

    mock_toast_manager.error.assert_has_calls([
        call(description=ERROR_UNABLE_TO_SET_PROXY_ENDPOINT),
        call(description='Unlock failed: Unlock error'),
    ])
    setting_view_model._page_navigation.settings_page.assert_called_once()


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
def test_check_proxy_endpoint(mock_setting_card_repository, setting_view_model):
    """Test check_proxy_endpoint method."""
    setting_view_model.is_loading = Mock()
    setting_view_model.run_in_thread = Mock()

    proxy_endpoint = '  http://test.proxy  '
    password = 'test_password'

    setting_view_model.check_proxy_endpoint(proxy_endpoint, password)

    setting_view_model.is_loading.emit.assert_called_once_with(True)
    assert setting_view_model.password == password
    setting_view_model.run_in_thread.assert_called_once()
    call_args = setting_view_model.run_in_thread.call_args[0][1]
    assert isinstance(call_args['args'][0], CheckProxyEndpointRequestModel)
    assert call_args['args'][0].proxy_endpoint == proxy_endpoint.strip()


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
def test_set_bitcoind_host_success(mock_setting_card_repository, setting_view_model):
    """Test set_bitcoind_host method success case."""
    setting_view_model.is_loading = Mock()
    setting_view_model._lock_wallet = Mock(return_value=True)
    setting_view_model.bitcoind_rpc_host_set_event = Mock()
    setting_view_model.on_page_load = Mock()
    mock_setting_card_repository.set_default_endpoints.return_value = IsDefaultEndpointSet(
        is_enabled=True,
    )

    setting_view_model.set_bitcoind_host('localhost', 'password')

    setting_view_model.is_loading.emit.assert_called_once_with(True)
    setting_view_model._lock_wallet.assert_called_once_with(
        SAVED_BITCOIND_RPC_HOST, 'localhost',
    )
    mock_setting_card_repository.set_default_endpoints.assert_called_once_with(
        SAVED_BITCOIND_RPC_HOST, 'localhost',
    )
    setting_view_model.bitcoind_rpc_host_set_event.emit.assert_called_once_with(
        'localhost',
    )
    setting_view_model.on_page_load.assert_called_once()


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_bitcoind_host_error(mock_toast_manager, setting_view_model):
    """Test set_bitcoind_host method error case."""
    setting_view_model.is_loading = Mock()
    error = CommonException('Test error')
    setting_view_model._lock_wallet = Mock(side_effect=error)

    setting_view_model.set_bitcoind_host('localhost', 'password')

    setting_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_manager.error.assert_called_once_with(description=error.message)


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
def test_set_bitcoind_port_success(mock_setting_card_repository, setting_view_model):
    """Test set_bitcoind_port method success case."""
    setting_view_model.is_loading = Mock()
    setting_view_model._lock_wallet = Mock(return_value=True)
    setting_view_model.bitcoind_rpc_port_set_event = Mock()
    setting_view_model.on_page_load = Mock()
    mock_setting_card_repository.set_default_endpoints.return_value = IsDefaultEndpointSet(
        is_enabled=True,
    )

    setting_view_model.set_bitcoind_port(8332, 'password')

    setting_view_model.is_loading.emit.assert_called_once_with(True)
    setting_view_model._lock_wallet.assert_called_once_with(
        SAVED_BITCOIND_RPC_PORT, 8332,
    )
    mock_setting_card_repository.set_default_endpoints.assert_called_once_with(
        SAVED_BITCOIND_RPC_PORT, 8332,
    )
    setting_view_model.bitcoind_rpc_port_set_event.emit.assert_called_once_with(
        8332,
    )
    setting_view_model.on_page_load.assert_called_once()


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_bitcoind_port_error(mock_toast_manager, setting_view_model):
    """Test set_bitcoind_port method error case."""
    setting_view_model.is_loading = Mock()
    error = CommonException('Test error')
    setting_view_model._lock_wallet = Mock(side_effect=error)

    setting_view_model.set_bitcoind_port(8332, 'password')

    setting_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_manager.error.assert_called_once_with(description=error.message)


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
def test_set_announce_address_success(mock_setting_card_repository, setting_view_model):
    """Test set_announce_address method success case."""
    setting_view_model.is_loading = Mock()
    setting_view_model._lock_wallet = Mock(return_value=True)
    setting_view_model.announce_address_set_event = Mock()
    setting_view_model.on_page_load = Mock()
    mock_setting_card_repository.set_default_endpoints.return_value = IsDefaultEndpointSet(
        is_enabled=True,
    )

    setting_view_model.set_announce_address('test_address', 'password')

    setting_view_model.is_loading.emit.assert_called_once_with(True)
    setting_view_model._lock_wallet.assert_called_once_with(
        SAVED_ANNOUNCE_ADDRESS, ['test_address'],
    )
    mock_setting_card_repository.set_default_endpoints.assert_called_once_with(
        SAVED_ANNOUNCE_ADDRESS, 'test_address',
    )
    setting_view_model.announce_address_set_event.emit.assert_called_once_with(
        'test_address',
    )
    setting_view_model.on_page_load.assert_called_once()


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_announce_address_error(mock_toast_manager, setting_view_model):
    """Test set_announce_address method error case."""
    setting_view_model.is_loading = Mock()
    error = CommonException('Test error')
    setting_view_model._lock_wallet = Mock(side_effect=error)

    setting_view_model.set_announce_address('test_address', 'password')

    setting_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_manager.error.assert_called_once_with(description=error.message)


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
def test_set_announce_alias_success(mock_setting_card_repository, setting_view_model):
    """Test set_announce_alias method success case."""
    setting_view_model.is_loading = Mock()
    setting_view_model._lock_wallet = Mock(return_value=True)
    setting_view_model.announce_alias_set_event = Mock()
    setting_view_model.on_page_load = Mock()
    mock_setting_card_repository.set_default_endpoints.return_value = IsDefaultEndpointSet(
        is_enabled=True,
    )

    setting_view_model.set_announce_alias('test_alias', 'password')

    setting_view_model.is_loading.emit.assert_called_once_with(True)
    setting_view_model._lock_wallet.assert_called_once_with(
        SAVED_ANNOUNCE_ALIAS, 'test_alias',
    )
    mock_setting_card_repository.set_default_endpoints.assert_called_once_with(
        SAVED_ANNOUNCE_ALIAS, 'test_alias',
    )
    setting_view_model.announce_alias_set_event.emit.assert_called_once_with(
        'test_alias',
    )
    setting_view_model.on_page_load.assert_called_once()


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_announce_alias_error(mock_toast_manager, setting_view_model):
    """Test set_announce_alias method error case."""
    setting_view_model.is_loading = Mock()
    error = CommonException('Test error')
    setting_view_model._lock_wallet = Mock(side_effect=error)

    setting_view_model.set_announce_alias('test_alias', 'password')

    setting_view_model.is_loading.emit.assert_has_calls(
        [call(True), call(False)],
    )
    mock_toast_manager.error.assert_called_once_with(description=error.message)


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_min_confirmation_success(mock_toast_manager, mock_setting_card_repository, setting_view_model):
    """Test set_min_confirmation method success case."""
    setting_view_model.min_confirmation_set_event = Mock()
    setting_view_model.on_page_load = Mock()
    mock_setting_card_repository.set_default_min_confirmation.return_value = IsDefaultMinConfirmationSet(
        is_enabled=True,
    )

    setting_view_model.set_min_confirmation(6)

    mock_setting_card_repository.set_default_min_confirmation.assert_called_once_with(
        6,
    )
    mock_toast_manager.success.assert_called_once_with(
        description=INFO_SET_MIN_CONFIRMATION_SUCCESSFULLY,
    )
    setting_view_model.min_confirmation_set_event.emit.assert_called_once_with(
        6,
    )
    setting_view_model.on_page_load.assert_called_once()

    # Test CommonException handling
    mock_setting_card_repository.set_default_min_confirmation.side_effect = CommonException(
        'Error',
    )
    setting_view_model.set_min_confirmation(6)
    setting_view_model.min_confirmation_set_event.emit.assert_called_with(
        MIN_CONFIRMATION,
    )
    mock_toast_manager.error.assert_called_with(description='Error')

    # Test generic Exception handling
    mock_setting_card_repository.set_default_min_confirmation.side_effect = Exception()
    setting_view_model.set_min_confirmation(6)
    setting_view_model.min_confirmation_set_event.emit.assert_called_with(
        MIN_CONFIRMATION,
    )
    mock_toast_manager.error.assert_called_with(
        description=ERROR_SOMETHING_WENT_WRONG,
    )


@patch('src.viewmodels.setting_view_model.SettingCardRepository')
@patch('src.viewmodels.setting_view_model.ToastManager')
def test_set_min_confirmation_failure(mock_toast_manager, mock_setting_card_repository, setting_view_model):
    """Test set_min_confirmation method failure case."""
    setting_view_model.min_confirmation_set_event = Mock()
    mock_setting_card_repository.set_default_min_confirmation.return_value = IsDefaultMinConfirmationSet(
        is_enabled=False,
    )

    setting_view_model.set_min_confirmation(6)

    setting_view_model.min_confirmation_set_event.emit.assert_called_once_with(
        MIN_CONFIRMATION,
    )
    mock_toast_manager.error.assert_called_once_with(
        description=ERROR_UNABLE_TO_SET_MIN_CONFIRMATION,
    )


@patch('src.viewmodels.setting_view_model.CommonOperationRepository')
def test_lock_wallet(mock_common_operation_repository, setting_view_model):
    """Test _lock_wallet method."""
    setting_view_model.run_in_thread = Mock()

    setting_view_model._lock_wallet('test_key', 'test_value')

    assert setting_view_model.key == 'test_key'
    assert setting_view_model.value == 'test_value'
    setting_view_model.run_in_thread.assert_called_once()
    call_args = setting_view_model.run_in_thread.call_args[0][1]
    assert call_args['args'] == []
    assert call_args['callback'] == setting_view_model._on_success_lock
    assert call_args['error_callback'] == setting_view_model._on_error_lock


def test_on_success_lock(setting_view_model):
    """Test _on_success_lock method."""
    setting_view_model.unlock_the_wallet = Mock()
    setting_view_model.key = 'test_key'
    setting_view_model.value = 'test_value'

    setting_view_model._on_success_lock()

    setting_view_model.unlock_the_wallet.assert_called_once_with(
        'test_key', 'test_value',
    )


@patch('src.viewmodels.setting_view_model.ToastManager')
def test_on_error_lock(mock_toast_manager, setting_view_model):
    """Test _on_error_lock method."""
    setting_view_model.is_loading = Mock()
    error = CommonException('Test error')

    setting_view_model._on_error_lock(error)

    setting_view_model.is_loading.emit.assert_called_once_with(False)
    mock_toast_manager.error.assert_called_once_with(description=error.message)
