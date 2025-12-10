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

import os
import tempfile

import keyring
import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope='session', autouse=True)
def qt_app():
    """Fixture to set up the QApplication instance for the test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

# ---------------- Global Safety Fixtures -----------------


@pytest.fixture(scope='session', autouse=True)
def _isolate_user_dirs():
    """Redirect user data/config/cache dirs to a temporary location for the entire test session."""
    with tempfile.TemporaryDirectory(prefix='iris_wallet_tests_') as td:
        os.environ.setdefault('HOME', td)
        os.environ.setdefault(
            'XDG_DATA_HOME', os.path.join(td, '.local', 'share'),
        )
        os.environ.setdefault('XDG_CONFIG_HOME', os.path.join(td, '.config'))
        os.environ.setdefault('XDG_CACHE_HOME', os.path.join(td, '.cache'))
        os.environ.setdefault(
            'IRIS_WALLET_DATA_DIR',
            os.path.join(td, 'iris-wallet-vault'),
        )
        yield


@pytest.fixture(autouse=True)
def _mock_keyring(monkeypatch):
    """Ensure keyring operations are in-memory and never hit the system keychain."""

    _store: dict[tuple[str, str], str] = {}

    def _get_password(service_name: str, username: str) -> str | None:
        return _store.get((service_name, username))

    def _set_password(service_name: str, username: str, password: str) -> None:
        _store[(service_name, username)] = password

    def _delete_password(service_name: str, username: str) -> None:
        _store.pop((service_name, username), None)

    monkeypatch.setattr(keyring, 'get_password', _get_password, raising=False)
    monkeypatch.setattr(keyring, 'set_password', _set_password, raising=False)
    monkeypatch.setattr(
        keyring, 'delete_password',
        _delete_password, raising=False,
    )

    if hasattr(keyring, 'set_keyring'):
        class _InMemoryBackend:  # pragma: no cover
            priority = 1

            def get_password(self, service: str, username: str) -> str | None:
                """Get password from in-memory store."""
                return _get_password(service, username)

            def set_password(self, service: str, username: str, password: str) -> None:
                """Set password in in-memory store."""
                return _set_password(service, username, password)

            def delete_password(self, service: str, username: str) -> None:
                """Delete password from in-memory store."""
                return _delete_password(service, username)
        try:
            keyring.set_keyring(_InMemoryBackend())
        except Exception:
            pass
