"""
Module for handling the OnCloseDialogBox, which manages the closing process of application
"""
# pylint: disable=E1121,too-many-instance-attributes
from __future__ import annotations

from PySide6.QtCore import QProcess
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QVBoxLayout

from src.data.repository.setting_repository import SettingRepository
from src.data.service.backup_service import BackupService
from src.model.enums.enums_model import NetworkEnumModel
from src.utils.constant import MAX_ATTEMPTS_FOR_CLOSE
from src.utils.constant import MNEMONIC_KEY
from src.utils.constant import NODE_CLOSE_INTERVAL
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.error_message import ERROR_UNABLE_TO_STOP_NODE
from src.utils.keyring_storage import get_value
from src.utils.ln_node_manage import LnNodeServerManager
from src.utils.logging import logger
from src.utils.worker import ThreadManager
from src.viewmodels.header_frame_view_model import HeaderFrameViewModel
from src.views.ui_restore_mnemonic import RestoreMnemonicWidget


class OnCloseDialogBox(QDialog, ThreadManager):
    """
    A dialog box that appears when the application is being closed. It manages the backup process
    and the closing of the Lightning Node server, displaying appropriate status messages and
    handling errors that may occur during these operations.
    """

    def __init__(self, parent=None):
        """
        Initialize the OnCloseDialogBox with the parent widget, setting up the layout, status labels,
        and connecting signals for the Lightning Node server manager.

        Args:
            parent (QWidget): The parent widget for this dialog.
        """
        super().__init__(parent)
        self.dialog_title = 'Please wait for backup or close node'
        self.qmessage_question = 'Are you sure you want to close while the backup is in progress?'
        self.qmessage_info = 'The backup process has been completed successfully!'
        self.is_node_closing_onprogress = False
        self.is_backup_onprogress = False
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ln_node_manage: LnNodeServerManager = LnNodeServerManager.get_instance()
        self.ln_node_manage.process_finished_on_request_app_close.connect(
            self._on_success_close_node,
        )
        self.ln_node_manage.process_finished_on_request_app_close_error.connect(
            self._on_error_of_closing_node,
        )
        self.header_frame_view_model = HeaderFrameViewModel()

        # Set minimum size for flexibility but still prevent excessive resizing
        self.setMinimumSize(200, 200)

        # Set the window title and remove the close button from the title bar
        self.setWindowTitle(self.dialog_title)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Add a loading GIF to the center
        self.loading_label = QLabel(self)
        # Replace with your loading GIF path
        self.loading_movie = QMovie(':assets/loading.gif')
        self.loading_movie.setScaledSize(
            QSize(100, 100),
        )  # Adjust size as needed
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loading_label)

        # Add a label to show status updates
        self.status_label = QLabel('Starting backup...')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
                                        color: white;
                                        font-weight:500
                                        """)
        # Enable word wrap to handle long status text
        self.status_label.setWordWrap(True)
        # Limit the height to prevent excessive expansion
        self.status_label.setMaximumHeight(90)
        layout.addWidget(self.status_label)

        # Start the GIF animation
        self.loading_movie.start()

        # Set the layout for the dialog
        self.setLayout(layout)

    def _update_status(self, status):
        """
        Update the status label with the provided status message.

        Args:
            status (str): The status message to display.
        """
        self.status_label.setText(status)

    def _start_process(self, is_backup_require: bool):
        """
        Start the backup or node shutdown process based on the given condition.

        Args:
            is_backup_require (bool): Whether a backup process is required before shutting down the node.
        """
        self._update_status('Process started...')
        if is_backup_require:
            logger.info('Backup called')
            keyring_status: bool = SettingRepository.get_keyring_status()
            if keyring_status:
                mnemonic_dialog = RestoreMnemonicWidget(origin_page='on_close')
                mnemonic_dialog.on_continue.connect(self._start_backup)
                mnemonic_dialog.cancel_button.clicked.connect(
                    self._close_node_app,
                )
                mnemonic_dialog.exec()
            else:
                network: NetworkEnumModel = SettingRepository.get_wallet_network()
                mnemonic: str = get_value(MNEMONIC_KEY, network.value)
                password: str = get_value(
                    key=WALLET_PASSWORD_KEY,
                    network=network.value,
                )
                self._start_backup(mnemonic, password)
        else:
            self._close_node_app()

    def exec(self, is_backup_require: bool = False):
        """
        Override the exec method to run a method when the dialog is executed.
        Args:
            is_backup_require (bool): Whether a backup process is required before shutting down the node.
        """
        self._start_process(is_backup_require)
        return super().exec()

    def _start_backup(self, mnemonic: str, password: str):
        """
        Start the backup process, updating the status and running the backup in a separate thread.
        """
        self._update_status('Backup process started')
        self.is_backup_onprogress = True
        self.run_in_thread(
            BackupService.backup, {
                'args': [mnemonic, password],
                'callback': self._on_success_of_backup,
                'error_callback': self._on_error_of_backup,
            },
        )

    def _on_success_of_backup(self):
        """
        Handle the successful completion of the backup process, updating the status and proceeding to close the node.
        """
        self.is_backup_onprogress = False
        self._update_status('Backup process finished')
        self._close_node_app()

    def _on_error_of_backup(self):
        """
        Handle any errors that occur during the backup process, updating the status and showing an error message.

        Args:
            error (Exception): The exception that occurred during the backup process.
        """
        self.is_backup_onprogress = False
        self._update_status('Something went wrong during the backup')
        self.qmessage_info = ERROR_SOMETHING_WENT_WRONG
        QMessageBox.critical(self, 'Failed', self.qmessage_info)
        self._close_node_app()

    def _on_error_of_closing_node(self):
        """
        Handle errors that occur during the node closing process, updating the status and quitting the application.
        """
        self.is_node_closing_onprogress = False
        self._update_status(ERROR_UNABLE_TO_STOP_NODE)
        self.qmessage_info = ERROR_UNABLE_TO_STOP_NODE
        QMessageBox.critical(self, 'Failed', self.qmessage_info)
        QApplication.instance().exit()

    def _on_success_close_node(self):
        """
        Handle the successful closure of the node, updating the status and quitting the application.
        """
        self.is_node_closing_onprogress = False
        self._update_status('The node closed successfully!')
        self.header_frame_view_model.stop_network_checker()
        QApplication.instance().exit()

    def _close_node_app(self):
        """
        Initiate the process of closing the Lightning Node application. If the node is still running,
        start the closing process and update the status. If the node is not running, quit the application.
        """
        self.is_backup_onprogress = False
        if self.ln_node_manage.process.state() == QProcess.Running:
            self.is_node_closing_onprogress = True
            self._update_status(
                f'Node closing process started. It may take up to {
                    MAX_ATTEMPTS_FOR_CLOSE * NODE_CLOSE_INTERVAL
                } seconds',
            )
            self.dialog_title = 'Node closing in progress'
            self.ln_node_manage.stop_server_from_close_button()
        else:
            self.header_frame_view_model.stop_network_checker()
            QApplication.instance().exit()

    # pylint disable(invalid-name) because of closeEvent is internal function of QWidget
    def closeEvent(self, event):  # pylint:disable=invalid-name
        """
        Handle the close event for the dialog. If a backup or node closing is in progress, show a confirmation
        message and manage the close process accordingly.

        Args:
            event (QCloseEvent): The close event that triggered this method.
        """
        if self.is_backup_onprogress:
            reply = QMessageBox.question(
                self, 'Confirmation', self.qmessage_question,
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                event.accept()  # Close the dialog
                self._close_node_app()
            else:
                event.ignore()  # Ignore the close event
        elif self.is_node_closing_onprogress:
            event.ignore()
            self._update_status(
                f'Please wait until the node closes. It may take up to {
                    MAX_ATTEMPTS_FOR_CLOSE * NODE_CLOSE_INTERVAL
                } seconds',
            )
        else:
            event.accept()
            QApplication.instance().exit()
