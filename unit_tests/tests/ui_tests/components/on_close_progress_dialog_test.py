"""Unit test for On close progress dialog."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMessageBox

from src.data.repository.setting_repository import SettingRepository
from src.data.service.backup_service import BackupService
from src.utils.constant import MAX_ATTEMPTS_FOR_CLOSE
from src.utils.constant import MNEMONIC_KEY
from src.utils.constant import NODE_CLOSE_INTERVAL
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.error_message import ERROR_UNABLE_TO_STOP_NODE
from src.utils.ln_node_manage import LnNodeServerManager
from src.views.components.on_close_progress_dialog import OnCloseDialogBox
from src.views.ui_restore_mnemonic import RestoreMnemonicWidget


@pytest.fixture
def on_close_progress_dialog_widget(qtbot):
    """Fixture to create and return an instance of OnCloseDialogBox."""
    widget = OnCloseDialogBox()
    qtbot.addWidget(widget)
    return widget


@patch.object(OnCloseDialogBox, '_close_node_app')
def test_start_process_without_backup_required(mock_close_node, on_close_progress_dialog_widget):
    """Test _start_process method when backup is not required."""
    on_close_progress_dialog_widget._start_process(is_backup_require=False)
    mock_close_node.assert_called_once()


@patch.object(RestoreMnemonicWidget, 'exec')
@patch.object(SettingRepository, 'get_keyring_status', return_value=True)
def test_start_process_with_backup_required_keyring(mock_keyring_status, mock_exec, on_close_progress_dialog_widget):
    """Test _start_process method when backup is required and keyring is enabled."""
    on_close_progress_dialog_widget._start_process(is_backup_require=True)
    mock_keyring_status.assert_called_once()
    mock_exec.assert_called_once()


@patch('src.views.components.on_close_progress_dialog.get_value')
@patch.object(SettingRepository, 'get_wallet_network', return_value=MagicMock(value='testnet'))
@patch.object(OnCloseDialogBox, '_start_backup')
@patch.object(SettingRepository, 'get_keyring_status', return_value=False)
def test_start_process_with_backup_required_no_keyring(
    mock_keyring_status, mock_start_backup, mock_wallet_network, mock_get_value, on_close_progress_dialog_widget,
):
    """Test _start_process method when backup is required and keyring is not used."""

    # Mock get_value to return specific values for each key
    def mock_get_value_side_effect(key, network):
        if key == MNEMONIC_KEY:
            return 'mocked_mnemonic'
        if key == WALLET_PASSWORD_KEY:
            return 'mocked_password'
        return None

    mock_get_value.side_effect = mock_get_value_side_effect

    # Call the method under test
    on_close_progress_dialog_widget._start_process(is_backup_require=True)

    # Verify that get_value is called with the correct arguments using named parameters
    expected_calls = [
        call(MNEMONIC_KEY, 'testnet'),
        call(key=WALLET_PASSWORD_KEY, network='testnet'),
    ]
    mock_get_value.assert_has_calls(expected_calls, any_order=True)

    # Verify the correct arguments are passed to _start_backup
    mock_start_backup.assert_called_once_with(
        'mocked_mnemonic', 'mocked_password',
    )


@patch.object(OnCloseDialogBox, '_close_node_app')
def test_on_success_of_backup(mock_close_node, on_close_progress_dialog_widget):
    """Test _on_success_of_backup method to ensure node closes after successful backup."""
    on_close_progress_dialog_widget._on_success_of_backup()
    assert on_close_progress_dialog_widget.is_backup_onprogress is False
    mock_close_node.assert_called_once()


@patch.object(QMessageBox, 'critical')
@patch.object(OnCloseDialogBox, '_close_node_app')
def test_on_error_of_backup(mock_close_node, mock_critical, on_close_progress_dialog_widget):
    """Test _on_error_of_backup method to ensure error handling during backup."""
    on_close_progress_dialog_widget._on_error_of_backup()
    assert on_close_progress_dialog_widget.is_backup_onprogress is False
    mock_critical.assert_called_once_with(
        on_close_progress_dialog_widget, 'Failed', ERROR_SOMETHING_WENT_WRONG,
    )
    mock_close_node.assert_called_once()


@patch.object(QMessageBox, 'critical')
@patch.object(QApplication, 'exit')
def test_on_error_of_closing_node(mock_exit, mock_critical, on_close_progress_dialog_widget):
    """Test _on_error_of_closing_node method to ensure error handling during node closing."""
    on_close_progress_dialog_widget._on_error_of_closing_node()
    assert on_close_progress_dialog_widget.is_node_closing_onprogress is False
    mock_critical.assert_called_once_with(
        on_close_progress_dialog_widget, 'Failed', ERROR_UNABLE_TO_STOP_NODE,
    )
    mock_exit.assert_called_once()


@patch.object(QApplication, 'exit')
def test_on_success_close_node(mock_quit, on_close_progress_dialog_widget):
    """Test _on_success_close_node method to ensure application quits after node closes."""
    on_close_progress_dialog_widget._on_success_close_node()
    assert on_close_progress_dialog_widget.is_node_closing_onprogress is False
    mock_quit.assert_called_once()


@patch.object(LnNodeServerManager, 'stop_server_from_close_button')
@patch.object(QApplication, 'exit')
def test_close_node_app_when_node_running(mock_exit, mock_stop_server, on_close_progress_dialog_widget):
    """Test _close_node_app method when node is still running."""
    mock_state = MagicMock(return_value=QProcess.Running)
    on_close_progress_dialog_widget.ln_node_manage.process.state = mock_state
    on_close_progress_dialog_widget._close_node_app()
    assert on_close_progress_dialog_widget.is_backup_onprogress is False
    assert on_close_progress_dialog_widget.is_node_closing_onprogress is True
    mock_stop_server.assert_called_once()
    mock_exit.assert_not_called()


@patch.object(QApplication, 'exit')
def test_close_node_app_when_node_not_running(mock_exit, on_close_progress_dialog_widget):
    """Test _close_node_app method when node is not running."""
    mock_state = MagicMock(return_value=QProcess.NotRunning)
    on_close_progress_dialog_widget.ln_node_manage.process.state = mock_state
    on_close_progress_dialog_widget._close_node_app()
    mock_exit.assert_called_once()


def test_close_event_backup_in_progress(on_close_progress_dialog_widget):
    """Test closeEvent when backup is in progress."""
    event = MagicMock()  # Mock the QCloseEvent

    # Case 1: Backup in progress, user confirms to close (Yes)
    on_close_progress_dialog_widget.is_backup_onprogress = True
    with patch('PySide6.QtWidgets.QMessageBox.question', return_value=QMessageBox.Yes):
        on_close_progress_dialog_widget.closeEvent(event)
        event.accept.assert_called_once()
        event.ignore.assert_not_called()

    # Reset the mock for the next case
    event.reset_mock()

    # Case 2: Backup in progress, user cancels the close (No)
    on_close_progress_dialog_widget.is_backup_onprogress = True
    with patch('PySide6.QtWidgets.QMessageBox.question', return_value=QMessageBox.No):
        on_close_progress_dialog_widget.closeEvent(event)
        event.ignore.assert_called_once()
        event.accept.assert_not_called()

    # Reset the mock for the next case
    event.reset_mock()

    # Case 3: Node closing in progress
    on_close_progress_dialog_widget.is_backup_onprogress = False
    on_close_progress_dialog_widget.is_node_closing_onprogress = True
    on_close_progress_dialog_widget.closeEvent(event)
    event.ignore.assert_called_once()
    event.accept.assert_not_called()

    # Reset the mock for the next case
    event.reset_mock()

    # Case 4: No backup or node closing in progress
    on_close_progress_dialog_widget.is_backup_onprogress = False
    on_close_progress_dialog_widget.is_node_closing_onprogress = False
    on_close_progress_dialog_widget.closeEvent(event)
    event.accept.assert_called_once()
    event.ignore.assert_not_called()


def test_close_event_node_closing_in_progress(on_close_progress_dialog_widget):
    """Test closeEvent when node closing is in progress."""
    on_close_progress_dialog_widget.is_node_closing_onprogress = True
    event = MagicMock()
    on_close_progress_dialog_widget.closeEvent(event)
    event.ignore.assert_called_once()
    assert on_close_progress_dialog_widget.status_label.text() == f'Please wait until the node closes. It may take up to {
        MAX_ATTEMPTS_FOR_CLOSE * NODE_CLOSE_INTERVAL
    } seconds'


def test_close_event_no_process_in_progress(on_close_progress_dialog_widget):
    """Test closeEvent when no backup or node closing is in progress."""
    on_close_progress_dialog_widget.is_backup_onprogress = False
    on_close_progress_dialog_widget.is_node_closing_onprogress = False
    event = MagicMock()
    on_close_progress_dialog_widget.closeEvent(event)
    event.accept.assert_called_once()


def test_ui(on_close_progress_dialog_widget: OnCloseDialogBox):
    """Test the UI elements in OnCloseDialogBox."""
    assert on_close_progress_dialog_widget.windowTitle(
    ) == 'Please wait for backup or close node'
    assert on_close_progress_dialog_widget.status_label.text() == 'Starting backup...'
    assert on_close_progress_dialog_widget.loading_label.movie().isValid()


@patch.object(OnCloseDialogBox, '_update_status')
@patch.object(OnCloseDialogBox, 'run_in_thread')
def test_start_backup(mock_run_in_thread, mock_update_status, on_close_progress_dialog_widget):
    """Test _start_backup method to ensure status update and thread initiation."""
    mnemonic = 'test_mnemonic'
    password = 'test_password'

    # Automatically simulate the backup process without manual intervention
    on_close_progress_dialog_widget._start_backup(mnemonic, password)

    # Verify that the status is updated
    mock_update_status.assert_called_once_with('Backup process started')

    # Verify that is_backup_onprogress is set to True
    assert on_close_progress_dialog_widget.is_backup_onprogress is True

    # Simulate the automatic completion of the backup process
    on_close_progress_dialog_widget._on_success_of_backup()

    # Verify that run_in_thread is called with the correct arguments
    mock_run_in_thread.assert_called_once_with(
        BackupService.backup, {
            'args': [mnemonic, password],
            'callback': on_close_progress_dialog_widget._on_success_of_backup,
            'error_callback': on_close_progress_dialog_widget._on_error_of_backup,
        },
    )
