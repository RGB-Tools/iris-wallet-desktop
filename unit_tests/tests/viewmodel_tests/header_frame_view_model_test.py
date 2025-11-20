"""Unit test for header frame view model"""
# pylint: disable=redefined-outer-name,unused-argument
from __future__ import annotations

from unittest.mock import MagicMock

from src.utils.constant import PING_DNS_SERVER_CALL_INTERVAL
from src.viewmodels.header_frame_view_model import HeaderFrameViewModel
from src.viewmodels.header_frame_view_model import NetworkCheckerThread


def test_network_checker_thread_success(mocker, qtbot):
    """NetworkCheckerThread emits True when network is available."""
    network_checker = NetworkCheckerThread()

    # Proper mock socket
    mock_socket = MagicMock()
    mocker.patch('socket.create_connection', return_value=mock_socket)

    # start() is mocked globally to call run() synchronously
    with qtbot.waitSignal(
        network_checker.network_status_signal, timeout=500,
    ) as blocker:
        network_checker.start()

    assert blocker.args == [True]


def test_network_checker_thread_failure(mocker, qtbot):
    """NetworkCheckerThread emits False when network is unavailable."""
    network_checker = NetworkCheckerThread()

    mocker.patch('socket.create_connection', side_effect=OSError)

    with qtbot.waitSignal(
        network_checker.network_status_signal, timeout=500,
    ) as blocker:
        network_checker.start()

    assert blocker.args == [False]


def test_check_internet_conn_success(mocker):
    """Test check_internet_conn returns True when socket connection succeeds."""
    network_checker = NetworkCheckerThread()

    mock_socket = MagicMock()
    mocker.patch('socket.create_connection', return_value=mock_socket)

    assert network_checker.check_internet_conn() is True


def test_check_internet_conn_failure(mocker):
    """Test check_internet_conn returns False when socket connection fails."""
    network_checker = NetworkCheckerThread()

    mocker.patch('socket.create_connection', side_effect=OSError)

    assert network_checker.check_internet_conn() is False


def test_header_frame_view_model_init(mocker):
    """Test that HeaderFrameViewModel initializes correctly with a running timer."""
    mock_timer = mocker.patch(
        'src.viewmodels.header_frame_view_model.QTimer',
    )

    view_model = HeaderFrameViewModel()

    # Ensure QTimer was instantiated
    mock_timer.assert_called_once()

    # Retrieve the mocked QTimer instance
    mock_timer_instance = mock_timer.return_value

    # Ensure timer settings and start behavior are correct
    mock_timer_instance.setInterval.assert_called_once_with(
        PING_DNS_SERVER_CALL_INTERVAL,
    )
    mock_timer_instance.timeout.connect.assert_called_once_with(
        view_model.start_network_check,
    )
    mock_timer_instance.start.assert_called_once()


def test_header_frame_view_model_network_check(mocker):
    """Test that start_network_check creates a NetworkCheckerThread and starts it."""
    view_model = HeaderFrameViewModel()

    mock_thread = mocker.patch(
        'src.viewmodels.header_frame_view_model.NetworkCheckerThread',
    )
    mock_instance = mock_thread.return_value

    view_model.start_network_check()

    mock_thread.assert_called_once()
    mock_instance.network_status_signal.connect.assert_called_once_with(
        view_model.handle_network_status,
    )
    mock_instance.start.assert_called_once()


def test_header_frame_view_model_handle_network_status():
    """Test that handle_network_status emits the correct signal."""
    view_model = HeaderFrameViewModel()
    received_signals = []

    def signal_received(value):
        received_signals.append(value)

    view_model.network_status_signal.connect(signal_received)

    view_model.handle_network_status(True)
    view_model.handle_network_status(False)

    assert received_signals == [True, False]


def test_header_frame_view_model_stop_network_checker(mocker):
    """Test that stop_network_checker stops the timer."""
    view_model = HeaderFrameViewModel()

    mock_timer = mocker.patch.object(view_model.timer, 'stop')

    view_model.stop_network_checker()

    mock_timer.assert_called_once()
