# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import,implicit-str-concat
"""This module contains the Backup class,
 which represents the UI for backup wallet.
 """
from __future__ import annotations

import os

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import BACKUP_CLOSE_BUTTON
from accessible_constant import BACKUP_NODE_DATA_BUTTON
from accessible_constant import CONFIGURE_BACKUP_BUTTON
from accessible_constant import MNEMONIC_FRAME
from accessible_constant import SHOW_MNEMONIC_BUTTON
from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import ToastPreset
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import MNEMONIC_KEY
from src.utils.error_message import ERROR_G_DRIVE_CONFIG_FAILED
from src.utils.gauth import authenticate
from src.utils.gauth import TOKEN_PICKLE_PATH
from src.utils.helpers import load_stylesheet
from src.utils.info_message import INFO_G_DRIVE_CONFIG_SUCCESS
from src.utils.keyring_storage import get_value
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.toast import ToastManager
from src.views.components.wallet_logo_frame import WalletLogoFrame
from src.views.ui_restore_mnemonic import RestoreMnemonicWidget


class Backup(QWidget):
    """This class represents all the UI elements of the backup page."""

    def __init__(self, view_model):
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.setStyleSheet(load_stylesheet('views/qss/backup_style.qss'))
        self.grid_layout_backup_page = QGridLayout(self)
        self.sidebar = None
        self.grid_layout_backup_page.setObjectName('grid_layout_backup_page')
        self.vertical_spacer_19 = QSpacerItem(
            20, 190, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout_backup_page.addItem(
            self.vertical_spacer_19, 0, 2, 1, 1,
        )

        self.wallet_logo_frame = WalletLogoFrame(self)
        self.grid_layout_backup_page.addWidget(
            self.wallet_logo_frame, 0, 0, 1, 2,
        )
        self.backup_widget = QWidget(self)
        self.backup_widget.setObjectName('backup_widget')

        self.backup_widget.setMaximumSize(QSize(499, 615))
        self.grid_layout = QGridLayout(self.backup_widget)
        self.grid_layout.setObjectName('grid_layout')
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(6)
        self.grid_layout.setContentsMargins(1, 4, 1, 10)
        self.vertical_layout_backup_wallet_widget = QVBoxLayout()
        self.vertical_layout_backup_wallet_widget.setSpacing(15)
        self.vertical_layout_backup_wallet_widget.setObjectName(
            'vertical_layout_backup_wallet_widget',
        )
        self.title_layout = QHBoxLayout()
        self.title_layout.setObjectName('title_layout')
        self.title_layout.setContentsMargins(40, 9, 40, 0)
        self.backup_title_label = QLabel(self.backup_widget)
        self.backup_title_label.setObjectName('backup_title_label')
        self.backup_title_label.setMinimumSize(QSize(415, 50))
        self.backup_title_label.setMaximumSize(QSize(16777215, 50))
        self.title_layout.addWidget(self.backup_title_label)

        self.backup_close_btn = QPushButton(self.backup_widget)
        self.backup_close_btn.setObjectName('backup_close_btn')
        self.backup_close_btn.setAccessibleName(BACKUP_CLOSE_BUTTON)
        self.backup_close_btn.setMinimumSize(QSize(24, 24))
        self.backup_close_btn.setMaximumSize(QSize(50, 65))
        self.backup_close_btn.setAutoFillBackground(False)
        close_icon = QIcon()
        close_icon.addFile(
            ':/assets/x_circle.png',
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.backup_close_btn.setIcon(close_icon)
        self.backup_close_btn.setIconSize(QSize(24, 24))
        self.backup_close_btn.setCheckable(False)
        self.backup_close_btn.setChecked(False)

        self.title_layout.addWidget(self.backup_close_btn, 0, Qt.AlignHCenter)

        self.vertical_layout_backup_wallet_widget.addLayout(self.title_layout)

        self.line_backup_widget = QFrame(self.backup_widget)
        self.line_backup_widget.setObjectName('line_backup_widget')
        self.line_backup_widget.setFrameShape(QFrame.Shape.HLine)
        self.line_backup_widget.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout_backup_wallet_widget.addWidget(
            self.line_backup_widget,
        )

        self.backup_info_text = QLabel(self.backup_widget)
        self.backup_info_text.setWordWrap(True)
        self.backup_info_text.setObjectName('backup_info_text')
        self.backup_info_text.setMinimumSize(QSize(402, 63))
        self.backup_info_text.setMaximumSize(QSize(16777215, 63))
        self.vertical_layout_backup_wallet_widget.addWidget(
            self.backup_info_text, 0, Qt.AlignHCenter,
        )

        self.show_mnemonic_frame = QFrame(self.backup_widget)
        self.show_mnemonic_frame.setObjectName('show_mnemonic_frame')

        self.show_mnemonic_frame.setMinimumSize(QSize(402, 194))
        self.show_mnemonic_frame.setMaximumSize(QSize(402, 197))

        self.show_mnemonic_frame.setFrameShape(QFrame.StyledPanel)
        self.show_mnemonic_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_1 = QVBoxLayout(self.show_mnemonic_frame)
        self.vertical_layout_1.setObjectName('vertical_layout_1')
        self.show_mnemonic_text_label = QLabel(self.show_mnemonic_frame)
        self.show_mnemonic_text_label.setWordWrap(True)
        self.show_mnemonic_text_label.setObjectName('show_mnemonic_text')
        self.show_mnemonic_text_label.setMinimumSize(QSize(354, 105))
        self.show_mnemonic_text_label.setMaximumSize(QSize(16777215, 105))

        self.vertical_layout_1.addWidget(
            self.show_mnemonic_text_label, 0, Qt.AlignHCenter,
        )

        self.show_mnemonic_button = QPushButton(self.show_mnemonic_frame)
        self.show_mnemonic_button.setObjectName('show_mnemonic_button')
        self.show_mnemonic_button.setAccessibleName(SHOW_MNEMONIC_BUTTON)
        self.show_mnemonic_button.setMinimumSize(QSize(354, 40))
        self.show_mnemonic_button.setMaximumSize(QSize(354, 40))
        self.show_mnemonic_button.setCursor(
            Qt.CursorShape.PointingHandCursor,
        )  # Set cursor to pointing hand
        self.icon3 = QIcon()
        self.icon3.addFile(
            ':/assets/show_mnemonic.png', QSize(), QIcon.Normal, QIcon.Off,
        )
        self.show_mnemonic_button.setIcon(self.icon3)

        self.vertical_layout_1.addWidget(
            self.show_mnemonic_button, 0, Qt.AlignHCenter,
        )

        self.mnemonic_frame = QFrame(self.show_mnemonic_frame)
        self.mnemonic_frame.setObjectName('mnemonic_frame')
        self.mnemonic_frame.setAccessibleName(MNEMONIC_FRAME)
        self.mnemonic_frame.setMinimumSize(QSize(354, 157))
        self.mnemonic_frame.setMaximumSize(QSize(354, 157))
        self.mnemonic_frame.setFrameShape(QFrame.StyledPanel)
        self.mnemonic_frame.setFrameShadow(QFrame.Raised)
        self.horizontal_layout_5 = QHBoxLayout(self.mnemonic_frame)
        self.horizontal_layout_5.setSpacing(6)
        self.horizontal_layout_5.setObjectName('horizontalLayout_5')
        self.mnemonic_layout_1 = QVBoxLayout()
        self.mnemonic_layout_1.setSpacing(0)
        self.mnemonic_layout_1.setObjectName('mnemonic_layout_1')
        self.mnemonic_layout_1.setContentsMargins(0, -1, -1, -1)
        self.mnemonic_text_label_1 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_1.setObjectName('mnemonic_text_label_1')
        self.mnemonic_text_label_1.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_1.addWidget(
            self.mnemonic_text_label_1, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_2 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_2.setObjectName('mnemonic_text_label_2')
        self.mnemonic_text_label_2.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_1.addWidget(
            self.mnemonic_text_label_2, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_3 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_3.setObjectName('mnemonic_text_label_3')
        self.mnemonic_text_label_3.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_1.addWidget(
            self.mnemonic_text_label_3, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_4 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_4.setObjectName('mnemonic_text_label_4')
        self.mnemonic_text_label_4.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_1.addWidget(
            self.mnemonic_text_label_4, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_5 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_5.setObjectName('mnemonic_text_label_5')
        self.mnemonic_text_label_5.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_1.addWidget(
            self.mnemonic_text_label_5, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_6 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_6.setObjectName('mnemonic_text_label_6')
        self.mnemonic_text_label_6.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_1.addWidget(
            self.mnemonic_text_label_6, 0, Qt.AlignLeft,
        )

        self.horizontal_layout_5.addLayout(self.mnemonic_layout_1)

        self.mnemonic_layout_2 = QVBoxLayout()
        self.mnemonic_layout_2.setSpacing(0)
        self.mnemonic_layout_2.setObjectName('mnemonic_layout_2')
        self.mnemonic_text_label_7 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_7.setObjectName('mnemonic_text_label_7')
        self.mnemonic_text_label_7.setStyleSheet('padding-left:16px;')

        self.mnemonic_layout_2.addWidget(
            self.mnemonic_text_label_7, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_8 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_8.setObjectName('mnemonic_text_label_8')
        self.mnemonic_text_label_8.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_2.addWidget(
            self.mnemonic_text_label_8, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_9 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_9.setObjectName('mnemonic_text_label_9')
        self.mnemonic_text_label_9.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_2.addWidget(
            self.mnemonic_text_label_9, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_10 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_10.setObjectName('mnemonic_text_label_10')
        self.mnemonic_text_label_10.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_2.addWidget(
            self.mnemonic_text_label_10, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_11 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_11.setObjectName('mnemonic_text_label_11')
        self.mnemonic_text_label_11.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_2.addWidget(
            self.mnemonic_text_label_11, 0, Qt.AlignLeft,
        )

        self.mnemonic_text_label_12 = QLabel(self.mnemonic_frame)
        self.mnemonic_text_label_12.setObjectName('mnemonic_text_label_12')
        self.mnemonic_text_label_12.setStyleSheet('padding-left:16px')

        self.mnemonic_layout_2.addWidget(
            self.mnemonic_text_label_12, 0, Qt.AlignLeft,
        )

        self.horizontal_layout_5.addLayout(self.mnemonic_layout_2)

        self.vertical_layout_1.addWidget(
            self.mnemonic_frame, 0, Qt.AlignHCenter,
        )
        self.mnemonic_frame.hide()

        self.vertical_layout_backup_wallet_widget.addWidget(
            self.show_mnemonic_frame, 0, Qt.AlignHCenter,
        )

        self.configure_backup_frame = QFrame(self.backup_widget)
        self.configure_backup_frame.setObjectName('configure_backup_frame')
        self.configure_backup_frame.setMinimumSize(QSize(402, 190))
        self.configure_backup_frame.setMaximumSize(QSize(402, 190))

        self.configure_backup_frame.setFrameShape(QFrame.StyledPanel)
        self.configure_backup_frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_2 = QVBoxLayout(self.configure_backup_frame)
        self.vertical_layout_2.setObjectName('vertical_layout_2')
        self.configure_backup_text = QLabel(
            self.configure_backup_frame,
        )
        self.configure_backup_text.setWordWrap(True)
        self.configure_backup_text.setObjectName('configure_backup_text')
        self.configure_backup_text.setMinimumSize(QSize(360, 0))
        self.configure_backup_text.setMaximumSize(QSize(360, 105))

        self.vertical_layout_2.addWidget(
            self.configure_backup_text, 0, Qt.AlignHCenter,
        )

        self.configure_backup_button = QPushButton(self.configure_backup_frame)
        self.configure_backup_button.setAccessibleName(CONFIGURE_BACKUP_BUTTON)
        self.configure_backup_button.setObjectName('configure_backup_button')
        self.configure_backup_button.setMinimumSize(QSize(354, 40))
        self.configure_backup_button.setMaximumSize(QSize(354, 40))
        self.configure_backup_button.setCursor(
            Qt.CursorShape.PointingHandCursor,
        )  # Set cursor to pointing hand

        icon4 = QIcon()
        icon4.addFile(
            ':/assets/configure_backup.png',
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.configure_backup_button.setIcon(icon4)

        self.vertical_layout_2.addWidget(
            self.configure_backup_button, 0, Qt.AlignHCenter,
        )

        self.back_node_data_button = PrimaryButton()
        self.back_node_data_button.setObjectName('back_node_data_button')
        self.back_node_data_button.setAccessibleName(BACKUP_NODE_DATA_BUTTON)
        self.back_node_data_button.setMinimumSize(QSize(354, 40))
        self.back_node_data_button.setMaximumSize(QSize(354, 40))
        self.back_node_data_button.setCursor(
            Qt.CursorShape.PointingHandCursor,
        )  # Set cursor to pointing hand

        self.vertical_layout_2.addWidget(
            self.back_node_data_button, 0, Qt.AlignHCenter,
        )

        self.vertical_layout_backup_wallet_widget.addWidget(
            self.configure_backup_frame, 0, Qt.AlignHCenter,
        )

        self.vertical_spacer_backup = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_backup_wallet_widget.addItem(
            self.vertical_spacer_backup,
        )

        self.grid_layout.addLayout(
            self.vertical_layout_backup_wallet_widget, 0, 0, 1, 1,
        )

        self.grid_layout_backup_page.addWidget(self.backup_widget, 1, 1, 2, 2)

        self.horizontal_spacer_12 = QSpacerItem(
            265, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout_backup_page.addItem(
            self.horizontal_spacer_12, 1, 3, 1, 1,
        )

        self.horizontal_spacer_11 = QSpacerItem(
            266, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.grid_layout_backup_page.addItem(
            self.horizontal_spacer_11, 2, 0, 1, 1,
        )

        self.vertical_spacer_20 = QSpacerItem(
            20, 190, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.grid_layout_backup_page.addItem(
            self.vertical_spacer_20, 3, 1, 1, 1,
        )

        self.retranslate_ui()
        self.is_already_configured()

    def retranslate_ui(self):
        """Retranslate ui"""
        self.hide_mnemonic_text = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'hide_mnemonic', None,
        )
        self.show_mnemonic_text = QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'show_mnemonic', None,
        )
        self.backup_title_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'backup', None,
            ),
        )
        self.backup_info_text.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'backup_info',
                None,
            ),
        )
        self.show_mnemonic_text_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'mnemonic_info',
                None,
            ),
        )
        self.show_mnemonic_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'show_mnemonic', None,
            ),
        )
        self.configure_backup_text.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'configure_backup_info',
                None,
            ),
        )
        self.configure_backup_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'configure_backup', 'Configure Backup',
            ),
        )

        self.back_node_data_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'take_backup', 'Backup node data',
            ),
        )

        self.setup_ui_connection()
        self.set_mnemonic_visibility()

    def setup_ui_connection(self):
        """Set up connections for UI elements."""
        self.show_mnemonic_button.clicked.connect(
            self.handle_mnemonic_visibility,
        )
        self.configure_backup_button.clicked.connect(self.configure_backup)
        self.backup_close_btn.clicked.connect(self.close_button_navigation)
        self.back_node_data_button.clicked.connect(self.backup_data)
        self._view_model.backup_view_model.is_loading.connect(
            self.update_loading_state,
        )

    def close_button_navigation(self):
        """
        Navigate to the specified page when the close button is clicked.
        """
        self.sidebar = self._view_model.page_navigation.sidebar()
        originating_page = self.get_checked_button_translation_key(
            self.sidebar,
        )

        navigation_map = {
            'fungibles': self._view_model.page_navigation.fungibles_asset_page,
            'NIA': self._view_model.page_navigation.fungibles_asset_page,
            'CFA': self._view_model.page_navigation.collectibles_asset_page,
            'create_invoice': self._view_model.page_navigation.fungibles_asset_page,
            'channel_management': self._view_model.page_navigation.channel_management_page,
            'collectibles': self._view_model.page_navigation.collectibles_asset_page,
            'faucets': self._view_model.page_navigation.faucets_page,
            'view_unspent_list': self._view_model.page_navigation.view_unspent_list_page,
            'help': self._view_model.page_navigation.help_page,
            'settings': self._view_model.page_navigation.settings_page,
            'backup': self._view_model.page_navigation.backup_page,
            'about': self._view_model.page_navigation.about_page,
        }
        backup_navigate = navigation_map.get(originating_page)
        if backup_navigate:
            backup_navigate()
        else:
            ToastManager.show_toast(
                parent=self,
                preset=ToastPreset.ERROR,
                description=f"""No navigation defined for {
                    originating_page
                }""",
            )

    def handle_mnemonic_visibility(self):
        """
        Handles the visibility of the mnemonic and toggles the button text and icon accordingly.
        """
        show_mnemonic_text_val = QApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'show_mnemonic', 'Show Mnemonic',
        )
        if self.show_mnemonic_button.text() == show_mnemonic_text_val:
            network: NetworkEnumModel = SettingRepository.get_wallet_network()
            mnemonic_string: str = get_value(MNEMONIC_KEY, network.value)
            mnemonic_array: list[str] = mnemonic_string.split()
            for i, mnemonic in enumerate(mnemonic_array, start=1):
                label_name = f'mnemonic_text_label_{i}'
                label = getattr(self, label_name)
                format_value = f'{i}. {mnemonic}'
                label.setText(format_value)
            self.show_mnemonic_widget()
            self.show_mnemonic_button.setText(self.hide_mnemonic_text)
            icon4 = QIcon()
            icon4.addFile(
                ':/assets/hide_mnemonic.png', QSize(), QIcon.Normal, QIcon.Off,
            )
            self.show_mnemonic_button.setIcon(icon4)
        else:
            self.hide_mnemonic_widget()
            self.show_mnemonic_button.setText(self.show_mnemonic_text)
            self.show_mnemonic_button.setIcon(self.icon3)

    def show_mnemonic_widget(self):
        """
        Shows the mnemonic widget and adjusts the layout.
        """
        self.mnemonic_frame.show()
        self.grid_layout_backup_page.addWidget(
            self.wallet_logo_frame, 0, 0, 1, 1,
        )
        self.backup_widget.setMinimumSize(QSize(499, 808))
        self.backup_widget.setMaximumSize(QSize(499, 808))
        self.show_mnemonic_frame.setMinimumSize(QSize(402, 370))
        self.show_mnemonic_frame.setMaximumSize(QSize(402, 370))

    def hide_mnemonic_widget(self):
        """
        Hides the mnemonic widget and adjusts the layout.
        """
        self.mnemonic_frame.hide()
        self.backup_widget.setMinimumSize(QSize(499, 608))
        self.backup_widget.setMaximumSize(QSize(499, 615))
        self.show_mnemonic_frame.setMinimumSize(QSize(402, 194))
        self.show_mnemonic_frame.setMaximumSize(QSize(402, 197))
        self.grid_layout_backup_page.addWidget(
            self.wallet_logo_frame, 0, 0, 1, 2,
        )

    def configure_backup(self):
        """
        Configures the backup and updates the button state and appearance based on the configuration status.
        """
        response = authenticate(QApplication.instance())
        if response is False:
            ToastManager.show_toast(
                parent=self, preset=ToastPreset.ERROR,
                description=ERROR_G_DRIVE_CONFIG_FAILED,
            )
        else:
            SettingRepository.set_backup_configured(True)
            self.configure_backup_button.hide()
            self.back_node_data_button.show()
            ToastManager.show_toast(
                parent=self,
                preset=ToastPreset.SUCCESS,
                description=INFO_G_DRIVE_CONFIG_SUCCESS,
            )

    def is_already_configured(self):
        """
        Checks if the Google Drive configuration is already done.
        Disables the configure_backup_button and updates its appearance accordingly.
        """
        if os.path.exists(TOKEN_PICKLE_PATH):
            self.back_node_data_button.show()
            self.configure_backup_button.hide()
        else:
            self.configure_backup_button.show()
            self.back_node_data_button.hide()

    def backup_data(self):
        """Call back handler on backup_node_data_button emit"""
        keyring_status = SettingRepository.get_keyring_status()
        if keyring_status:
            # when keyring disable it open dialog to take mnemonic and password from user
            mnemonic_dialog = RestoreMnemonicWidget(
                view_model=self._view_model, origin_page='backup_page',
            )
            mnemonic_dialog.exec()
        else:
            self._view_model.backup_view_model.backup()

    def update_loading_state(self, is_loading: bool):
        """
        Updates the loading state of the backup_node_data object.
        """
        if is_loading:
            self.back_node_data_button.start_loading()
        else:
            self.back_node_data_button.stop_loading()

    def set_mnemonic_visibility(self):
        """
        Sets the visibility of the mnemonic frame based on the keyring status.

        If keyring storage is disabled (stored as True), the mnemonic frame is hidden.
        """
        stored_keyring_status = SettingRepository.get_keyring_status()
        if stored_keyring_status is True:
            self.show_mnemonic_frame.hide()

    def get_checked_button_translation_key(self, sidebar):
        """
        Get the translation key of the checked sidebar button.
        """
        buttons = [
            sidebar.backup,
            sidebar.help,
            sidebar.view_unspent_list,
            sidebar.faucet,
            sidebar.channel_management,
            sidebar.my_fungibles,
            sidebar.my_collectibles,
            sidebar.settings,
            sidebar.about,
        ]
        for button in buttons:
            if button.isChecked():
                return button.get_translation_key()
        return None
