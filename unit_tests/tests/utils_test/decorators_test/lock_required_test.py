"""Unit test for lock required decorator"""
# pylint: disable=redefined-outer-name,unused-argument,too-many-arguments,redefined-argument-from-local
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError

from src.utils.custom_exception import CommonException
from src.utils.decorators.lock_required import call_lock
from src.utils.decorators.lock_required import lock_required
from src.utils.endpoints import LOCK_ENDPOINT
from src.utils.endpoints import NODE_INFO_ENDPOINT
from src.utils.error_message import ERROR_NODE_IS_LOCKED_CALL_UNLOCK
from src.utils.helpers import check_node
from src.utils.request import Request

# Test is_node_locked function


@patch.object(Request, 'get')
@patch('src.utils.logging.logger')
def test_is_node_locked_not_locked(mock_logger, mock_get):
    """Test the node is not locked."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = check_node('lock_required')

    assert result is False

    mock_get.assert_called_once_with(NODE_INFO_ENDPOINT)


@patch.object(Request, 'get')
@patch('src.utils.logging.logger')
def test_is_node_locked_locked(mock_logger, mock_get):
    """Test the node is locked."""
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.return_value = {
        'error': ERROR_NODE_IS_LOCKED_CALL_UNLOCK, 'code': 403,
    }
    mock_get.side_effect = HTTPError(response=mock_response)

    expected_result = check_node('lock_required')

    assert expected_result is True
    mock_get.assert_called_once_with(NODE_INFO_ENDPOINT)


@patch.object(Request, 'get')
@patch('src.utils.logging.logger')
def test_is_node_locked_http_error(mock_logger, mock_get):
    """Test is_node_locked with an HTTP error."""
    test_response = MagicMock()
    test_response.status_code = 500
    test_response.json.return_value = {'error': 'Unhandled error'}
    mock_get.side_effect = HTTPError(response=test_response)

    with pytest.raises(CommonException) as exc_info:
        check_node('lock_required')

    assert str(exc_info.value) == 'Unhandled error'


@patch.object(Request, 'get')
def test_is_node_locked_value_error(mock_get):
    """Test is_node_locked handling of ValueError during JSON parsing."""
    test_response = MagicMock()
    test_response.status_code = 403
    test_response.json.side_effect = ValueError('Invalid JSON')
    mock_get.side_effect = HTTPError(response=test_response)

    result = check_node('lock_required')

    assert result is False

# Test call_lock function


@patch.object(Request, 'post')
def test_call_lock_success(mock_post):
    """Test successful lock call."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    call_lock()

    mock_post.assert_called_once_with(LOCK_ENDPOINT)

# Test lock_required decorator


def mock_method():
    """Mocked value for decorated_method"""
    return 'success'


@patch.object(Request, 'post')
@patch('src.utils.decorators.lock_required.check_node', return_value=False)
def test_lock_required_decorator(mock_check_node, mock_post):
    """Test lock_required decorator."""
    @lock_required
    def decorated_method():
        return mock_method()

    with patch.object(Request, 'post') as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        result = decorated_method()

    assert result == 'success'
    mock_check_node.assert_called_once()
    mock_post.assert_called_once_with(LOCK_ENDPOINT)


@patch.object(Request, 'post')
@patch('src.utils.decorators.lock_required.check_node', return_value=True)
def test_lock_required_decorator_when_locked(mock_check_node, mock_post):
    """Test lock_required decorator when node is locked."""
    @lock_required
    def decorated_method():
        return 'should not be reached'

    with patch.object(Request, 'post') as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        result = decorated_method()

    assert result == 'should not be reached'
    mock_check_node.assert_called_once()


@patch.object(Request, 'get')
def test_is_node_locked_general_exception(mock_get):
    """Test is_node_locked to ensure the general Exception block is hit."""
    mock_get.side_effect = Exception('General exception')

    with pytest.raises(CommonException) as exc:
        check_node('lock_required')

    assert str(
        exc.value,
    ) == 'Decorator(lock_required): Error while checking if node is locked'


@patch.object(Request, 'post')
def test_is_node_locked_node_connection_error(mock_post):
    """Test unlock node with a connection error."""
    mock_post.side_effect = RequestsConnectionError()

    with pytest.raises(CommonException) as exc_info:
        check_node('lock_required')

    assert str(exc_info.value) == 'Unable to connect to node'


@patch.object(Request, 'post')
def test_call_lock_connection_error(mock_post):
    """Test unlock node with a connection error."""
    mock_post.side_effect = RequestsConnectionError()

    with pytest.raises(CommonException) as exc_info:
        call_lock()

    assert str(exc_info.value) == 'Unable to connect to node'

# Test call_lock function with a general Exception


@patch.object(Request, 'post')
@patch('src.utils.logging.logger')
def test_call_lock_general_exception(mock_logger, mock_post):
    """Test call_lock with a general exception."""
    # Simulate a general exception
    mock_post.side_effect = Exception('General error')

    with pytest.raises(CommonException) as exc_info:
        call_lock()

    assert str(
        exc_info.value,
    ) == 'Decorator(call_lock): Error while calling lock API'
    mock_post.assert_called_once_with(LOCK_ENDPOINT)
