"""Helper utilities for settings widget configuration.

This module contains helper functions for settings frame operations,
network endpoint configuration, and keyring state management.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.utils.constant import BITCOIND_RPC_HOST_MAINNET
from src.utils.constant import BITCOIND_RPC_HOST_REGTEST
from src.utils.constant import BITCOIND_RPC_HOST_TESTNET
from src.utils.constant import BITCOIND_RPC_HOST_TESTNET4
from src.utils.constant import BITCOIND_RPC_PORT_MAINNET
from src.utils.constant import BITCOIND_RPC_PORT_REGTEST
from src.utils.constant import BITCOIND_RPC_PORT_TESTNET
from src.utils.constant import BITCOIND_RPC_PORT_TESTNET4
from src.utils.constant import INDEXER_URL_MAINNET
from src.utils.constant import INDEXER_URL_REGTEST
from src.utils.constant import INDEXER_URL_TESTNET
from src.utils.constant import INDEXER_URL_TESTNET4
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import PROXY_ENDPOINT_MAINNET
from src.utils.constant import PROXY_ENDPOINT_REGTEST
from src.utils.constant import PROXY_ENDPOINT_TESTNET
from src.utils.constant import PROXY_ENDPOINT_TESTNET4
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.keyring_storage import get_value
from src.views.ui_restore_mnemonic import RestoreMnemonicWidget


def set_endpoint_based_on_network() -> tuple[str, str, str, int]:
    """Set various endpoints based on the currently selected wallet network.

    Returns:
        Tuple containing (indexer_url, proxy_endpoint, bitcoind_host, bitcoind_port)

    Raises:
        ValueError: If the stored network type is unsupported.
    """
    network_config_map = {
        NetworkEnumModel.MAINNET: (
            INDEXER_URL_MAINNET, PROXY_ENDPOINT_MAINNET,
            BITCOIND_RPC_HOST_MAINNET, BITCOIND_RPC_PORT_MAINNET,
        ),
        NetworkEnumModel.TESTNET: (
            INDEXER_URL_TESTNET, PROXY_ENDPOINT_TESTNET,
            BITCOIND_RPC_HOST_TESTNET, BITCOIND_RPC_PORT_TESTNET,
        ),
        NetworkEnumModel.TESTNET4: (
            INDEXER_URL_TESTNET4, PROXY_ENDPOINT_TESTNET4,
            BITCOIND_RPC_HOST_TESTNET4, BITCOIND_RPC_PORT_TESTNET4,
        ),
        NetworkEnumModel.REGTEST: (
            INDEXER_URL_REGTEST, PROXY_ENDPOINT_REGTEST,
            BITCOIND_RPC_HOST_REGTEST, BITCOIND_RPC_PORT_REGTEST,
        ),
    }
    stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()
    config = network_config_map.get(stored_network)
    if config:
        return config
    raise ValueError(f"Unsupported network type: {stored_network}")


def set_frame_content(
    frame, input_value, expiry_time_unit=None,
    validator=None, time_unit_combobox=None, suggestion_desc=None,
):
    """Set the content for a given settings frame.

    Args:
        frame: The frame to configure.
        input_value: The value to set in the input field.
        expiry_time_unit: Current expiry time unit for comparison.
        validator: Optional validator for the input field.
        time_unit_combobox: Optional time unit combobox widget.
        suggestion_desc: Optional suggestion description widget.
    """
    if isinstance(input_value, float) and input_value.is_integer():
        input_value = int(input_value)

    frame.input_value.setText(str(input_value))
    frame.input_value.setPlaceholderText(str(input_value))
    frame.input_value.setValidator(validator)

    if not suggestion_desc:
        frame.suggestion_desc.hide()

    if time_unit_combobox:
        index = time_unit_combobox.findText(
            expiry_time_unit, Qt.MatchFixedString,
        )
        if index != -1:
            time_unit_combobox.setCurrentIndex(index)
    else:
        frame.time_unit_combobox.hide()

    frame.input_value.textChanged.connect(
        lambda: update_save_button(frame, input_value, expiry_time_unit),
    )

    if time_unit_combobox:
        frame.time_unit_combobox.currentTextChanged.connect(
            lambda: update_save_button(
                frame, input_value, expiry_time_unit, time_unit_combobox,
            ),
        )

    # Initial call to set the correct button state
    update_save_button(
        frame, input_value,
        expiry_time_unit, time_unit_combobox,
    )


def update_save_button(frame, input_value, expiry_time_unit: str, time_unit_combobox=None):
    """Update the state of the save button based on input changes.

    Args:
        frame: The frame containing the save button.
        input_value: The original value to compare against.
        expiry_time_unit: Current expiry time unit for comparison.
        time_unit_combobox: Optional time unit combobox widget.
    """
    current_text = frame.input_value.text().strip()
    current_unit = frame.time_unit_combobox.currentText() if time_unit_combobox else ''

    time_unit_changed = current_unit != expiry_time_unit

    if current_text and (current_text != str(input_value) or (time_unit_combobox and time_unit_changed)):
        frame.save_button.setDisabled(False)
    else:
        frame.save_button.setDisabled(True)


def check_keyring_state_for_password(parent, view_model) -> str | None:
    """Check keyring status and retrieve wallet password.

    Retrieves password either from secure storage if keyring is disabled,
    or via user prompt through a mnemonic dialog if enabled.

    Args:
        parent: Parent widget for dialog display.
        view_model: The main view model.

    Returns:
        The wallet password string if retrieved, None otherwise.
    """
    keyring_status = SettingRepository.get_keyring_status()
    if keyring_status is False:
        network: NetworkEnumModel = SettingRepository.get_wallet_network()
        password: str = get_value(WALLET_PASSWORD_KEY, network.value)
        return password
    if keyring_status is True:
        mnemonic_dialog = RestoreMnemonicWidget(
            parent=parent, view_model=view_model, origin_page='setting_card', mnemonic_visibility=False,
        )
        mnemonic_dialog.mnemonic_detail_text_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'lock_unlock_password_required', None,
            ),
        )
        mnemonic_dialog.mnemonic_detail_text_label.setFixedHeight(40)
        result = mnemonic_dialog.exec()
        if result == QDialog.Accepted:
            password = mnemonic_dialog.password_input.text()
            return password
    return None
