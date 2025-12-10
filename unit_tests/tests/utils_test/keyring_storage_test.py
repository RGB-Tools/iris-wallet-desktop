"""Unit test for keyring """
# pylint: disable=redefined-outer-name,unused-argument,too-many-arguments
from __future__ import annotations

import keyring as kr
import pytest

from src.utils.constant import APP_NAME
from src.utils.keyring_storage import delete_value
from src.utils.keyring_storage import get_value
from src.utils.keyring_storage import set_value


@pytest.fixture
def mock_keyring(mocker):
    """Fixture to mock the keyring module."""
    mocker.patch('keyring.set_password')
    mocker.patch('keyring.get_password')
    mocker.patch('keyring.delete_password')
    mocker.patch('keyring.get_keyring', return_value='mock_backend')


def test_set_value_success(mock_keyring):
    """Test that set_value returns True when the value is successfully set."""
    kr.get_password.return_value = 'test_value'
    result = set_value('test_key', 'test_value', network='regtest')
    assert result is True
    kr.set_password.assert_called_once_with(
        APP_NAME, 'test_key_regtest', 'test_value',
    )


def test_set_value_failure(mock_keyring):
    """Test that set_value returns False when the value is not set correctly."""
    kr.get_password.return_value = None
    result = set_value('test_key', 'test_value', network='regtest')
    assert result is False
    kr.set_password.assert_called_once_with(
        APP_NAME, 'test_key_regtest', 'test_value',
    )


def test_set_value_exception(mock_keyring):
    """Test that set_value returns False when a KeyringError occurs."""
    kr.set_password.side_effect = kr.errors.KeyringError('Test Error')
    result = set_value('test_key', 'test_value', network='regtest')
    assert result is False
    kr.set_password.assert_called_once_with(
        APP_NAME, 'test_key_regtest', 'test_value',
    )


def test_set_value_generic_exception(mock_keyring):
    """Test that set_value returns False when a generic exception occurs."""
    kr.set_password.side_effect = Exception('Generic Error')
    result = set_value('test_key', 'test_value')
    assert result is False
    kr.set_password.assert_called_once_with(APP_NAME, 'test_key', 'test_value')


def test_get_value_success(mock_keyring):
    """Test that get_value returns the correct value."""
    kr.get_password.return_value = 'test_value'
    result = get_value('test_key', network='regtest')
    assert result == 'test_value'
    kr.get_password.assert_called_once_with(APP_NAME, 'test_key_regtest')


def test_get_value_exception(mock_keyring):
    """Test that get_value returns None when a KeyringError occurs."""
    kr.get_password.side_effect = kr.errors.KeyringError('Test Error')
    result = get_value('test_key', network='regtest')
    assert result is None
    kr.get_password.assert_called_once_with(APP_NAME, 'test_key_regtest')


def test_delete_value_success(mock_keyring):
    """Test that delete_value calls the delete_password method correctly."""
    delete_value('test_key', network='regtest')
    kr.delete_password.assert_called_once_with(APP_NAME, 'test_key_regtest')


def test_delete_value_exception(mock_keyring):
    """Test that delete_value handles a KeyringError correctly."""
    kr.delete_password.side_effect = kr.errors.KeyringError('Test Error')
    delete_value('test_key', network='regtest')
    kr.delete_password.assert_called_once_with(APP_NAME, 'test_key_regtest')
