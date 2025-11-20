"""
Utility functions for handling various operations in the application.

These functions provide functionalities such as address shortening, stylesheet loading,
pixmap creation, Google Auth token checking, mnemonic hashing and validation, port checking,
and retrieving configuration arguments for node setup.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import socket
import sys
from typing import Any

from mnemonic import Mnemonic
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPixmap
from requests import HTTPError
from requests.exceptions import ConnectionError as RequestsConnectionError

from src.data.repository.setting_repository import SettingRepository
from src.flavour import __ldk_port__
from src.model.common_operation_model import UnlockRequestModel
from src.model.enums.enums_model import NetworkEnumModel
from src.utils.build_app_path import app_paths
from src.utils.cache import Cache
from src.utils.constant import ANNOUNCE_ADDRESS
from src.utils.constant import ANNOUNCE_ALIAS
from src.utils.constant import BITCOIND_RPC_HOST_MAINNET
from src.utils.constant import BITCOIND_RPC_HOST_REGTEST
from src.utils.constant import BITCOIND_RPC_HOST_TESTNET
from src.utils.constant import BITCOIND_RPC_PASSWORD_MAINNET
from src.utils.constant import BITCOIND_RPC_PASSWORD_REGTEST
from src.utils.constant import BITCOIND_RPC_PASSWORD_TESTNET
from src.utils.constant import BITCOIND_RPC_PORT_MAINNET
from src.utils.constant import BITCOIND_RPC_PORT_REGTEST
from src.utils.constant import BITCOIND_RPC_PORT_TESTNET
from src.utils.constant import BITCOIND_RPC_USER_MAINNET
from src.utils.constant import BITCOIND_RPC_USER_REGTEST
from src.utils.constant import BITCOIND_RPC_USER_TESTNET
from src.utils.constant import DAEMON_PORT
from src.utils.constant import INDEXER_URL_MAINNET
from src.utils.constant import INDEXER_URL_REGTEST
from src.utils.constant import INDEXER_URL_TESTNET
from src.utils.constant import LDK_PORT
from src.utils.constant import LDK_PORT_KEY
from src.utils.constant import LIGHTNING_URL_KEY
from src.utils.constant import PROXY_ENDPOINT_MAINNET
from src.utils.constant import PROXY_ENDPOINT_REGTEST
from src.utils.constant import PROXY_ENDPOINT_TESTNET
from src.utils.constant import SAVED_ANNOUNCE_ADDRESS
from src.utils.constant import SAVED_ANNOUNCE_ALIAS
from src.utils.constant import SAVED_BITCOIND_RPC_HOST
from src.utils.constant import SAVED_BITCOIND_RPC_PASSWORD
from src.utils.constant import SAVED_BITCOIND_RPC_PORT
from src.utils.constant import SAVED_BITCOIND_RPC_USER
from src.utils.constant import SAVED_INDEXER_URL
from src.utils.constant import SAVED_PROXY_ENDPOINT
from src.utils.custom_exception import CommonException
from src.utils.endpoints import NODE_INFO_ENDPOINT
from src.utils.error_message import ERROR_NODE_IS_LOCKED_CALL_UNLOCK
from src.utils.gauth import TOKEN_PICKLE_PATH
from src.utils.local_store import local_store
from src.utils.logging import logger
from src.utils.request import Request


def handle_asset_address(address: str, short_len: int = 12) -> str:
    """
    Shortens the given address for display.

    Parameters:
    address (str): The full address to be shortened.
    short_len (int): The number of characters to keep from the start and end of the address. Default is 12.

    Returns:
    str: The shortened address with the first `short_len` and last `short_len` characters displayed.
    """
    new_address = str(address)
    shortened_address = f'{new_address[:short_len]}...{
        new_address[-short_len:]
    }'
    return shortened_address


def load_stylesheet(file: str = 'views/qss/style.qss') -> str:
    """
    Loads the QSS stylesheet from the specified file.

    Parameters:
    file (str): The relative path to the QSS file. Defaults to "views/qss/style.qss".

    Returns:
    str: The content of the QSS file as a string.

    Raises:
    FileNotFoundError: If the QSS file is not found at the specified path.
    """
    if getattr(sys, 'frozen', False):
        # If the application is frozen (compiled with PyInstaller)
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)),
        )
        qss_folder_path = os.path.join(base_path, 'views/qss')
        filename = os.path.basename(file)
        file = os.path.join(qss_folder_path, filename)
    else:
        if not os.path.isabs(file):
            # Get the directory of the current script (helpers.py)
            base_path = os.path.dirname(os.path.abspath(__file__))
            # Construct the full path to the QSS file relative to the script's location
            file = os.path.join(base_path, '..', file)

    try:
        with open(file, encoding='utf-8') as _f:
            stylesheet = _f.read()
        return stylesheet
    except FileNotFoundError:
        logger.error("Error: Stylesheet file '%s' not found.", file)
        raise


def create_circular_pixmap(diameter: int, color: QColor) -> QPixmap:
    """
    Create a circular pixmap with a transparent background.

    This function generates a circular pixmap of the specified diameter,
    filled with the given color, and with a transparent background.
    The resulting pixmap can be used for various graphical purposes
    within a Qt application, such as creating custom icons or buttons with circular shapes.

    Parameters:
    diameter (int): The diameter of the circular pixmap to be created.
    color (QColor): The color to fill the circular pixmap with.

    Returns:
    QPixmap: The generated circular pixmap with the specified color and transparent background.
    """
    pixmap = QPixmap(diameter, diameter)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(color)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, diameter, diameter)
    painter.end()

    return pixmap


def check_google_auth_token_available() -> bool:
    """
    Check if the Google Auth token is available at the specified location.

    Returns:
    bool: True if the token file exists, False otherwise.
    """
    return os.path.exists(TOKEN_PICKLE_PATH)


def hash_mnemonic(mnemonic_phrase: str) -> str:
    """
    Hashes the given mnemonic phrase.

    Validates the mnemonic phrase and then hashes it using SHA-256,
    followed by Base32 encoding. The result is truncated to the first 10 characters.

    Parameters:
    mnemonic_phrase (str): The mnemonic phrase to be hashed.

    Returns:
    str: The hashed and encoded mnemonic.
    """
    validate_mnemonic(mnemonic_phrase=mnemonic_phrase)

    sha256_hash = hashlib.sha256(mnemonic_phrase.encode()).digest()
    base32_encoded = base64.b32encode(sha256_hash).decode().rstrip('=')

    return base32_encoded[:10]


def validate_mnemonic(mnemonic_phrase: str):
    """
    Validates the given mnemonic phrase.

    Parameters:
    mnemonic_phrase (str): The mnemonic phrase to be validated.

    Raises:
    ValueError: If the mnemonic phrase is invalid.
    """
    mnemonic = Mnemonic('english')
    if not mnemonic.check(mnemonic_phrase):
        raise ValueError('Invalid mnemonic phrase')


def is_port_available(port: int) -> bool:
    """
    Checks if a given port is available on the local host.

    Parameters:
    port (int): The port number to check.

    Returns:
    bool: True if the port is available, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


def get_available_port(port: int) -> int:
    """
    Finds and returns the next available port starting from the given port.

    Parameters:
    port (int): The starting port number to check for availability.

    Returns:
    int: The next available port number.
    """
    if is_port_available(port):
        return port
    return get_available_port(port + 1)


def get_node_arg_config(network: NetworkEnumModel) -> list:
    """
    Retrieves the configuration arguments for setting up the node based on the network.

    Parameters:
    network (NetworkEnumModel): The network model enum indicating the network type.

    Returns:
    list: A list of arguments for configuring the node.

    Raises:
    Exception: If any error occurs during the retrieval of configuration arguments.
    """
    try:
        daemon_port = get_available_port(DAEMON_PORT)
        if __ldk_port__ is None:
            ldk_port = get_available_port(LDK_PORT)
        else:
            ldk_port = __ldk_port__
        node_data_path = app_paths.node_data_path
        node_url = f'http://127.0.0.1:{daemon_port}'
        local_store.set_value(LIGHTNING_URL_KEY, node_url)
        local_store.set_value(LDK_PORT_KEY, ldk_port)
        return [
            node_data_path,
            '--daemon-listening-port', str(daemon_port),
            '--ldk-peer-listening-port', str(ldk_port),
            '--network', network.value,
        ]
    except Exception as exc:
        raise exc


def get_build_info() -> dict | None:
    """Load build JSON file and return value in case of freeze."""
    if getattr(sys, 'frozen', False):
        base_path = getattr(
            sys, '_MEIPASS', os.path.dirname(
                os.path.abspath(__file__),
            ),
        )
        build_file_path = os.path.join(base_path, 'build_info.json')

        try:
            with open(build_file_path, encoding='utf-8') as build_file:
                data = json.load(build_file)
            return {
                'build_flavour': data.get('build_flavour'),
                'machine_arch': data.get('machine_arch'),
                'os_type': data.get('os_type'),
                'arch_type': data.get('arch_type'),
                'app-version': data.get('app-version'),
            }
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            logger.error(
                'Exception occurred while get_build_info: %s, Message: %s', type(
                    exc,
                ).__name__, str(exc),
            )
            return None
    # In case of not frozen and not executable return None
    return None


def get_bitcoin_config(network: NetworkEnumModel, password) -> UnlockRequestModel:
    """
    Retrieves the Bitcoin wallet configuration for the specified network.

    Combines shared and network-specific settings (RPC credentials, indexer URL, proxy endpoint)
    to create an `UnlockRequestModel` for the given network (MAINNET, TESTNET, or REGTEST).

    Args:
        network (NetworkEnumModel): The network type (MAINNET, TESTNET, REGTEST).
        password (str): The wallet password.

    Returns:
        UnlockRequestModel: The configuration for unlocking the wallet.

    Raises:
        Exception: If an error occurs while retrieving the configuration.
    """
    try:
        # Constants shared across all networks
        shared_config = {
            SAVED_ANNOUNCE_ADDRESS: ANNOUNCE_ADDRESS,
            SAVED_ANNOUNCE_ALIAS: ANNOUNCE_ALIAS,
        }

        # Network-specific configurations
        config_mapping = {
            NetworkEnumModel.MAINNET: {
                SAVED_BITCOIND_RPC_USER: BITCOIND_RPC_USER_MAINNET,
                SAVED_BITCOIND_RPC_PASSWORD: BITCOIND_RPC_PASSWORD_MAINNET,
                SAVED_BITCOIND_RPC_HOST: BITCOIND_RPC_HOST_MAINNET,
                SAVED_BITCOIND_RPC_PORT: BITCOIND_RPC_PORT_MAINNET,
                SAVED_INDEXER_URL: INDEXER_URL_MAINNET,
                SAVED_PROXY_ENDPOINT: PROXY_ENDPOINT_MAINNET,
            },
            NetworkEnumModel.TESTNET: {
                SAVED_BITCOIND_RPC_USER: BITCOIND_RPC_USER_TESTNET,
                SAVED_BITCOIND_RPC_PASSWORD: BITCOIND_RPC_PASSWORD_TESTNET,
                SAVED_BITCOIND_RPC_HOST: BITCOIND_RPC_HOST_TESTNET,
                SAVED_BITCOIND_RPC_PORT: BITCOIND_RPC_PORT_TESTNET,
                SAVED_INDEXER_URL: INDEXER_URL_TESTNET,
                SAVED_PROXY_ENDPOINT: PROXY_ENDPOINT_TESTNET,
            },
            NetworkEnumModel.REGTEST: {
                SAVED_BITCOIND_RPC_USER: BITCOIND_RPC_USER_REGTEST,
                SAVED_BITCOIND_RPC_PASSWORD: BITCOIND_RPC_PASSWORD_REGTEST,
                SAVED_BITCOIND_RPC_HOST: BITCOIND_RPC_HOST_REGTEST,
                SAVED_BITCOIND_RPC_PORT: BITCOIND_RPC_PORT_REGTEST,
                SAVED_INDEXER_URL: INDEXER_URL_REGTEST,
                SAVED_PROXY_ENDPOINT: PROXY_ENDPOINT_REGTEST,
            },
        }
        # Retrieve the appropriate configuration based on the network
        network_config = config_mapping.get(network) or {}

        # Merge shared config with network-specific config
        complete_config = {**network_config, **shared_config}

        # Retrieve or set values in local_store dynamically using constants as keys
        dynamic_config = {}
        for key, value in complete_config.items():
            dynamic_config[key] = SettingRepository.get_config_value(
                key, value,
            )

        # Create and return the UnlockRequestModel
        bitcoin_config = UnlockRequestModel(
            bitcoind_rpc_username=dynamic_config[SAVED_BITCOIND_RPC_USER],
            bitcoind_rpc_password=dynamic_config[SAVED_BITCOIND_RPC_PASSWORD],
            bitcoind_rpc_host=dynamic_config[SAVED_BITCOIND_RPC_HOST],
            bitcoind_rpc_port=dynamic_config[SAVED_BITCOIND_RPC_PORT],
            indexer_url=dynamic_config[SAVED_INDEXER_URL],
            proxy_endpoint=dynamic_config[SAVED_PROXY_ENDPOINT],
            announce_addresses=[dynamic_config[SAVED_ANNOUNCE_ADDRESS]],
            announce_alias=dynamic_config[SAVED_ANNOUNCE_ALIAS],
            password=password,
        )
        return bitcoin_config
    except Exception as exc:
        raise exc


def process_response(response, invalidate_cache: bool = True, expect_json: bool = True) -> Any:
    """
    Processes the response from a request.
    """
    response.raise_for_status()
    if invalidate_cache:
        cache = Cache.get_cache_session()
        if cache is not None:
            cache.invalidate_cache()
    if expect_json:
        return response.json()
    return None


def handle_connection_error(context: str, exc: Exception) -> None:
    """Handle connection error."""
    logger.error(
        'Exception occurred at Decorator(%s): %s, Message: %s',
        context,
        type(exc).__name__,
        str(exc),
    )

    raise CommonException('Unable to connect to node') from exc


def handle_generic_error(context: str, exc: Exception, message: str) -> None:
    """Handle generic error."""
    logger.error(
        'Exception occurred at Decorator(%s): %s, Message: %s',
        context,
        type(exc).__name__,
        str(exc),
    )

    raise CommonException(message) from exc


def check_node(context: str) -> bool:
    """Shared node-lock check used by lock_required/unlock_required decorators.

    Returns False when node is not locked (2xx).
    Returns True when server reports locked (specific 403 payload).
    Raises CommonException for other HTTP errors.
    Delegates connection and generic errors to shared handlers.
    """
    try:
        response = Request.get(NODE_INFO_ENDPOINT)
        response.raise_for_status()
        return False
    except HTTPError as error:
        if error.response.status_code == 403:
            try:
                error_data = error.response.json()
                if error_data.get('error') == ERROR_NODE_IS_LOCKED_CALL_UNLOCK and error_data.get('code') == 403:
                    return True
            except ValueError:
                pass
        else:
            error_data = error.response.json()
            error_message = error_data.get('error', 'Unhandled error')
            logger.error(error_message)
            raise CommonException(error_message) from error
    except RequestsConnectionError as exc:
        handle_connection_error(context, exc)
    except Exception as exc:
        handle_generic_error(
            context, exc, f'Decorator({
                context
            }): Error while checking if node is locked',
        )
    return False
