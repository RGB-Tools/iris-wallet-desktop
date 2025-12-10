"""Unit tests for RGB asset helper functions."""
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

from PySide6.QtWidgets import QLabel

from src.utils.rgb_asset_helpers import handle_img_path
from src.utils.rgb_asset_helpers import is_hex_string
from src.utils.rgb_asset_helpers import is_path
from src.utils.rgb_asset_helpers import set_asset_image


def test_valid_hex_string():
    """Test with valid hex strings."""
    valid_hex_strings = [
        '00',  # simple hex
        '0a1b2c3d4e5f',  # longer valid hex
        'AABBCCDDEE',  # uppercase hex
        '1234567890abcdef',  # mixed lower and uppercase
    ]
    for hex_string in valid_hex_strings:
        assert is_hex_string(hex_string) is True


def test_invalid_hex_string():
    """Test with invalid hex strings."""
    invalid_hex_strings = [
        '00G1',  # contains non-hex character 'G'
        '123z',  # contains non-hex character 'z'
        '12345',  # odd length
        '0x1234',  # prefixed with '0x'
        ' ',  # empty or space character
    ]
    for hex_string in invalid_hex_strings:
        assert is_hex_string(hex_string) is False


def test_empty_string():
    """Test with an empty string."""
    assert is_hex_string('') is False


def test_odd_length_string():
    """Test with a string of odd length."""
    odd_length_hex_strings = [
        '1',  # single character
        '123',  # three characters
        '12345',  # five characters
    ]
    for hex_string in odd_length_hex_strings:
        assert is_hex_string(hex_string) is False


def test_is_path_valid():
    """Test the is_path function with valid Unix-like paths."""
    # Test valid Unix-like paths
    assert is_path('/path/to/file') is True
    assert is_path('/usr/local/bin/') is True
    assert is_path('/home/user/doc-1.txt') is True


def test_is_path_invalid():
    """Test the is_path function with invalid paths."""
    # Test invalid paths
    assert is_path('invalid/path') is False  # No leading slash
    assert is_path(123) is False  # Non-string input
    assert is_path('') is False  # Empty string
    assert is_path('C:\\Windows\\Path') is False  # Windows path format


@patch('src.utils.rgb_asset_helpers.convert_hex_to_image')
@patch('src.utils.rgb_asset_helpers.resize_image')
def test_set_asset_image_with_hex(mock_resize_image, mock_convert_hex_to_image):
    """Test setting asset image from hex string."""
    # Setup
    mock_label = MagicMock(spec=QLabel)
    mock_pixmap = MagicMock()
    mock_resized = MagicMock()
    mock_convert_hex_to_image.return_value = mock_pixmap
    mock_resize_image.return_value = mock_resized

    # Call with hex string
    set_asset_image(mock_label, '1234567890abcdef')

    # Verify
    mock_convert_hex_to_image.assert_called_once_with('1234567890abcdef')
    mock_resize_image.assert_called_once_with(mock_pixmap, 335, 335)
    mock_label.setPixmap.assert_called_once_with(mock_resized)


@patch('src.utils.rgb_asset_helpers.resize_image')
def test_set_asset_image_with_path(mock_resize_image):
    """Test setting asset image from file path."""
    # Setup
    mock_label = MagicMock(spec=QLabel)
    mock_resized = MagicMock()
    mock_resize_image.return_value = mock_resized

    # Call with file path (not hex string)
    set_asset_image(mock_label, '/path/to/image.png')

    # Verify
    mock_resize_image.assert_called_once_with('/path/to/image.png', 335, 335)


@patch('src.utils.rgb_asset_helpers.set_asset_image')
@patch('src.utils.rgb_asset_helpers.QLabel')
def test_handle_img_path_with_path(mock_qlabel_class, mock_set_asset_image):
    """Test handle_img_path with a valid image path."""
    # Setup mocks
    mock_widget = MagicMock()
    mock_layout = MagicMock()
    mock_frame = MagicMock()
    mock_label = MagicMock(spec=QLabel)
    mock_qlabel_class.return_value = mock_label
    image_path = '/path/to/image.png'

    # Call
    result = handle_img_path(
        mock_widget,
        image_path,
        mock_layout,
        mock_frame,
    )

    # Verify widget configuration
    mock_widget.setMinimumSize.assert_called_once()
    mock_widget.setFixedWidth.assert_called_once_with(499)

    # Verify label was created
    mock_qlabel_class.assert_called_once_with(mock_widget)
    assert result == mock_label

    # Verify set_asset_image was called
    mock_set_asset_image.assert_called_once_with(
        mock_label, image_hex=image_path,
    )
    # Setup
    mock_widget = MagicMock()
    mock_layout = MagicMock()
    mock_frame = MagicMock()
    existing_label = MagicMock(spec=QLabel)

    # Call with no path
    result = handle_img_path(
        mock_widget,
        '',
        mock_layout,
        mock_frame,
        existing_label,
    )

    # Verify nothing was configured and existing label was returned
    assert result == existing_label
    mock_widget.setMinimumSize.assert_not_called()
    mock_layout.addWidget.assert_not_called()


@patch('src.utils.rgb_asset_helpers.set_asset_image')
def test_handle_img_path_with_existing_label(mock_set_asset_image):
    """Test handle_img_path with an existing label."""
    # Setup
    mock_widget = MagicMock()
    mock_layout = MagicMock()
    mock_frame = MagicMock()
    existing_label = MagicMock(spec=QLabel)
    image_path = '/path/to/image.png'

    # Call with existing label
    result = handle_img_path(
        mock_widget,
        image_path,
        mock_layout,
        mock_frame,
        existing_label,
    )

    # Verify existing label was used and configured
    assert result == existing_label
    existing_label.setMaximumSize.assert_called_once()
    existing_label.setStyleSheet.assert_called_once()

    # Verify set_asset_image was called with existing label
    mock_set_asset_image.assert_called_once_with(
        existing_label, image_hex=image_path,
    )
