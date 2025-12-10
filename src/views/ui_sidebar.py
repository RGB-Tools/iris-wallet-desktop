# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the Sidebar class,
which represents the UI for application Sidebar.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import ABOUT_BUTTON
from accessible_constant import BACKUP_BUTTON
from accessible_constant import CHANNEL_MANAGEMENT_BUTTON
from accessible_constant import COLLECTIBLE_BUTTON
from accessible_constant import FAUCET_BUTTON
from accessible_constant import FUNGIBLE_BUTTON
from accessible_constant import HELP_BUTTON
from accessible_constant import SETTINGS_BUTTON
from accessible_constant import SIDEBAR_RECEIVE_ASSET_BUTTON
from accessible_constant import VIEW_UNSPENT_LIST_BUTTON
from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.model.selection_page_model import AssetDataModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.buttons import SidebarButton


class Sidebar(QWidget):
    """This class represents all the UI elements of the sidebar."""

    def __init__(self, view_model):
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.setObjectName('sidebar')
        self.setMinimumSize(QSize(360, 720))
        self.setStyleSheet(
            'background-color: rgb(3, 11, 37);\n'
            'color: rgb(255, 255, 255);\n'
            'border: 0px solid white;\n'
            'font: 8px"Inter"\n',
        )
        self.vertical_layout_1 = QVBoxLayout(self)
        self.vertical_layout_1.setSpacing(6)
        self.vertical_layout_1.setObjectName('vertical_layout_1')
        self.vertical_layout_1.setContentsMargins(9, -1, 9, 25)
        self.iris_wallet = QHBoxLayout()
        self.iris_wallet.setObjectName('iris_wallet')
        self.iris_wallet.setContentsMargins(9, -1, -1, -1)
        self.frame = QFrame(self)
        self.frame.setObjectName('frame')
        self.frame.setMinimumSize(QSize(32, 32))
        self.frame.setMaximumSize(QSize(50, 50))
        self.frame.setStyleSheet('image: url(:/assets/iris_logo.png);')
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.iris_wallet.addWidget(self.frame)

        self.iris_wallet_text = QLabel(self)
        self.iris_wallet_text.setObjectName('iris_wallet_text')
        self.iris_wallet_text.setMinimumSize(QSize(296, 60))
        self.iris_wallet_text.setStyleSheet(
            'font: 16px;\n'
            'margin-top: 10px;\n'
            'margin-bottom: 10px;\n'
            'font-weight: bold;\n'
            '',
        )

        self.iris_wallet.addWidget(self.iris_wallet_text)

        self.vertical_layout_1.addLayout(self.iris_wallet)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName('verticalLayout')
        self.grid_layout_sidebar = QGridLayout()
        self.grid_layout_sidebar.setSpacing(6)
        self.grid_layout_sidebar.setObjectName('gridLayout')
        self.grid_layout_sidebar.setContentsMargins(10, 5, 10, 5)
        self.backup = SidebarButton(
            'Backup', ':/assets/backup.png', translation_key='backup',
        )
        self.backup.setAccessibleName(BACKUP_BUTTON)
        self.backup.setCheckable(False)
        self.grid_layout_sidebar.addWidget(self.backup, 6, 0, 1, 1)

        self.help = SidebarButton(
            'Help', ':/assets/question_circle', translation_key='help',
        )
        self.help.setAccessibleName(HELP_BUTTON)
        self.grid_layout_sidebar.addWidget(self.help, 8, 0, 1, 1)

        self.view_unspent_list = SidebarButton(
            'View unspent list',
            ':/assets/view_unspent_list.png', translation_key='view_unspent_list',
        )
        self.view_unspent_list.setAccessibleName(VIEW_UNSPENT_LIST_BUTTON)
        self.grid_layout_sidebar.addWidget(self.view_unspent_list, 3, 0, 1, 1)

        self.faucet = SidebarButton(
            'Faucet', ':/assets/faucets.png', translation_key='faucets',
        )
        self.faucet.setAccessibleName(FAUCET_BUTTON)
        self.grid_layout_sidebar.addWidget(self.faucet, 5, 0, 1, 1)

        self.channel_management = SidebarButton(
            'Channel management',
            ':/assets/channel_management.png',
            translation_key='channel_management',
        )
        self.channel_management.setAccessibleName(CHANNEL_MANAGEMENT_BUTTON)
        self.grid_layout_sidebar.addWidget(self.channel_management, 2, 0, 1, 1)

        self.my_fungibles = SidebarButton(
            'My Fungibles', ':/assets/my_asset.png', translation_key='fungibles',
        )
        self.my_fungibles.setAccessibleName(FUNGIBLE_BUTTON)
        self.my_fungibles.setChecked(True)

        self.grid_layout_sidebar.addWidget(self.my_fungibles, 0, 0, 1, 1)

        self.my_collectibles = SidebarButton(
            'My Assets', ':/assets/my_asset.png', translation_key='collectibles',
        )
        self.my_collectibles.setAccessibleName(COLLECTIBLE_BUTTON)
        self.grid_layout_sidebar.addWidget(self.my_collectibles, 1, 0, 1, 1)

        self.settings = SidebarButton(
            'Settings', ':/assets/settings.png', translation_key='settings',
        )
        self.settings.setAccessibleName(SETTINGS_BUTTON)
        self.grid_layout_sidebar.addWidget(self.settings, 7, 0, 1, 1)

        self.about = SidebarButton(
            'About', ':/assets/about.png', translation_key='about',
        )
        self.about.setAccessibleName(ABOUT_BUTTON)
        self.grid_layout_sidebar.addWidget(self.about, 9, 0, 1, 1)

        self.vertical_layout.addLayout(self.grid_layout_sidebar)

        self.vertical_spacer = QSpacerItem(
            20,
            40,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout.addItem(self.vertical_spacer)

        self.vertical_layout_1.addLayout(self.vertical_layout)
        self.receive_asset_button = PrimaryButton()
        self.receive_asset_button.setAccessibleName(
            SIDEBAR_RECEIVE_ASSET_BUTTON,
        )
        self.receive_asset_button.setMinimumSize(QSize(335, 40))
        self.receive_asset_button.setMaximumSize(QSize(335, 40))
        self.vertical_layout.addWidget(
            self.receive_asset_button, 0, Qt.AlignCenter,
        )
        self.retranslate_ui()
        self.setup_ui_connections()

    def setup_ui_connections(self):
        """Set up connections for UI elements."""
        self.channel_management.clicked.connect(
            self._view_model.page_navigation.channel_management_page,
        )
        self.my_fungibles.clicked.connect(
            self._view_model.page_navigation.fungibles_asset_page,
        )
        self.my_collectibles.clicked.connect(
            self._view_model.page_navigation.collectibles_asset_page,
        )
        self.view_unspent_list.clicked.connect(
            self._view_model.page_navigation.view_unspent_list_page,
        )
        self.backup.clicked.connect(
            self._view_model.page_navigation.backup_page,
        )
        self.settings.clicked.connect(
            self._view_model.page_navigation.settings_page,
        )
        self.about.clicked.connect(
            self._view_model.page_navigation.about_page,
        )
        self.faucet.clicked.connect(
            self._view_model.page_navigation.faucets_page,
        )
        self.help.clicked.connect(self._view_model.page_navigation.help_page)
        self.receive_asset_button.clicked.connect(
            lambda: self._view_model.page_navigation.receive_cfa_page(
                params=AssetDataModel(
                    asset_type=self.get_checked_button_translation_key(),
                ),
            ),
        )

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.network = SettingRepository.get_wallet_network().value
        if self.network == NetworkEnumModel.MAINNET.value:
            self.iris_wallet_text.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'iris_wallet', None,
                ),
            )
        else:
            self.iris_wallet_text.setText(
                f'{QCoreApplication.translate(IRIS_WALLET_TRANSLATIONS_CONTEXT, "iris_wallet", None)} {
                    self.network.capitalize()
                }',
            )
        self.receive_asset_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'receive_assets',
                None,
            ),
        )

    def get_checked_button_translation_key(self):
        """
        Get the translation key of the checked sidebar button.
        """
        buttons = [
            self.backup,
            self.help,
            self.view_unspent_list,
            self.faucet,
            self.channel_management,
            self.my_fungibles,
            self.my_collectibles,
            self.settings,
            self.about,
        ]
        for button in buttons:
            if button.isChecked():
                return button.get_translation_key()
        return None
