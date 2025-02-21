# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument, too-many-lines, no-value-for-parameter, use-implicit-booleaness-not-comparison
"""unit tests for common utils"""
from __future__ import annotations

import base64
import binascii
import os
import time
import zipfile
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QSize
from PySide6.QtGui import QImage
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPlainTextEdit

from src.flavour import __network__
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import TokenSymbol
from src.model.selection_page_model import SelectionPageModel
from src.utils.common_utils import close_button_navigation
from src.utils.common_utils import convert_hex_to_image
from src.utils.common_utils import convert_timestamp
from src.utils.common_utils import copy_text
from src.utils.common_utils import download_file
from src.utils.common_utils import find_files_with_name
from src.utils.common_utils import generate_identicon
from src.utils.common_utils import get_bitcoin_info_by_network
from src.utils.common_utils import load_translator
from src.utils.common_utils import network_info
from src.utils.common_utils import resize_image
from src.utils.common_utils import set_qr_code
from src.utils.common_utils import sigterm_handler
from src.utils.common_utils import translate_value
from src.utils.common_utils import zip_logger_folder
from src.utils.constant import APP_NAME
from src.utils.constant import DEFAULT_LOCALE
from src.utils.constant import LOG_FOLDER_NAME
from src.utils.custom_exception import CommonException
from src.version import __version__
from src.views.components.toast import ToastManager


@pytest.fixture
def app():
    """Set up a QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def mock_clipboard():
    """Mock the clipboard functionality."""
    clipboard = MagicMock()
    with patch.object(QApplication, 'clipboard', return_value=clipboard):
        yield clipboard


@pytest.fixture
def mock_toast():
    """Mock the ToastManager."""
    with patch.object(ToastManager, 'success') as mock_toast:
        yield mock_toast


def test_copy_text_from_label(app, mock_clipboard, mock_toast):
    """Test copying text from a QLabel."""
    label = QLabel('Test QLabel text')
    copy_text(label)

    mock_clipboard.setText.assert_called_once_with('Test QLabel text')
    mock_toast.assert_called_once_with(description='Text copied to clipboard')


def test_copy_text_from_plain_text_edit(app, mock_clipboard, mock_toast):
    """Test copying text from a QPlainTextEdit."""
    plain_text_edit = QPlainTextEdit()
    plain_text_edit.setPlainText('Test QPlainTextEdit text')
    copy_text(plain_text_edit)

    mock_clipboard.setText.assert_called_once_with('Test QPlainTextEdit text')
    mock_toast.assert_called_once_with(description='Text copied to clipboard')


def test_copy_text_from_string(app, mock_clipboard, mock_toast):
    """Test copying text from a string."""
    text = 'Test string text'
    copy_text(text)

    mock_clipboard.setText.assert_called_once_with('Test string text')
    mock_toast.assert_called_once_with(description='Text copied to clipboard')


def test_copy_text_unsupported_widget(app):
    """Test copying text from an unsupported widget type."""
    unsupported_widget = 12345

    with patch('src.utils.logging.logger.error') as mock_logger:
        copy_text(unsupported_widget)

        # Verify the logger was called once
        assert mock_logger.call_count == 1

        # Get the actual call
        call_args = mock_logger.call_args_list[0]

        # Verify the format string and error message
        assert call_args[0][0] == 'Error: Unable to copy text - %s'
        assert str(call_args[0][1]) == 'Unsupported widget type'


def test_load_translator_successful_load_system_locale():
    """Test successful loading of translator for system locale."""
    # Create a mock locale for English US
    mock_locale = MagicMock()
    mock_locale.name.return_value = 'en_US'

    # Mock QLocale.system() and QTranslator.load() methods
    with patch('PySide6.QtCore.QLocale.system', return_value=mock_locale):
        with patch('PySide6.QtCore.QTranslator.load', return_value=True) as mock_load:
            translator = load_translator()
            assert translator is not None
            mock_load.assert_called_once_with('en_US', ':/translations')


def test_load_translator_fallback_to_default_locale():
    """Test fallback to default locale if system locale translation is unavailable."""
    mock_locale = MagicMock()
    mock_locale.name.return_value = 'en_US'

    with patch('PySide6.QtCore.QLocale.system', return_value=mock_locale):
        with patch('PySide6.QtCore.QTranslator.load') as mock_load:
            mock_load.side_effect = [False, True]
            translator = load_translator()
            assert translator is not None
            mock_load.assert_any_call('en_US', ':/translations')
            mock_load.assert_any_call(DEFAULT_LOCALE, ':/translations')


def test_load_translator_failed_to_load_default_locale():
    """Test that None is returned if both system and default locale translations fail."""
    mock_locale = MagicMock()
    mock_locale.name.return_value = 'en_US'

    with patch('PySide6.QtCore.QLocale.system', return_value=mock_locale):
        with patch('PySide6.QtCore.QTranslator.load') as mock_load:
            mock_load.side_effect = [False, False]
            translator = load_translator()
            assert translator is None
            mock_load.assert_any_call('en_US', ':/translations')
            mock_load.assert_any_call(DEFAULT_LOCALE, ':/translations')


def test_load_translator_file_not_found_error():
    """Test file not found error during translator loading."""
    mock_locale = MagicMock()
    mock_locale.name.return_value = 'en_US'

    error = FileNotFoundError('Translation file not found')
    with patch('PySide6.QtCore.QLocale.system', return_value=mock_locale):
        with patch('PySide6.QtCore.QTranslator.load', side_effect=error):
            with patch('src.utils.logging.logger.error') as mock_logger:
                translator = load_translator()
                assert translator is None
                mock_logger.assert_called_once()
                assert mock_logger.call_args[0][0] == 'Error: Unable to load translator - %s'
                assert str(
                    mock_logger.call_args[0][1],
                ) == 'Translation file not found'


def test_load_translator_os_error():
    """Test OSError during translator loading."""
    mock_locale = MagicMock()
    mock_locale.name.return_value = 'en_US'

    error = OSError('OS error occurred')
    with patch('PySide6.QtCore.QLocale.system', return_value=mock_locale):
        with patch('PySide6.QtCore.QTranslator.load', side_effect=error):
            with patch('src.utils.logging.logger.error') as mock_logger:
                translator = load_translator()
                assert translator is None
                mock_logger.assert_called_once()
                assert mock_logger.call_args[0][0] == 'Error: Unable to load translator - %s'
                assert str(mock_logger.call_args[0][1]) == 'OS error occurred'


def test_set_qr_code_with_attribute_error():
    """Test QR code generation that raises an AttributeError."""
    data = 'https://example.com'

    with patch('qrcode.QRCode') as mock_qr:
        mock_qr_instance = MagicMock()
        mock_qr.return_value = mock_qr_instance
        error = AttributeError('Attribute Error')
        mock_qr_instance.make_image.side_effect = error

        # Ensure that the exception is handled correctly
        with patch('src.utils.logging.logger.error') as mock_logger:
            qt_image = set_qr_code(data)
            assert qt_image is None
            mock_logger.assert_called_once_with(
                'Error: Unable to create QR image - %s',
                error,  # Convert error to string to match actual behavior
            )


def test_set_qr_code_with_value_error():
    """Test QR code generation that raises a ValueError."""
    data = 'https://example.com'

    with patch('qrcode.QRCode') as mock_qr:
        mock_qr_instance = MagicMock()
        mock_qr.return_value = mock_qr_instance
        error = ValueError('Value Error')
        mock_qr_instance.make_image.side_effect = error

        # Ensure that the exception is handled correctly
        with patch('src.utils.logging.logger.error') as mock_logger:
            qt_image = set_qr_code(data)
            assert qt_image is None
            mock_logger.assert_called_once_with(
                'Error: Unable to create QR image - %s',
                error,  # Pass the error object directly
            )


def test_convert_hex_to_image_valid_data():
    """Test convert_hex_to_image with valid hex data."""
    # This is a minimal valid PNG file in hex
    valid_hex = (
        '89504e470d0a1a0a'  # PNG signature
        '0000000d49484452'  # IHDR chunk header
        '00000001'          # Width: 1
        '00000001'          # Height: 1
        '08'                # Bit depth
        '02'                # Color type
        '00000000'          # Other IHDR fields
        '3128932e'          # IHDR CRC
        '0000000c4944415478'  # IDAT chunk
        '9c63641800000000ffff'  # IDAT data
        '0000ffff'          # IDAT CRC
        '0000000049454e44ae426082'  # IEND chunk
    )

    with patch('PySide6.QtGui.QImage.fromData', return_value=QImage()), \
            patch('PySide6.QtGui.QPixmap.fromImage', return_value=QPixmap()):
        pixmap = convert_hex_to_image(valid_hex)
        assert isinstance(pixmap, QPixmap)


def test_zip_logger_folder():
    """
    Tests the zip_logger_folder function.

    This function uses the `unittest.mock` library to patch several functions used by the
    `zip_logger_folder` function. This allows us to control the behavior of these functions
    and test the logic of the function itself.

    The test first sets up the mocks to simulate the existence of certain files and
    directories. Then, it calls the `zip_logger_folder` function and asserts the expected
    behavior. The assertions check the returned zip filename, output directory, and the
    calls made to the mocked functions.

    This is a basic unit test that covers the main functionality of the
    `zip_logger_folder` function. You can further expand this test to cover edge cases
    and other scenarios.
    """

    @patch('os.path.exists')
    @patch('shutil.make_archive')
    @patch('os.makedirs')
    @patch('shutil.copy')
    @patch('os.path.join')
    def _test_zip_logger_folder(
        mock_join,
        mock_copy,
        mock_makedirs,
        mock_make_archive,
        mock_exists,
    ):
        # Set up mocks
        mock_exists.side_effect = [True, True, True, False]
        base_path = '/tmp'
        epoch_time = str(int(time.time()))
        # network = 'regtest'

        # Call the function
        zip_filename, output_dir = zip_logger_folder(base_path)

        # Expected behavior
        expected_zip_filename = f'{
            APP_NAME
        }-logs-{epoch_time}-{__version__}-{__network__}.zip'
        expected_output_dir = os.path.join(
            base_path, f'embedded-{APP_NAME}-logs{epoch_time}-{__network__}',
        )
        expected_wallet_logs_path = os.path.join(base_path, LOG_FOLDER_NAME)
        expected_ln_node_logs_path = os.path.join(
            base_path, f"dataldk{__network__}", '.ldk', 'logs', 'logs.txt',
        )
        _expected_calls = [
            (
                expected_wallet_logs_path, os.path.join(
                    expected_output_dir, APP_NAME,
                ),
            ),
            (
                expected_ln_node_logs_path, os.path.join(
                    expected_output_dir, 'ln-node',
                ),
            ),
        ]

        # Assert
        assert zip_filename == expected_zip_filename
        assert output_dir == expected_output_dir
        mock_makedirs.assert_called_with(expected_output_dir, exist_ok=True)

    _test_zip_logger_folder()


def test_convert_hex_to_image_invalid_data():
    """Test convert_hex_to_image with invalid hex data."""
    invalid_hex = 'invalid hex data'
    result = convert_hex_to_image(invalid_hex)
    assert isinstance(result, binascii.Error)


def test_convert_hex_to_image_odd_length():
    """Test convert_hex_to_image with odd-length hex string."""
    odd_hex = '123'  # Odd length hex string
    result = convert_hex_to_image(odd_hex)
    assert isinstance(result, binascii.Error)


def test_convert_hex_to_image_empty_hex():
    """Test convert_hex_to_image with empty hex data."""
    empty_hex = ''
    result = convert_hex_to_image(empty_hex)
    assert isinstance(result, QPixmap)
    assert result.isNull()


def test_convert_hex_to_image_invalid_value():
    """Test convert_hex_to_image with hex data that leads to invalid value."""
    invalid_value_hex = 'FFFFFFFFFFFFFFFFFFFFFFFF'
    result = convert_hex_to_image(invalid_value_hex)
    assert isinstance(result, QPixmap)
    assert result.isNull()


def test_convert_hex_to_image_none_data():
    """Test convert_hex_to_image with None data."""
    none_data = None
    with pytest.raises(AttributeError) as exc_info:
        convert_hex_to_image(none_data)
    assert str(exc_info.value) == "'NoneType' object has no attribute 'strip'"


@patch('src.utils.common_utils.SettingRepository.get_wallet_network')
@patch('src.utils.common_utils.get_offline_asset_ticker')
def test_get_bitcoin_info_by_network(mock_get_offline_asset_ticker, mock_get_wallet_network):
    """Test bitcoin info for mainnet."""
    # Setup mock values
    mock_get_wallet_network.return_value = NetworkEnumModel.MAINNET
    mock_get_offline_asset_ticker.return_value = TokenSymbol.BITCOIN.value

    # Call the function
    result = get_bitcoin_info_by_network()

    # Assert the correct output
    assert result == (
        TokenSymbol.BITCOIN.value,
        'bitcoin', ':/assets/bitcoin.png',
    )


@patch('src.utils.common_utils.SettingRepository.get_wallet_network')
@patch('src.utils.common_utils.get_offline_asset_ticker')
def test_get_bitcoin_info_by_network_testnet(mock_get_offline_asset_ticker, mock_get_wallet_network):
    """Test bitcoin info for testnet."""
    # Setup mock values
    mock_get_wallet_network.return_value = NetworkEnumModel.TESTNET
    mock_get_offline_asset_ticker.return_value = TokenSymbol.TESTNET_BITCOIN.value

    # Call the function
    result = get_bitcoin_info_by_network()

    # Assert the correct output
    assert result == (
        TokenSymbol.TESTNET_BITCOIN.value,
        'testnet bitcoin', ':/assets/testnet_bitcoin.png',
    )


@patch('src.utils.common_utils.SettingRepository.get_wallet_network')
@patch('src.utils.common_utils.get_offline_asset_ticker')
def test_get_bitcoin_info_by_network_regtest(mock_get_offline_asset_ticker, mock_get_wallet_network):
    """Test bitcoin info for regtest."""
    # Setup mock values
    mock_get_wallet_network.return_value = NetworkEnumModel.REGTEST
    mock_get_offline_asset_ticker.return_value = TokenSymbol.REGTEST_BITCOIN.value

    # Call the function
    result = get_bitcoin_info_by_network()

    # Assert the correct output
    assert result == (
        TokenSymbol.REGTEST_BITCOIN.value,
        'regtest bitcoin', ':/assets/regtest_bitcoin.png',
    )


@patch('src.utils.common_utils.SettingRepository.get_wallet_network')
@patch('src.utils.common_utils.get_offline_asset_ticker')
def test_get_bitcoin_info_by_network_invalid_ticker(mock_get_offline_asset_ticker, mock_get_wallet_network):
    """Test bitcoin info with invalid ticker."""
    # Setup mock values for invalid ticker
    mock_get_wallet_network.return_value = NetworkEnumModel.MAINNET
    mock_get_offline_asset_ticker.return_value = 'invalid_ticker'

    # Call the function
    result = get_bitcoin_info_by_network()

    # Assert the result is None since the ticker is invalid
    assert result is None


@patch('src.utils.common_utils.SettingRepository.get_wallet_network')
@patch('src.utils.common_utils.get_offline_asset_ticker')
def test_get_bitcoin_info_by_network_none_network(mock_get_offline_asset_ticker, mock_get_wallet_network):
    """Test bitcoin info with None network."""
    # Setup mock for None network
    mock_get_wallet_network.return_value = None
    mock_get_offline_asset_ticker.return_value = TokenSymbol.BITCOIN.value

    # Call the function and verify it raises AttributeError
    with pytest.raises(AttributeError) as exc_info:
        get_bitcoin_info_by_network()

    # Verify the specific error message
    assert str(exc_info.value) == "'NoneType' object has no attribute 'value'"


# Mock the os.walk method
@patch('os.walk')
def test_find_files_with_name_file_match(mock_os_walk):
    """test find files with name file match"""
    # Setup mock for os.walk, simulating directory structure
    mock_os_walk.return_value = [
        ('/path/to/dir', ['subdir'], ['file1.txt', 'file2.txt']),
        ('/path/to/dir/subdir', [], ['file3.txt', 'file4.txt']),
    ]

    # Call the function with a matching file name
    result = find_files_with_name('/path/to/dir', 'file3.txt')

    # Assert the correct result (should find file3.txt in subdir)
    assert result == ['/path/to/dir/subdir/file3.txt']


@patch('os.walk')
def test_find_files_with_name_exact_match(mock_os_walk):
    """Test find_files_with_name with an exact match."""
    # Setup mock for os.walk, simulating directory structure
    mock_os_walk.return_value = [
        ('/path/to/dir', ['subdir'], ['file1.txt', 'file2.txt']),
        ('/path/to/dir/subdir', [], ['file3.txt', 'file4.txt']),
    ]

    # Call the function with an exact matching file name
    result = find_files_with_name('/path/to/dir', 'file1.txt')

    # Assert the correct result (should find only the exact match)
    assert result == ['/path/to/dir/file1.txt']


@patch('os.walk')
def test_find_files_with_name_no_match(mock_os_walk):
    """Test find_files_with_name with no match."""
    # Setup mock for os.walk, simulating directory structure
    mock_os_walk.return_value = [
        ('/path/to/dir', ['subdir'], ['file1.txt', 'file2.txt']),
        ('/path/to/dir/subdir', [], ['file3.txt', 'file4.txt']),
    ]

    # Call the function with a non-matching keyword
    result = find_files_with_name('/path/to/dir', 'nonexistent.txt')

    # Assert the result is an empty list since no files match
    assert result == []


@patch('os.walk')
def test_find_files_with_name_empty_directory(mock_os_walk):
    """Test find_files_with_name with an empty directory."""
    # Setup mock for os.walk with an empty directory
    mock_os_walk.return_value = [
        ('/path/to/dir', [], []),
    ]

    # Call the function with a directory having no files or subdirectories
    result = find_files_with_name('/path/to/dir', 'file.txt')

    # Assert the result is an empty list since no files exist
    assert result == []


@patch('src.utils.page_navigation.PageNavigation')
def test_close_button_navigation_wallet_selection_page(mock_page_navigation):
    """Test close button navigation from wallet selection page."""
    # Setup mocks
    parent = MagicMock()
    parent.originating_page = 'wallet_selection_page'

    # Create mock page navigation instance
    mock_navigation = MagicMock()
    mock_page_navigation.return_value = mock_navigation

    # Setup page navigation methods
    parent.view_model.page_navigation = mock_navigation

    # Call the method
    close_button_navigation(parent)

    # Assert that wallet_method_page was called
    mock_navigation.wallet_method_page.assert_called_once()

    # Create expected SelectionPageModel
    expected_model = SelectionPageModel(
        title='connection_type',
        logo_1_path=':/assets/embedded.png',
        logo_1_title='embedded',
        logo_2_path=':/assets/remote.png',
        logo_2_title='remote',
        asset_id='none',
        asset_name=None,
        callback='none',
        back_page_navigation=None,
        rgb_asset_page_load_model=None,
    )

    # Call wallet_connection_page with model
    mock_navigation.wallet_connection_page(expected_model)

    # Verify wallet_connection_page was called with expected model
    mock_navigation.wallet_connection_page.assert_called_once_with(
        expected_model,
    )


@patch('src.utils.page_navigation.PageNavigation')
def test_close_button_navigation_settings_page(mock_page_navigation):
    """Test close button navigation from settings page."""
    # Setup mocks
    parent = MagicMock()
    parent.originating_page = 'settings_page'

    # Create mock page navigation instance
    mock_navigation = MagicMock()
    mock_page_navigation.return_value = mock_navigation

    # Setup page navigation methods
    parent.view_model.page_navigation = mock_navigation

    # Call the method
    close_button_navigation(parent)

    # Assert that settings_page was called
    mock_navigation.settings_page.assert_called_once()

 # Replace `your_module` with the actual module name


# Mock SettingRepository
@patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network')
@patch('src.views.components.toast.ToastManager.error')  # Mock ToastManager
@patch('src.utils.logging.logger.error')   # Mock logger
def test_network_info_success(mock_logger_error, mock_toast_error, mock_get_wallet_network):
    """Test network info success."""
    # Mock successful network retrieval
    mock_network = MagicMock()
    mock_network.value = 'test_network'
    mock_get_wallet_network.return_value = mock_network

    # Create a mock parent
    parent = MagicMock()

    # Call the function
    network_info(parent)

    # Assert that the network was set correctly
    assert parent.network == 'test_network'

    # Ensure no error or toast was triggered
    mock_logger_error.assert_not_called()
    mock_toast_error.assert_not_called()


# Mock SettingRepository
@patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network')
@patch('src.views.components.toast.ToastManager.error')  # Mock ToastManager
@patch('src.utils.logging.logger.error')
def test_network_info_common_exception(mock_logger_error, mock_toast_error, mock_get_wallet_network):
    """Test network info common exception."""
    # Mock CommonException being raised
    mock_exc = CommonException('Test exception message')
    mock_get_wallet_network.side_effect = mock_exc

    # Create a mock parent without spec to avoid attribute creation
    parent = MagicMock()
    delattr(parent, 'network')  # Explicitly remove network attribute

    # Call the function
    network_info(parent)

    # Assert that network was not set
    assert not hasattr(parent, 'network')

    # Ensure logger error and toast were triggered with the correct values
    mock_logger_error.assert_called_once_with(
        'Exception occurred: %s, Message: %s',
        'CommonException',
        'Test exception message',
    )
    mock_toast_error.assert_called_once_with(
        parent=None, title=None, description=mock_exc.message,
    )


# Mock SettingRepository
@patch('src.data.repository.setting_repository.SettingRepository.get_wallet_network')
@patch('src.views.components.toast.ToastManager.error')  # Mock ToastManager
@patch('src.utils.logging.logger.error')  # Mock logger
def test_network_info_generic_exception(mock_logger_error, mock_toast_error, mock_get_wallet_network):
    """Test network info generic exception."""
    # Mock a generic exception being raised
    mock_exc = Exception('Test generic exception message')
    mock_get_wallet_network.side_effect = mock_exc

    # Create a mock parent without spec to avoid attribute creation
    parent = MagicMock(spec=[])

    # Call the function
    network_info(parent)

    # Assert that network was not set
    assert not hasattr(parent, 'network')

    # Ensure logger error and toast were triggered with the correct values
    mock_logger_error.assert_called_once_with(
        'Exception occurred: %s, Message: %s',
        'Exception',
        'Test generic exception message',
    )
    mock_toast_error.assert_called_once_with(
        # Replace with the value of `ERROR_SOMETHING_WENT_WRONG`
        parent=None, title=None, description='Something went wrong',
    )


@patch('pydenticon.Generator.generate')  # Mock the pydenticon generator
@patch('PIL.Image.open')  # Mock PIL.Image.open
@patch('PIL.ImageDraw.Draw')  # Mock ImageDraw.Draw
@patch('PIL.ImageOps.fit')  # Mock ImageOps.fit
def test_generate_identicon(mock_image_ops_fit, mock_image_draw, mock_image_open, mock_generator_generate):
    """Test generate_identicon function"""
    # Mock pydenticon generator output
    # Return bytes instead of MagicMock
    mock_generator_generate.return_value = b'mock_identicon_bytes'

    # Mock PIL Image.open
    mock_image = MagicMock()
    mock_image.size = (40, 40)
    mock_image.convert.return_value = mock_image
    mock_image.transpose.return_value = mock_image
    mock_image_open.return_value = mock_image

    # Mock ImageDraw
    mock_draw = MagicMock()
    mock_image_draw.return_value = mock_draw

    # Mock ImageOps.fit
    mock_circular_image = MagicMock()
    mock_image_ops_fit.return_value = mock_circular_image

    # Mock the save method to write mock data
    mock_circular_image.save = MagicMock(
        side_effect=lambda buf, format: buf.write(b'mock_image_data'),
    )

    # Call the function
    result = generate_identicon('test_data', size=40)

    # Assert that the generator was called with correct parameters
    mock_generator_generate.assert_called_once_with(
        'test_data', 40, 40, output_format='png',
    )

    # Assert that PIL.Image.open was called
    mock_image_open.assert_called_once()

    # Assert that the image was properly transposed
    mock_image.transpose.assert_called_once()

    # Assert that the mask was drawn
    mock_image_draw.assert_called_once()

    # Assert that ImageOps.fit was called to resize and fit the circular image
    mock_image_ops_fit.assert_called_once_with(
        mock_image, (40, 40), centering=(0.5, 0.5),
    )

    # Assert that the circular image was saved
    assert mock_circular_image.save.call_count == 1

    # Verify the final output is base64 encoded
    expected_base64 = base64.b64encode(b'mock_image_data').decode('utf-8')
    assert result == expected_base64


@patch('zipfile.ZipFile')  # Mock zipfile.ZipFile
@patch('os.walk')  # Mock os.walk
# Mock ToastManager.success
@patch('src.views.components.toast.ToastManager.success')
# Mock ToastManager.error
@patch('src.views.components.toast.ToastManager.error')
@patch('shutil.rmtree')  # Mock shutil.rmtree
def test_download_file_success(mock_rmtree, mock_error, mock_success, mock_os_walk, mock_zipfile):
    """Test download file success."""
    # Mock input values
    save_path = '/mock/save_path'
    output_dir = '/mock/output_dir'

    # Mock os.walk to simulate files in the directory
    mock_os_walk.return_value = [
        ('/mock/output_dir', ['subdir'], ['file1.txt', 'file2.txt']),
        ('/mock/output_dir/subdir', [], ['file3.txt']),
    ]

    # Mock the ZipFile object
    mock_zipf = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zipf

    # Call the function
    download_file(save_path, output_dir)

    # Assert save_path is adjusted to include .zip extension
    expected_save_path = save_path + '.zip'

    # Assert that zipfile.ZipFile was called with correct parameters
    mock_zipfile.assert_called_once_with(
        expected_save_path, 'w', zipfile.ZIP_DEFLATED,
    )

    # Assert that files were written to the zip archive
    expected_calls = [
        (os.path.join('/mock/output_dir', 'file1.txt'), 'file1.txt'),
        (os.path.join('/mock/output_dir', 'file2.txt'), 'file2.txt'),
        (
            os.path.join('/mock/output_dir/subdir', 'file3.txt'),
            os.path.join('subdir', 'file3.txt'),
        ),
    ]
    for call in expected_calls:
        mock_zipf.write.assert_any_call(*call)

    # Assert success message was displayed with the actual message used in the code
    mock_success.assert_called_once_with(
        description=f"Logs have been saved to {expected_save_path}",
    )

    # Assert cleanup of the output directory
    mock_rmtree.assert_called_once_with(output_dir)

    # Assert no error message was displayed
    mock_error.assert_not_called()


@patch('zipfile.ZipFile')  # Mock zipfile.ZipFile
@patch('shutil.rmtree')  # Mock shutil.rmtree
# Mock ToastManager.error
@patch('src.views.components.toast.ToastManager.error')
def test_download_file_exception(mock_error, mock_rmtree, mock_zipfile):
    """Test download file exception."""
    # Mock input values
    save_path = '/mock/save_path'
    output_dir = '/mock/output_dir'

    # Force an exception during zip file creation
    mock_zipfile.side_effect = Exception('Mock exception')

    # Call the function
    download_file(save_path, output_dir)

    # Assert error message was displayed
    mock_error.assert_called_once_with(
        description='Failed to save logs: Mock exception',
    )

    # Assert cleanup of the output directory still occurs
    mock_rmtree.assert_called_once_with(output_dir)


@patch('src.utils.common_utils.QImage')  # Mock QImage where it's used
@patch('src.utils.common_utils.QPixmap')  # Mock QPixmap where it's used
@patch('os.path.exists')  # Mock os.path.exists
def test_resize_image_file_path(mock_exists, mock_qpixmap, mock_qimage):
    """Test resizing an image from a file path"""
    # Mock file path existence
    mock_exists.return_value = True

    # Mock QImage instance
    mock_qimage_instance = MagicMock()
    mock_qimage.return_value = mock_qimage_instance

    # Mock image scaling
    mock_scaled_image = MagicMock()
    mock_qimage_instance.scaled.return_value = mock_scaled_image

    # Mock QPixmap.fromImage
    mock_pixmap = MagicMock()
    mock_qpixmap.fromImage.return_value = mock_pixmap

    # Call the function
    file_path = '/mock/path/image.png'
    result = resize_image(file_path, 100, 200)

    # Assert file existence was checked
    mock_exists.assert_called_once_with(file_path)

    # Assert QImage was created with file path
    mock_qimage.assert_called_once_with(file_path)

    # Assert scaling was called with correct dimensions
    mock_qimage_instance.scaled.assert_called_once_with(100, 200)

    # Assert QPixmap.fromImage was called
    mock_qpixmap.fromImage.assert_called_once_with(mock_scaled_image)

    # Assert the correct result was returned
    assert result == mock_pixmap


def test_resize_image_qimage():
    """Test resizing a QImage object"""
    # Mock a QImage object
    mock_image = MagicMock(spec=QImage)
    mock_scaled_image = MagicMock(spec=QImage)
    mock_image.scaled.return_value = mock_scaled_image

    # Mock QPixmap.fromImage
    with patch('PySide6.QtGui.QPixmap.fromImage') as mock_from_image:
        mock_pixmap = MagicMock()
        mock_from_image.return_value = mock_pixmap

        # Call the function
        result = resize_image(mock_image, 150, 300)

        # Assert scaling was called with correct dimensions
        mock_image.scaled.assert_called_once_with(150, 300)

        # Assert QPixmap.fromImage was called
        mock_from_image.assert_called_once_with(mock_scaled_image)

        # Assert the correct result was returned
        assert result == mock_pixmap


def test_resize_image_qpixmap():
    """Test resizing a QPixmap object"""
    # Create a mock QPixmap that passes isinstance check
    mock_pixmap = MagicMock(spec=QPixmap)
    mock_image = MagicMock(spec=QImage)
    mock_scaled_image = MagicMock(spec=QImage)

    # Set up the mock chain
    mock_pixmap.toImage.return_value = mock_image
    mock_image.scaled.return_value = mock_scaled_image

    # Mock QPixmap.fromImage
    with patch('PySide6.QtGui.QPixmap.fromImage') as mock_from_image:
        mock_resized_pixmap = MagicMock(spec=QPixmap)
        mock_from_image.return_value = mock_resized_pixmap

        # Call the function
        result = resize_image(mock_pixmap, 50, 50)

        # Assert toImage was called
        mock_pixmap.toImage.assert_called_once()

        # Assert scaling was called with correct dimensions
        mock_image.scaled.assert_called_once_with(50, 50)

        # Assert QPixmap.fromImage was called
        mock_from_image.assert_called_once_with(mock_scaled_image)

        # Assert the correct result was returned
        assert result == mock_resized_pixmap


def test_resize_image_invalid_type():
    """Test resizing an image with an invalid type"""
    # Call the function with an invalid type
    with pytest.raises(TypeError) as exc_info:
        resize_image(123, 100, 100)

    # Assert the exception message
    assert str(exc_info.value) == (
        'image_input must be a file path (str), QImage, or QPixmap object.'
    )


@patch('os.path.exists')  # Mock os.path.exists
def test_resize_image_file_not_found(mock_exists):
    """Test resizing an image with a file not found"""
    # Mock file path existence
    mock_exists.return_value = False

    # Call the function and expect a FileNotFoundError
    with pytest.raises(FileNotFoundError) as exc_info:
        resize_image('/mock/path/nonexistent.png', 100, 100)

    # Assert the exception message
    assert str(
        exc_info.value,
    ) == 'The file /mock/path/nonexistent.png does not exist.'


@patch('PySide6.QtWidgets.QMessageBox.warning')
@patch('src.utils.ln_node_manage.LnNodeServerManager.get_instance')
@patch('PySide6.QtWidgets.QApplication.instance')
def test_sigterm_handler(mock_qapp_instance, mock_ln_node_manager_get_instance, mock_qmessagebox_warning):
    """
    Unit test for sigterm_handler to ensure all branches are covered without displaying the GUI.
    """
    # Mock the QApplication instance
    mock_qapp = MagicMock()
    mock_qapp_instance.return_value = mock_qapp

    # Mock the LnNodeServerManager instance
    mock_ln_node_manager = MagicMock()
    mock_ln_node_manager_get_instance.return_value = mock_ln_node_manager

    # Case 1: User clicks "OK"
    mock_qmessagebox_warning.return_value = QMessageBox.Ok
    sigterm_handler(None, None)

    # Assertions for the "OK" case
    mock_qmessagebox_warning.assert_called_once_with(
        None,
        'Are you sure you want to exit?',
        QApplication.translate(
            'iris_wallet_desktop',
            'sigterm_warning_message', None,
        ),
        QMessageBox.Ok | QMessageBox.Cancel,
    )
    mock_ln_node_manager.stop_server_from_close_button.assert_called_once()
    mock_qapp.exit.assert_called_once()

    # Reset mocks for next case
    mock_qmessagebox_warning.reset_mock()
    mock_ln_node_manager.stop_server_from_close_button.reset_mock()
    mock_qapp.quit.reset_mock()

    # Case 2: User clicks "Cancel"
    mock_qmessagebox_warning.return_value = QMessageBox.Cancel
    sigterm_handler(None, None)

    # Assertions for the "Cancel" case
    mock_qmessagebox_warning.assert_called_once_with(
        None,
        'Are you sure you want to exit?',
        QApplication.translate(
            'iris_wallet_desktop',
            'sigterm_warning_message', None,
        ),
        QMessageBox.Ok | QMessageBox.Cancel,
    )
    mock_ln_node_manager.stop_server_from_close_button.assert_not_called()
    mock_qapp.quit.assert_not_called()


@patch('src.utils.common_utils.QPixmap')
@patch('src.utils.common_utils.QImage')
def test_set_qr_code_success(mock_qimage, mock_qpixmap):
    """Test for set_qr_code method success case."""
    data = 'https://example.com'
    mock_qimage_instance = MagicMock(spec=QImage)
    mock_qimage.return_value = mock_qimage_instance
    mock_qpixmap_instance = MagicMock(spec=QPixmap)
    mock_qpixmap.fromImage.return_value = mock_qpixmap_instance

    qr_image = set_qr_code(data)

    assert qr_image is not None
    assert isinstance(qr_image, QImage), 'QR code image should be a QImage'
    qr_image = QPixmap.fromImage(qr_image)
    assert isinstance(qr_image, QPixmap), 'QR code image should be a QPixmap'
    assert qr_image.size() == QSize(335, 335)


@patch('src.utils.common_utils.convert_timestamp')
def test_convert_timestamp(mock_convert_timestamp):
    """Test for convert_timestamp method."""
    timestamp = 1633072800
    mock_convert_timestamp.return_value = ('2021-10-01', '12:50:00')

    date_str, time_str = convert_timestamp(timestamp)

    assert date_str == '2021-10-01'
    assert time_str == '12:50:00'

# Test for failure in QR code generation (invalid data)


@patch('src.utils.common_utils.qrcode.QRCode')
@patch('src.utils.common_utils.ImageQt')
def test_set_qr_code_failure(mock_imageqt, mock_qrcode):
    """Test for set_qr_code method failure case."""
    data = 'https://example.com'
    mock_qrcode.side_effect = ValueError('Invalid QR code data')

    qr_image = set_qr_code(data)

    assert qr_image is None
    mock_imageqt.assert_not_called()


@pytest.fixture
def mock_logger():
    """Fixture to mock the logger."""
    with patch('src.utils.logging.logger') as mock_logger:
        yield mock_logger


@pytest.fixture
def mock_translate():
    """Fixture to mock QCoreApplication.translate."""
    with patch('PySide6.QtCore.QCoreApplication.translate', return_value='Translated Text') as mock_translate:
        yield mock_translate


def test_translate_value_valid_element(mock_translate):
    """Test with a valid element that supports setText."""
    element = Mock(spec=QLabel)
    key = 'test_key'

    translate_value(element, key)

    element.setText.assert_called_once_with('Translated Text')
    mock_translate.assert_called_once_with('iris_wallet_desktop', key, None)


def test_translate_value_invalid_element_type():
    """Test with an element that does not support setText."""
    element = Mock()
    delattr(element, 'setText')  # Remove setText to trigger TypeError
    key = 'test_key'

    with pytest.raises(TypeError) as excinfo:
        translate_value(element, key)

    assert f"The element of type {
        type(
            element
        ).__name__
    } does not support the setText method." in str(excinfo.value)


def test_translate_value_unexpected_exception(mock_logger):
    """Test when an unexpected exception occurs during translation."""
    element = Mock(spec=QLabel)
    key = 'test_key'

    with patch('PySide6.QtCore.QCoreApplication.translate', side_effect=Exception('Unexpected Error')):
        with pytest.raises(Exception) as excinfo:
            translate_value(element, key)

    assert 'Unexpected Error' in str(excinfo.value)
    mock_logger.error.assert_not_called()
