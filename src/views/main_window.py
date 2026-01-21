# pylint:disable = too-many-instance-attributes
"""This module contains the MainWindow class,
which represents the main window of the application.
"""
from __future__ import annotations

from PySide6.QtCore import QMetaObject
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QWidget

from src.data.repository.setting_repository import SettingRepository
from src.flavour import __app_name_suffix__
from src.model.enums.enums_model import LoaderDisplayModel
from src.model.enums.enums_model import NetworkEnumModel
from src.utils.helpers import load_stylesheet
from src.utils.ln_node_manage import LnNodeServerManager
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.loading_screen import LoadingTranslucentScreen
from src.views.ui_sidebar import Sidebar


class MainWindow:
    """This class represents all the UI elements of the main window page."""

    def __init__(self):
        """Initialize the MainWindow class."""
        self.view_model: MainViewModel
        self.sidebar: Sidebar
        self.main_window: QMainWindow
        self.central_widget: QWidget
        self.grid_layout_main: QGridLayout
        self.horizontal_layout: QHBoxLayout
        self.stacked_widget: QStackedWidget
        self._loading_translucent_screen = None
        self.network: NetworkEnumModel = SettingRepository.get_wallet_network()
        self.ln_node_server_manager = LnNodeServerManager().get_instance()

    def set_ui_and_model(self, view_model: MainViewModel):
        """Set the UI and view model."""
        self.view_model = view_model
        self.sidebar = Sidebar(self.view_model)
        self.horizontal_layout.addWidget(self.sidebar)
        self.horizontal_layout.addWidget(self.stacked_widget)
        self.grid_layout_main.addLayout(self.horizontal_layout, 0, 0, 1, 1)
        self.view_model.splash_view_model.show_main_window_loader.connect(
            self.show_main_window_loading_screen,
        )
        self.ln_node_server_manager.main_window_loader.connect(
            self.show_main_window_loading_screen,
        )
        self.view_model.splash_view_model.load_wallet_transfer_selection_view_model(
            # This ensures that the splash view consistently uses the same instance throughout the application, preventing abnormal behavior.
            self.view_model.wallet_transfer_selection_view_model,
        )

    def setup_ui(self, main_window: QMainWindow):
        """Set up the UI elements."""
        self.main_window = main_window
        if not self.main_window.objectName():
            self.main_window.setObjectName('main_window')
        self.main_window.resize(1000, 800)
        self.main_window.setStyleSheet(load_stylesheet())
        self.central_widget = QWidget(self.main_window)
        self.central_widget.setObjectName('central_widget')
        self.grid_layout_main = QGridLayout(self.central_widget)
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setObjectName('grid_layout_main')
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setSpacing(0)
        self.horizontal_layout.setObjectName('horizontal_layout')
        # Stacked widget
        self.stacked_widget = QStackedWidget(self.central_widget)
        self.stacked_widget.setObjectName('stacked_widget')
        self.stacked_widget.setMinimumSize(QSize(1172, 900))
        self.main_window.setCentralWidget(self.central_widget)
        self.retranslate_ui()
        QMetaObject.connectSlotsByName(self.main_window)

    def show_main_window_loading_screen(self, loading_status: bool, loader_description: str):
        """Handles showing or hiding the loading screen on the main window."""
        current_widget = self.stacked_widget.currentWidget().objectName()
        if current_widget == 'splash_page':
            return

        if loading_status:
            self._loading_translucent_screen = LoadingTranslucentScreen(
                parent=self.main_window,
                description_text=loader_description,
                loader_type=LoaderDisplayModel.FULL_SCREEN,
            )
            self._loading_translucent_screen.start()
            self._loading_translucent_screen.make_parent_disabled_during_loading(
                True,
            )
        else:
            if hasattr(self, '_loading_translucent_screen') and self._loading_translucent_screen:
                self._loading_translucent_screen.stop()
                self._loading_translucent_screen.make_parent_disabled_during_loading(
                    False,
                )

    def retranslate_ui(self):
        """Retranslate all the UI contents."""
        app_title = f'Iris Wallet {self.network.value.capitalize()}'
        if __app_name_suffix__ is not None:
            app_title = f'Iris Wallet {self.network.value.capitalize()} {
                __app_name_suffix__
            }'
        self.main_window.setWindowTitle(
            app_title,
        )

    def set_app_icon(self):
        """This method set the wallet icon according to the network"""
        app_icon = None
        network: NetworkEnumModel = SettingRepository.get_wallet_network()
        if network.value == NetworkEnumModel.REGTEST.value:
            app_icon = QIcon(':/assets/icons/regtest-icon.ico')
        if network.value == NetworkEnumModel.TESTNET.value:
            app_icon = QIcon(':/assets/icons/testnet-icon.ico')
        if network.value == NetworkEnumModel.TESTNET4.value:
            app_icon = QIcon(':/assets/icons/testnet-icon.ico')
        if network.value == NetworkEnumModel.MAINNET.value:
            app_icon = QIcon(':/assets/icons/mainnet-icon.ico')
        self.main_window.setWindowIcon(app_icon)
