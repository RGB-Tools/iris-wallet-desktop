# pylint: disable=too-many-instance-attributes, too-many-statements
"""This module contains the HeaderFrame class,
which represents the component for header frame.
"""
from __future__ import annotations

import os

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QObject
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout

from accessible_constant import NETWORK_AND_BACKUP_FRAME
from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel
from src.model.enums.enums_model import WalletType
from src.model.setting_model import IsBackupConfiguredModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.gauth import TOKEN_PICKLE_PATH
from src.utils.helpers import load_stylesheet
from src.utils.page_navigation_events import PageNavigationEventManager
from src.viewmodels.header_frame_view_model import HeaderFrameViewModel


class HeaderFrame(QFrame, QObject):
    """
    HeaderFrame creates a header frame with a logo and title text.
    This frame also has a specific size and background style.

    :param title_name: The text to display as the title.
    :param title_logo_path: Path to the logo image to display next to the title.
    """

    def __init__(self, title_name: str, title_logo_path: str):
        """
        Initializes the HeaderFrame with a title and a logo.

        :param title_name: The title text to display.
        :param title_logo_path: Path to the image file for the logo.
        """
        super().__init__()
        self.title = title_name
        self.is_backup_warning = False
        self.title_logo_path = title_logo_path
        self.header_frame_view_model = HeaderFrameViewModel()
        self.setObjectName('title_frame_main')
        self.setStyleSheet(load_stylesheet('views/qss/header_frame_style.qss'))
        self.setGeometry(QRect(200, 190, 1016, 70))
        self.setMinimumSize(QSize(1016, 57))
        self.setMaximumHeight(57)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.title_frame_main_horizontal_layout = QHBoxLayout(self)
        self.title_frame_main_horizontal_layout.setSpacing(4)
        self.title_frame_main_horizontal_layout.setObjectName(
            'title_frame_main_horizontal_layout',
        )
        self.title_frame_main_horizontal_layout.setContentsMargins(
            16, 8, 16, 8,
        )
        self.title_logo = QLabel(self)
        self.title_logo.setObjectName('title_logo')
        self.title_logo.setMinimumSize(QSize(0, 0))
        self.title_logo.setStyleSheet('')
        self.title_logo.setPixmap(QPixmap(self.title_logo_path))
        self.title_logo.setMargin(0)

        self.title_frame_main_horizontal_layout.addWidget(self.title_logo)

        self.title_name = QLabel(self)
        self.title_name.setObjectName('title_name')

        self.title_frame_main_horizontal_layout.addWidget(self.title_name)

        self.network_error_frame = QFrame(self)
        self.network_error_frame.setObjectName('network_error_frame')
        self.network_error_frame.setAccessibleName(NETWORK_AND_BACKUP_FRAME)
        self.network_error_frame.setMinimumSize(QSize(332, 42))
        self.network_error_frame.setMaximumSize(QSize(332, 42))
        self.network_error_frame.setFrameShape(QFrame.StyledPanel)
        self.network_error_frame.setFrameShadow(QFrame.Raised)
        self.network_error_frame_horizontal_layout = QHBoxLayout(
            self.network_error_frame,
        )
        self.network_error_frame_horizontal_layout.setSpacing(10)
        self.network_error_frame_horizontal_layout.setObjectName(
            'network_error_frame_horizontal_layout',
        )
        self.network_error_frame_horizontal_layout.setContentsMargins(
            16, 8, 16, 8,
        )
        self.network_icon_frame = QFrame(self.network_error_frame)
        self.network_icon_frame.setObjectName('network_icon_frame')
        self.network_icon_frame.setMinimumSize(QSize(26, 26))
        self.network_icon_frame.setMaximumSize(QSize(26, 26))
        self.network_icon_frame.setFrameShape(QFrame.StyledPanel)
        self.network_icon_frame.setFrameShadow(QFrame.Raised)
        self.network_icon_vertical_layout = QVBoxLayout(
            self.network_icon_frame,
        )
        self.network_icon_vertical_layout.setSpacing(0)
        self.network_icon_vertical_layout.setObjectName(
            'network_icon_vertical_layout',
        )
        self.network_icon_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.network_error_icon_label = QLabel(self.network_icon_frame)
        self.network_error_icon_label.setObjectName('network_error_icon_label')
        self.network_error_icon_label.setPixmap(
            QPixmap(':assets/network_error.png'),
        )

        self.network_icon_vertical_layout.addWidget(
            self.network_error_icon_label, 0, Qt.AlignHCenter,
        )

        self.network_error_frame_horizontal_layout.addWidget(
            self.network_icon_frame,
        )

        self.network_error_info_label = QLabel(self.network_error_frame)
        self.network_error_info_label.setObjectName('network_error_info_label')

        self.network_error_frame_horizontal_layout.addWidget(
            self.network_error_info_label,
        )

        self.title_frame_main_horizontal_layout.addWidget(
            self.network_error_frame,
        )

        self.horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.title_frame_main_horizontal_layout.addItem(self.horizontal_spacer)

        self.action_button = QPushButton(self)
        self.action_button.setObjectName('action_button')
        self.action_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.title_frame_main_horizontal_layout.addWidget(self.action_button)

        self.refresh_page_button = QPushButton(self)
        self.refresh_page_button.setAccessibleName('refresh_button')
        self.refresh_page_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.refresh_page_button.setObjectName('refresh_page_button')
        self.refresh_page_button.setMinimumSize(QSize(24, 24))

        refresh_icon = QIcon()
        refresh_icon.addFile(
            ':/assets/refresh_2x.png',
            QSize(), QIcon.Mode.Normal, QIcon.State.Off,
        )
        self.refresh_page_button.setIcon(refresh_icon)
        self.refresh_page_button.setIconSize(QSize(24, 24))

        self.title_frame_main_horizontal_layout.addWidget(
            self.refresh_page_button,
        )
        self.network_error_frame.hide()
        self.retranslate_ui()
        self.header_frame_view_model.network_status_signal.connect(
            self.handle_network_frame_visibility,
        )
        self.set_wallet_backup_frame()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.title_name.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, self.title, None,
            ),
        )
        self.network_error_info_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'connection_error_message', None,
            ),
        )
        self.action_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'issue_new_asset', None,
            ),
        )

    def handle_network_frame_visibility(self, network_status: bool):
        """
        This method manages the visibility of the network frame based on the network status.
        First, it checks for an internet connection. If connected, it checks for the wallet backup configuration.
        """
        refresh_and_action_button_list = [
            'collectibles', 'fungibles', 'channel_management',
        ]
        refresh_button_list = ['view_unspent_list']

        if not network_status and (SettingRepository.get_wallet_network() != NetworkEnumModel.REGTEST):
            # Show network error frame for internet connection issue
            self.network_error_info_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'connection_error_message', None,
                ),
            )
            self.network_error_frame.show()
            self.network_error_frame.setStyleSheet("""
                #network_error_frame {
                    border-radius: 8px;
                    background-color: #331D32;
                }
            """)
            self.network_error_icon_label.setPixmap(
                QPixmap(':assets/network_error.png'),
            )
            self.network_error_frame.setMinimumSize(QSize(332, 42))
            self.network_error_frame.setMaximumSize(QSize(332, 42))

            # Disable user interactions and remove tooltip since there is no internet
            self.network_error_frame.setToolTip('')
            self.network_error_frame.setCursor(
                QCursor(Qt.CursorShape.ArrowCursor),
            )

            # Handle visibility of buttons based on the title
            self.set_button_visibility(
                refresh_and_action_button_list, refresh_button_list, False,
            )
            self.is_backup_warning = False

        else:
            # Enable user interactions and check wallet backup configuration
            self.set_wallet_backup_frame()

            # Handle visibility of buttons based on the title
            self.set_button_visibility(
                refresh_and_action_button_list, refresh_button_list, True,
            )

    def set_button_visibility(self, refresh_and_action_button_list, refresh_button_list, visible):
        """
        A helper method to handle button visibility based on the network status and title.
        """
        if self.title in refresh_and_action_button_list:
            self.action_button.setVisible(visible)
            self.refresh_page_button.setVisible(visible)

        if self.title in refresh_button_list:
            self.refresh_page_button.setVisible(visible)

    def set_wallet_backup_frame(self):
        """
        This method manages the wallet backup warning frame.
        If the wallet backup is not configured, it shows the backup warning frame.
        """
        is_backup_configured: IsBackupConfiguredModel = SettingRepository.is_backup_configured()
        token_path_exists = os.path.exists(TOKEN_PICKLE_PATH)
        wallet_type: WalletType = SettingRepository.get_wallet_type().value

        if not token_path_exists and not is_backup_configured.is_backup_configured and (wallet_type == WalletType.EMBEDDED_TYPE_WALLET.value):
            # Show backup warning frame
            self.network_error_frame.setStyleSheet("""
                QFrame {
                    background-color: #0B226E;
                    border-radius: 8px;
                }
            """)
            self.network_error_info_label.setText(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'backup_not_configured', None,
                ),
            )
            self.network_error_frame.setMinimumSize(QSize(220, 42))
            self.network_error_frame.show()

            # Change the icon and tooltip to indicate backup is not configured
            self.network_error_icon_label.setPixmap(
                QPixmap(':assets/no_backup.png'),
            )
            self.network_error_frame.setCursor(
                QCursor(Qt.CursorShape.PointingHandCursor),
            )
            self.network_error_frame.setToolTip(
                QCoreApplication.translate(
                    IRIS_WALLET_TRANSLATIONS_CONTEXT, 'backup_tooltip_text', None,
                ),
            )

            # Set flag to indicate this is a backup warning
            self.is_backup_warning = True
        else:
            # Hide the frame and reset the backup warning flag
            self.network_error_frame.hide()
            self.is_backup_warning = False

    # pylint disable(invalid-name) because of mousePressEvent is internal function of QWidget
    def mousePressEvent(self, event):  # pylint:disable=invalid-name
        """
        Handle mouse press events.
        Navigates to the backup page if the network_error_frame is visible and it's a backup warning.
        """
        if self.network_error_frame.isVisible() and self.is_backup_warning:
            frame_rect = self.network_error_frame.geometry()
            if frame_rect.contains(event.pos()):
                self.on_network_frame_click()

        # Call the parent method to ensure other click functionality works
        super().mousePressEvent(event)

    def on_network_frame_click(self):
        """
        Handle logic when network_error_frame is clicked.
        Only navigates to the backup page if the frame is showing a backup warning.
        """
        if self.network_error_frame.isVisible() and self.is_backup_warning:
            # Only navigate if the frame is visible and it's showing a backup warning
            PageNavigationEventManager.get_instance().backup_page_signal.emit()
