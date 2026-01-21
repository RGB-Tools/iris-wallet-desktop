"""
This module contains the common utils methods, which represent
an operation manager for common operation functionalities.
"""
from __future__ import annotations

import base64
import binascii
import os
import shutil
import time
import zipfile
from datetime import datetime
from io import BytesIO

import pydenticon
import qrcode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from PIL.ImageQt import ImageQt
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QLocale
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QTranslator
from PySide6.QtGui import QImage
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtWidgets import QWidget

from src.data.repository.setting_repository import SettingRepository
from src.data.service.helpers.main_asset_page_helper import get_offline_asset_ticker
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import TokenSymbol
from src.model.enums.enums_model import WalletType
from src.model.selection_page_model import SelectionPageModel
from src.utils.build_app_path import app_paths
from src.utils.constant import APP_NAME
from src.utils.constant import BITCOIN_EXPLORER_URL
from src.utils.constant import DEFAULT_LOCALE
from src.utils.constant import FAST_TRANSACTION_FEE_BLOCKS
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import MEDIUM_TRANSACTION_FEE_BLOCKS
from src.utils.constant import SLOW_TRANSACTION_FEE_BLOCKS
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_SAVE_LOGS
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.info_message import INFO_COPY_MESSAGE
from src.utils.info_message import INFO_LOG_SAVE_DESCRIPTION
from src.utils.ln_node_manage import LnNodeServerManager
from src.utils.logging import logger
from src.version import __version__
from src.views.components.toast import ToastManager


def copy_text(widget) -> None:
    """This method copies the text from the QLabel or QPlainTextEdit to the clipboard."""
    try:
        # Determine the type of widget and get the text accordingly
        if isinstance(widget, QLabel):
            text = widget.text()
        elif isinstance(widget, QPlainTextEdit):
            text = widget.toPlainText()
        elif isinstance(widget, str):
            text = widget
        else:
            raise AttributeError('Unsupported widget type')

        # Get the clipboard and set the text
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        ToastManager.success(
            description=INFO_COPY_MESSAGE,
        )
    except AttributeError as error:
        logger.error('Error: Unable to copy text - %s', error)


def convert_timestamp(timestamp_value):
    """This method converts a timestamp to a formatted date and time string."""
    try:
        converted_time = datetime.fromtimestamp(timestamp_value)
        date_str = str(converted_time.strftime('%Y-%m-%d'))
        time_str = str(converted_time.strftime('%H:%M:%S'))
        return date_str, time_str
    except (ValueError, OSError) as error:
        logger.error('Error: Unable to convert timestamp - %s', error)
        return None, None


def load_translator():
    """Load translations for the application."""
    try:
        translator = QTranslator()
        system_locale = QLocale.system().name()

        if translator.load(system_locale, ':/translations'):
            return translator
        print(
            f'Translation for {
                system_locale
            } not available. Loading default translation.',
        )

        if translator.load(DEFAULT_LOCALE, ':/translations'):
            return translator

        print(
            f'Failed to load translation file for default locale {
                DEFAULT_LOCALE
            }',
        )
        return None

    except (FileNotFoundError, OSError) as error:
        logger.error('Error: Unable to load translator - %s', error)
        return None


def set_qr_code(data):
    """This method generates a QR code from the provided data."""
    try:
        # Create a QR code instance
        _qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        _qr.add_data(data)
        _qr.make()

        # Create an image from the QR Code instance
        img = _qr.make_image(
            fill='black', back_color='white',
        ).resize((335, 335))

        # Convert the PIL image to a QPixmap
        qt_image = ImageQt(img)

        return qt_image
    except (AttributeError, ValueError) as error:
        logger.error('Error: Unable to create QR image - %s', error)
        return None


def generate_identicon(data, size=40):
    """This method generates the identicon for nia asset"""
    generator = pydenticon.Generator(
        5, 5,
        foreground=[
            'rgb(45,79,255)', 'rgb(254,180,44)', 'rgb(226,121,234)',
            'rgb(30,179,253)', 'rgb(232,77,65)', 'rgb(49,203,115)', 'rgb(141,69,170)',
        ],
        background='rgb(224,224,224)',
    )
    identicon = generator.generate(data, size, size, output_format='png')

    # Convert identicon to a circular image
    buffered = BytesIO(identicon)
    image = Image.open(buffered).convert('RGBA')
    # Ensure proper orientation for PyQt
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    size = image.size
    # Create circular mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)

    # Draw a smooth ellipse using anti-aliasing
    draw.ellipse([(0, 0), (size[0] - 1, size[1] - 1)], fill=255)

    # Apply mask to create circular image
    circular_image = ImageOps.fit(image, size, centering=(0.5, 0.5))
    circular_image.putalpha(mask)

    # Save circular image to a buffer
    circular_buffer = BytesIO()
    circular_image.save(circular_buffer, format='PNG')

    # Encode circular image to base64
    img_str = base64.b64encode(circular_buffer.getvalue()).decode('utf-8')
    return img_str


def zip_logger_folder(base_path) -> tuple[str, str, str]:
    """
    Zips the logger folder along with an additional folder.

    Parameters:
    base_path (str): The base path where the logs folder is located.

    Returns:
    tuple: A tuple containing (zip_filename, output_dir, zip_file_path)
           - zip_filename: The name of the zip file
           - output_dir: The temporary directory where logs were collected
           - zip_file_path: The full path to the created zip file
    """
    # Generate the log folder name using the current epoch time value
    epoch_time = str(int(time.time()))
    network: NetworkEnumModel = SettingRepository.get_wallet_network()
    ln_node_logs_path = app_paths.node_logs_path
    wallet_logs_path = app_paths.app_logs_path
    ldk_logs_path = app_paths.ldk_logs_path
    zip_filename = f'{
        APP_NAME
    }-logs-{epoch_time}-{__version__}-{network.value}.zip'

    # Create a temporary directory to hold the combined logs
    output_dir = os.path.join(
        base_path, f'embedded-{APP_NAME}-logs{epoch_time}-{network.value}',
    )
    os.makedirs(output_dir, exist_ok=True)

    def copy_filtered(src, dst):
        """
        Copies files from src to dst, ignoring .ini files and files starting with 'data'.
        """
        for root, _, files in os.walk(src):
            for file in files:
                if file.endswith('.ini') or file.startswith('data'):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, src)
                dst_path = os.path.join(dst, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy(file_path, dst_path)

    # Copy the main logs folder to the temporary directory if it exists
    if os.path.exists(wallet_logs_path):
        copy_filtered(wallet_logs_path, os.path.join(output_dir, APP_NAME))

    # Copy the additional folder to the temporary directory if it exists
    if os.path.exists(ln_node_logs_path):
        copy_filtered(ln_node_logs_path, os.path.join(output_dir, 'ln-node'))

    # Include the dataldk logs file
    if os.path.exists(ldk_logs_path):
        ldk_output_dir = os.path.join(output_dir, 'ldk-logs')
        os.makedirs(ldk_output_dir, exist_ok=True)
        shutil.copy(ldk_logs_path, ldk_output_dir)

    # Find the 'log' file and add it to the temporary directory
    log_files = find_files_with_name(base_path, 'log')
    if log_files:
        log_output_dir = os.path.join(output_dir, 'rgb-lib-logs')
        os.makedirs(log_output_dir, exist_ok=True)
        for log_file in log_files:
            shutil.copy(log_file, log_output_dir)

    # Finally, zip the folder
    zip_file_path = os.path.join(base_path, zip_filename)
    shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', output_dir)
    return zip_filename, output_dir, zip_file_path


def convert_hex_to_image(bytes_hex):
    """This method returns pixmap from the bytes hex"""
    hex_data = bytes_hex.strip()
    try:
        byte_data = binascii.unhexlify(hex_data)
        qbyte_array = QByteArray(byte_data)
        image = QImage.fromData(qbyte_array)
        pixmap = QPixmap.fromImage(image)
        return pixmap
    except (binascii.Error, ValueError) as error:
        return error


def download_file(save_path, output_dir):
    """This method create a zip and save it to the directory"""
    try:
        # Ensure the save path has a .zip extension
        if not save_path.endswith('.zip'):
            save_path += '.zip'

        # Create the zip file directly at the chosen location
        with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)

        ToastManager.success(
            description=INFO_LOG_SAVE_DESCRIPTION.format(save_path),
        )
    except Exception as e:
        ToastManager.error(
            description=ERROR_SAVE_LOGS.format(e),
        )
    finally:
        # Clean up the output directory
        shutil.rmtree(output_dir)


def translate_value(element: QWidget, key: str):
    """
    Translates the given key and sets it as the text for the provided element.

    Args:
        element (QWidget): The UI element (e.g., button, label) whose text will be set.
        key (str): The key used to look up the translated text.

    Raises:
        Exception: If any other unexpected error occurs during translation.
    """
    try:
        if hasattr(element, 'setText'):
            element.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT,
                    key,
                    None,
                ),
            )
        else:
            raise TypeError(
                f'The element of type {
                    type(element).__name__
                } does not support the setText method.',
            )
    except CommonException as e:
        logger.error('An unexpected error occurred: %s', e)
        raise


def resize_image(image_input, width: int, height: int) -> QPixmap:
    """
    Resize the given image and return it as a QPixmap.

    Args:
        image_input (Union[str, QImage, QPixmap]): The image to be resized. Can be a file path, a QImage, or a QPixmap.
        width (int): The desired width.
        height (int): The desired height.

    Returns:
        QPixmap: The resized image as a QPixmap.
    """
    # Check if the input is a string (file path), QImage, or QPixmap
    if isinstance(image_input, str):
        # Load the image from the file path
        if not os.path.exists(image_input):
            raise FileNotFoundError(f'The file {image_input} does not exist.')
        image = QImage(image_input)
    elif isinstance(image_input, QImage):
        image = image_input
    elif isinstance(image_input, QPixmap):
        # Convert QPixmap to QImage
        image = image_input.toImage()
    else:
        raise TypeError(
            'image_input must be a file path (str), QImage, or QPixmap object.',
        )

    # Resize the image
    resized_image = image.scaled(width, height)

    # Convert QImage to QPixmap
    resized_pixmap = QPixmap.fromImage(resized_image)

    return resized_pixmap


def insert_zero_width_spaces(text, interval=8):
    """
    Inserts zero-width spaces into a given text at regular intervals.

    This method splits the input text into chunks of a specified length
    and inserts a zero-width space ('\u200B') between each chunk.
    The zero-width space is an invisible character that helps in wrapping
    long strings of text, such as URLs or transaction IDs, to improve
    readability in UI elements.

    Parameters:
    - text (str): The input string where zero-width spaces will be inserted.
    - interval (int): The number of characters between each zero-width space.
    Default is 8.

    Returns:
    - str: The modified string with zero-width spaces inserted.
    """
    return '\u200B'.join(text[i:i + interval] for i in range(0, len(text), interval))


def get_bitcoin_explorer_url(tx_id: str, base_url: str = BITCOIN_EXPLORER_URL) -> str:
    """
    Constructs a Bitcoin Explorer URL based on the network type and transaction ID.

    Args:
        tx_id (str): The transaction ID.
        base_url (str, optional): The base URL for the Bitcoin Explorer. Defaults to 'https://mempool.space'.

    Returns:
        str: The URL to view the transaction on the Bitcoin Explorer.
    """
    # Default network value if not provided
    network = SettingRepository.get_wallet_network().value

    # Construct URL based on the network
    if network == NetworkEnumModel.MAINNET.value:
        return f"{base_url}/tx/{tx_id}"
    return f"{base_url}/{network}/tx/{tx_id}"


def network_info(parent):
    """Get current network selected from local store"""
    try:
        network: NetworkEnumModel = SettingRepository.get_wallet_network()
        parent.network = network.value
    except CommonException as exc:
        logger.error(
            'Exception occurred: %s, Message: %s',
            type(exc).__name__, str(exc),
        )
        ToastManager.error(parent=None, title=None, description=exc.message)
    except Exception as exc:
        logger.error(
            'Exception occurred: %s, Message: %s',
            type(exc).__name__, str(exc),
        )
        ToastManager.error(
            parent=None, title=None,
            description=ERROR_SOMETHING_WENT_WRONG,
        )


def close_button_navigation(parent, back_page_navigation=None):
    """Close button navigation method"""
    if parent.originating_page == 'wallet_selection_page':
        title = 'connection_type'
        logo_1_path = ':/assets/embedded.png'
        logo_1_title = 'embedded'
        logo_2_path = ':/assets/remote.png'
        logo_2_title = WalletType.REMOTE_TYPE_WALLET.value
        params = SelectionPageModel(
            title=title,
            logo_1_path=logo_1_path,
            logo_1_title=logo_1_title,
            logo_2_path=logo_2_path,
            logo_2_title=logo_2_title,
            asset_id='none',
            callback='none',
            back_page_navigation=back_page_navigation,

        )
        parent.view_model.page_navigation.wallet_method_page(params)

    if parent.originating_page == 'settings_page':
        parent.view_model.page_navigation.settings_page()


def find_files_with_name(path, keyword):
    """This method finds a file using the provided name."""
    found_files = []

    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == keyword:  # Check if the file name exactly matches the keyword
                # Store the full path of the file
                found_files.append(os.path.join(root, file))

        # Additionally, check for matching directory names
        for directory in dirs:
            if directory == keyword:  # Check if the directory name exactly matches the keyword
                # Store the full path of the directory
                found_files.append(os.path.join(root, dir))

    return found_files


def sigterm_handler(_sig, _frame):
    """
    Handles the SIGTERM signal, which is sent to gracefully terminate the application.

    When the signal is received, this method displays a QMessageBox warning the user about
    the impending termination. If the user confirms by clicking "OK", it stops the Lightning
    Node server via the LnNodeServerManager and quits the application. If the user cancels,
    the application continues running.

    Args:
        sig (int): The signal number received (SIGTERM).
    """
    sigterm_warning_message = QApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'sigterm_warning_message', None,
    )
    qwarning = QMessageBox.warning(
        None,
        'Are you sure you want to exit?',
        sigterm_warning_message,
        QMessageBox.Ok | QMessageBox.Cancel,
    )

    if qwarning == QMessageBox.Ok:
        # Stop the LN node server and quit the application
        ln_node_manager = LnNodeServerManager.get_instance()
        ln_node_manager.stop_server_from_close_button()
        QApplication.instance().exit()


def set_number_validator(input_widget: QLineEdit) -> None:
    """
    Sets a validator on the given QLineEdit to allow only positive integers.

    Args:
        input_widget (QLineEdit): The input field to which the validator is applied.
    """
    number_pattern = QRegularExpression(r'^\d+$')
    validator = QRegularExpressionValidator(number_pattern, input_widget)
    input_widget.setValidator(validator)


def sat_to_msat(sat) -> int:
    """
    Convert satoshis (sat) to millisatoshis (mSAT).

    Args:
        sat (int): The amount in satoshis.

    Returns:
        int: The equivalent amount in millisatoshis.
    """
    sat_int = int(sat)
    return sat_int * 1000


def set_placeholder_value(parent: QLineEdit):
    """
        Ensures a QLineEdit input adheres to proper formatting for numeric values.

        - If the input is a single '0', it keeps it unchanged.
        - If the input starts with '0' but contains additional digits (e.g., '0123'),
        it removes the leading zeros while preserving the remaining digits.
        - If removing leading zeros results in an empty string, it sets the value back to '0'.

        Args:
            parent (QLineEdit): The QLineEdit widget whose text needs to be formatted.
    """

    text = parent.text()

    if text == '0':
        parent.setText('0')
    elif text.startswith('0') and len(text) > 1:
        striped_text = text.lstrip('0')
        parent.setText(striped_text or '0')


def extract_amount(balance_text, unit=' SATS'):
    """
    Parses a balance text, removes the specified unit, and converts it to an integer.

    Parameters:
    - balance_text (str): The balance text to parse.
    - unit (str): The unit to strip from the text (e.g., " SATS").

    Returns:
    - int: The balance as an integer, or 0 if the text is empty or invalid.
    """
    try:
        # Remove the unit and convert to an integer
        return int(balance_text.strip().replace(unit, ''))
    except ValueError:
        # Return 0 if parsing fails (e.g., empty or non-numeric text)
        return 0


def get_bitcoin_info_by_network():
    """
    Get Bitcoin ticker, name (with network type), and image path based on the current network.

    Returns:
        tuple: (ticker, network-specific Bitcoin name, image path)
    """
    network: NetworkEnumModel = SettingRepository.get_wallet_network()
    ticker: str = get_offline_asset_ticker(network)

    bitcoin_img_path = {
        NetworkEnumModel.MAINNET.value: ':/assets/bitcoin.png',
        NetworkEnumModel.REGTEST.value: ':/assets/regtest_bitcoin.png',
        NetworkEnumModel.TESTNET.value: ':/assets/testnet_bitcoin.png',
        NetworkEnumModel.TESTNET4.value: ':/assets/testnet_bitcoin.png',
    }
    img_path = bitcoin_img_path.get(network.value)

    if TokenSymbol.BITCOIN.value in ticker:
        bitcoin_asset = AssetType.BITCOIN.value.lower()
        if ticker == TokenSymbol.BITCOIN.value:
            return (ticker, f'{bitcoin_asset}', img_path)
        if ticker == TokenSymbol.TESTNET_BITCOIN.value:
            return (ticker, f'{NetworkEnumModel.TESTNET.value} {bitcoin_asset}', img_path)
        if ticker == TokenSymbol.TESTNET4_BITCOIN.value:
            return (ticker, f'{NetworkEnumModel.TESTNET4.value} {bitcoin_asset}', img_path)
        if ticker == TokenSymbol.REGTEST_BITCOIN.value:
            return (ticker, f'{NetworkEnumModel.REGTEST.value} {bitcoin_asset}', img_path)

    return None


TRANSACTION_SPEEDS = {
    'slow_checkBox': SLOW_TRANSACTION_FEE_BLOCKS,
    'medium_checkBox': MEDIUM_TRANSACTION_FEE_BLOCKS,
    'fast_checkBox': FAST_TRANSACTION_FEE_BLOCKS,
}


def disable_rln_node_termination_handling(wallet_type: WalletType):
    """
    Disconnects the RLN node process termination handler when the user closes the application.

    This ensures that the rln node termination handling logic does not trigger when the user explicitly exits.

    Args:
        wallet_type (WalletType): The type of the wallet being used.
    """
    if wallet_type.value == WalletType.EMBEDDED_TYPE_WALLET.value:
        ln_node_manager = LnNodeServerManager.get_instance()

        try:
            ln_node_manager.process.finished.disconnect()
        except CommonException as exc:
            logger.error(
                'Exception occurred: %s, Message: %s',
                type(exc).__name__, str(exc),
            )


def cleanup_debug_logs(zip_file_path: str, logs_dir=None):
    """
    Deletes the generated zip file and the extracted logs directory after successful use.

    Parameters:
    zip_file_path (str): Path to the zip file that needs to be deleted.
    logs_dir (str, optional): Path to the temporary logs directory to be removed. Defaults to None.
    """
    # Delete the zip file if it exists
    if os.path.exists(zip_file_path) and os.path.isfile(zip_file_path):
        os.remove(zip_file_path)

    # Delete the logs directory if it exists
    if logs_dir and os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        shutil.rmtree(logs_dir)
