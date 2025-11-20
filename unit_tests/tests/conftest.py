"""
Pytest fixture to ensure a QApplication instance is available for the test session.

This fixture is automatically used for the entire test session (`autouse=True`)
and ensures that a single instance of `QApplication` is created and shared
among all tests. If an instance of `QApplication` already exists, it will use
the existing one; otherwise, it creates a new instance.

The `scope="session"` parameter ensures that the `QApplication` instance is
created only once per test session, and is reused across all tests, which is
useful for tests that involve PySide6/Qt widgets.

Yields:
    QApplication: An instance of `QApplication` to be used in tests.
"""
from __future__ import annotations

import pytest
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope='session', autouse=True)
def qt_app():
    """Fixture to set up the QApplication instance for the test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()


@pytest.fixture(autouse=True)
def mock_qthread_start(mocker):
    """
    Automatically mock QThread.start() to prevent actual thread creation.

    This prevents 'QThread: Destroyed while thread is still running' errors
    that cause pytest-xdist to fail with 'ValueError: list.remove(x): x not in list'.

    Tests that need actual threading should call thread.run() directly instead.
    """

    def mock_start_wrapper(self):
        """Mock start that calls run() synchronously instead of starting a thread."""
        # Call run() directly in the same thread instead of starting a new thread
        self.run()

    mocker.patch.object(QThread, 'start', mock_start_wrapper)


@pytest.fixture(autouse=True)
def mock_toast_manager(mocker, request):
    """
    Automatically mock ToastManager methods to prevent 'Main window not set' errors.

    ToastManager requires a main window to be set before creating toasts,
    which is not available in unit tests. This fixture mocks all toast methods
    to prevent the ValueError from being raised during tests.

    Skip mocking for toast_test.py since those tests specifically test ToastManager.
    """
    # Skip mocking for toast_test.py which specifically tests ToastManager
    if 'toast_test.py' in str(request.fspath):
        return

    mocker.patch('src.views.components.toast.ToastManager.error')
    mocker.patch('src.views.components.toast.ToastManager.success')
    mocker.patch('src.views.components.toast.ToastManager.info')
    mocker.patch('src.views.components.toast.ToastManager.warning')
