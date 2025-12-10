# pylint: disable=redefined-outer-name,unused-argument,too-many-arguments
"""unit tests for helper.py"""
from __future__ import annotations

import json
import os
import tempfile
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from src.model.enums.enums_model import NetworkEnumModel
from src.utils.helpers import check_google_auth_token_available
from src.utils.helpers import create_circular_pixmap
from src.utils.helpers import get_available_port
from src.utils.helpers import get_build_info
from src.utils.helpers import get_node_arg_config
from src.utils.helpers import handle_asset_address
from src.utils.helpers import hash_mnemonic
from src.utils.helpers import is_port_available
from src.utils.helpers import load_stylesheet
from src.utils.helpers import read_ln_node_commit_id_file
from src.utils.helpers import validate_mnemonic
from src.utils.helpers import write_ln_node_commit_id_file


@pytest.fixture
def mock_token_file():
    """Fixture to create a temporary file to simulate a token file."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b'token data')
        temp_file.flush()
        yield temp_file.name
        os.remove(temp_file.name)


@pytest.fixture
def mock_local_store():
    """Fixture to mock the local_store used in utility functions."""
    with patch('src.utils.helpers.local_store') as mock:
        yield mock


def test_handle_asset_address():
    """Test the `handle_asset_address` function to ensure it correctly shortens the address."""
    address = '1234567890abcdef'
    short_len = 4
    expected = '1234...cdef'
    assert handle_asset_address(address, short_len) == expected


def test_check_google_auth_token_available(mock_token_file):
    """Test the `check_google_auth_token_available` function to ensure it returns True when the token file is available."""
    with patch('src.utils.helpers.TOKEN_PICKLE_PATH', mock_token_file):
        assert check_google_auth_token_available() is True


def test_hash_mnemonic():
    """Test the `hash_mnemonic` function to ensure it returns a hashed mnemonic of the expected length."""
    mnemonic_phrase = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about'
    hashed = hash_mnemonic(mnemonic_phrase)
    assert len(hashed) == 10


def test_validate_mnemonic_valid():
    """Test the `validate_mnemonic` function to ensure it does not raise an error for a valid mnemonic phrase."""
    mnemonic_phrase = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about'
    try:
        validate_mnemonic(mnemonic_phrase)
    except ValueError:
        pytest.fail('validate_mnemonic raised ValueError unexpectedly!')


def test_validate_mnemonic_invalid():
    """Test the `validate_mnemonic` function to ensure it raises a ValueError for an invalid mnemonic phrase."""
    mnemonic_phrase = 'invalid mnemonic phrase'
    with pytest.raises(ValueError):
        validate_mnemonic(mnemonic_phrase)


def test_is_port_available(mocker):
    """Test the `is_port_available` function to ensure it correctly identifies an available port."""
    mocker.patch('socket.socket')
    socket_instance = mocker.MagicMock()
    socket_instance.connect_ex.return_value = 1
    mocker.patch('socket.socket', return_value=socket_instance)
    assert is_port_available(1234) is True


def test_get_available_port(mocker):
    """Test the `get_available_port` function to ensure it returns the next available port."""
    mocker.patch(
        'src.utils.helpers.is_port_available',
        side_effect=lambda port: port != 1234,
    )
    assert get_available_port(1234) == 1235


def test_get_build_info(mocker):
    """Test the `get_build_info` function to ensure it correctly parses and returns the build information."""
    build_info = {
        'build_flavour': 'release',
        'machine_arch': 'x86_64',
        'os_type': 'Linux',
        'arch_type': 'x86_64',
        'app-version': '1.0.0',
    }

    mocker.patch('builtins.open', mock_open(read_data=json.dumps(build_info)))

    with patch('src.utils.helpers.sys') as mock_sys:
        mock_sys.frozen = True

        with patch('src.utils.helpers.logger') as mock_logger:
            result = get_build_info()
            assert result == build_info
            mock_logger.error.assert_not_called()


def test_get_build_info_when_none_return(mocker):
    """Test the `get_build_info` function to ensure it returns None when the build info file is not found."""
    mocker.patch('builtins.open', side_effect=FileNotFoundError)
    with mocker.patch('src.utils.helpers.logger'):
        result = get_build_info()
        assert result is None


def test_get_node_arg_config(mocker):
    """Test the `get_node_arg_config` function to ensure it returns the correct configuration for the given network."""
    mock_local_store = mocker.patch('src.utils.helpers.local_store')
    mock_local_store.set_value = MagicMock()
    network = NetworkEnumModel.MAINNET

    with patch('src.utils.helpers.logger') as mock_logger:
        result = get_node_arg_config(network)
        assert isinstance(result, list)
        mock_logger.error.assert_not_called()


def test_get_node_arg_config_on_error(mocker):
    """Test the `get_node_arg_config` function to ensure it raises a ValueError when an error occurs."""
    mock_local_store = mocker.patch('src.utils.helpers.local_store')
    mock_local_store.set_value = MagicMock()
    mock_get_available_port = mocker.patch(
        'src.utils.helpers.get_available_port',
    )
    mock_get_available_port.side_effect = ValueError('Testing purpose')
    network = NetworkEnumModel.MAINNET
    with pytest.raises(ValueError) as exc_info:
        get_node_arg_config(network)
    assert str(exc_info.value) == 'Testing purpose'


def test_load_stylesheet_success(mocker):
    """Test load_stylesheet_success helper."""
    qss_content = 'QWidget { background-color: #000; }'
    mocker.patch('builtins.open', mock_open(read_data=qss_content))
    mocker.patch('os.path.isabs', return_value=False)
    mocker.patch('os.path.abspath', return_value='/mock/path/helpers.py')
    mocker.patch('os.path.dirname', return_value='/mock/path')
    mocker.patch('os.path.join', return_value='/mock/path/views/qss/style.qss')
    result = load_stylesheet()
    assert result == qss_content


def test_load_stylesheet_file_not_found(mocker):
    """Test when file not found."""
    mocker.patch('builtins.open', side_effect=FileNotFoundError)
    mocker.patch('os.path.isabs', return_value=False)
    mocker.patch('os.path.abspath', return_value='/mock/path/helpers.py')
    mocker.patch('os.path.dirname', return_value='/mock/path')
    mocker.patch('os.path.join', return_value='/mock/path/views/qss/style.qss')
    with pytest.raises(FileNotFoundError):
        load_stylesheet()


def test_load_stylesheet_frozen(mocker):
    """Test the `load_stylesheet` function to ensure it correctly loads and returns a stylesheet."""
    with patch('src.utils.helpers.sys') as mock_sys:
        mock_sys.frozen = True
        qss_content = 'QWidget { background-color: #000; }'
        mocker.patch('builtins.open', mock_open(read_data=qss_content))
        mocker.patch(
            'os.path.join',
            return_value='/frozen/path/views/qss/style.qss',
        )
        result = load_stylesheet()
        assert result == qss_content


def test_load_stylesheet_non_absolute_path(mocker):
    """Load stylesheet when non absolute path."""
    qss_content = 'QWidget { background-color: #000; }'
    mocker.patch('builtins.open', mock_open(read_data=qss_content))
    mocker.patch('os.path.isabs', return_value=False)
    mocker.patch('os.path.abspath', return_value='/mock/path/helpers.py')
    mocker.patch('os.path.dirname', return_value='/mock/path')
    mocker.patch('os.path.join', return_value='/mock/path/views/qss/style.qss')
    result = load_stylesheet(file='views/qss/style.qss')
    assert result == qss_content


@patch('src.utils.helpers.Qt')
@patch('src.utils.helpers.QPixmap')
@patch('src.utils.helpers.QPainter')
@patch('src.utils.helpers.QColor')
def test_create_circular_pixmap(mock_qcolor, mock_qpainter, mock_qpixmap, mock_qt):
    """Test the `create_circular_pixmap` function to ensure it returns a circular QPixmap."""
    mock_qt.NoPen = 'NoPenValue'
    mock_qt.transparent = 'TransparentValue'
    mock_qpainter.Antialiasing = 'AntialiasingValue'

    diameter = 100
    color = mock_qcolor
    mock_pixmap_instance = MagicMock()
    mock_qpixmap.return_value = mock_pixmap_instance
    mock_painter_instance = MagicMock()
    mock_qpainter.return_value = mock_painter_instance

    result = create_circular_pixmap(diameter, color)
    mock_qpixmap.assert_called_once_with(diameter, diameter)
    mock_pixmap_instance.fill.assert_called_once_with('TransparentValue')
    mock_qpainter.assert_called_once_with(mock_pixmap_instance)
    mock_painter_instance.setRenderHint.assert_called_once_with(
        'AntialiasingValue',
    )
    mock_painter_instance.setBrush.assert_called_once_with(color)
    mock_painter_instance.setPen.assert_called_once_with('NoPenValue')
    mock_painter_instance.drawEllipse.assert_called_once_with(
        0, 0, diameter, diameter,
    )
    mock_painter_instance.end.assert_called_once()
    assert result == mock_pixmap_instance


@patch('src.utils.helpers.SettingRepository.get_rln_node_commit_id')
@patch('src.utils.helpers.app_paths')
def test_write_ln_node_commit_id_file_writes_and_returns_path_and_name(
    mock_app_paths, mock_get_commit_id,
):
    """Test the `write_ln_node_commit_id_file` function to ensure it writes the commit ID to a file and returns the path and name."""
    mock_app_paths.backup_folder_path = '/fake/backup'
    mock_get_commit_id.return_value = 'commit123'
    m = mock_open()
    with patch('builtins.open', m):
        path, name = write_ln_node_commit_id_file('wallet')

    expected_name = 'wallet.commit'
    expected_path = os.path.join('/fake/backup', expected_name)

    assert name == expected_name
    assert path == expected_path
    m.assert_called_once_with(expected_path, 'w', encoding='utf-8')
    handle = m()
    handle.write.assert_called_once_with('commit123')


@patch('src.utils.helpers.app_paths')
def test_read_ln_node_commit_id_file_returns_content(
    mock_app_paths,
):
    """Test the `read_ln_node_commit_id_file` function to ensure it returns the content of the commit ID file."""
    mock_app_paths.restore_folder_path = '/fake/restore'

    file_name = 'wallet.commit'
    full_path = os.path.join('/fake/restore', file_name)
    m = mock_open(read_data='commitXYZ')
    with patch('builtins.open', m):
        result = read_ln_node_commit_id_file(file_name)
    m.assert_called_once_with(full_path, encoding='utf-8')
    assert result == 'commitXYZ'


@patch('src.utils.helpers.app_paths')
def test_read_ln_node_commit_id_file_returns_unknown_when_missing(
    mock_app_paths,
):
    """Test the `read_ln_node_commit_id_file` function to ensure it returns 'unknown' when the commit ID file is missing."""
    mock_app_paths.restore_folder_path = '/fake/restore'
    m = mock_open()
    m.side_effect = FileNotFoundError
    with patch('builtins.open', m):
        result = read_ln_node_commit_id_file('missing.commit')
    assert result == 'unknown'
