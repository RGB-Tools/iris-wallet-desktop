"""Unit test for local store"""
# pylint: disable=redefined-outer-name,unused-argument,too-many-arguments
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.utils.constant import APP_NAME
from src.utils.constant import ORGANIZATION_DOMAIN
from src.utils.constant import ORGANIZATION_NAME
from src.utils.local_store import LocalStore


@pytest.fixture
def mock_qsettings():
    """Fixture to mock QSettings."""
    with patch('PySide6.QtCore.QSettings', autospec=True) as mock_qsettings:
        yield mock_qsettings


@pytest.fixture
def mock_qdir():
    """Fixture to mock QDir."""
    with patch('PySide6.QtCore.QDir', autospec=True) as mock_qdir:
        mock_qdir.return_value.filePath.return_value = '/mock/path'
        mock_qdir.return_value.mkpath = MagicMock()
        yield mock_qdir


@pytest.fixture
def local_store(mock_qsettings, mock_qdir):
    """Fixture to initialize LocalStore."""
    # Mock the writableLocation return value
    with patch('PySide6.QtCore.QStandardPaths.writableLocation', return_value='/mock/path'):
        return LocalStore(APP_NAME, ORGANIZATION_NAME, ORGANIZATION_DOMAIN)


def test_set_value(local_store):
    """Test that set_value sets the value in settings."""
    local_store.settings.setValue = MagicMock()
    local_store.set_value('test_key', 'test_value')
    local_store.settings.setValue.assert_called_once_with(
        'test_key', 'test_value',
    )


def test_get_value(local_store):
    """Test that get_value retrieves the value from settings."""
    local_store.settings.value = MagicMock(return_value='test_value')
    result = local_store.get_value('test_key')
    assert result == 'test_value'
    local_store.settings.value.assert_called_once_with('test_key')


def test_get_value_with_type_conversion(local_store):
    """Test that get_value converts the value to the specified type."""
    local_store.settings.value = MagicMock(return_value='123')
    result = local_store.get_value('test_key', int)
    assert result == 123


def test_get_value_conversion_failure(local_store):
    """Test that get_value returns None if type conversion fails."""
    local_store.settings.value = MagicMock(return_value='not_an_int')
    result = local_store.get_value('test_key', int)
    assert result is None


def test_remove_key(local_store):
    """Test that remove_key removes the key from settings."""
    local_store.settings.remove = MagicMock()
    local_store.remove_key('test_key')
    local_store.settings.remove.assert_called_once_with('test_key')


def test_clear_settings(local_store):
    """Test that clear_settings clears all settings."""
    local_store.settings.clear = MagicMock()
    local_store.clear_settings()
    local_store.settings.clear.assert_called_once()


def test_all_keys(local_store):
    """Test that all_keys returns all keys."""
    local_store.settings.allKeys = MagicMock(return_value=['key1', 'key2'])
    result = local_store.all_keys()
    assert result == ['key1', 'key2']
    local_store.settings.allKeys.assert_called_once()


def test_get_path(local_store):
    """Test that get_path returns the base path."""
    result = local_store.get_path()
    assert result == '/mock/path'


def test_create_folder(local_store, mock_qdir):
    """Test that create_folder creates a folder and returns its path."""
    mock_qdir().mkpath = MagicMock()
    result = local_store.create_folder('test_folder')
    assert result == '/mock/path/test_folder'
