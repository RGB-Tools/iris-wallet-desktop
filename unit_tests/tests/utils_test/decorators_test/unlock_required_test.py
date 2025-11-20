# Unit test for unlock required decorator
# pylint: disable=redefined-outer-name,unused-argument,too-many-arguments
"""Unit tests for unlocked_required decorator"""
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError

from src.data.repository.setting_repository import SettingRepository
from src.model.common_operation_model import UnlockRequestModel
from src.model.enums.enums_model import NetworkEnumModel
from src.utils.decorators.unlock_required import unlock_node
from src.utils.decorators.unlock_required import unlock_required
from src.utils.endpoints import NODE_INFO_ENDPOINT
from src.utils.endpoints import UNLOCK_ENDPOINT
from src.utils.error_message import ERROR_NODE_IS_LOCKED_CALL_UNLOCK
from src.utils.error_message import ERROR_NODE_WALLET_NOT_INITIALIZED
from src.utils.error_message import ERROR_PASSWORD_INCORRECT
from src.utils.handle_exception import CommonException
from src.utils.helpers import check_node
from src.utils.page_navigation_events import PageNavigationEventManager
from src.utils.request import Request


@pytest.fixture
def test_response():
    """Fixture to create a generic mock response object."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {}
    return mock_resp


@patch.object(Request, 'post')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status', return_value=False)
@patch('src.utils.decorators.unlock_required.get_value', return_value='mock_password')
@patch(
    'src.utils.decorators.unlock_required.get_bitcoin_config', return_value=UnlockRequestModel(
        password='mock_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='password',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    ),
)
def test_unlock_node_success(mock_get_bitcoin_config, mock_get_value, mock_get_keyring_status, mock_post):
    """Test successful unlock of the node."""
    # Mock response setup
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'status': 'success'}

    # Assign the mock response to the post return value
    mock_post.return_value = mock_response

    # Call the unlock_node function
    result = unlock_node()

    # Asserts that the result is True since the response is successful
    assert result is True

    # Ensure that post is called with the expected payload
    mock_post.assert_called_once_with(
        UNLOCK_ENDPOINT, mock_get_bitcoin_config.return_value.model_dump(),
    )


@patch('src.utils.decorators.unlock_required.get_value')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status')
@patch('src.utils.decorators.unlock_required.get_bitcoin_config')
@patch.object(Request, 'post')
def test_unlock_node_http_error(mock_post, mock_get_config, mock_get_keyring_status, mock_get_value, test_response):
    """Test unlock node with an HTTP error."""
    # Setup mocks
    mock_get_keyring_status.return_value = False
    mock_get_value.return_value = 'test_password'
    mock_get_config.return_value = UnlockRequestModel(
        password='test_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='pass',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    )

    # Setup HTTP error response
    test_response.status_code = 401
    test_response.json.return_value = {
        'error': ERROR_PASSWORD_INCORRECT,
        'code': 401,
    }
    mock_post.side_effect = HTTPError(response=test_response)

    # Test the error handling
    with patch.object(PageNavigationEventManager.get_instance(), 'enter_wallet_password_page_signal') as mock_navigate_signal:
        with patch('src.utils.decorators.unlock_required.logger.error') as mock_logger:
            with pytest.raises(CommonException) as exc_info:
                unlock_node()

            # Verify the error was logged
            mock_logger.assert_called_once_with(ERROR_PASSWORD_INCORRECT)
            # Verify navigation signal was emitted
            mock_navigate_signal.emit.assert_called_once()
            # Verify correct exception was raised
            assert str(exc_info.value) == ERROR_PASSWORD_INCORRECT


@patch('src.utils.decorators.unlock_required.get_value')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status')
@patch('src.utils.decorators.unlock_required.get_bitcoin_config')
@patch.object(Request, 'post')
def test_unlock_node_wallet_not_initialized(
    mock_post, mock_get_config, mock_get_keyring_status, mock_get_value, test_response,
):
    """Test unlock node with wallet not initialized error."""
    # Setup mocks
    mock_get_keyring_status.return_value = False
    mock_get_value.return_value = 'test_password'
    mock_get_config.return_value = UnlockRequestModel(
        password='test_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='pass',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    )

    test_response.status_code = 403
    test_response.json.return_value = {
        'error': ERROR_NODE_WALLET_NOT_INITIALIZED,
        'code': 403,
    }
    mock_post.side_effect = HTTPError(response=test_response)

    with patch.object(PageNavigationEventManager.get_instance(), 'term_and_condition_page_signal') as mock_navigate_signal:
        with patch.object(SettingRepository, 'unset_wallet_initialized') as mock_unset_wallet_initialized:
            with patch('src.utils.decorators.unlock_required.logger.error') as mock_logger:
                with pytest.raises(CommonException) as exc_info:
                    unlock_node()

                # Verify error was logged
                mock_logger.assert_called_once_with(
                    ERROR_NODE_WALLET_NOT_INITIALIZED,
                )
                # Verify wallet was uninitialized
                mock_unset_wallet_initialized.assert_called_once()
                # Verify navigation signal was emitted
                mock_navigate_signal.emit.assert_called_once()
                # Verify correct exception was raised
                assert str(exc_info.value) == ERROR_NODE_WALLET_NOT_INITIALIZED


@patch('src.utils.decorators.unlock_required.get_value')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status')
@patch('src.utils.decorators.unlock_required.get_bitcoin_config')
@patch.object(Request, 'post')
def test_unlock_node_connection_error(
    mock_get, mock_get_config, mock_get_keyring_status, mock_get_value,
):
    """Test unlock node with a connection error."""
    # Setup mocks
    mock_get_keyring_status.return_value = False
    mock_get_value.return_value = 'test_password'
    mock_get_config.return_value = UnlockRequestModel(
        password='test_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='pass',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    )

    mock_get.side_effect = RequestsConnectionError()

    with patch('src.utils.decorators.unlock_required.logger.error') as mock_logger:
        with pytest.raises(CommonException) as exc_info:
            unlock_node()

        # Verify error was logged
        mock_logger.assert_called_once_with(
            'Exception occurred at Decorator(%s): %s, Message: %s',
            'unlock_required',
            'ConnectionError',
            '',
        )
        assert str(exc_info.value) == 'Unable to connect to node'


@patch('src.utils.decorators.unlock_required.check_node', return_value=True)
@patch('src.utils.decorators.unlock_required.unlock_node')
def test_unlock_required_decorator(mock_unlock_node, mock_check_node):
    """Test unlock_required decorator."""
    @unlock_required
    def mock_method():
        return 'success'

    result = mock_method()

    assert result == 'success'
    mock_check_node.assert_called_once()
    mock_unlock_node.assert_called_once()


@patch.object(Request, 'get')
def test_is_node_locked_not_locked(mock_get, test_response):
    """Test the node is not locked."""
    test_response.status_code = 200
    mock_get.return_value = test_response

    result = check_node('unlock_required')

    assert result is False
    mock_get.assert_called_once_with(NODE_INFO_ENDPOINT)


@patch.object(Request, 'get')
def test_is_node_locked_locked(mock_get, test_response):
    """Test the node is locked."""
    test_response.status_code = 403
    test_response.json.return_value = {
        'error': ERROR_NODE_IS_LOCKED_CALL_UNLOCK, 'code': 403,
    }
    mock_get.side_effect = HTTPError(response=test_response)

    result = check_node('unlock_required')

    assert result is True
    mock_get.assert_called_once_with(NODE_INFO_ENDPOINT)


@patch.object(Request, 'get')
@patch('src.utils.logging.logger')
def test_is_node_locked_http_error(mock_logger, mock_get, test_response):
    """Test is_node_locked with an HTTP error."""
    test_response.status_code = 500
    test_response.json.return_value = {'error': 'Unhandled error'}
    mock_get.side_effect = HTTPError(response=test_response)

    with pytest.raises(CommonException) as exc_val:
        check_node('unlock_required')

    assert str(exc_val.value) == 'Unhandled error'


@patch.object(Request, 'get')
def test_is_node_locked_value_error(mock_get):
    """Test is_node_locked handling of ValueError during JSON parsing."""
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.side_effect = ValueError('Invalid JSON')
    mock_get.side_effect = HTTPError(response=mock_response)

    result = check_node('unlock_required')

    assert result is False


@patch.object(Request, 'post')
def test_unlock_node_general_exception(mock_post):
    """Test unlock_node to ensure the general Exception block is hit."""
    mock_post.side_effect = Exception('General exception')

    with patch.object(PageNavigationEventManager.get_instance(), 'term_and_condition_page_signal'):
        with pytest.raises(CommonException) as exc_info:
            unlock_node()

        # Expect the generic helper message
        assert str(
            exc_info.value,
        ) == 'Decorator(unlock_required): Error while checking if node is locked'
        # Do not require any navigation in generic exception path


@patch.object(Request, 'get')
def test_is_node_locked_general_exception(mock_get):
    """Test is_node_locked to ensure the general Exception block is hit."""
    mock_get.side_effect = Exception('General exception')

    with pytest.raises(CommonException) as exc_info:
        check_node('unlock_required')

    assert str(
        exc_info.value,
    ) == 'Decorator(unlock_required): Error while checking if node is locked'


@patch.object(Request, 'get')
def test_is_node_locked_node_connection_error(mock_get):
    """Test unlock node with a connection error."""
    mock_get.side_effect = RequestsConnectionError()

    with pytest.raises(CommonException) as exc_info:
        check_node('unlock_required')

    assert str(exc_info.value) == 'Unable to connect to node'


@patch('src.utils.decorators.unlock_required.get_value')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status')
@patch('src.utils.decorators.unlock_required.get_bitcoin_config')
@patch.object(Request, 'post')
def test_unlock_node_password_incorrect(
    mock_post, mock_get_config, mock_get_keyring_status, mock_get_value, test_response,
):
    """Test unlock node with incorrect password error."""
    # Setup mocks
    mock_get_keyring_status.return_value = False
    mock_get_value.return_value = 'test_password'
    mock_get_config.return_value = UnlockRequestModel(
        password='test_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='pass',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    )

    # Setup mock response for incorrect password
    test_response.status_code = 401
    test_response.json.return_value = {
        'error': ERROR_PASSWORD_INCORRECT,
        'code': 401,
    }
    mock_post.side_effect = HTTPError(response=test_response)

    # Mock the navigation event manager
    with patch.object(PageNavigationEventManager.get_instance(), 'enter_wallet_password_page_signal') as mock_signal:
        with patch('src.utils.decorators.unlock_required.logger.error') as mock_logger:
            with pytest.raises(CommonException) as exc_info:
                unlock_node()

            # Verify error was logged
            mock_logger.assert_called_once_with(ERROR_PASSWORD_INCORRECT)
            # Verify navigation signal was emitted
            mock_signal.emit.assert_called_once()
            # Verify correct exception was raised
            assert str(exc_info.value) == ERROR_PASSWORD_INCORRECT


@patch('src.utils.decorators.unlock_required.get_value')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status')
@patch('src.utils.decorators.unlock_required.get_bitcoin_config')
@patch.object(Request, 'post')
def test_unlock_node_wallet_not_initialized_detailed(
    mock_post, mock_get_config, mock_get_keyring_status, mock_get_value, test_response,
):
    """Test unlock node with wallet not initialized error - detailed test."""
    # Setup mocks
    mock_get_keyring_status.return_value = False
    mock_get_value.return_value = 'test_password'
    mock_get_config.return_value = UnlockRequestModel(
        password='test_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='pass',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    )

    # Setup mock response for wallet not initialized
    test_response.status_code = 403
    test_response.json.return_value = {
        'error': ERROR_NODE_WALLET_NOT_INITIALIZED,
        'code': 403,
    }
    mock_post.side_effect = HTTPError(response=test_response)

    # Test with all dependencies mocked
    with patch.object(PageNavigationEventManager.get_instance(), 'term_and_condition_page_signal') as mock_signal:
        with patch.object(SettingRepository, 'unset_wallet_initialized') as mock_unset:
            with patch('src.utils.decorators.unlock_required.logger.error') as mock_logger:
                with pytest.raises(CommonException) as exc_info:
                    unlock_node()

                # Verify error was logged
                mock_logger.assert_called_once_with(
                    ERROR_NODE_WALLET_NOT_INITIALIZED,
                )
                # Verify wallet was uninitialized
                mock_unset.assert_called_once()
                # Verify navigation signal was emitted
                mock_signal.emit.assert_called_once()
                # Verify correct exception was raised
                assert str(exc_info.value) == ERROR_NODE_WALLET_NOT_INITIALIZED


@patch('src.utils.decorators.unlock_required.get_value')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status')
@patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network')
@patch('src.utils.decorators.unlock_required.get_bitcoin_config')
@patch.object(Request, 'post')
def test_unlock_node_connection_error_detailed(
    mock_post, mock_get_config, mock_get_network, mock_get_keyring_status, mock_get_value,
):
    """Test unlock node with connection error - detailed test."""
    # Setup mocks
    mock_get_keyring_status.return_value = False
    mock_get_value.return_value = 'test_password'
    mock_get_network.return_value = NetworkEnumModel.REGTEST
    mock_get_config.return_value = UnlockRequestModel(
        password='test_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='pass',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    )

    # Create a specific connection error
    connection_error = RequestsConnectionError('Failed to connect')
    mock_post.side_effect = connection_error

    with patch('src.utils.decorators.unlock_required.logger.error') as mock_logger:
        with pytest.raises(CommonException) as exc_info:
            unlock_node()

        # Verify error was logged with correct format
        mock_logger.assert_called_once_with(
            'Exception occurred at Decorator(%s): %s, Message: %s',
            'unlock_required',
            'ConnectionError',
            'Failed to connect',
        )
        # Verify correct exception was raised
        assert str(exc_info.value) == 'Unable to connect to node'


@patch('src.utils.decorators.unlock_required.get_value')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status')
@patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network')
@patch('src.utils.decorators.unlock_required.get_bitcoin_config')
@patch.object(Request, 'post')
def test_unlock_node_http_error_without_json(
    mock_post, mock_get_config, mock_get_network, mock_get_keyring_status, mock_get_value,
):
    """Test unlock node with HTTP error that doesn't have JSON response."""
    # Setup mocks
    mock_get_keyring_status.return_value = False
    mock_get_value.return_value = 'test_password'
    mock_get_network.return_value = NetworkEnumModel.REGTEST
    mock_get_config.return_value = UnlockRequestModel(
        password='test_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='pass',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    )

    # Create a mock response that will fail JSON parsing
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = 'Invalid JSON data'
    mock_response.json.return_value = {'error': 'Unhandled error'}

    # Create HTTPError with the mock response
    http_error = HTTPError()
    http_error.response = mock_response
    mock_post.side_effect = http_error

    with patch('src.utils.decorators.unlock_required.logger.error') as mock_logger:
        with pytest.raises(CommonException) as exc_info:
            unlock_node()

        # Verify error was logged
        mock_logger.assert_called_once_with('Unhandled error')
        assert str(exc_info.value) == 'Unhandled error'


@patch('src.utils.decorators.unlock_required.get_value')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status')
@patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network')
@patch('src.utils.decorators.unlock_required.get_bitcoin_config')
@patch.object(Request, 'post')
def test_unlock_node_http_error_without_response_text(
    mock_post, mock_get_config, mock_get_network, mock_get_keyring_status, mock_get_value,
):
    """Test unlock node with HTTP error that has no response text."""
    # Setup mocks
    mock_get_keyring_status.return_value = False
    mock_get_value.return_value = 'test_password'
    mock_get_network.return_value = NetworkEnumModel.REGTEST
    mock_get_config.return_value = UnlockRequestModel(
        password='test_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='pass',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    )

    # Create a mock response without text
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = None
    mock_response.json.return_value = {'error': 'Unhandled error'}

    # Create HTTPError with the mock response
    http_error = HTTPError()
    http_error.response = mock_response
    mock_post.side_effect = http_error

    with patch('src.utils.decorators.unlock_required.logger.error') as mock_logger:
        with pytest.raises(CommonException) as exc_info:
            unlock_node()

        # Verify error was logged
        mock_logger.assert_called_once_with('Unhandled error')
        assert str(exc_info.value) == 'Unhandled error'


@patch('src.utils.decorators.unlock_required.get_value')
@patch('src.data.repository.setting_repository.SettingRepository.get_keyring_status')
@patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network')
@patch('src.utils.decorators.unlock_required.get_bitcoin_config')
@patch.object(Request, 'post')
def test_unlock_node_http_error_with_json_error(
    mock_post, mock_get_config, mock_get_network, mock_get_keyring_status, mock_get_value,
):
    """Test unlock node with HTTP error that has JSON error response."""
    # Setup mocks
    mock_get_keyring_status.return_value = False
    mock_get_value.return_value = 'test_password'
    mock_get_network.return_value = NetworkEnumModel.REGTEST
    mock_get_config.return_value = UnlockRequestModel(
        password='test_password',
        bitcoind_rpc_username='user',
        bitcoind_rpc_password='pass',
        bitcoind_rpc_host='localhost',
        bitcoind_rpc_port=18443,
        indexer_url='127.0.0.1:50001',
        proxy_endpoint='rpc://127.0.0.1:3000/json-rpc',
        announce_addresses=['pub.addr.example.com:9735'],
        announce_alias='nodeAlias',
    )

    # Create a mock response with JSON error
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.json.return_value = {'error': 'Custom error message'}

    # Create HTTPError with the mock response
    http_error = HTTPError()
    http_error.response = mock_response
    mock_post.side_effect = http_error

    with patch('src.utils.decorators.unlock_required.logger.error') as mock_logger:
        with pytest.raises(CommonException) as exc_info:
            unlock_node()

        # Verify error was logged
        mock_logger.assert_called_once_with('Custom error message')
        assert str(exc_info.value) == 'Custom error message'
