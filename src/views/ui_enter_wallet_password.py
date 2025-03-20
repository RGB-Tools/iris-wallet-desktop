# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the EnterWalletPasswordWidget class,
which represents the UI for wallet password.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

import src.resources_rc
from accessible_constant import ENTER_WALLET_PASSWORD
from accessible_constant import LOGIN_BUTTON
from src.model.enums.enums_model import ToastPreset
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import SYNCING_CHAIN_LABEL_TIMER
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.toast import ToastManager
from src.views.components.wallet_logo_frame import WalletLogoFrame


class EnterWalletPassword(QWidget):
    """This class represents all the UI elements of the enter wallet password page."""

    def __init__(self, view_model):
        super().__init__()
        self._view_model: MainViewModel = view_model

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)

        self.setStyleSheet(
            load_stylesheet(
                'views/qss/enter_wallet_password_style.qss',
            ),
        )
        self.enter_wallet_password_grid_layout = QGridLayout(self)
        self.enter_wallet_password_grid_layout.setObjectName(
            'enter_wallet_password_grid_layout',
        )
        self.wallet_logo = WalletLogoFrame(self)

        self.enter_wallet_password_grid_layout.addWidget(
            self.wallet_logo, 0, 0, 1, 1,
        )

        self.vertical_spacer_1 = QSpacerItem(
            20, 250, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )

        self.enter_wallet_password_grid_layout.addItem(
            self.vertical_spacer_1, 0, 2, 1, 1,
        )

        self.enter_wallet_password_widget = QWidget(self)
        self.enter_wallet_password_widget.setObjectName(
            'setup_wallet_password_widget_3',
        )
        self.enter_wallet_password_widget.setMinimumSize(QSize(499, 300))
        self.enter_wallet_password_widget.setMaximumSize(QSize(466, 608))

        self.grid_layout_1 = QGridLayout(self.enter_wallet_password_widget)
        self.grid_layout_1.setSpacing(6)
        self.grid_layout_1.setObjectName('grid_layout_1')
        self.grid_layout_1.setContentsMargins(1, 4, 1, 30)
        self.vertical_layout_enter_wallet_password = QVBoxLayout()
        self.vertical_layout_enter_wallet_password.setSpacing(6)
        self.vertical_layout_enter_wallet_password.setObjectName(
            'verticalLayout_setup_wallet_password_3',
        )
        self.horizontal_layout_1 = QHBoxLayout()
        self.horizontal_layout_1.setObjectName('horizontal_layout_1')
        self.horizontal_layout_1.setContentsMargins(25, 9, 40, 0)
        self.enter_wallet_password = QLabel(self.enter_wallet_password_widget)
        self.enter_wallet_password.setObjectName('Enter_wallet_password')
        self.enter_wallet_password.setMinimumSize(QSize(415, 63))

        self.horizontal_layout_1.addWidget(self.enter_wallet_password)

        self.vertical_layout_enter_wallet_password.addLayout(
            self.horizontal_layout_1,
        )

        self.header_line = QFrame(self.enter_wallet_password_widget)
        self.header_line.setObjectName('header_line')

        self.header_line.setFrameShape(QFrame.Shape.HLine)
        self.header_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout_enter_wallet_password.addWidget(self.header_line)

        self.horizontal_layout_2 = QHBoxLayout()
        self.horizontal_layout_2.setSpacing(0)
        self.horizontal_layout_2.setObjectName('horizontal_layout_2')
        self.horizontal_layout_2.setContentsMargins(47, -1, 48, -1)

        self.vert_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred,
        )
        self.vertical_layout_enter_wallet_password.addItem(self.vert_spacer)
        self.enter_password_input = QLineEdit(
            self.enter_wallet_password_widget,
        )
        self.enter_password_input.setObjectName('enter_password_input_3')
        self.enter_password_input.setAccessibleName(ENTER_WALLET_PASSWORD)
        self.enter_password_input.setMinimumSize(QSize(352, 40))
        self.enter_password_input.setMaximumSize(QSize(352, 40))

        self.enter_password_input.setFrame(False)
        self.enter_password_input.setEchoMode(QLineEdit.Password)
        self.enter_password_input.setClearButtonEnabled(False)

        self.horizontal_layout_2.addWidget(self.enter_password_input)

        self.enter_password_visibility_button = QPushButton(
            self.enter_wallet_password_widget,
        )
        self.enter_password_visibility_button.setObjectName(
            'enter_password_visibility_button_3',
        )
        self.enter_password_visibility_button.setMinimumSize(QSize(50, 0))
        self.enter_password_visibility_button.setMaximumSize(QSize(50, 40))

        icon = QIcon()
        icon.addFile(
            ':/assets/eye_visible.png',
            QSize(), QIcon.Normal, QIcon.Off,
        )
        self.enter_password_visibility_button.setIcon(icon)

        self.horizontal_layout_2.addWidget(
            self.enter_password_visibility_button,
        )

        self.vertical_layout_enter_wallet_password.addLayout(
            self.horizontal_layout_2,
        )

        self.horizontal_layout_3 = QHBoxLayout()
        self.horizontal_layout_3.setSpacing(0)
        self.horizontal_layout_3.setObjectName('horizontal_layout_3')
        self.horizontal_layout_3.setContentsMargins(40, -1, 40, -1)

        self.vertical_layout_enter_wallet_password.addLayout(
            self.horizontal_layout_3,
        )

        self.vertical_spacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_enter_wallet_password.addItem(
            self.vertical_spacer_2,
        )

        self.footer_line = QFrame(self.enter_wallet_password_widget)
        self.footer_line.setObjectName('footer_line')

        self.footer_line.setFrameShape(QFrame.Shape.HLine)
        self.footer_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_layout_enter_wallet_password.addWidget(self.footer_line)

        self.horizontal_layout_4 = QHBoxLayout()
        self.horizontal_layout_4.setObjectName('horizontal_layout_4')
        self.horizontal_layout_4.setContentsMargins(-1, 22, -1, -1)
        self.horizontal_spacer_1 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.horizontal_layout_4.addItem(self.horizontal_spacer_1)

        self.login_wallet_button = PrimaryButton()
        self.login_wallet_button.setAccessibleName(LOGIN_BUTTON)
        size_policy_login_button = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed,
        )
        size_policy_login_button.setHorizontalStretch(1)
        size_policy_login_button.setVerticalStretch(0)
        size_policy_login_button.setHeightForWidth(
            self.login_wallet_button.sizePolicy().hasHeightForWidth(),
        )
        self.login_wallet_button.setSizePolicy(size_policy_login_button)
        self.login_wallet_button.setMinimumSize(QSize(0, 40))
        self.login_wallet_button.setMaximumSize(QSize(402, 16777215))

        self.horizontal_layout_4.addWidget(self.login_wallet_button)

        self.horizontal_spacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.horizontal_layout_4.addItem(self.horizontal_spacer_2)

        self.vertical_layout_enter_wallet_password.addLayout(
            self.horizontal_layout_4,
        )
        self.syncing_chain_info_label = QLabel(self)
        self.syncing_chain_info_label.setObjectName('syncing_chain_info_label')
        self.syncing_chain_info_label.setWordWrap(True)
        self.syncing_chain_info_label.setMaximumSize(QSize(450, 40))
        self.syncing_chain_info_label.hide()
        self.vertical_layout_enter_wallet_password.addWidget(
            self.syncing_chain_info_label,
        )

        self.grid_layout_1.addLayout(
            self.vertical_layout_enter_wallet_password, 0, 0, 1, 1,
        )

        self.enter_wallet_password_grid_layout.addWidget(
            self.enter_wallet_password_widget, 1, 1, 2, 2,
        )

        self.horizontal_spacer_3 = QSpacerItem(
            338, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.enter_wallet_password_grid_layout.addItem(
            self.horizontal_spacer_3, 1, 3, 1, 1,
        )

        self.horizontal_spacer_4 = QSpacerItem(
            338, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum,
        )

        self.enter_wallet_password_grid_layout.addItem(
            self.horizontal_spacer_4, 2, 0, 1, 1,
        )

        self.vertical_spacer_3 = QSpacerItem(
            20, 250, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding,
        )

        self.enter_wallet_password_grid_layout.addItem(
            self.vertical_spacer_3, 3, 1, 1, 1,
        )

        self.retranslate_ui()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.enter_wallet_password.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'enter_wallet_password', None,
            ),
        )

        self.enter_password_input.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'enter_your_password', None,
            ),
        )
        self.login_wallet_button.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'login', None,
            ),
        )
        self.setup_ui_connection()
        self.syncing_chain_info_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'syncing_chain_info', None,
            ),
        )

    def setup_ui_connection(self):
        """Set up connections for UI elements."""

        self.enter_password_visibility_button.clicked.connect(
            lambda: self.toggle_password_visibility(self.enter_password_input),
        )

        self._view_model.enter_wallet_password_view_model.message.connect(
            self.handle_wallet_message,
        )

        self.login_wallet_button.clicked.connect(
            lambda: self.set_wallet_password(
                self.enter_password_input,
            ),
        )

        self._view_model.enter_wallet_password_view_model.is_loading.connect(
            self.update_loading_state,
        )

        self.login_wallet_button.setDisabled(True)

        self.enter_password_input.textChanged.connect(
            self.handle_button_enabled,
        )
        self.timer.timeout.connect(self.syncing_chain_info_label.show)

    def set_wallet_password(self, enter_password_input: QLineEdit):
        """Take password input from ui and pass view model method set_wallet_password"""
        self._view_model.enter_wallet_password_view_model.set_wallet_password(
            enter_password_input.text(),
        )

    def toggle_password_visibility(self, line_edit):
        """This method toggle the password visibility."""
        self._view_model.enter_wallet_password_view_model.toggle_password_visibility(
            line_edit,
        )

    def handle_button_enabled(self):
        """Updates the enabled state of the login button."""
        if self.enter_password_input.text():
            self.login_wallet_button.setDisabled(False)
        else:
            self.login_wallet_button.setDisabled(True)

    def handle_wallet_message(self, message_type: ToastPreset, message: str):
        """This method handled to show  wallet message."""
        if message_type == ToastPreset.ERROR:
            ToastManager.error(message)
        else:
            ToastManager.success(message)

    def update_loading_state(self, is_loading: bool):
        """
        Updates the loading state of the proceed_wallet_password object.

        This method prints the loading state and starts or stops the loading animation
        of the proceed_wallet_password object based on the value of is_loading.
        """
        if is_loading:
            self.login_wallet_button.start_loading()
            self.enter_password_input.hide()
            self.enter_password_visibility_button.hide()
            self.footer_line.hide()
            self.header_line.hide()
            self.enter_wallet_password_widget.setMinimumSize(QSize(499, 200))
            self.enter_wallet_password_widget.setMaximumSize(QSize(466, 200))
            self.timer.start(SYNCING_CHAIN_LABEL_TIMER)
        else:
            self.login_wallet_button.stop_loading()
            self.enter_password_input.show()
            self.enter_password_visibility_button.show()
            self.footer_line.show()
            self.header_line.show()
            self.enter_wallet_password_widget.setMinimumSize(QSize(499, 300))
            self.enter_wallet_password_widget.setMaximumSize(QSize(466, 608))
            self.syncing_chain_info_label.hide()
            self.timer.stop()
