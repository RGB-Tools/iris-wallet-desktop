"""
Authenticate the user and obtain credentials for Google Drive API.
"""
from __future__ import annotations

import os
import pickle
import socket
import threading
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qs
from urllib.parse import urlparse

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from PySide6.QtCore import QEventLoop
from PySide6.QtCore import QUrl
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from accessible_constant import BACKUP_WINDOW
from config import client_config
from src.utils.constant import G_SCOPES as SCOPES
from src.utils.local_store import local_store
from src.utils.logging import logger

application_local_store_base_path = local_store.get_path()
CREDENTIALS_JSON_PATH = os.path.join(
    os.path.dirname(__file__), '../../credentials.json',
)
TOKEN_PICKLE_PATH = os.path.join(
    application_local_store_base_path, 'token.pickle',
)


class OAuthHandlerWindow(QWidget):
    """
    This class handles the OAuth web flow by displaying a browser window for the user to log in.
    """

    auth_code_received = Signal(str)

    def __init__(self, auth_url):
        """
        Initializes the OAuthHandlerWindow.

        :param auth_url: The URL for the OAuth authentication page.
        """
        super().__init__()
        self.auth_url = auth_url
        self.auth_code = None
        self.loop = QEventLoop()
        self.setAccessibleName(BACKUP_WINDOW)
        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.browser.load(QUrl(self.auth_url))
        self.browser.loadFinished.connect(self.handle_load_finished)
        self.auth_code_received.connect(self.handle_auth_code_received)

    def handle_load_finished(self):
        """
        Slot called when the page load is finished.
        """
        logger.info('Auth Page load finished')

    # We cannot rename closeEvent to snake_case because these methods are part of QWidget that why (pylint: disable=invalid-name).
    def closeEvent(self, event):  # pylint: disable=invalid-name
        """
        Handle the window close event.

        :param event: The close event.
        """
        logger.info('Window closed')
        self.loop.quit()
        super().closeEvent(event)

    @Slot(str)
    def handle_auth_code_received(self, auth_code):
        """
        Slot to handle received auth code.

        :param auth_code: The received auth code.
        """
        logger.info('Auth code received')
        self.auth_code = auth_code
        self.close()
        self.loop.quit()


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """
    This class handles the OAuth callback redirects.
    """

    def __init__(self, *args, app=None, **kwargs):
        self.app = app
        super().__init__(*args, **kwargs)

    # We cannot rename do_GET to snake_case because these methods are part of BaseHTTPRequestHandler that why (pylint: disable=invalid-name)..
    def do_GET(self):  # pylint: disable=invalid-name
        """
        Handle GET requests by extracting the authorization code and emitting it.
        """
        logger.info('Callback received')
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        auth_code = query_params.get('code', [None])[0]
        self.app.auth_window.auth_code_received.emit(auth_code)


def find_free_port():
    """
    Find a free port on the localhost.

    :return: A free port number.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def start_local_server(app):
    """
    Start a local server to handle the OAuth callback.

    :param app: The QApplication instance.
    :return: The port number and server instance.
    """
    port = find_free_port()
    server_address = ('localhost', port)
    server = HTTPServer(
        server_address,
        lambda *args, **kwargs: OAuthCallbackHandler(*args, app=app, **kwargs),
    )
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True  # Ensure the thread exits when the main program does
    server_thread.start()
    return port  # Unused variable 'server' is intentional


def authenticate(app):
    """
    Authenticate the user and obtain credentials for Google Drive API.

    :param app: The QApplication instance.
    :return: The Google Drive service instance if authentication is successful.
    """
    try:
        creds = None
        if os.path.exists(TOKEN_PICKLE_PATH):
            with open(TOKEN_PICKLE_PATH, 'rb') as token:
                creds = pickle.load(token)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PICKLE_PATH, 'wb') as token:
                pickle.dump(creds, token)
        elif not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_config(
                client_config, scopes=SCOPES,
            )

            port = start_local_server(app)
            redirect_uri = f'http://localhost:{port}/'
            flow.redirect_uri = redirect_uri

            auth_url, _ = flow.authorization_url(prompt='consent')

            app.auth_window = OAuthHandlerWindow(auth_url)
            app.auth_window.show()

            logger.info('Starting event loop')
            app.auth_window.loop.exec()
            logger.info('Event loop finished')

            if app.auth_window.auth_code:
                logger.info('Fetching token')
                flow.fetch_token(code=app.auth_window.auth_code)
                creds = flow.credentials

                with open(TOKEN_PICKLE_PATH, 'wb') as token:
                    pickle.dump(creds, token)
            else:
                return False

        if creds:
            service = build('drive', 'v3', credentials=creds)
            return service

        return False
    except Exception as exc:
        logger.error(
            'Exception occurred at gauth: %s, Message: %s',
            type(exc).__name__, str(exc),
        )
        return False
    finally:
        if hasattr(app, 'auth_window') and app.auth_window:
            app.auth_window.close()
