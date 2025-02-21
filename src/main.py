"""
main.py
=======

Description:
------------
This is the entry point of the application.
"""
# pylint: disable=unused-import, broad-except
from __future__ import annotations

import signal
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QGraphicsBlurEffect
from PySide6.QtWidgets import QMainWindow

import src.resources_rc  # noqa: F401
import src.utils.bootstrap
from src.data.repository.setting_repository import SettingRepository
from src.flavour import __network__
from src.model.enums.enums_model import WalletType
from src.model.setting_model import IsBackupConfiguredModel
from src.model.setting_model import IsWalletInitialized
from src.utils.cache import Cache
from src.utils.common_utils import load_translator
from src.utils.common_utils import sigterm_handler
from src.utils.excluded_page import excluded_page
from src.utils.helpers import check_google_auth_token_available
from src.utils.ln_node_manage import LnNodeServerManager
from src.utils.logging import logger
from src.utils.page_navigation import PageNavigation
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.custom_toast import ToasterManager
from src.views.components.message_box import MessageBox
from src.views.components.on_close_progress_dialog import OnCloseDialogBox
from src.views.main_window import MainWindow
from src.views.ui_backup_configure_dialog import BackupConfigureDialog
PAGE_NAVIGATION: PageNavigation  # To make navigation global


class IrisWalletMainWindow(QMainWindow):
    """This class represents the main window of the application."""

    def __init__(self):
        super().__init__()
        self.__init_ui__()
        self.progress_dialog = None
        self.ln_node_manager = LnNodeServerManager.get_instance()

    def __init_ui__(self):
        """This method initializes the main window UI of the application."""
        self.ui_ = MainWindow()
        self.ui_.setup_ui(self)
        ToasterManager.set_main_window(self.ui_.main_window)

    def resizeEvent(self, event):  # pylint:disable=invalid-name
        """Handle window resize and trigger toaster repositioning."""
        ToasterManager.reposition_toasters()
        super().resizeEvent(event)

    # pylint disable(invalid-name) because of closeEvent is internal function of QWidget
    def closeEvent(self, event):  # pylint:disable=invalid-name
        """This method is called when the window is about to close."""
        # Show the progress dialog and perform the backup
        page_name = PAGE_NAVIGATION.current_stack['name']
        cache = Cache.get_cache_session()
        if cache is not None:
            cache.invalidate_cache()
        wallet_type: WalletType = SettingRepository.get_wallet_type()
        if wallet_type.value == WalletType.REMOTE_TYPE_WALLET.value or page_name in excluded_page:
            QApplication.instance().exit()
        else:
            self.show_backup_progress()
            # Ignore the close event until the backup is complete
            event.ignore()

    def show_backup_progress(self):
        """This method shows a custom progress dialog while performing the backup."""
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        backup_configure_status: IsBackupConfiguredModel = SettingRepository.is_backup_configured()
        self.progress_dialog = OnCloseDialogBox(self)
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)
        page_name = PAGE_NAVIGATION.current_stack['name']
        if backup_configure_status.is_backup_configured and page_name not in ['EnterWalletPassword', 'SetWalletPassword']:
            response = check_google_auth_token_available()
            if not response:
                backup_configure_dialog_box = BackupConfigureDialog(
                    PAGE_NAVIGATION,
                )
                backup_configure_dialog_box.exec()
            else:
                self.progress_dialog.exec(True)
        self.progress_dialog.exec()


def main():
    """This method is the entry point of the application."""
    try:
        global PAGE_NAVIGATION
        app = QApplication(sys.argv)
        translator = load_translator()
        app.installTranslator(translator)
        view = IrisWalletMainWindow()
        # Initialize PageNavigation
        PAGE_NAVIGATION = PageNavigation(view.ui_)
        # Initialize MainViewModel with PageNavigation
        main_view_model = MainViewModel(PAGE_NAVIGATION)
        # Set view model in your MainWindow instance
        view.ui_.set_ui_and_model(main_view_model)
        signal.signal(signal.SIGTERM, sigterm_handler)
        wallet: IsWalletInitialized = SettingRepository.is_wallet_initialized()
        if wallet.is_wallet_initialized:
            PAGE_NAVIGATION.splash_screen_page()
        else:
            PAGE_NAVIGATION.term_and_condition_page()
        view.show()
        sys.exit(app.exec())
    except Exception as exc:
        logger.error(
            'Exception occurred during application up: %s, Message: %s', type(
                exc,
            ).__name__, str(exc),
        )
        error_message = str(exc)
        MessageBox('critical', error_message)
        sys.exit(1)


if __name__ == '__main__':
    main()
