# pylint: disable=too-many-instance-attributes, too-many-statements, unused-import
"""This module contains the SetWalletPasswordWidget class,
which represents the UI for wallet password.
"""
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtGui import QCursor
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
from accessible_constant import CONFIRM_PASSWORD_INPUT
from accessible_constant import CONFIRM_PASSWORD_VISIBILITY_BUTTON
from accessible_constant import PASSWORD_INPUT
from accessible_constant import PASSWORD_SUGGESTION_BUTTON
from accessible_constant import PASSWORD_VISIBILITY_BUTTON
from accessible_constant import SET_WALLET_PASSWORD_CLOSE_BUTTON
from accessible_constant import SET_WALLET_PASSWORD_PROCEED_BUTTON
from src.model.enums.enums_model import ToastPreset
from src.model.enums.enums_model import WalletType
from src.model.selection_page_model import SelectionPageModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.utils.constant import SYNCING_CHAIN_LABEL_TIMER
from src.utils.helpers import load_stylesheet
from src.viewmodels.main_view_model import MainViewModel
from src.views.components.buttons import PrimaryButton
from src.views.components.toast import ToastManager
from src.views.components.wallet_logo_frame import WalletLogoFrame


class SetWalletPasswordWidget(QWidget):
    """This class represents all the UI elements of the set wallet password page."""

    def __init__(self, view_model, originating_page):
        super().__init__()
        self._view_model: MainViewModel = view_model
        self.originating_page = originating_page
        self.password_validation = None
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.setStyleSheet(
            load_stylesheet(
                'views/qss/set_wallet_password_style.qss',
            ),
        )
        self.setObjectName('setup_wallet_password_page')
        self.widget_grid_layout = QGridLayout(self)
        self.widget_grid_layout.setObjectName('grid_layout_22')
        self.wallet_logo_frame = WalletLogoFrame()
        self.widget_grid_layout.addWidget(self.wallet_logo_frame, 0, 0, 1, 2)

        self.horizontal_spacer_1 = QSpacerItem(
            265,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.widget_grid_layout.addItem(self.horizontal_spacer_1, 1, 3, 1, 1)

        self.vertical_spacer_1 = QSpacerItem(
            20,
            190,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )

        self.widget_grid_layout.addItem(self.vertical_spacer_1, 3, 1, 1, 1)

        self.horizontal_spacer_set_password = QSpacerItem(
            266,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.widget_grid_layout.addItem(
            self.horizontal_spacer_set_password, 2, 0, 1, 1,
        )

        self.vertical_spacer_set_password_2 = QSpacerItem(
            20,
            190,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )

        self.widget_grid_layout.addItem(
            self.vertical_spacer_set_password_2, 0, 2, 1, 1,
        )

        self.setup_wallet_password_widget = QWidget(self)
        self.setup_wallet_password_widget.setObjectName(
            'setup_wallet_password_widget',
        )
        self.setup_wallet_password_widget.setMinimumSize(QSize(499, 350))
        self.setup_wallet_password_widget.setMaximumSize(QSize(466, 350))

        self.grid_layout_1 = QGridLayout(self.setup_wallet_password_widget)
        self.grid_layout_1.setSpacing(6)
        self.grid_layout_1.setObjectName('grid_layout_1')
        self.grid_layout_1.setContentsMargins(1, 4, 1, 30)
        self.vertical_layout_setup_wallet_password = QVBoxLayout()
        self.vertical_layout_setup_wallet_password.setSpacing(6)
        self.vertical_layout_setup_wallet_password.setObjectName(
            'verticalLayout_setup_wallet_password',
        )
        self.set_wallet_password_title_layout = QHBoxLayout()
        self.set_wallet_password_title_layout.setObjectName(
            'horizontalLayout_8',
        )
        self.set_wallet_password_title_layout.setContentsMargins(35, 9, 40, 0)
        self.set_wallet_password_label = QLabel(
            self.setup_wallet_password_widget,
        )
        self.set_wallet_password_label.setObjectName(
            'set_wallet_password_label',
        )
        self.set_wallet_password_label.setMinimumSize(QSize(415, 63))

        self.set_wallet_password_title_layout.addWidget(
            self.set_wallet_password_label,
        )

        self.close_btn_set_password_page = QPushButton(
            self.setup_wallet_password_widget,
        )
        self.close_btn_set_password_page.setObjectName('close_btn')
        self.close_btn_set_password_page.setAccessibleName(
            SET_WALLET_PASSWORD_CLOSE_BUTTON,
        )
        self.close_btn_set_password_page.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.close_btn_set_password_page.setMinimumSize(QSize(24, 24))
        self.close_btn_set_password_page.setMaximumSize(QSize(50, 65))
        self.close_btn_set_password_page.setAutoFillBackground(False)

        set_password_close_icon = QIcon()
        set_password_close_icon.addFile(
            ':/assets/x_circle.png',
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.close_btn_set_password_page.setIcon(set_password_close_icon)
        self.close_btn_set_password_page.setIconSize(QSize(24, 24))
        self.close_btn_set_password_page.setCheckable(False)
        self.close_btn_set_password_page.setChecked(False)

        self.set_wallet_password_title_layout.addWidget(
            self.close_btn_set_password_page, 0, Qt.AlignHCenter,
        )

        self.vertical_layout_setup_wallet_password.addLayout(
            self.set_wallet_password_title_layout,
        )

        self.header_line = QFrame(self.setup_wallet_password_widget)
        self.header_line.setObjectName('header_line')

        self.header_line.setFrameShape(QFrame.HLine)
        self.header_line.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_setup_wallet_password.addWidget(self.header_line)

        self.vert_spacer = QSpacerItem(
            20,
            40,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Preferred,
        )

        self.vertical_layout_setup_wallet_password.addItem(
            self.vert_spacer,
        )

        self.enter_password_field_layout = QHBoxLayout()
        self.enter_password_field_layout.setSpacing(0)
        self.enter_password_field_layout.setObjectName('horizontal_layout_1')
        self.enter_password_field_layout.setContentsMargins(40, -1, 40, -1)
        self.enter_password_input = QLineEdit(
            self.setup_wallet_password_widget,
        )
        self.enter_password_input.setObjectName('enter_password_input')
        self.enter_password_input.setAccessibleName(PASSWORD_INPUT)
        self.enter_password_input.setMinimumSize(QSize(350, 40))
        self.enter_password_input.setMaximumSize(QSize(370, 40))

        self.enter_password_input.setFrame(False)
        self.enter_password_input.setEchoMode(QLineEdit.Password)
        self.enter_password_input.setClearButtonEnabled(False)

        self.enter_password_field_layout.addWidget(self.enter_password_input)

        self.enter_password_visibility_button = QPushButton(
            self.setup_wallet_password_widget,
        )
        self.enter_password_visibility_button.setObjectName(
            'enter_password_visibility_button',
        )
        self.enter_password_visibility_button.setAccessibleName(
            PASSWORD_VISIBILITY_BUTTON,
        )
        self.enter_password_visibility_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.enter_password_visibility_button.setMinimumSize(QSize(50, 0))
        self.enter_password_visibility_button.setMaximumSize(QSize(50, 40))

        icon_eye_visible = QIcon()
        icon_eye_visible.addFile(
            ':/assets/eye_visible.png',
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.enter_password_visibility_button.setIcon(icon_eye_visible)

        self.enter_password_field_layout.addWidget(
            self.enter_password_visibility_button,
        )

        self.vertical_layout_setup_wallet_password.addLayout(
            self.enter_password_field_layout,
        )

        self.vert_spacer_2 = QSpacerItem(
            20,
            40,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Preferred,
        )

        self.vertical_layout_setup_wallet_password.addItem(
            self.vert_spacer_2,
        )

        self.confirm_password_layout = QHBoxLayout()
        self.confirm_password_layout.setSpacing(0)
        self.confirm_password_layout.setObjectName('horizontal_layout_2')
        self.confirm_password_layout.setContentsMargins(40, -1, 40, -1)
        self.confirm_password_input = QLineEdit(
            self.setup_wallet_password_widget,
        )
        self.confirm_password_input.setObjectName('confirm_password_input')
        self.confirm_password_input.setAccessibleName(CONFIRM_PASSWORD_INPUT)
        self.confirm_password_input.setMinimumSize(QSize(0, 40))
        self.confirm_password_input.setMaximumSize(QSize(370, 40))

        self.confirm_password_input.setFrame(False)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setClearButtonEnabled(False)

        self.confirm_password_layout.addWidget(self.confirm_password_input)

        self.password_suggestion_button = QPushButton(
            self.setup_wallet_password_widget,
        )
        self.password_suggestion_button.setObjectName(
            'password_suggestion_button',
        )
        self.password_suggestion_button.setAccessibleName(
            PASSWORD_SUGGESTION_BUTTON,
        )
        self.password_suggestion_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.password_suggestion_button.setMinimumSize(QSize(30, 0))
        self.password_suggestion_button.setMaximumSize(QSize(30, 40))

        password_suggestion_icon = QIcon()
        password_suggestion_icon.addFile(
            ':/assets/key.png',
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.password_suggestion_button.setIcon(password_suggestion_icon)
        self.confirm_password_layout.addWidget(
            self.password_suggestion_button,
        )

        self.confirm_password_visibility_button = QPushButton(
            self.setup_wallet_password_widget,
        )
        self.confirm_password_visibility_button.setObjectName(
            'confirm_password_visibility_button',
        )
        self.confirm_password_visibility_button.setAccessibleName(
            CONFIRM_PASSWORD_VISIBILITY_BUTTON,
        )
        self.confirm_password_visibility_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor),
        )
        self.confirm_password_visibility_button.setMinimumSize(QSize(50, 0))
        self.confirm_password_visibility_button.setMaximumSize(QSize(50, 40))

        self.confirm_password_visibility_button.setIcon(icon_eye_visible)

        self.confirm_password_layout.addWidget(
            self.confirm_password_visibility_button,
        )

        self.vertical_layout_setup_wallet_password.addLayout(
            self.confirm_password_layout,
        )

        self.vertical_spacer_2 = QSpacerItem(
            20,
            40,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )

        self.vertical_layout_setup_wallet_password.addItem(
            self.vertical_spacer_2,
        )

        self.footer_line = QFrame(self.setup_wallet_password_widget)
        self.footer_line.setObjectName('footer_line')

        self.footer_line.setFrameShape(QFrame.HLine)
        self.footer_line.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_setup_wallet_password.addWidget(self.footer_line)

        self.proceed_button_layout = QVBoxLayout()
        self.proceed_button_layout.setObjectName('horizontalLayout_5')
        self.proceed_button_layout.setContentsMargins(-1, 22, -1, -1)
        self.proceed_button_layout.setSpacing(6)
        self.proceed_wallet_password = PrimaryButton()
        self.proceed_wallet_password.setAccessibleName(
            SET_WALLET_PASSWORD_PROCEED_BUTTON,
        )
        self.proceed_wallet_password.setMinimumSize(QSize(414, 40))
        self.proceed_wallet_password.setMaximumSize(QSize(404, 40))

        self.proceed_button_layout.addWidget(
            self.proceed_wallet_password, 0, Qt.AlignCenter,
        )

        self.syncing_chain_info_label = QLabel(self)
        self.syncing_chain_info_label.setObjectName('syncing_chain_info_label')
        self.syncing_chain_info_label.setWordWrap(True)
        self.syncing_chain_info_label.setMinimumSize(QSize(414, 40))

        self.syncing_chain_info_label.setMaximumSize(QSize(404, 40))
        self.syncing_chain_info_label.hide()
        self.proceed_button_layout.addWidget(
            self.syncing_chain_info_label, alignment=Qt.AlignmentFlag.AlignCenter,
        )
        self.vertical_layout_setup_wallet_password.addLayout(
            self.proceed_button_layout,
        )

        self.grid_layout_1.addLayout(
            self.vertical_layout_setup_wallet_password,
            0,
            0,
            1,
            1,
        )

        self.widget_grid_layout.addWidget(
            self.setup_wallet_password_widget,
            1,
            1,
            2,
            2,
        )
        self.retranslate_ui()

    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.set_wallet_password_label.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'set_your_wallet_password',
                None,
            ),
        )
        self.enter_password_input.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'enter_your_password',
                None,
            ),
        )
        self.confirm_password_input.setPlaceholderText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT,
                'confirm_your_password',
                None,
            ),
        )
        self.proceed_wallet_password.setText(
            QCoreApplication.translate(
                IRIS_WALLET_TRANSLATIONS_CONTEXT, 'proceed', None,
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
        self._view_model.set_wallet_password_view_model.message.connect(
            self.handle_message,
        )
        self.proceed_wallet_password.setDisabled(True)
        self.enter_password_input.textChanged.connect(
            self.handle_button_enabled,
        )
        self.confirm_password_input.textChanged.connect(
            self.handle_button_enabled,
        )
        self._view_model.set_wallet_password_view_model.is_loading.connect(
            self.update_loading_state,
        )
        self.enter_password_visibility_button.clicked.connect(
            lambda: self.toggle_password_visibility(self.enter_password_input),
        )
        self.confirm_password_visibility_button.clicked.connect(
            lambda: self.toggle_password_visibility(
                self.confirm_password_input,
            ),
        )
        self.close_btn_set_password_page.clicked.connect(self.close_navigation)
        self.proceed_wallet_password.clicked.connect(
            lambda: self.set_wallet_password(
                self.enter_password_input,
                self.confirm_password_input,
            ),
        )
        self.password_suggestion_button.clicked.connect(
            self.set_password_suggestion,
        )
        self.timer.timeout.connect(self.syncing_chain_info_label.show)

    def toggle_password_visibility(self, line_edit):
        """This method toggle the password visibility."""
        self._view_model.set_wallet_password_view_model.toggle_password_visibility(
            line_edit,
        )

    def set_wallet_password(
        self,
        enter_password_input,
        vertical_layout_setup_wallet_password,
    ):
        """This method handled set password."""
        self._view_model.set_wallet_password_view_model.set_wallet_password_in_thread(
            enter_password_input,
            vertical_layout_setup_wallet_password,
            self.show_password_validation_label,
        )

    def close_navigation(self):
        """This method handled close button navigation"""
        if self.originating_page == WalletType.EMBEDDED_TYPE_WALLET.value:
            self._view_model.page_navigation.welcome_page()
        if self.originating_page == WalletType.REMOTE_TYPE_WALLET.value:
            title = 'connection_type'
            embedded_path = ':/assets/embedded.png'
            embedded_title = WalletType.EMBEDDED_TYPE_WALLET.value
            connect_path = ':/assets/remote.png'
            connect_title = WalletType.REMOTE_TYPE_WALLET.value
            params = SelectionPageModel(
                title=title,
                logo_1_path=embedded_path,
                logo_1_title=embedded_title,
                logo_2_path=connect_path,
                logo_2_title=connect_title,
                asset_id='none',
                callback='none',
            )
            self._view_model.page_navigation.wallet_connection_page(params)

    def show_password_validation_label(self, message):
        """This method handled password validation."""
        if self.password_validation is not None:
            self.password_validation.deleteLater()
        self.password_validation = QLabel(
            message,
            self.setup_wallet_password_widget,
        )
        self.password_validation.setObjectName('password_validation')
        self.password_validation.setMinimumSize(QSize(0, 25))
        self.password_validation.setStyleSheet(
            load_stylesheet(
                'views/qss/style.qss',
            ),
        )
        self.password_validation.show()
        self.vertical_layout_setup_wallet_password.insertWidget(
            6,
            self.password_validation,
            0,
            Qt.AlignHCenter,
        )
        self.password_validation.show()

    def set_password_suggestion(self):
        """This method handled strong password suggestion."""
        generate_password = (
            self._view_model.set_wallet_password_view_model.generate_password(
                12,
            )
        )
        self.enter_password_input.setText(generate_password)
        self.confirm_password_input.setText(generate_password)

    def update_loading_state(self, is_loading: bool):
        """
        Updates the loading state of the proceed_wallet_password object.

        This method prints the loading state and starts or stops the loading animation
        of the proceed_wallet_password object based on the value of is_loading.
        """
        if is_loading:
            self.proceed_wallet_password.start_loading()
            self.close_btn_set_password_page.hide()
            self.enter_password_input.hide()
            self.confirm_password_input.hide()
            self.password_suggestion_button.hide()
            self.confirm_password_visibility_button.hide()
            self.enter_password_visibility_button.hide()
            self.header_line.hide()
            self.footer_line.hide()
            self.setup_wallet_password_widget.setMinimumSize(QSize(499, 150))
            self.setup_wallet_password_widget.setMaximumSize(QSize(466, 200))
            self.timer.start(SYNCING_CHAIN_LABEL_TIMER)
        else:
            self.proceed_wallet_password.stop_loading()
            self.close_btn_set_password_page.show()
            self.enter_password_input.show()
            self.confirm_password_input.show()
            self.password_suggestion_button.show()
            self.confirm_password_visibility_button.show()
            self.enter_password_visibility_button.show()
            self.header_line.show()
            self.footer_line.show()
            self.setup_wallet_password_widget.setMinimumSize(QSize(499, 350))
            self.setup_wallet_password_widget.setMaximumSize(QSize(466, 350))
            self.syncing_chain_info_label.hide()
            self.timer.stop()

    def handle_button_enabled(self):
        """Updates the enabled state of the send button."""
        if (self.enter_password_input.text() and self.confirm_password_input.text()):
            self.proceed_wallet_password.setDisabled(False)
        else:
            self.proceed_wallet_password.setDisabled(True)

    def handle_message(self, msg_type, message: str):
        """This method handled to show message."""
        if msg_type == ToastPreset.ERROR:
            ToastManager.error(message)
        else:
            ToastManager.success(message)
